"""Crawler tests: robots handling, parser robustness, replay pipeline."""
from __future__ import annotations

from pathlib import Path

from app.pipeline.robots import RobotsCache, set_robots_snapshot_dir
from app.pipeline.crawler import CrawlRunner


def _write(path: Path, content: str) -> Path:
    path.write_text(content)
    return path


def test_robots_disallow_enforced(tmp_path):
    _write(tmp_path / "example.org.robots.txt",
           "User-agent: *\nDisallow: /private/\n")
    set_robots_snapshot_dir(tmp_path)
    cache = RobotsCache()
    assert not cache.allowed("https://example.org/private/page")
    assert cache.allowed("https://example.org/public/page")
    set_robots_snapshot_dir(None)


def test_robots_missing_means_allowed(tmp_path):
    set_robots_snapshot_dir(tmp_path)  # no robots file for this host
    cache = RobotsCache()
    assert cache.allowed("https://unknown-host.example/anything")
    set_robots_snapshot_dir(None)


def test_robots_specific_agent(tmp_path):
    _write(tmp_path / "example.org.robots.txt",
           "User-agent: EaseurExerciseBot\nDisallow: /\nUser-agent: *\nAllow: /\n")
    set_robots_snapshot_dir(tmp_path)
    cache = RobotsCache()
    assert not cache.allowed("https://example.org/page")  # our UA disallowed
    set_robots_snapshot_dir(None)


def test_replay_crawl_end_to_end(db, seeded, tmp_path):
    """Full replay pipeline against a mini corpus, incl. robots skip."""
    pages = tmp_path / "pages"
    pages.mkdir()
    (pages / "ok.md").write_text(
        "# Test Program\n\n## Test Wall Stretch\n\n**Main muscles worked:** Gastrocnemius\n\n"
        "**Equipment needed:** None\n\nStep-by-step directions\n\n"
        "- Stand facing a wall with your affected leg straight behind you.\n"
        "- Keep both heels flat on the floor and press your hips forward toward the wall.\n"
        "- Hold this stretch for 30 seconds and then relax for 30 seconds.\n\n"
        "## Chair Balance Drill\n\n- Sit on a chair and lift one foot.\n"
        "- Balance for 30 seconds and keep a tall spine.\n- Repeat three times.\n")
    (pages / "blocked.md").write_text("# Blocked\n\n## Secret Stretch\n\n- Do things.\n- Slowly.\n")
    (tmp_path / "example.org.robots.txt").write_text(
        "User-agent: *\nDisallow: /blocked/\n")
    (tmp_path / "manifest.json").write_text(
        '{"pages": ['
        '{"url": "https://example.org/program", "file": "pages/ok.md", "source_slug": "orthoinfo-aaos", "title": "Test"},'
        '{"url": "https://example.org/blocked/page", "file": "pages/blocked.md", "source_slug": "orthoinfo-aaos", "title": "Blocked"}'
        ']}')
    runner = CrawlRunner(db, __import__("app.enums", fromlist=["CrawlMode"]).CrawlMode.replay,
                         corpus_dir=tmp_path)
    stats = runner.run()
    assert stats["pages_processed"] == 1
    assert stats["skipped_robots"] == 1
    assert stats["created"] >= 1

    from sqlalchemy import select
    from app.enums import CrawlUrlStatus, RecordOrigin
    from app.models import CrawlUrl, Exercise
    urls = db.execute(select(CrawlUrl)).scalars().all()
    statuses = {u.status for u in urls}
    assert CrawlUrlStatus.skipped_robots in statuses
    exercises = db.execute(select(Exercise).where(
        Exercise.origin == RecordOrigin.aggregated)).scalars().all()
    assert any("gastrocnemius" in str([em.muscle.slug for em in e.exercise_muscles])
               for e in exercises)


def test_link_discovery_filters_same_domain():
    from app.pipeline.crawler import _discover_links
    html = """
    <a href="/recovery/knee-conditioning-program/">Knee conditioning exercises</a>
    <a href="/about/">About us</a>
    <a href="https://evil.example/knee-exercise">Knee exercise</a>
    """
    links = _discover_links(html, "https://www.orthoinfo.org/recovery/")
    assert links == ["https://www.orthoinfo.org/recovery/knee-conditioning-program/"]
