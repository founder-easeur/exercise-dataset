"""Crawl orchestration.

Two modes:
  live   — real HTTP against registered sources (robots-checked, rate-limited)
  replay — processes a local snapshot corpus (manifest.json) so the pipeline
           can run in environments without general egress (like CI or this
           project's build sandbox). The extraction -> normalization ->
           dedup -> validation stages are identical.
"""
from __future__ import annotations

import hashlib
import json
import logging
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import settings
from app.enums import (
    CrawlJobStatus, CrawlMode, CrawlUrlStatus, LicenseStatus, RobotsStatus,
)
from app.log import log_event
from app.models import CrawlJob, CrawlUrl, Source, SourceDocument
from app.pipeline import robots as robots_mod
from app.pipeline.extract import extract_candidates
from app.pipeline.fetcher import FetchResult, Fetcher
from app.pipeline.ingest import ingest_candidates
from app.pipeline.research_queries import generate_queries
from app.taxonomy.anatomy_data import MUSCLES

log = logging.getLogger("easeur.crawl")

LINK_PATTERN = re.compile(
    r"(exercise|stretch|mobili|rehab|physio|conditioning|therapeutic|warm-?up|"
    r"cool-?down|flexib)", re.I,
)


@dataclass
class CrawlStats:
    pages_processed: int = 0
    pages_failed: int = 0
    skipped_robots: int = 0
    skipped_policy: int = 0
    duplicate_content: int = 0
    candidates: int = 0
    created: int = 0
    linked: int = 0
    rejected: int = 0
    conflicts: int = 0
    errors: list = field(default_factory=list)

    def to_dict(self) -> dict:
        d = {k: v for k, v in self.__dict__.items() if k != "errors"}
        d["errors"] = self.errors[:10]
        return d


class CrawlRunner:
    def __init__(self, db: Session, mode: CrawlMode, corpus_dir: Path | None = None):
        self.db = db
        self.mode = mode
        self.corpus_dir = corpus_dir
        self.stats = CrawlStats()
        self.seen_hashes: set[str] = set()

    # ------------------------------------------------------------------ run
    def run(self, source_slugs: list[str] | None = None, max_pages: int | None = None) -> dict:
        max_pages = max_pages or settings.crawler_max_pages_per_job
        queries = generate_queries(MUSCLES, limit=50)  # recorded for transparency
        job = CrawlJob(
            mode=self.mode, status=CrawlJobStatus.running,
            config={"max_pages": max_pages, "sources": source_slugs,
                    "research_queries_sample": [q["query"] for q in queries[:50]]},
            started_at=datetime.now(timezone.utc),
        )
        self.db.add(job)
        self.db.commit()
        log_event(log, "crawl_started", job_id=job.id, mode=self.mode.value,
                  sources=source_slugs)

        try:
            if self.mode == CrawlMode.replay:
                self._run_replay(job, source_slugs, max_pages)
            else:
                self._run_live(job, source_slugs, max_pages)
            job.status = CrawlJobStatus.completed
        except Exception as exc:  # noqa: BLE001
            job.status = CrawlJobStatus.failed
            job.error = str(exc)
            self.stats.errors.append(str(exc))
            log_event(log, "crawl_failed", job_id=job.id, error=str(exc), level=logging.ERROR)
        finally:
            job.finished_at = datetime.now(timezone.utc)
            job.stats = self.stats.to_dict()
            self.db.commit()
            log_event(log, "crawl_completed", job_id=job.id, mode=self.mode.value,
                      stats=self.stats.to_dict())
        return {"job_id": job.id, **self.stats.to_dict()}

    # -------------------------------------------------------------- replay
    def _run_replay(self, job: CrawlJob, source_slugs: list[str] | None, max_pages: int) -> None:
        assert self.corpus_dir and self.corpus_dir.exists(), "corpus dir missing"
        robots_mod.set_robots_snapshot_dir(self.corpus_dir)
        manifest_path = self.corpus_dir / "manifest.json"
        manifest = json.loads(manifest_path.read_text())
        pages = manifest["pages"]
        if source_slugs:
            pages = [p for p in pages if p["source_slug"] in source_slugs]

        for page in pages[:max_pages]:
            url: str = page["url"]
            curl = CrawlUrl(crawl_job_id=job.id, url=url)
            self.db.add(curl)
            source = self._source_by_slug(page["source_slug"])
            if source is None:
                curl.status = CrawlUrlStatus.failed
                curl.error = "source not registered"
                self.stats.pages_failed += 1
                self.db.commit()
                continue

            # robots enforcement (snapshot-based in replay mode)
            if not robots_mod.RobotsCache().allowed(url):
                curl.status = CrawlUrlStatus.skipped_robots
                self.stats.skipped_robots += 1
                source.robots_status = RobotsStatus.disallowed
                self.db.commit()
                log_event(log, "url_skipped", url=url, reason="robots_disallow")
                continue
            source.robots_status = RobotsStatus.allowed

            file = self.corpus_dir / page["file"]
            if not file.exists():
                curl.status = CrawlUrlStatus.failed
                curl.error = "snapshot file missing"
                self.stats.pages_failed += 1
                self.db.commit()
                continue
            content = file.read_text(encoding="utf-8", errors="replace")
            result = FetchResult(url=url, status=200, content=content,
                                 content_type="text/markdown")
            self._process_document(job, curl, source, result, is_markdown=True)

    # ---------------------------------------------------------------- live
    def _run_live(self, job: CrawlJob, source_slugs: list[str] | None, max_pages: int) -> None:
        fetcher = Fetcher()
        sources = self.db.execute(select(Source).where(Source.is_active.is_(True))).scalars().all()
        if source_slugs:
            sources = [s for s in sources if s.slug in source_slugs]
        robots_cache = robots_mod.RobotsCache()

        for source in sources:
            frontier = list(LIVE_SEED_URLS.get(source.slug, []))
            budget = max_pages // max(1, len(sources))
            visited: set[str] = set()
            processed = 0
            while frontier and processed < budget:
                url = frontier.pop(0)
                if url in visited:
                    continue
                visited.add(url)
                curl = CrawlUrl(crawl_job_id=job.id, url=url)
                self.db.add(curl)

                if not robots_cache.allowed(url):
                    curl.status = CrawlUrlStatus.skipped_robots
                    self.stats.skipped_robots += 1
                    self.db.commit()
                    log_event(log, "url_skipped", url=url, reason="robots_disallow")
                    continue
                source.robots_status = RobotsStatus.allowed

                result = fetcher.fetch(url)
                curl.http_status = result.status
                curl.error = result.error
                if not result.ok:
                    curl.status = CrawlUrlStatus.failed
                    self.stats.pages_failed += 1
                    self.db.commit()
                    continue
                self.db.commit()

                # same-domain link discovery for the next depth level
                if len(visited) < settings.crawler_max_depth * 8:
                    for link in _discover_links(result.content or "", url):
                        if link not in visited and link not in frontier:
                            frontier.append(link)
                    frontier = frontier[:40]

                processed += 1
                self._process_document(job, curl, source, result, is_markdown=False)

    # ------------------------------------------------------------ document
    def _process_document(self, job: CrawlJob, curl: CrawlUrl, source: Source,
                          result: FetchResult, *, is_markdown: bool) -> None:
        content = result.content or ""
        content_hash = hashlib.sha256(content.encode("utf-8", "replace")).hexdigest()
        if content_hash in self.seen_hashes:
            curl.status = CrawlUrlStatus.duplicate_content
            curl.content_hash = content_hash
            self.stats.duplicate_content += 1
            self.db.commit()
            return
        self.seen_hashes.add(content_hash)

        doc = self.db.execute(
            select(SourceDocument).where(SourceDocument.url == result.url)
        ).scalar_one_or_none()
        if doc is None:
            doc = SourceDocument(
                source_id=source.id, url=result.url,
                fetch_mode=self.mode, http_status=result.status or 200)
            self.db.add(doc)
        from app.pipeline.extract import page_title, parse_markdown
        from app.services.text import truncate
        soup = parse_markdown(content) if is_markdown else __import__(
            "bs4", fromlist=["BeautifulSoup"]).BeautifulSoup(content, "html.parser")
        doc.title = page_title(soup)
        doc.content_hash = content_hash
        doc.word_count = len(content.split())
        doc.text_excerpt = truncate(content, 4000)
        doc.fetched_at = datetime.now(timezone.utc)

        candidates = extract_candidates(content, result.url, source.slug, is_markdown=is_markdown)
        doc.extraction_stats = {"candidates": len(candidates)}
        curl.status = CrawlUrlStatus.processed
        curl.content_hash = content_hash
        curl.fetched_at = datetime.now(timezone.utc)
        self.db.commit()

        ingest = ingest_candidates(self.db, candidates)
        self.stats.candidates += len(candidates)
        self.stats.created += ingest.created_count
        self.stats.linked += ingest.linked_count
        self.stats.rejected += len(ingest.rejected)
        self.stats.conflicts += len(ingest.conflicts)
        self.stats.pages_processed += 1

    def _source_by_slug(self, slug: str) -> Source | None:
        return self.db.execute(select(Source).where(Source.slug == slug)).scalar_one_or_none()


# Live-mode seed URLs: hand-vetted hub pages per registered source.
LIVE_SEED_URLS: dict[str, list[str]] = {
    "orthoinfo-aaos": [
        "https://www.orthoinfo.org/recovery/rotator-cuff-and-shoulder-conditioning-program/",
        "https://www.orthoinfo.org/recovery/knee-conditioning-program/",
        "https://www.orthoinfo.org/recovery/foot-and-ankle-conditioning-program/",
    ],
    "versus-arthritis": [
        "https://www.arthritis-uk.org/information-and-support/living-with-arthritis/health-and-wellbeing/exercising-with-arthritis/exercises-for-healthy-joints/",
        "https://www.arthritis-uk.org/information-and-support/living-with-arthritis/health-and-wellbeing/exercising-with-arthritis/exercises-for-healthy-joints/exercises-for-the-neck/",
        "https://www.arthritis-uk.org/information-and-support/living-with-arthritis/health-and-wellbeing/exercising-with-arthritis/exercises-for-healthy-joints/exercises-for-the-fingers-hands-and-wrists/",
        "https://www.arthritis-uk.org/information-and-support/living-with-arthritis/health-and-wellbeing/exercising-with-arthritis/exercises-for-healthy-joints/exercises-for-the-toes-feet-and-ankles/",
        "https://www.arthritis-uk.org/information-and-support/living-with-arthritis/health-and-wellbeing/exercising-with-arthritis/exercises-for-healthy-joints/exercises-for-the-elbows/",
        "https://www.arthritis-uk.org/information-and-support/living-with-arthritis/health-and-wellbeing/exercising-with-arthritis/exercises-for-healthy-joints/exercises-for-the-back/",
    ],
    "nhs-inform-scotland": [
        "https://www.nhsinform.scot/illnesses-and-conditions/muscle-bone-and-joints/arm-shoulder-and-hand-problems-and-conditions/exercises-for-wrist-hand-and-finger-problems",
        "https://www.nhsinform.scot/illnesses-and-conditions/muscle-bone-and-joints/neck-and-back-problems-and-conditions/exercises-for-neck-problems",
        "https://www.nhsinform.scot/illnesses-and-conditions/muscle-bone-and-joints/leg-foot-and-hip-problems-and-conditions/exercises-for-hip-problems",
        "https://www.nhsinform.scot/illnesses-and-conditions/muscle-bone-and-joints/leg-foot-and-hip-problems-and-conditions/exercises-for-knee-problems",
        "https://www.nhsinform.scot/illnesses-and-conditions/muscle-bone-and-joints/leg-foot-and-hip-problems-and-conditions/exercises-for-ankle-problems",
        "https://www.nhsinform.scot/illnesses-and-conditions/muscle-bone-and-joints/leg-foot-and-hip-problems-and-conditions/exercises-for-foot-and-toe-problems",
    ],
    "nhs-uk": [
        "https://www.nhs.uk/conditions/back-pain/",
        "https://www.nhs.uk/conditions/knee-pain/",
    ],
}


def _discover_links(html: str, base_url: str) -> list[str]:
    """Same-domain links whose path/text looks exercise-related (live mode only)."""
    from bs4 import BeautifulSoup
    from urllib.parse import urljoin, urlsplit
    try:
        soup = BeautifulSoup(html, "html.parser")
    except Exception:  # noqa: BLE001
        return []
    origin = f"{urlsplit(base_url).scheme}://{urlsplit(base_url).netloc}"
    out: list[str] = []
    for a in soup.find_all("a", href=True):
        href = a["href"].split("#")[0]
        text = a.get_text(" ", strip=True)
        if not (LINK_PATTERN.search(href) or LINK_PATTERN.search(text or "")):
            continue
        if href.startswith("/"):
            href = urljoin(origin, href)
        if href.startswith(origin):
            out.append(href)
    return out[:20]
