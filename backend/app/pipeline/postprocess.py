"""Post-processing: dedup scan, conflict persistence, validation sweep.

Runs after ingestion (and on demand from the CLI) to populate the review
queue with duplicate pairs, conflicts, licensing/medical/low-confidence flags.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import settings
from app.enums import (
    ConflictStatus, RecordOrigin, ReviewItemType, ReviewItemStatus, ReviewStatus,
)
from app.log import log_event
from app.models import DataConflict, Exercise, ReviewQueueItem
from app.pipeline.dedup import find_duplicate_pairs
from app.pipeline.validate import validate_exercise

log = logging.getLogger("easeur.postprocess")


@dataclass
class _Rec:
    """Lightweight adapter for the dedup engine."""
    id: int
    canonical_name: str
    aliases: list
    muscle_slugs: set
    region_slugs: set
    category_slug: str | None
    merged_into_id: int | None = None


def _records(db: Session) -> list[_Rec]:
    out: list[_Rec] = []
    for ex in db.execute(
        select(Exercise).where(Exercise.merged_into_id.is_(None),
                               Exercise.review_status != ReviewStatus.rejected)
    ).scalars():
        out.append(_Rec(
            id=ex.id,
            canonical_name=ex.canonical_name,
            aliases=list(ex.aliases or []),
            muscle_slugs={em.muscle.slug for em in ex.exercise_muscles},
            region_slugs={r.body_region.slug for r in ex.body_regions},
            category_slug=ex.category.slug if ex.category else None,
        ))
    return out


def _existing_pairs(db: Session) -> set[tuple[int, int]]:
    pairs: set[tuple[int, int]] = set()
    items = db.execute(select(ReviewQueueItem).where(
        ReviewQueueItem.item_type == ReviewItemType.duplicate_pair)).scalars()
    for it in items:
        if it.exercise_id and it.related_exercise_id:
            pairs.add((min(it.exercise_id, it.related_exercise_id),
                       max(it.exercise_id, it.related_exercise_id)))
    return pairs


def run_dedup_scan(db: Session) -> dict:
    """Full dedup scan: auto-merge near-exact, queue the rest for review."""
    stats = {"auto_merged": 0, "review_pairs": 0, "scanned": 0}
    recs = _records(db)
    stats["scanned"] = len(recs)
    pairs = find_duplicate_pairs(
        recs, auto_merge_threshold=settings.duplicate_auto_merge_threshold,
        existing_pairs=_existing_pairs(db),
    )
    by_id = {ex.id: ex for ex in db.execute(select(Exercise)).scalars()}

    for pair in sorted(pairs, key=lambda p: -p.score):
        a, b = by_id.get(pair.a_id), by_id.get(pair.b_id)
        if not a or not b or a.merged_into_id or b.merged_into_id:
            continue
        if pair.recommendation == "auto_merge":
            _merge(db, a, b, note=f"auto-merge {pair.stage} score={pair.score}")
            stats["auto_merged"] += 1
        elif pair.recommendation == "review":
            db.add(ReviewQueueItem(
                item_type=ReviewItemType.duplicate_pair,
                exercise_id=pair.a_id, related_exercise_id=pair.b_id,
                payload={"similarity": pair.score, "stage": pair.stage,
                         "components": pair.components,
                         "names": [pair.a_name, pair.b_name]},
                priority=2 if pair.score >= 0.8 else 4,
                reason=f"Potential duplicate ({pair.stage}, similarity {pair.score:.2f})",
            ))
            stats["review_pairs"] += 1
            log_event(log, "duplicate_detected", stage=pair.stage,
                      a=pair.a_id, b=pair.b_id, score=pair.score, action="queued_for_review")
    db.commit()
    return stats


def _merge(db: Session, target: Exercise, dup: Exercise, *, note: str) -> None:
    """Merge `dup` into `target`: move sources/provenance, alias the name, park dup."""
    from app.models import ExerciseSource, Provenance
    for es in db.execute(select(ExerciseSource).where(ExerciseSource.exercise_id == dup.id)).scalars():
        es.exercise_id = target.id
    for p in db.execute(select(Provenance).where(Provenance.exercise_id == dup.id)).scalars():
        p.exercise_id = target.id
    aliases = set(target.aliases or []) | {dup.canonical_name} | set(dup.aliases or [])
    target.aliases = sorted(a for a in aliases if a.lower() != target.canonical_name.lower())[:10]
    dup.merged_into_id = target.id
    dup.review_status = ReviewStatus.rejected
    db.add(ReviewQueueItem(
        item_type=ReviewItemType.other,
        exercise_id=target.id, related_exercise_id=dup.id,
        payload={"merged": True, "note": note},
        status=ReviewItemStatus.resolved,
        reason=f"Merged automatically: {note}",
        resolved_at=datetime.now(timezone.utc),
    ))
    log_event(log, "review_action", action="auto_merge", target=target.id, merged=dup.id)


def run_validation_sweep(db: Session) -> dict:
    """Validate every non-merged aggregated exercise; queue issues."""
    stats = {"checked": 0, "issues": 0, "by_code": {}}
    open_items = {
        (i.exercise_id, i.payload.get("code"))
        for i in db.execute(select(ReviewQueueItem).where(
            ReviewQueueItem.status == ReviewItemStatus.open)).scalars()
        if i.exercise_id
    }
    exercises = db.execute(select(Exercise).where(Exercise.merged_into_id.is_(None))).scalars()
    for ex in exercises:
        if ex.origin == RecordOrigin.curated:
            continue
        stats["checked"] += 1
        ex.confidence = ex.confidence or 0.5
        if ex.confidence < settings.low_confidence_threshold:
            issues = validate_exercise(db, ex)
            if not any(i.code == "low_confidence" for i in issues):
                from app.pipeline.validate import ValidationIssue
                issues.append(ValidationIssue(
                    ex.id, "low_confidence",
                    f"Confidence {ex.confidence:.2f} below threshold "
                    f"{settings.low_confidence_threshold}.",
                    ReviewItemType.low_confidence, priority=4))
        else:
            issues = validate_exercise(db, ex)
        for issue in issues:
            key = (issue.exercise_id, issue.code)
            if key in open_items:
                continue
            stats["issues"] += 1
            stats["by_code"][issue.code] = stats["by_code"].get(issue.code, 0) + 1
            db.add(ReviewQueueItem(
                item_type=issue.item_type, exercise_id=issue.exercise_id,
                payload={"code": issue.code, **(issue.payload or {})},
                priority=issue.priority, reason=issue.message,
            ))
    db.commit()
    return stats


def persist_conflicts(db: Session, conflicts: list[dict]) -> int:
    """Store ingestion-detected conflicts (already carry exercise_id/source_ids)."""
    for c in conflicts:
        db.add(DataConflict(
            exercise_id=c["exercise_id"], field_name=c["field"],
            values=c["values"], source_ids=c["source_ids"],
            status=ConflictStatus.open,
        ))
    db.commit()
    return len(conflicts)


def run_full_postprocess(db: Session) -> dict:
    dedup_stats = run_dedup_scan(db)
    validation_stats = run_validation_sweep(db)
    return {"dedup": dedup_stats, "validation": validation_stats}
