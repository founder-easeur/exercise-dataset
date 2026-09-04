"""Dataset export (JSON / JSONL / CSV) + versioning."""
from __future__ import annotations

import csv
import io
import json
from datetime import datetime, timezone

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.enums import RecordOrigin, ReviewStatus
from app.models import (
    BodyRegion, DatasetVersion, Equipment, Exercise, ExerciseBodyRegion,
    ExerciseEquipment, ExerciseJoint, ExerciseMuscle, ExerciseType, Joint,
    Muscle, Source,
)


def exercise_row(db: Session, ex: Exercise, full: bool = True) -> dict:
    muscles = sorted(
        [{"slug": em.muscle.slug, "name": em.muscle.name, "role": em.role.value,
          "structure_type": em.muscle.structure_type} for em in ex.exercise_muscles],
        key=lambda m: {"primary": 0, "stretch_target": 1, "secondary": 2, "stabilizer": 3}.get(m["role"], 9))
    regions = [{"slug": r.body_region.slug, "name": r.body_region.name,
                "role": r.role.value} for r in ex.body_regions]
    row = {
        "id": ex.id,
        "slug": ex.slug,
        "name": ex.canonical_name,
        "aliases": ex.aliases,
        "type": ex.category.slug if ex.category else None,
        "type_name": ex.category.name if ex.category else None,
        "difficulty": ex.difficulty.value,
        "position": ex.position,
        "movement_pattern": ex.movement_pattern,
        "body_regions": regions,
        "muscles": muscles,
        "primary_muscles": [m["slug"] for m in muscles if m["role"] in ("primary", "stretch_target")],
        "joints": [{"slug": j.joint.slug, "name": j.joint.name, "movement": j.movement}
                   for j in ex.joints],
        "equipment": [e.equipment.slug for e in ex.equipment],
        "instructions": ex.instructions,
        "breathing": ex.breathing,
        "safety_notes": ex.safety_notes,
        "contraindications": ex.contraindications,
        "clinical_relevance": ex.clinical_relevance,
        "dosage": ex.dosage,
        "origin": ex.origin.value,
        "confidence": ex.confidence,
        "review_status": ex.review_status.value,
        "is_medical_claim": ex.is_medical_claim,
        "source_count": len(ex.sources or []),
        "updated_at": ex.updated_at.isoformat() if ex.updated_at else None,
    }
    if full:
        row["sources"] = [
            {"source": s.source.name, "domain": s.source.domain,
             "url": s.source_document.url if s.source_document else s.source.homepage_url,
             "license": s.source.license.value,
             "retrieved_at": s.retrieved_at.isoformat() if s.retrieved_at else None}
            for s in (ex.sources or [])
        ]
    return row


def export_exercises(db: Session, fmt: str = "json", *, approved_only: bool = True,
                     origin: str | None = None, include_pending: bool = False) -> str | bytes:
    from sqlalchemy.orm import selectinload
    rows = db.execute(
        select(Exercise)
        .where(Exercise.merged_into_id.is_(None),
               *([Exercise.review_status == ReviewStatus.approved]
                 if approved_only and not include_pending else []),
               *([Exercise.origin == RecordOrigin(origin)] if origin else []))
        .options(
            selectinload(Exercise.category),
            selectinload(Exercise.exercise_muscles).selectinload(ExerciseMuscle.muscle),
            selectinload(Exercise.body_regions).selectinload(ExerciseBodyRegion.body_region),
            selectinload(Exercise.joints).selectinload(ExerciseJoint.joint),
            selectinload(Exercise.equipment).selectinload(ExerciseEquipment.equipment),
            selectinload(Exercise.sources),
        )
    ).scalars().unique().all()

    data = [exercise_row(db, ex) for ex in rows]
    if fmt == "jsonl":
        return "\n".join(json.dumps(d, default=str) for d in data)
    if fmt == "csv":
        buf = io.StringIO()
        flat_keys = ["id", "slug", "name", "type", "difficulty", "position",
                     "primary_muscles", "body_regions", "equipment", "origin",
                     "confidence", "review_status", "source_count"]
        writer = csv.DictWriter(buf, fieldnames=flat_keys, extrasaction="ignore")
        writer.writeheader()
        for d in data:
            flat = dict(d)
            flat["primary_muscles"] = ";".join(d["primary_muscles"])
            flat["body_regions"] = ";".join(r["slug"] for r in d["body_regions"])
            flat["equipment"] = ";".join(d["equipment"])
            writer.writerow(flat)
        return buf.getvalue()
    return json.dumps({"exported_at": datetime.now(timezone.utc).isoformat(),
                       "count": len(data), "exercises": data}, indent=2, default=str)


def export_taxonomy(db: Session, what: str, fmt: str = "json") -> str:
    if what == "muscles":
        rows = db.execute(select(Muscle)).scalars().all()
        data = [{"id": m.id, "slug": m.slug, "name": m.name, "latin_name": m.latin_name,
                 "structure_type": m.structure_type,
                 "body_region": m.body_region.slug if m.body_region else None,
                 "is_small_overlooked": m.is_small_overlooked,
                 "aliases": m.search_aliases} for m in rows]
    elif what == "body-regions":
        rows = db.execute(select(BodyRegion).order_by(BodyRegion.sort_order)).scalars().all()
        data = [{"id": r.id, "slug": r.slug, "name": r.name, "description": r.description}
                for r in rows]
    elif what == "joints":
        rows = db.execute(select(Joint)).scalars().all()
        data = [{"id": j.id, "slug": j.slug, "name": j.name, "joint_type": j.joint_type,
                 "body_region": j.body_region.slug if j.body_region else None} for j in rows]
    elif what == "equipment":
        rows = db.execute(select(Equipment)).scalars().all()
        data = [{"id": e.id, "slug": e.slug, "name": e.name} for e in rows]
    elif what == "exercise-types":
        rows = db.execute(select(ExerciseType).order_by(ExerciseType.sort_order)).scalars().all()
        data = [{"id": t.id, "slug": t.slug, "name": t.name, "description": t.description}
                for t in rows]
    else:
        raise ValueError(f"unknown taxonomy export: {what}")
    if fmt == "csv":
        buf = io.StringIO()
        keys = sorted({k for d in data for k in d})
        writer = csv.DictWriter(buf, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)
        return buf.getvalue()
    if fmt == "jsonl":
        return "\n".join(json.dumps(d) for d in data)
    return json.dumps(data, indent=2, default=str)


def snapshot_version(db: Session, version: str, label: str | None = None,
                     notes: str | None = None) -> DatasetVersion:
    """Create a dataset version with diff stats vs previous version."""
    from app.services.stats import dashboard_stats
    stats = dashboard_stats(db)
    prev = db.execute(
        select(DatasetVersion).order_by(DatasetVersion.created_at.desc())
    ).scalars().first()
    diff = {"added": 0, "removed": 0, "changed": 0, "merged": 0, "reclassified": 0}
    if prev:
        diff["added"] = max(0, stats["total_exercises"] - prev.stats.get("total_exercises", 0))
        diff["removed"] = max(0, prev.stats.get("total_exercises", 0) - stats["total_exercises"])
        diff["merged"] = max(0, prev.stats.get("potential_duplicates", 0) - stats["potential_duplicates"])
    ver = DatasetVersion(version=version, label=label, notes=notes, stats=stats, diff=diff)
    db.add(ver)
    db.commit()
    return ver
