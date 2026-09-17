"""Data-quality validation + conflict detection.

Validation checks run against persisted exercises and produce review-queue
items; conflict detection compares per-source anatomy claims recorded in
provenance (each source's muscle list is stored on the provenance row).
"""
from __future__ import annotations

import json
from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.enums import LicenseStatus, RecordOrigin, ReviewItemType
from app.models import Exercise, ExerciseSource, Provenance, Source, SourceDocument


@dataclass
class ValidationIssue:
    exercise_id: int
    code: str
    message: str
    item_type: ReviewItemType
    priority: int = 5
    payload: dict | None = None


def validate_exercise(db: Session, ex: Exercise) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    if not ex.exercise_muscles and not ex.body_regions:
        issues.append(ValidationIssue(
            ex.id, "missing_anatomy", "No muscles or body regions linked.",
            ReviewItemType.invalid_taxonomy, priority=2))
    if not ex.instructions:
        issues.append(ValidationIssue(
            ex.id, "missing_instructions", "No normalized instructions.",
            ReviewItemType.other, priority=3))
    src_rows = db.execute(
        select(ExerciseSource).where(ExerciseSource.exercise_id == ex.id)
    ).scalars().all()
    if not src_rows:
        issues.append(ValidationIssue(
            ex.id, "missing_source", "Exercise has no source linkage.",
            ReviewItemType.other, priority=1))
    unknown_license = any(
        (src := db.get(Source, row.source_id)) is not None and src.license == LicenseStatus.unknown
        for row in src_rows
    )
    if ex.origin == RecordOrigin.aggregated and unknown_license:
        issues.append(ValidationIssue(
            ex.id, "licensing_unknown",
            "At least one linked source has unknown licensing.",
            ReviewItemType.licensing_unknown, priority=3,
            payload={"source_ids": [r.source_id for r in src_rows]}))
    if ex.is_medical_claim:
        issues.append(ValidationIssue(
            ex.id, "medical_claim",
            "Source text contains treatment/medical claim language; needs clinical review.",
            ReviewItemType.medical_claim, priority=2))
    if ex.ai_generated_fields:
        issues.append(ValidationIssue(
            ex.id, "ai_generated",
            f"AI-generated fields present: {', '.join(ex.ai_generated_fields)}",
            ReviewItemType.ai_generated, priority=3,
            payload={"fields": ex.ai_generated_fields}))
    return issues


def detect_anatomy_conflicts(db: Session, ex: Exercise) -> list[dict]:
    """Compare the primary-muscle sets different sources claim for one exercise.

    Each source's claim is a provenance row: field_name='muscles', value=JSON
    list of slugs, source_document_id -> source. Two sources whose sets differ
    produce a conflict record.
    """
    prov_rows = db.execute(
        select(Provenance).where(
            Provenance.exercise_id == ex.id, Provenance.field_name == "muscles")
    ).scalars().all()

    doc_to_source = {
        d.id: d.source_id for d in db.execute(
            select(SourceDocument).where(
                SourceDocument.id.in_([p.source_document_id for p in prov_rows if p.source_document_id]))
        ).scalars().all()
    }

    by_source: dict[int, set[str]] = {}
    for p in prov_rows:
        src_id = doc_to_source.get(p.source_document_id) if p.source_document_id else None
        if src_id is None:
            continue
        try:
            slugs = set(json.loads(p.value or "[]"))
        except (json.JSONDecodeError, TypeError):
            continue
        by_source.setdefault(src_id, set()).update(slugs)

    conflicts: list[dict] = []
    sources = list(by_source)
    for i, base in enumerate(sources):
        for other in sources[i + 1:]:
            if by_source[base] != by_source[other]:
                conflicts.append({
                    "field": "muscles",
                    "source_ids": [base, other],
                    "values": {str(base): sorted(by_source[base]),
                               str(other): sorted(by_source[other])},
                    "difference": sorted(by_source[base] ^ by_source[other]),
                })
    return conflicts
