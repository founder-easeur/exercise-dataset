"""Controlled HTTP fetcher: caching, retries, rate limiting, bounded concurrency."""
from __future__ import annotations

import hashlib
import json
import logging
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path

import httpx

from app.config import settings
from app.pipeline.security import (
    SafeRedirectValidator, UnsafeURLError, validate_external_url,
)

log = logging.getLogger("easeur.fetcher")

RETRY_STATUS = {429, 500, 502, 503, 504}


@dataclass
class FetchResult:
    url: str
    status: int | None = None
    content: str | None = None
    content_type: str | None = None
    from_cache: bool = False
    retries: int = 0
    error: str | None = None
    fetched_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    @property
    def ok(self) -> bool:
        return self.status is not None and 200 <= self.status < 300 and self.content is not None

    @property
    def content_hash(self) -> str | None:
        if self.content is None:
            return None
        return hashlib.sha256(self.content.encode("utf-8", "replace")).hexdigest()


class DiskCache:
    """Tiny file-backed response cache keyed by URL hash with TTL."""

    def __init__(self, directory: Path | str, ttl_seconds: int):
        self.dir = Path(directory)
        self.ttl = timedelta(seconds=ttl_seconds)
        self.dir.mkdir(parents=True, exist_ok=True)

    def _key(self, url: str) -> Path:
        return self.dir / (hashlib.sha256(url.encode()).hexdigest() + ".json")

    def get(self, url: str) -> dict | None:
        path = self._key(url)
        if not path.exists():
            return None
        try:
            data = json.loads(path.read_text())
        except Exception:  # noqa: BLE001
            return None
        fetched = datetime.fromisoformat(data["fetched_at"])
        if datetime.now(timezone.utc) - fetched > self.ttl:
            return None
        return data

    def put(self, result: FetchResult) -> None:
        self._key(result.url).write_text(json.dumps({
            "url": result.url, "status": result.status, "content": result.content,
            "content_type": result.content_type,
            "fetched_at": result.fetched_at,
        }))


class RateLimiter:
    """Per-domain minimum delay, conservative global concurrency."""

    def __init__(self, min_delay: float, max_concurrency: int):
        self.min_delay = min_delay
        self._last: dict[str, float] = {}
        self._sem = __import__("threading").BoundedSemaphore(max_concurrency)

    def wait(self, domain: str) -> None:
        import time as _t
        now = _t.monotonic()
        last = self._last.get(domain, 0.0)
        delta = now - last
        if delta < self.min_delay:
            time.sleep(self.min_delay - delta)
        self._last[domain] = time.monotonic()


class Fetcher:
    def __init__(self, cache_dir: Path | None = None):
        self.cache = DiskCache(
            cache_dir or Path(settings.crawler_cache_dir),
            settings.crawler_cache_ttl_seconds,
        )
        self.rate = RateLimiter(settings.crawler_min_delay_seconds, settings.crawler_max_concurrency)
        self.redirect_guard = SafeRedirectValidator()

    def fetch(self, url: str, *, use_cache: bool = True) -> FetchResult:
        try:
            url = validate_external_url(url)  # SSRF guard incl. DNS resolution
        except UnsafeURLError as exc:
            log.warning("refused unsafe URL %s: %s", url, exc)
            return FetchResult(url=url, error=f"blocked by policy: {exc}")
        if use_cache:
            cached = self.cache.get(url)
            if cached is not None:
                return FetchResult(url=url, status=cached["status"],
                                   content=cached["content"], content_type=cached["content_type"],
                                   from_cache=True)
        import urllib.parse
        domain = urllib.parse.urlsplit(url).netloc
        self.rate.wait(domain)

        retries = 0
        last_error: str | None = None
        for attempt in range(3):
            if attempt:
                time.sleep(1.5 * attempt)  # linear backoff
            try:
                with httpx.Client(
                    follow_redirects=True,
                    max_redirects=settings.crawler_max_redirects,
                    timeout=settings.crawler_timeout_seconds,
                    headers={"User-Agent": settings.crawler_user_agent,
                             "Accept": "text/html,application/xhtml+xml"},
                    event_hooks={"request": [self.redirect_guard]},
                ) as client:
                    resp = client.get(url)
                if resp.status_code in RETRY_STATUS and attempt < 2:
                    last_error = f"retryable status {resp.status_code}"
                    retries += 1
                    continue
                content_type = resp.headers.get("content-type", "")
                if resp.status_code == 200 and "html" not in content_type and "text" not in content_type:
                    return FetchResult(url=url, status=resp.status_code, error="non-HTML content",
                                       content_type=content_type)
                result = FetchResult(url=str(resp.url), status=resp.status_code,
                                     content=resp.text if resp.status_code == 200 else None,
                                     content_type=content_type, retries=retries)
                if result.ok:
                    self.cache.put(result)
                return result
            except httpx.HTTPError as exc:
                last_error = str(exc)
                retries += 1
        return FetchResult(url=url, error=last_error or "fetch failed", retries=retries)
