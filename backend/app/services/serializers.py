"""Dict serializers for API responses (used by API + exports)."""
from __future__ import annotations

from app.media_registry import resolve_media
from app.models import (
    BodyRegion, DataConflict, Exercise, ExerciseSource, Joint, Muscle,
    Provenance, ReviewQueueItem, Source, SourceDocument,
)

ROLE_ORDER = {"primary": 0, "stretch_target": 1, "secondary": 2, "stabilizer": 3}


def exercise_summary(ex: Exercise) -> dict:
    muscles = sorted(ex.exercise_muscles, key=lambda m: ROLE_ORDER.get(m.role.value, 9))
    return {
        "id": ex.id, "slug": ex.slug, "name": ex.canonical_name,
        "aliases": ex.aliases or [],
        "type": ex.category.slug if ex.category else None,
        "type_name": ex.category.name if ex.category else None,
        "difficulty": ex.difficulty.value,
        "position": ex.position,
        "body_regions": [{"slug": r.body_region.slug, "name": r.body_region.name}
                         for r in ex.body_regions],
        "primary_muscles": [
            {"slug": em.muscle.slug, "name": em.muscle.name,
             "role": em.role.value, "structure_type": em.muscle.structure_type}
            for em in muscles if em.role.value in ("primary", "stretch_target")][:6],
        "all_muscles": [{"slug": em.muscle.slug, "name": em.muscle.name,
                         "role": em.role.value} for em in muscles],
        "equipment": [e.equipment.slug for e in ex.equipment],
        "confidence": ex.confidence,
        "review_status": ex.review_status.value,
        "origin": ex.origin.value,
        "is_medical_claim": ex.is_medical_claim,
        "source_count": len(ex.sources or []),
        "sources": [
            {
                "slug": es.source.slug,
                "name": es.source.name,
                "domain": es.source.domain,
                "url": (es.source_document.url
                        if es.source_document else es.source.homepage_url),
                "authority": es.source.authority.value,
                "license": es.source.license.value,
                "attribution_required": es.source.attribution_required,
            }
            for es in (ex.sources or [])[:4]
        ],
        "media": resolve_media(ex),
    }


def exercise_detail(db_ex: Exercise, *, include_research: bool = False) -> dict:
    data = exercise_summary(db_ex)
    data.update({
        "movement_pattern": db_ex.movement_pattern,
        "instructions": db_ex.instructions,
        "breathing": db_ex.breathing,
        "safety_notes": db_ex.safety_notes,
        "contraindications": db_ex.contraindications,
        "clinical_relevance": db_ex.clinical_relevance,
        "dosage": db_ex.dosage,
        "created_at": db_ex.created_at.isoformat() if db_ex.created_at else None,
        "updated_at": db_ex.updated_at.isoformat() if db_ex.updated_at else None,
        "joints": [{"slug": j.joint.slug, "name": j.joint.name, "movement": j.movement}
                   for j in db_ex.joints],
        "muscles": [
            {"slug": em.muscle.slug, "name": em.muscle.name,
             "role": em.role.value, "structure_type": em.muscle.structure_type,
             "confidence": em.confidence, "origin": em.origin,
             "is_small_overlooked": em.muscle.is_small_overlooked}
            for em in sorted(db_ex.exercise_muscles,
                             key=lambda m: ROLE_ORDER.get(m.role.value, 9))],
        "sources": [source_ref(s) for s in (db_ex.sources or [])],
        "merged_into_id": db_ex.merged_into_id,
    })
    if include_research:
        data["provenance"] = [provenance_ref(p) for p in db_ex.provenance]
        data["ai_generated_fields"] = db_ex.ai_generated_fields or []
    return data


def source_ref(s: ExerciseSource) -> dict:
    doc: SourceDocument | None = s.source_document
    return {
        "source_id": s.source.id, "source_slug": s.source.slug,
        "source_name": s.source.name, "domain": s.source.domain,
        "source_type": s.source.source_type.value,
        "authority": s.source.authority.value,
        "license": s.source.license.value,
        "commercial_use_allowed": s.source.commercial_use_allowed.value,
        "attribution_required": s.source.attribution_required,
        "url": doc.url if doc else s.source.homepage_url,
        "document_title": doc.title if doc else None,
        "retrieved_at": s.retrieved_at.isoformat() if s.retrieved_at else None,
        "confidence": s.confidence,
    }


def provenance_ref(p: Provenance) -> dict:
    return {
        "field": p.field_name,
        "value": (p.value[:200] + "…") if p.value and len(p.value) > 200 else p.value,
        "origin": p.origin.value,
        "source_document_id": p.source_document_id,
        "source_url": p.source_document.url if p.source_document else None,
        "ai_model": p.ai_model, "ai_prompt_version": p.ai_prompt_version,
        "confidence": p.confidence,
        "created_at": p.created_at.isoformat() if p.created_at else None,
    }


def muscle_detail(m: Muscle, *, exercises: list[Exercise] | None = None,
                  coverage: dict | None = None) -> dict:
    data = {
        "id": m.id, "slug": m.slug, "name": m.name, "latin_name": m.latin_name,
        "structure_type": m.structure_type,
        "description": m.description,
        "is_small_overlooked": m.is_small_overlooked,
        "aliases": m.search_aliases or [],
        "body_region": {"slug": m.body_region.slug, "name": m.body_region.name}
        if m.body_region else None,
        "muscle_group": {"slug": m.muscle_group.slug, "name": m.muscle_group.name}
        if m.muscle_group else None,
    }
    if exercises is not None:
        data["exercise_count"] = len(exercises)
        data["exercises"] = [exercise_summary(e) for e in exercises]
    if coverage is not None:
        data["coverage"] = coverage
    return data


def source_detail(s: Source, *, exercise_count: int | None = None,
                  document_count: int | None = None, last_crawl: dict | None = None) -> dict:
    data = {
        "id": s.id, "slug": s.slug, "name": s.name, "domain": s.domain,
        "homepage_url": s.homepage_url,
        "source_type": s.source_type.value,
        "authority": s.authority.value,
        "license": s.license.value,
        "commercial_use_allowed": s.commercial_use_allowed.value,
        "attribution_required": s.attribution_required,
        "license_url": s.license_url,
        "terms_url": s.terms_url,
        "robots_status": s.robots_status.value,
        "is_active": s.is_active,
        "notes": s.notes,
    }
    if exercise_count is not None:
        data["exercise_count"] = exercise_count
    if document_count is not None:
        data["document_count"] = document_count
    if last_crawl is not None:
        data["last_crawl"] = last_crawl
    return data


def review_item(i: ReviewQueueItem) -> dict:
    return {
        "id": i.id,
        "item_type": i.item_type.value,
        "status": i.status.value,
        "exercise_id": i.exercise_id,
        "exercise_name": getattr(i, "_exercise_name", None),
        "related_exercise_id": i.related_exercise_id,
        "related_exercise_name": getattr(i, "_related_name", None),
        "payload": i.payload or {},
        "priority": i.priority,
        "reason": i.reason,
        "resolution_note": i.resolution_note,
        "created_at": i.created_at.isoformat() if i.created_at else None,
        "resolved_at": i.resolved_at.isoformat() if i.resolved_at else None,
    }


def conflict(c: DataConflict) -> dict:
    return {
        "id": c.id, "exercise_id": c.exercise_id, "field": c.field_name,
        "values": c.values, "source_ids": c.source_ids,
        "status": c.status.value, "resolution": c.resolution,
        "created_at": c.created_at.isoformat() if c.created_at else None,
    }
