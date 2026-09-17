"""Dashboard stats and anatomical coverage."""
from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.enums import (
    ConflictStatus, ExerciseRole, LicenseStatus, RecordOrigin, ReviewItemStatus,
    ReviewItemType, ReviewStatus,
)
from app.models import (
    BodyRegion, DataConflict, Exercise, ExerciseBodyRegion, ExerciseMuscle,
    ExerciseSource, ExerciseType, Muscle, ReviewQueueItem, Source,
)


def dashboard_stats(db: Session) -> dict:
    active = Exercise.merged_into_id.is_(None)
    total = db.scalar(select(func.count()).select_from(Exercise).where(active)) or 0
    verified = db.scalar(select(func.count()).select_from(Exercise).where(
        active, Exercise.review_status == ReviewStatus.approved)) or 0
    pending = db.scalar(select(func.count()).select_from(Exercise).where(
        active, Exercise.review_status == ReviewStatus.pending_review)) or 0
    curated = db.scalar(select(func.count()).select_from(Exercise).where(
        active, Exercise.origin == RecordOrigin.curated)) or 0
    aggregated = db.scalar(select(func.count()).select_from(Exercise).where(
        active, Exercise.origin == RecordOrigin.aggregated)) or 0
    low_conf = db.scalar(select(func.count()).select_from(Exercise).where(
        active, Exercise.confidence < 0.55)) or 0
    sources = db.scalar(select(func.count()).select_from(Source)) or 0
    dup_pairs = db.scalar(select(func.count()).select_from(ReviewQueueItem).where(
        ReviewQueueItem.item_type == ReviewItemType.duplicate_pair,
        ReviewQueueItem.status == ReviewItemStatus.open)) or 0
    conflicts = db.scalar(select(func.count()).select_from(DataConflict).where(
        DataConflict.status == ConflictStatus.open)) or 0
    open_review = db.scalar(select(func.count()).select_from(ReviewQueueItem).where(
        ReviewQueueItem.status == ReviewItemStatus.open)) or 0
    muscles_total = db.scalar(select(func.count()).select_from(Muscle)) or 0

    # muscles with at least one exercise (active only)
    muscles_covered = db.scalar(
        select(func.count(func.distinct(ExerciseMuscle.muscle_id)))
        .select_from(ExerciseMuscle)
        .join(Exercise, Exercise.id == ExerciseMuscle.exercise_id)
        .where(active)
    ) or 0

    # by category / region / source
    by_category = db.execute(
        select(ExerciseType.slug, ExerciseType.name, func.count(Exercise.id))
        .join(Exercise, Exercise.category_id == ExerciseType.id)
        .where(active).group_by(ExerciseType.slug, ExerciseType.name)
        .order_by(func.count(Exercise.id).desc())
    ).all()
    by_region = db.execute(
        select(BodyRegion.slug, BodyRegion.name, func.count(func.distinct(Exercise.id)))
        .join(ExerciseBodyRegion, ExerciseBodyRegion.body_region_id == BodyRegion.id)
        .join(Exercise, Exercise.id == ExerciseBodyRegion.exercise_id)
        .where(active).group_by(BodyRegion.slug, BodyRegion.name, BodyRegion.sort_order)
        .order_by(BodyRegion.sort_order)
    ).all()
    by_source = db.execute(
        select(Source.slug, Source.name, func.count(func.distinct(Exercise.id)))
        .join(ExerciseSource, ExerciseSource.source_id == Source.id)
        .join(Exercise, Exercise.id == ExerciseSource.exercise_id)
        .where(active).group_by(Source.slug, Source.name)
        .order_by(func.count(func.distinct(Exercise.id)).desc())
    ).all()
    top_muscles = db.execute(
        select(Muscle.slug, Muscle.name, func.count(ExerciseMuscle.exercise_id).label("c"))
        .join(ExerciseMuscle, ExerciseMuscle.muscle_id == Muscle.id)
        .join(Exercise, Exercise.id == ExerciseMuscle.exercise_id)
        .where(active).group_by(Muscle.slug, Muscle.name)
        .order_by(func.count(ExerciseMuscle.exercise_id).desc()).limit(12)
    ).all()

    unknown_license = db.scalar(
        select(func.count()).select_from(Source)
        .where(Source.license == LicenseStatus.unknown)) or 0

    return {
        "total_exercises": total,
        "verified_exercises": verified,
        "pending_review": pending,
        "curated_exercises": curated,
        "aggregated_exercises": aggregated,
        "low_confidence": low_conf,
        "sources": sources,
        "sources_unknown_license": unknown_license,
        "potential_duplicates": dup_pairs,
        "conflicts": conflicts,
        "open_review_items": open_review,
        "muscles_total": muscles_total,
        "muscles_covered": muscles_covered,
        "muscles_without_exercises": muscles_total - muscles_covered,
        "by_category": [dict(slug=s, name=n, count=c) for s, n, c in by_category],
        "by_region": [dict(slug=s, name=n, count=c) for s, n, c in by_region],
        "by_source": [dict(slug=s, name=n, count=c) for s, n, c in by_source],
        "top_muscles": [dict(slug=s, name=n, count=c) for s, n, c in top_muscles],
    }


def coverage_status(count: int, sources: int, needs_review: bool = False) -> str:
    if count == 0:
        return "missing"
    if needs_review:
        return "needs_review"
    if count >= 8 and sources >= 2:
        return "excellent"
    if count >= 4:
        return "good"
    return "limited"


def muscle_coverage(db: Session, region_slug: str | None = None) -> list[dict]:
    """Per-muscle coverage: counts by category + verified + sources + status."""
    rows = db.execute(
        select(
            Muscle.id, Muscle.slug, Muscle.name, Muscle.structure_type,
            Muscle.is_small_overlooked, BodyRegion.slug.label("region_slug"),
            BodyRegion.name.label("region_name"),
            func.count(func.distinct(Exercise.id)).label("total"),
            func.count(func.distinct(Exercise.id)).filter(
                Exercise.review_status == ReviewStatus.approved).label("verified"),
            func.count(func.distinct(Exercise.id)).filter(
                Exercise.review_status == ReviewStatus.pending_review).label("pending"),
            func.count(func.distinct(ExerciseSource.source_id)).label("sources"),
        )
        .join(BodyRegion, Muscle.body_region_id == BodyRegion.id)
        .outerjoin(ExerciseMuscle, ExerciseMuscle.muscle_id == Muscle.id)
        .outerjoin(Exercise, (Exercise.id == ExerciseMuscle.exercise_id)
                   & (Exercise.merged_into_id.is_(None))
                   & (Exercise.review_status != ReviewStatus.rejected))
        .outerjoin(ExerciseSource, ExerciseSource.exercise_id == Exercise.id)
        .group_by(Muscle.id, Muscle.slug, Muscle.name, Muscle.structure_type,
                  Muscle.is_small_overlooked, BodyRegion.slug, BodyRegion.name,
                  BodyRegion.sort_order)
        .order_by(BodyRegion.sort_order, Muscle.name)
    ).all()

    # per-category counts per muscle (single grouped query)
    cat_rows = db.execute(
        select(ExerciseMuscle.muscle_id, ExerciseType.slug,
               func.count(Exercise.id).label("c"))
        .join(Exercise, Exercise.id == ExerciseMuscle.exercise_id)
        .join(ExerciseType, ExerciseType.id == Exercise.category_id)
        .where(Exercise.merged_into_id.is_(None),
               Exercise.review_status != ReviewStatus.rejected)
        .group_by(ExerciseMuscle.muscle_id, ExerciseType.slug)
    ).all()
    cats: dict[int, dict[str, int]] = {}
    for muscle_id, slug, c in cat_rows:
        cats.setdefault(muscle_id, {})[slug] = c

    out = []
    for r in rows:
        c = cats.get(r.id, {})
        needs_review = r.total > 0 and r.pending > 0 and r.verified == 0
        out.append({
            "id": r.id, "slug": r.slug, "name": r.name,
            "structure_type": r.structure_type,
            "is_small_overlooked": r.is_small_overlooked,
            "region_slug": r.region_slug, "region_name": r.region_name,
            "total": r.total, "verified": r.verified, "pending": r.pending,
            "sources": r.sources,
            "stretching": c.get("stretching", 0),
            "mobility": c.get("mobility", 0),
            "rehabilitation": c.get("rehabilitation", 0) + c.get("physiotherapy", 0),
            "status": coverage_status(r.total, r.sources, needs_review),
        })
    if region_slug:
        out = [o for o in out if o["region_slug"] == region_slug]
    return out


def region_coverage(db: Session) -> list[dict]:
    rows = db.execute(
        select(
            BodyRegion.id, BodyRegion.slug, BodyRegion.name,
            func.count(func.distinct(Exercise.id)).label("total"),
            func.count(func.distinct(Exercise.id)).filter(
                Exercise.review_status == ReviewStatus.approved).label("verified"),
            func.count(func.distinct(ExerciseSource.source_id)).label("sources"),
            func.count(func.distinct(ExerciseMuscle.muscle_id)).label("muscles_covered"),
        )
        .outerjoin(ExerciseBodyRegion, ExerciseBodyRegion.body_region_id == BodyRegion.id)
        .outerjoin(Exercise, (Exercise.id == ExerciseBodyRegion.exercise_id)
                   & (Exercise.merged_into_id.is_(None)))
        .outerjoin(ExerciseSource, ExerciseSource.exercise_id == Exercise.id)
        .outerjoin(ExerciseMuscle, ExerciseMuscle.exercise_id == Exercise.id)
        .group_by(BodyRegion.id, BodyRegion.slug, BodyRegion.name, BodyRegion.sort_order)
        .order_by(BodyRegion.sort_order)
    ).all()
    muscle_counts = db.execute(
        select(BodyRegion.slug, func.count(Muscle.id))
        .join(Muscle, Muscle.body_region_id == BodyRegion.id)
        .group_by(BodyRegion.slug)
    ).all()
    mc = {s: c for s, c in muscle_counts}
    covered_counts = db.execute(
        select(BodyRegion.slug, func.count(func.distinct(Muscle.id)))
        .join(Muscle, Muscle.body_region_id == BodyRegion.id)
        .join(ExerciseMuscle, ExerciseMuscle.muscle_id == Muscle.id)
        .join(Exercise, Exercise.id == ExerciseMuscle.exercise_id)
        .where(Exercise.merged_into_id.is_(None))
        .group_by(BodyRegion.slug)
    ).all()
    cc = {s: c for s, c in covered_counts}
    return [
        {"id": r.id, "slug": r.slug, "name": r.name, "total": r.total,
         "verified": r.verified, "sources": r.sources,
         "muscles_total": mc.get(r.slug, 0), "muscles_covered": cc.get(r.slug, 0),
         "status": coverage_status(r.total, r.sources)}
        for r in rows
    ]
