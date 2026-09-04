"""Exercise / anatomy read queries with filtering + pagination (no N+1)."""
from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy import Select, func, or_, select
from sqlalchemy.orm import Session, joinedload, selectinload

from app.enums import Difficulty, ExerciseRole, RecordOrigin, RegionRole, ReviewStatus
from app.models import (
    BodyRegion, Equipment, Exercise, ExerciseBodyRegion, ExerciseEquipment,
    ExerciseJoint, ExerciseMuscle, ExerciseSource, ExerciseType, Joint, Muscle,
    Provenance, ReviewQueueItem, Source, SourceDocument,
)


@dataclass
class ExerciseFilters:
    q: str | None = None
    body_region: str | None = None
    muscle: str | None = None
    muscle_group: str | None = None
    joint: str | None = None
    exercise_type: str | None = None
    equipment: str | None = None
    difficulty: str | None = None
    position: str | None = None
    review_status: str | None = None      # 'all' or comma-separated statuses
    confidence_min: float | None = None
    source: str | None = None
    origin: str | None = None
    include_merged: bool = False
    sort: str = "name"                    # name | confidence | newest | region


def _apply_filters(query: Select, f: ExerciseFilters) -> Select:
    query = query.where(Exercise.merged_into_id.is_(None))
    if f.review_status in (None, "all"):
        query = query.where(Exercise.review_status != ReviewStatus.rejected)
    else:
        statuses = [ReviewStatus(s) for s in f.review_status.split(",") if s]
        query = query.where(Exercise.review_status.in_(statuses))
    if not f.include_merged:
        pass
    if f.origin:
        query = query.where(Exercise.origin == RecordOrigin(f.origin))
    if f.difficulty:
        query = query.where(Exercise.difficulty == Difficulty(f.difficulty))
    if f.position:
        query = query.where(Exercise.position.ilike(f"%{f.position}%"))
    if f.confidence_min is not None:
        query = query.where(Exercise.confidence >= f.confidence_min)
    if f.q:
        like = f"%{f.q}%"
        query = query.where(or_(
            Exercise.canonical_name.ilike(like),
            Exercise.normalized_name.ilike(like),
            func.array_to_string(Exercise.aliases, " ").ilike(like),
        ))
    if f.exercise_type:
        query = query.join(ExerciseType, Exercise.category_id == ExerciseType.id)
        query = query.where(ExerciseType.slug == f.exercise_type)
    if f.body_region:
        query = query.join(
            ExerciseBodyRegion, ExerciseBodyRegion.exercise_id == Exercise.id)
        query = query.join(BodyRegion, ExerciseBodyRegion.body_region_id == BodyRegion.id)
        query = query.where(BodyRegion.slug == f.body_region)
    if f.muscle or f.muscle_group:
        query = query.join(ExerciseMuscle, ExerciseMuscle.exercise_id == Exercise.id)
        query = query.join(Muscle, ExerciseMuscle.muscle_id == Muscle.id)
        if f.muscle:
            query = query.where(Muscle.slug == f.muscle)
        if f.muscle_group:
            from app.models import MuscleGroup
            query = query.join(MuscleGroup, Muscle.muscle_group_id == MuscleGroup.id)
            query = query.where(MuscleGroup.slug == f.muscle_group)
    if f.joint:
        query = query.join(ExerciseJoint, ExerciseJoint.exercise_id == Exercise.id)
        query = query.join(Joint, ExerciseJoint.joint_id == Joint.id)
        query = query.where(Joint.slug == f.joint)
    if f.equipment:
        query = query.join(ExerciseEquipment, ExerciseEquipment.exercise_id == Exercise.id)
        query = query.join(Equipment, ExerciseEquipment.equipment_id == Equipment.id)
        query = query.where(Equipment.slug == f.equipment)
    if f.source:
        query = query.join(ExerciseSource, ExerciseSource.exercise_id == Exercise.id)
        query = query.join(Source, ExerciseSource.source_id == Source.id)
        query = query.where(Source.slug == f.source)
    return query


_SORTS = {
    "name": Exercise.canonical_name.asc(),
    "confidence": Exercise.confidence.desc(),
    "newest": Exercise.created_at.desc(),
    "region": Exercise.canonical_name.asc(),
}


def list_exercises(db: Session, filters: ExerciseFilters, page: int = 1,
                   page_size: int = 24) -> dict:
    base = select(Exercise).distinct()
    base = _apply_filters(base, filters)
    total = db.scalar(select(func.count()).select_from(base.subquery())) or 0
    order = _SORTS.get(filters.sort or "name", _SORTS["name"])
    rows = db.execute(
        base.options(
            selectinload(Exercise.category),
            selectinload(Exercise.exercise_muscles).selectinload(ExerciseMuscle.muscle),
            selectinload(Exercise.body_regions).selectinload(ExerciseBodyRegion.body_region),
            selectinload(Exercise.equipment).selectinload(ExerciseEquipment.equipment),
            selectinload(Exercise.sources),
        )
        .order_by(order)
        .offset((page - 1) * page_size)
        .limit(page_size)
    ).scalars().unique().all()
    return {"total": total, "page": page, "page_size": page_size, "items": rows}


def get_exercise(db: Session, id_or_slug: str | int) -> Exercise | None:
    query = select(Exercise).options(
        selectinload(Exercise.category),
        selectinload(Exercise.exercise_muscles).selectinload(ExerciseMuscle.muscle),
        selectinload(Exercise.body_regions).selectinload(ExerciseBodyRegion.body_region),
        selectinload(Exercise.joints).selectinload(ExerciseJoint.joint),
        selectinload(Exercise.equipment).selectinload(ExerciseEquipment.equipment),
        selectinload(Exercise.sources).selectinload(ExerciseSource.source),
        selectinload(Exercise.sources).selectinload(ExerciseSource.source_document),
        selectinload(Exercise.provenance).selectinload(Provenance.source_document),
    )
    if isinstance(id_or_slug, int) or (isinstance(id_or_slug, str) and id_or_slug.isdigit()):
        return db.execute(query.where(Exercise.id == int(id_or_slug))).scalar_one_or_none()
    return db.execute(query.where(Exercise.slug == id_or_slug)).scalar_one_or_none()


def get_related_exercise(db: Session, exercise_id: int) -> Exercise | None:
    return db.execute(
        select(Exercise).where(Exercise.id == exercise_id)
        .options(selectinload(Exercise.exercise_muscles).selectinload(ExerciseMuscle.muscle),
                 selectinload(Exercise.body_regions).selectinload(ExerciseBodyRegion.body_region))
    ).scalar_one_or_none()


def exercises_for_muscle(db: Session, muscle_id: int) -> list[Exercise]:
    return db.execute(
        select(Exercise).join(ExerciseMuscle, ExerciseMuscle.exercise_id == Exercise.id)
        .where(ExerciseMuscle.muscle_id == muscle_id, Exercise.merged_into_id.is_(None))
        .options(selectinload(Exercise.category),
                 selectinload(Exercise.exercise_muscles).selectinload(ExerciseMuscle.muscle),
                 selectinload(Exercise.body_regions).selectinload(ExerciseBodyRegion.body_region))
        .distinct()
    ).scalars().unique().all()


def list_muscles(db: Session, q: str | None = None, region: str | None = None,
                 structure_type: str | None = None, small_only: bool = False,
                 muscle_group: str | None = None) -> list[Muscle]:
    from app.models import MuscleGroup
    query = select(Muscle).options(joinedload(Muscle.body_region), joinedload(Muscle.muscle_group))
    if q:
        like = f"%{q}%"
        query = query.where(or_(Muscle.name.ilike(like),
                                func.array_to_string(Muscle.search_aliases, " ").ilike(like)))
    if region:
        query = query.join(BodyRegion, Muscle.body_region_id == BodyRegion.id).where(
            BodyRegion.slug == region)
    if muscle_group:
        query = query.join(MuscleGroup, Muscle.muscle_group_id == MuscleGroup.id).where(
            MuscleGroup.slug == muscle_group)
    if structure_type:
        query = query.where(Muscle.structure_type == structure_type)
    if small_only:
        query = query.where(Muscle.is_small_overlooked.is_(True))
    return db.execute(query.order_by(Muscle.name).distinct()).scalars().all()


def get_muscle(db: Session, id_or_slug: str | int) -> Muscle | None:
    query = select(Muscle).options(joinedload(Muscle.body_region), joinedload(Muscle.muscle_group))
    if isinstance(id_or_slug, int) or (isinstance(id_or_slug, str) and id_or_slug.isdigit()):
        return db.execute(query.where(Muscle.id == int(id_or_slug))).scalar_one_or_none()
    return db.execute(query.where(Muscle.slug == id_or_slug)).scalar_one_or_none()
