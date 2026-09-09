"""robots.txt compliance for the crawler.

Caches robots.txt per domain, parses it, and honours Disallow rules for our
user agent plus '*'. Supports loading cached/snapshot robots files for replay
mode (no network).
"""
from __future__ import annotations

import io
import logging
import urllib.parse
import urllib.robotparser
from datetime import datetime, timedelta, timezone
from pathlib import Path

import httpx

from app.config import settings

log = logging.getLogger("easeur.robots")

ROBOTS_TTL = timedelta(hours=12)
_snapshot_dir: Path | None = None


def set_robots_snapshot_dir(path: Path | None) -> None:
    """In replay mode, robots.txt files are read from a local snapshot dir."""
    global _snapshot_dir
    _snapshot_dir = path


def robots_url_for(url: str) -> str:
    p = urllib.parse.urlsplit(url)
    return f"{p.scheme}://{p.netloc}/robots.txt"


def _snapshot_robots(origin: str) -> str | None:
    if _snapshot_dir is None:
        return None
    host = urllib.parse.urlsplit(origin).netloc.replace(":", "_")
    candidate = _snapshot_dir / f"{host}.robots.txt"
    if candidate.exists():
        return candidate.read_text(encoding="utf-8", errors="replace")
    return None


class RobotsCache:
    def __init__(self) -> None:
        self._cache: dict[str, tuple[datetime, urllib.robotparser.RobotFileParser | None]] = {}

    def _load(self, origin: str) -> urllib.robotparser.RobotFileParser | None:
        url = f"{origin}/robots.txt"
        text = _snapshot_robots(origin)
        if text is None:
            try:
                resp = httpx.get(
                    url,
                    timeout=10,
                    follow_redirects=True,
                    headers={"User-Agent": settings.crawler_user_agent},
                )
                if resp.status_code == 404:
                    return None  # no robots -> allowed
                resp.raise_for_status()
                text = resp.text
            except Exception as exc:  # noqa: BLE001
                log.warning("robots fetch failed for %s: %s", origin, exc)
                return None
        rp = urllib.robotparser.RobotFileParser()
        rp.parse(text.splitlines())
        return rp

    def allowed(self, url: str, user_agent: str | None = None) -> bool:
        ua = user_agent or settings.crawler_user_agent
        p = urllib.parse.urlsplit(url)
        origin = f"{p.scheme}://{p.netloc}"
        now = datetime.now(timezone.utc)
        hit = self._cache.get(origin)
        if hit is None or (now - hit[0]) > ROBOTS_TTL:
            parser = self._load(origin)
            self._cache[origin] = (now, parser)
        else:
            parser = hit[1]
        if parser is None:
            return True
        return parser.can_fetch(ua, url) and parser.can_fetch("*", url)

    def crawl_delay(self, url: str) -> float | None:
        p = urllib.parse.urlsplit(url)
        origin = f"{p.scheme}://{p.netloc}"
        hit = self._cache.get(origin)
        if hit is None:
            return None
        parser = hit[1]
        if parser is None:
            return None
        try:
            delay = parser.crawl_delay(settings.crawler_user_agent) or parser.crawl_delay("*")
        except Exception:  # noqa: BLE001
            return None
        return float(delay) if delay else None

