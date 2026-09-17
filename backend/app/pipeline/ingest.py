"""Ingestion: normalize candidates and persist with provenance + dedup hooks."""
from __future__ import annotations

import json
import logging

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.enums import (
    DataOrigin, Difficulty, ExerciseRole, RecordOrigin, RegionRole, ReviewStatus,
    SourceRelationship,
)
from app.log import log_event
from app.enums import ConflictStatus
from app.models import (
    BodyRegion, DataConflict, Equipment, Exercise, ExerciseBodyRegion,
    ExerciseEquipment, ExerciseJoint, ExerciseMuscle, ExerciseSource, ExerciseType,
    Joint, Muscle, Provenance, Source, SourceDocument,
)
from app.pipeline.extract import ExerciseCandidate
from app.pipeline.normalize import normalize_candidate
from app.pipeline.validate import detect_anatomy_conflicts

log = logging.getLogger("easeur.ingest")


class IngestResult:
    def __init__(self) -> None:
        self.created: list[int] = []
        self.linked: list[int] = []          # existing exercise gained a new source
        self.rejected: list[tuple[str, str]] = []
        self.conflicts: list[dict] = []

    @property
    def created_count(self) -> int:
        return len(self.created)

    @property
    def linked_count(self) -> int:
        return len(self.linked)


class TaxonomyCache:
    def __init__(self, db: Session) -> None:
        self.regions = {r.slug: r for r in db.execute(select(BodyRegion)).scalars()}
        self.muscles = {m.slug: m for m in db.execute(select(Muscle)).scalars()}
        self.joints = {j.slug: j for j in db.execute(select(Joint)).scalars()}
        self.equipment = {e.slug: e for e in db.execute(select(Equipment)).scalars()}
        self.types = {t.slug: t for t in db.execute(select(ExerciseType)).scalars()}
        self.sources = {s.slug: s for s in db.execute(select(Source)).scalars()}


def _doc_for(db: Session, cache: TaxonomyCache, url: str, cand_source_slug: str) -> SourceDocument | None:
    return db.execute(
        select(SourceDocument).where(SourceDocument.url == url)
    ).scalar_one_or_none()


def _link_source(db: Session, cache: TaxonomyCache, ex: Exercise, normalized,
                 doc: SourceDocument | None, source: Source) -> None:
    existing = db.execute(select(ExerciseSource).where(
        ExerciseSource.exercise_id == ex.id,
        ExerciseSource.source_id == source.id)).scalars().first()
    if existing and doc and existing.source_document_id == doc.id:
        return
    db.add(ExerciseSource(
        exercise_id=ex.id, source_id=source.id,
        source_document_id=doc.id if doc else None,
        source_relationship=SourceRelationship.original,
        license_at_retrieval=source.license,
        confidence=normalized.confidence if normalized else 0.7,
    ))


def _add_provenance(db: Session, ex: Exercise, field: str, value, doc: SourceDocument | None,
                    origin: DataOrigin, confidence: float, method: str) -> None:
    db.add(Provenance(
        exercise_id=ex.id, field_name=field,
        value=value if isinstance(value, str) else json.dumps(value, default=str),
        origin=origin, source_document_id=doc.id if doc else None,
        confidence=confidence,
        ai_model=method if origin == DataOrigin.ai_inference else None,
        ai_model_version=None,
        ai_prompt_version=None,
    ))


def _muscle_provenance_value(normalized) -> str:
    return json.dumps([slug for slug, _role in normalized.muscles])


def ingest_candidates(db: Session, candidates: list[ExerciseCandidate]) -> IngestResult:
    result = IngestResult()
    cache = TaxonomyCache(db)

    for cand in candidates:
        source = cache.sources.get(cand.source_slug)
        if source is None:
            result.rejected.append((cand.name, f"unknown source {cand.source_slug}"))
            continue
        normalized = normalize_candidate(cand)
        if normalized is None:
            result.rejected.append((cand.name, "normalization failed (no usable content)"))
            log_event(log, "exercise_rejected", name=cand.name, reason="normalization_failed")
            continue

        doc = _doc_for(db, cache, cand.url, cand.source_slug)

        # --- dedup stage 1: exact normalized-name match against active exercises
        existing = db.execute(
            select(Exercise).where(Exercise.normalized_name == normalized.normalized_name,
                                   Exercise.merged_into_id.is_(None))
        ).scalars().all()
        compatible = None
        for ex in existing:
            ex_regions = {r.body_region.slug for r in ex.body_regions}
            if not normalized.regions or not ex_regions or (set(normalized.regions) & ex_regions):
                compatible = ex
                break

        if compatible is not None:
            _link_source(db, cache, compatible, normalized, doc, source)
            _add_provenance(db, compatible, "muscles", _muscle_provenance_value(normalized),
                            doc, DataOrigin.source_fact, normalized.confidence,
                            normalized.extraction_method)
            result.linked.append(compatible.id)
            log_event(log, "duplicate_detected", stage="normalized_name",
                      exercise_id=compatible.id, name=normalized.name, source=source.slug)
            # conflict detection: does this source's muscle set differ?
            conflicts = detect_anatomy_conflicts(db, compatible)
            for c in conflicts:
                c["exercise_id"] = compatible.id
                result.conflicts.append(c)
                db.add(DataConflict(exercise_id=compatible.id, field_name=c["field"],
                                    values=c["values"], source_ids=c["source_ids"],
                                    status=ConflictStatus.open))
                log_event(log, "conflict_detected", exercise_id=compatible.id,
                          field="muscles", sources=c["source_ids"])
            continue

        # --- new exercise record
        base_slug = normalized.slug
        slug, n = base_slug, 2
        while db.execute(select(Exercise).where(Exercise.slug == slug)).scalar_one_or_none():
            slug = f"{base_slug}-{n}"
            n += 1

        ex = Exercise(
            slug=slug, canonical_name=normalized.name, aliases=normalized.aliases,
            category_id=cache.types[normalized.category_slug].id,
            movement_pattern=normalized.movement_pattern,
            difficulty=normalized.difficulty, position=normalized.position,
            instructions=normalized.instructions,
            safety_notes=normalized.safety_notes,
            confidence=normalized.confidence,
            review_status=ReviewStatus.pending_review,
            origin=RecordOrigin.aggregated,
            is_medical_claim=normalized.is_medical_claim,
            ai_generated_fields=normalized.ai_generated_fields,
            normalized_name=normalized.normalized_name,
        )
        db.add(ex)
        db.flush()

        for region in normalized.regions:
            if region in cache.regions:
                db.add(ExerciseBodyRegion(exercise_id=ex.id,
                                          body_region_id=cache.regions[region].id,
                                          role=RegionRole.primary))
        for mslug, role in normalized.muscles:
            if mslug in cache.muscles:
                db.add(ExerciseMuscle(exercise_id=ex.id,
                                      muscle_id=cache.muscles[mslug].id, role=role,
                                      confidence=normalized.confidence,
                                      origin=DataOrigin.source_fact.value))
        for jslug in normalized.joints:
            if jslug in cache.joints:
                db.add(ExerciseJoint(exercise_id=ex.id, joint_id=cache.joints[jslug].id))
        for eslug in normalized.equipment:
            if eslug in cache.equipment:
                db.add(ExerciseEquipment(exercise_id=ex.id,
                                         equipment_id=cache.equipment[eslug].id))

        _link_source(db, cache, ex, normalized, doc, source)
        _add_provenance(db, ex, "canonical_name", normalized.name, doc,
                        DataOrigin.source_fact, normalized.confidence,
                        normalized.extraction_method)
        _add_provenance(db, ex, "instructions", normalized.instructions, doc,
                        DataOrigin.source_fact, normalized.confidence,
                        normalized.extraction_method)
        _add_provenance(db, ex, "muscles", _muscle_provenance_value(normalized), doc,
                        DataOrigin.source_fact, normalized.confidence,
                        normalized.extraction_method)
        result.created.append(ex.id)
        log_event(log, "exercise_extracted", exercise_id=ex.id, name=normalized.name,
                  source=source.slug, method=normalized.extraction_method,
                  confidence=normalized.confidence)

    db.commit()
    return result
