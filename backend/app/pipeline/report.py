"""Data quality report generation -> docs/data-quality-report.md."""
from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.enums import (
    ConflictStatus, CrawlUrlStatus, LicenseStatus, RecordOrigin, ReviewItemStatus,
    ReviewItemType, ReviewStatus,
)
from app.models import (
    CrawlJob, CrawlUrl, DataConflict, Exercise, ExerciseMuscle, ExerciseSource,
    Muscle, ReviewQueueItem, Source,
)
from app.services.stats import coverage_status, muscle_coverage, region_coverage


def generate_report(db: Session) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    active = Exercise.merged_into_id.is_(None)
    total = db.scalar(select(func.count()).select_from(Exercise).where(active)) or 0
    curated = db.scalar(select(func.count()).select_from(Exercise).where(
        active, Exercise.origin == RecordOrigin.curated)) or 0
    aggregated = db.scalar(select(func.count()).select_from(Exercise).where(
        active, Exercise.origin == RecordOrigin.aggregated)) or 0
    approved = db.scalar(select(func.count()).select_from(Exercise).where(
        active, Exercise.review_status == ReviewStatus.approved)) or 0
    pending = db.scalar(select(func.count()).select_from(Exercise).where(
        active, Exercise.review_status == ReviewStatus.pending_review)) or 0
    merged = db.scalar(select(func.count()).select_from(Exercise).where(
        Exercise.merged_into_id.isnot(None))) or 0

    sources_total = db.scalar(select(func.count()).select_from(Source)) or 0
    sources_unknown = db.scalar(select(func.count()).select_from(Source).where(
        Source.license == LicenseStatus.unknown)) or 0

    jobs = db.execute(select(CrawlJob).order_by(CrawlJob.id)).scalars().all()
    pages_processed = sum((j.stats or {}).get("pages_processed", 0) for j in jobs)
    pages_failed = sum((j.stats or {}).get("pages_failed", 0) for j in jobs)
    skipped_robots = sum((j.stats or {}).get("skipped_robots", 0) for j in jobs)
    candidates = sum((j.stats or {}).get("candidates", 0) for j in jobs)
    linked = sum((j.stats or {}).get("linked", 0) for j in jobs)
    rejected = sum((j.stats or {}).get("rejected", 0) for j in jobs)

    url_status_counts = dict(db.execute(
        select(CrawlUrl.status, func.count()).group_by(CrawlUrl.status)).all())

    dup_open = db.scalar(select(func.count()).select_from(ReviewQueueItem).where(
        ReviewQueueItem.item_type == ReviewItemType.duplicate_pair,
        ReviewQueueItem.status == ReviewItemStatus.open)) or 0
    review_open = db.scalar(select(func.count()).select_from(ReviewQueueItem).where(
        ReviewQueueItem.status == ReviewItemStatus.open)) or 0
    conflicts = db.scalar(select(func.count()).select_from(DataConflict).where(
        DataConflict.status == ConflictStatus.open)) or 0
    low_conf = db.scalar(select(func.count()).select_from(Exercise).where(
        active, Exercise.confidence < 0.55)) or 0
    med_claims = db.scalar(select(func.count()).select_from(Exercise).where(
        active, Exercise.is_medical_claim.is_(True))) or 0

    muscles_total = db.scalar(select(func.count()).select_from(Muscle)) or 0
    covered = db.scalar(
        select(func.count(func.distinct(ExerciseMuscle.muscle_id)))
        .select_from(ExerciseMuscle)
        .join(Exercise, Exercise.id == ExerciseMuscle.exercise_id).where(active)) or 0

    m_cov = muscle_coverage(db)
    missing_muscles = [m["name"] for m in m_cov if m["status"] == "missing"]
    limited = [m for m in m_cov if m["status"] == "limited"]
    r_cov = region_coverage(db)

    by_status: dict[str, int] = {
        str(k.value if hasattr(k, "value") else k): v for k, v in url_status_counts.items()}

    lines = [
        "# Data Quality Report",
        "",
        f"_Generated {now} by the Easeur Exercise Knowledge Base pipeline._",
        "",
        "## Sources",
        "",
        f"- Sources registered: **{sources_total}**",
        f"- Sources with unknown licensing: **{sources_unknown}** (conservative default; flagged for review)",
        f"- Crawl jobs run: **{len(jobs)}** "
        f"({', '.join(sorted({j.mode.value for j in jobs})) or 'none'} mode)",
        "",
        "## Crawl & extraction",
        "",
        f"- Pages processed: **{pages_processed}**",
        f"- Pages failed: **{pages_failed}**",
        f"- URLs skipped by robots/policy: **{skipped_robots}**",
        f"- Exercise candidates extracted: **{candidates}**",
        f"- Candidates linked to existing exercises (dedup stage 1): **{linked}**",
        f"- Candidates rejected during normalization: **{rejected}**",
        f"- URL status breakdown: " + ", ".join(f"`{k}`={v}" for k, v in sorted(by_status.items())),
        "",
        "## Exercises",
        "",
        f"- Normalized exercises (active): **{total}**",
        f"  - Curated: **{curated}** (team-authored, approved)",
        f"  - Aggregated from sources: **{aggregated}**",
        f"- Approved: **{approved}** — Pending review: **{pending}**",
        f"- Merged duplicates (parked): **{merged}**",
        f"- Potential duplicate pairs awaiting review: **{dup_open}**",
        f"- Open data conflicts: **{conflicts}**",
        f"- Low-confidence records (<0.55): **{low_conf}**",
        f"- Records flagged with medical-claim language: **{med_claims}** (held for clinical review)",
        f"- Open review-queue items (all types): **{review_open}**",
        "",
        "## Anatomical coverage",
        "",
        f"- Structures in taxonomy: **{muscles_total}** "
        "(muscles, tendons, ligaments, fascia, nerves)",
        f"- Structures with at least one exercise: **{covered}** "
        f"({100 * covered / max(1, muscles_total):.0f}%)",
        f"- Structures with no exercises: **{len(missing_muscles)}**",
        "",
        "### By body region",
        "",
        "| Region | Exercises | Verified | Sources | Muscles covered | Status |",
        "|---|---|---|---|---|---|",
    ]
    for r in r_cov:
        lines.append(f"| {r['name']} | {r['total']} | {r['verified']} | {r['sources']} | "
                     f"{r['muscles_covered']}/{r['muscles_total']} | {r['status']} |")
    lines += [
        "",
        "### Muscles / structures with no exercises yet",
        "",
        (", ".join(missing_muscles) if missing_muscles else "_none — full coverage_"),
        "",
        "### Limited-coverage structures (1-3 exercises)",
        "",
        (", ".join(f"{m['name']} ({m['total']})" for m in limited) or "_none_"),
        "",
        "## Licensing summary",
        "",
        "| License | Sources |",
        "|---|---|",
    ]
    lic_rows = db.execute(select(Source.license, func.count())
                          .group_by(Source.license)).all()
    for lic, cnt in lic_rows:
        lines.append(f"| {lic.value} | {cnt} |")
    lines += [
        "",
        "## Notes & caveats",
        "",
        "- Aggregated records store **structured facts + provenance only** — never full "
        "copyrighted article text or media.",
        "- Where licensing is unclear, `commercial_use_allowed = unknown` and the exercise "
        "is queued for licensing review.",
        "- Medical-claim language detected in source text is flagged and requires review "
        "before approval; the pipeline never invents diagnoses or treatments.",
        "- AI enrichment: the deterministic anatomy mapper (`heuristic-anatomy-mapper v1`) "
        "performs classification; LLM enrichment is implemented but disabled unless "
        "`EASEUR_AI_API_KEY` is configured. All AI/inference output is marked "
        "`ai_inference` + `pending_review`.",
        "",
    ]
    return "\n".join(lines)
