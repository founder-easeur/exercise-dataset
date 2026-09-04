"""Database seeding: taxonomy, sources, curated exercises."""
from __future__ import annotations

import logging

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.enums import (
    DataOrigin, Difficulty, ExerciseRole, RecordOrigin, RegionRole, ReviewStatus,
)
from app.models import (
    AuditLog, BodyRegion, Equipment, Exercise, ExerciseBodyRegion, ExerciseEquipment,
    ExerciseJoint, ExerciseMuscle, ExerciseSource, ExerciseType, Joint, Muscle,
    MuscleGroup, Provenance, Source,
)
from app.seed.curated import ALL_CURATED_EXERCISES
from app.services.text import normalize_name
from app.taxonomy import anatomy_data as A
from app.taxonomy import reference_data as R
from app.taxonomy.source_registry import INITIAL_SOURCES

log = logging.getLogger("easeur.seed")


def seed_taxonomy(db: Session) -> dict:
    stats = {"body_regions": 0, "muscle_groups": 0, "muscles": 0, "joints": 0,
             "equipment": 0, "exercise_types": 0}

    regions: dict[str, BodyRegion] = {}
    for r in A.BODY_REGIONS:
        obj = db.execute(select(BodyRegion).where(BodyRegion.slug == r["slug"])).scalar_one_or_none()
        if not obj:
            obj = BodyRegion(slug=r["slug"], name=r["name"],
                             description=r.get("description"), sort_order=r["sort_order"])
            db.add(obj)
            stats["body_regions"] += 1
        regions[r["slug"]] = obj
    db.flush()  # assign ids before referencing them

    groups: dict[str, MuscleGroup] = {}
    for g in A.MUSCLE_GROUPS:
        obj = db.execute(select(MuscleGroup).where(MuscleGroup.slug == g["slug"])).scalar_one_or_none()
        if not obj:
            obj = MuscleGroup(slug=g["slug"], name=g["name"],
                              body_region_id=regions[g["region"]].id,
                              description=g.get("description"),
                              is_clinical_unit=g.get("is_clinical_unit", False))
            db.add(obj)
            stats["muscle_groups"] += 1
        groups[g["slug"]] = obj
    db.flush()

    for m in A.MUSCLES:
        obj = db.execute(select(Muscle).where(Muscle.slug == m["slug"])).scalar_one_or_none()
        if not obj:
            obj = Muscle(
                slug=m["slug"], name=m["name"], latin_name=m.get("latin_name"),
                structure_type=m.get("structure_type", "muscle"),
                muscle_group_id=groups[m["group"]].id,
                body_region_id=regions[m["region"]].id,
                description=m.get("description"),
                is_small_overlooked=m.get("is_small_overlooked", False),
                search_aliases=m.get("aliases", []),
            )
            db.add(obj)
            stats["muscles"] += 1

    for j in R.JOINTS:
        obj = db.execute(select(Joint).where(Joint.slug == j["slug"])).scalar_one_or_none()
        if not obj:
            db.add(Joint(slug=j["slug"], name=j["name"], joint_type=j.get("joint_type"),
                         body_region_id=regions[j["region"]].id if j.get("region") else None,
                         search_aliases=j.get("aliases", [])))
            stats["joints"] += 1

    for e in R.EQUIPMENT:
        obj = db.execute(select(Equipment).where(Equipment.slug == e["slug"])).scalar_one_or_none()
        if not obj:
            db.add(Equipment(slug=e["slug"], name=e["name"]))
            stats["equipment"] += 1

    for t in R.EXERCISE_TYPES:
        obj = db.execute(select(ExerciseType).where(ExerciseType.slug == t["slug"])).scalar_one_or_none()
        if not obj:
            db.add(ExerciseType(slug=t["slug"], name=t["name"],
                                description=t.get("description"), sort_order=stats["exercise_types"]))
            stats["exercise_types"] += 1

    db.commit()
    log.info("taxonomy seeded: %s", stats)
    return stats


def seed_sources(db: Session) -> int:
    created = 0
    for s in INITIAL_SOURCES:
        obj = db.execute(select(Source).where(Source.slug == s["slug"])).scalar_one_or_none()
        if obj:
            continue
        db.add(Source(**s))
        created += 1
    db.commit()
    log.info("sources seeded: %d new", created)
    return created


def seed_curated_exercises(db: Session) -> dict:
    """Insert curated exercises (origin=curated, approved, provenance=curated)."""
    stats = {"created": 0, "skipped": 0}
    regions = {r.slug: r for r in db.execute(select(BodyRegion)).scalars()}
    muscles = {m.slug: m for m in db.execute(select(Muscle)).scalars()}
    joints = {j.slug: j for j in db.execute(select(Joint)).scalars()}
    equipment = {e.slug: e for e in db.execute(select(Equipment)).scalars()}
    types = {t.slug: t for t in db.execute(select(ExerciseType)).scalars()}

    for data in ALL_CURATED_EXERCISES:
        existing = db.execute(select(Exercise).where(Exercise.slug == data["slug"])).scalar_one_or_none()
        if existing:
            stats["skipped"] += 1
            continue
        ex = Exercise(
            slug=data["slug"], canonical_name=data["name"],
            aliases=[a for a in data.get("aliases", [])],
            category_id=types[data["type"]].id,
            movement_pattern=data.get("movement"),
            difficulty=Difficulty(data.get("difficulty", "beginner")),
            position=data.get("position"),
            instructions=data.get("instructions"),
            breathing=data.get("breathing"),
            safety_notes=data.get("safety"),
            contraindications=data.get("contra"),
            clinical_relevance=data.get("clinical"),
            dosage=data.get("dosage"),
            confidence=data.get("confidence", 0.92),
            review_status=ReviewStatus.approved,
            origin=RecordOrigin.curated,
            normalized_name=normalize_name(data["name"]),
        )
        db.add(ex)
        db.flush()

        for item in data.get("regions", []):
            slug, role = item if isinstance(item, tuple) else (item, "primary")
            db.add(ExerciseBodyRegion(exercise_id=ex.id, body_region_id=regions[slug].id,
                                      role=RegionRole(role)))
        for item in data.get("muscles", []):
            slug, role = item
            db.add(ExerciseMuscle(exercise_id=ex.id, muscle_id=muscles[slug].id,
                                  role=ExerciseRole(role), confidence=0.95,
                                  origin=DataOrigin.curated.value))
        seen_joints: set[str] = set()
        for item in data.get("joints", []):
            slug, movement = item if isinstance(item, tuple) else (item, None)
            if slug in joints and slug not in seen_joints:
                seen_joints.add(slug)
                db.add(ExerciseJoint(exercise_id=ex.id, joint_id=joints[slug].id, movement=movement))
        seen_equip: set[str] = set()
        for item in data.get("equipment", []):
            slug = item[0] if isinstance(item, tuple) else item
            if slug in equipment and slug not in seen_equip:
                seen_equip.add(slug)
                db.add(ExerciseEquipment(exercise_id=ex.id, equipment_id=equipment[slug].id))

        # Full provenance for key fields: this is curated knowledge-base content
        from app.models import Provenance as P
        for field in ("canonical_name", "instructions", "muscles", "difficulty"):
            value = {"canonical_name": data["name"],
                     "instructions": data.get("instructions"),
                     "muscles": [m[0] for m in data.get("muscles", [])],
                     "difficulty": data.get("difficulty", "beginner")}.get(field)
            db.add(P(exercise_id=ex.id, field_name=field,
                     value=str(value), origin=DataOrigin.curated, confidence=0.95))

        stats["created"] += 1

    db.commit()
    db.add(AuditLog(actor="system", action="seed_curated", entity_type="dataset",
                    entity_id=0, details=stats))
    db.commit()
    log.info("curated exercises: %s", stats)
    return stats


def run_full_seed(db: Session) -> dict:
    result = {
        "taxonomy": seed_taxonomy(db),
        "sources": seed_sources(db),
        "exercises": seed_curated_exercises(db),
    }
    return result
