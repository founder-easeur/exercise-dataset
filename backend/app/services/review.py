"""Review queue actions with audit logging.

All mutating review endpoints require the admin API key.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.enums import (
    ConflictStatus, DataOrigin, Difficulty, ReviewAction, ReviewItemStatus,
    ReviewItemType, ReviewStatus,
)
from app.log import log_event
from app.models import (
    AuditLog, DataConflict, Exercise, ExerciseMuscle, ExerciseSource, ExerciseType,
    Provenance, ReviewQueueItem, Source,
)

log = logging.getLogger("easeur.review")


def list_queue(db: Session, item_type: str | None = None,
               status: str = "open", limit: int = 100) -> list[ReviewQueueItem]:
    query = select(ReviewQueueItem).order_by(ReviewQueueItem.priority,
                                             ReviewQueueItem.created_at.desc())
    if item_type:
        query = query.where(ReviewQueueItem.item_type == ReviewItemType(item_type))
    if status and status != "all":
        query = query.where(ReviewQueueItem.status == ReviewItemStatus(status))
    items = db.execute(query.limit(limit)).scalars().all()
    # attach exercise names cheaply
    ex_ids = {i.exercise_id for i in items if i.exercise_id} | \
             {i.related_exercise_id for i in items if i.related_exercise_id}
    if ex_ids:
        names = {e.id: e.canonical_name for e in db.execute(
            select(Exercise).where(Exercise.id.in_(ex_ids))).scalars()}
        for i in items:
            i._exercise_name = names.get(i.exercise_id)  # type: ignore[attr-defined]
            i._related_name = names.get(i.related_exercise_id)  # type: ignore[attr-defined]
    return items


def _audit(db: Session, actor: str, action: str, item: ReviewQueueItem, details: dict) -> None:
    db.add(AuditLog(actor=actor, action=action, entity_type="review_queue_item",
                    entity_id=item.id, details=details))


def apply_review_action(db: Session, item_id: int, action: ReviewAction,
                        actor: str = "admin", note: str | None = None,
                        edits: dict | None = None) -> ReviewQueueItem | None:
    item = db.get(ReviewQueueItem, item_id)
    if item is None:
        return None

    if action == ReviewAction.approve:
        _do_approve(db, item)
    elif action == ReviewAction.reject:
        _do_reject(db, item)
    elif action == ReviewAction.merge:
        _do_merge(db, item, keep=(edits or {}).get("keep", "primary"))
    elif action == ReviewAction.split:
        _do_split(db, item)
    elif action == ReviewAction.flag:
        item.status = ReviewItemStatus.flagged
    elif action == ReviewAction.dismiss:
        item.status = ReviewItemStatus.dismissed
    elif action == ReviewAction.edit and edits:
        _do_edit(db, item, edits)

    if note:
        item.resolution_note = note
    if item.status == ReviewItemStatus.open:
        # action-specific default status
        item.status = {
            ReviewAction.approve: ReviewItemStatus.approved,
            ReviewAction.reject: ReviewItemStatus.rejected,
            ReviewAction.merge: ReviewItemStatus.merged,
            ReviewAction.split: ReviewItemStatus.split,
            ReviewAction.edit: ReviewItemStatus.resolved,
            ReviewAction.flag: ReviewItemStatus.flagged,
            ReviewAction.dismiss: ReviewItemStatus.dismissed,
        }[action]
    item.resolved_at = datetime.now(timezone.utc)
    _audit(db, actor, f"review_{action.value}", item,
           {"action": action.value, "note": note, "edits": edits or {}})
    db.commit()
    log_event(log, "review_action", item_id=item.id, action=action.value,
              actor=actor, exercise_id=item.exercise_id)
    return item


def _do_approve(db: Session, item: ReviewQueueItem) -> None:
    if item.item_type == ReviewItemType.duplicate_pair:
        # approving a duplicate pair means "these are duplicates; merge them"
        _do_merge(db, item)
        return
    ex = db.get(Exercise, item.exercise_id) if item.exercise_id else None
    if ex is not None:
        ex.review_status = ReviewStatus.approved
        db.add(Provenance(exercise_id=ex.id, field_name="review",
                          value=f"approved via review item {item.id}",
                          origin=DataOrigin.human_reviewed, confidence=1.0))
    if item.item_type == ReviewItemType.anatomy_conflict and item.exercise_id:
        for c in db.execute(select(DataConflict).where(
                DataConflict.exercise_id == item.exercise_id,
                DataConflict.status == ConflictStatus.open)).scalars():
            c.status = ConflictStatus.resolved
            c.resolution = f"resolved via review item {item.id}"


def _do_reject(db: Session, item: ReviewQueueItem) -> None:
    ex = db.get(Exercise, item.exercise_id) if item.exercise_id else None
    if ex is not None and item.item_type != ReviewItemType.duplicate_pair:
        ex.review_status = ReviewStatus.rejected


def _do_merge(db: Session, item: ReviewQueueItem, keep: str = "primary") -> None:
    if not (item.exercise_id and item.related_exercise_id):
        return
    target = db.get(Exercise, item.exercise_id)
    dup = db.get(Exercise, item.related_exercise_id)
    if not target or not dup or target.id == dup.id:
        return
    if keep == "related":  # reviewer chose to keep the related record instead
        target, dup = dup, target
    for es in db.execute(select(ExerciseSource).where(
            ExerciseSource.exercise_id == dup.id)).scalars():
        es.exercise_id = target.id
    for p in db.execute(select(Provenance).where(
            Provenance.exercise_id == dup.id)).scalars():
        p.exercise_id = target.id
    # union of muscle links (preserve target roles)
    target_muscles = {(em.muscle_id, em.role) for em in target.exercise_muscles}
    for em in dup.exercise_muscles:
        if (em.muscle_id, em.role) not in target_muscles:
            db.add(ExerciseMuscle(exercise_id=target.id, muscle_id=em.muscle_id,
                                  role=em.role, confidence=em.confidence,
                                  origin=DataOrigin.human_reviewed.value))
    aliases = set(target.aliases or []) | {dup.canonical_name} | set(dup.aliases or [])
    target.aliases = sorted(a for a in aliases
                            if a.lower() != target.canonical_name.lower())[:10]
    dup.merged_into_id = target.id
    dup.review_status = ReviewStatus.rejected
    target.review_status = ReviewStatus.approved
    db.add(Provenance(exercise_id=target.id, field_name="merge",
                      value=f"merged exercise {dup.id} ({dup.canonical_name})",
                      origin=DataOrigin.human_reviewed, confidence=1.0))


def _do_split(db: Session, item: ReviewQueueItem) -> None:
    if item.item_type == ReviewItemType.duplicate_pair and item.related_exercise_id:
        dup = db.get(Exercise, item.related_exercise_id)
        if dup and dup.merged_into_id:
            dup.merged_into_id = None
            dup.review_status = ReviewStatus.pending_review


def _do_edit(db: Session, item: ReviewQueueItem, edits: dict) -> None:
    ex = db.get(Exercise, item.exercise_id) if item.exercise_id else None
    if ex is None:
        return
    allowed = {"canonical_name", "instructions", "safety_notes", "contraindications",
               "clinical_relevance", "breathing", "position", "movement_pattern", "dosage",
               "difficulty", "review_status", "confidence"}
    for field, value in edits.items():
        if field not in allowed:
            continue
        if field == "difficulty":
            ex.difficulty = Difficulty(value)
        elif field == "review_status":
            ex.review_status = ReviewStatus(value)
        else:
            setattr(ex, field, value)
        db.add(Provenance(exercise_id=ex.id, field_name=field, value=str(value),
                          origin=DataOrigin.human_reviewed, confidence=1.0))
