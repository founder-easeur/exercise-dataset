"""Data-quality + schema + review-flow tests."""
from __future__ import annotations

from sqlalchemy import select

from app.enums import (
    DataOrigin, Difficulty, LicenseStatus, RecordOrigin, ReviewAction,
    ReviewItemStatus, ReviewItemType, ReviewStatus, SourceType, StructureType,
)
from app.models import (
    AuditLog, DataConflict, Exercise, Provenance, ReviewQueueItem, Source,
)
from app.pipeline.postprocess import run_validation_sweep
from app.pipeline.validate import validate_exercise
from tests.conftest import AUTH


def _make_exercise(db, seeded, *, with_muscles=True, with_source=True,
                   origin=RecordOrigin.aggregated, name="Quality Test Exercise",
                   slug="quality-test"):
    from app.enums import ExerciseRole
    from app.models import ExerciseMuscle, ExerciseSource, Muscle
    ex = Exercise(slug=slug, canonical_name=name,
                  normalized_name=name.lower(), category_id=seeded and 1,
                  difficulty=Difficulty.beginner,
                  instructions="1. Do the thing carefully.",
                  review_status=ReviewStatus.pending_review, origin=origin,
                  confidence=0.8)
    db.add(ex)
    db.flush()
    if with_muscles:
        m = db.execute(select(Muscle).where(Muscle.slug == "levator-scapulae")).scalar_one()
        db.add(ExerciseMuscle(exercise_id=ex.id, muscle_id=m.id,
                              role=ExerciseRole.primary, confidence=0.9))
    if with_source:
        src = db.execute(select(Source).where(Source.license == LicenseStatus.unknown)).scalar()
        if src:
            db.add(ExerciseSource(exercise_id=ex.id, source_id=src.id))
    db.commit()
    return ex


def test_schema_has_all_core_tables(engine):
    from sqlalchemy import inspect
    insp = inspect(engine)
    tables = set(insp.get_table_names())
    expected = {"exercises", "muscles", "muscle_groups", "body_regions", "joints",
                "equipment", "exercise_muscles", "exercise_body_regions",
                "exercise_joints", "exercise_equipment", "exercise_variations",
                "sources", "source_documents", "exercise_sources", "provenance",
                "data_conflicts", "review_queue", "audit_log", "dataset_versions",
                "crawl_jobs", "crawl_urls", "exercise_types", "ai_events"}
    assert expected <= tables, expected - tables


def test_curated_records_have_curated_provenance(db, seeded):
    ex = db.execute(select(Exercise).where(
        Exercise.origin == RecordOrigin.curated)).scalars().first()
    provs = db.execute(select(Provenance).where(
        Provenance.exercise_id == ex.id)).scalars().all()
    assert provs and all(p.origin == DataOrigin.curated for p in provs)
    assert ex.review_status == ReviewStatus.approved


def test_anatomy_structure_types_are_distinct(db, seeded):
    from app.models import Muscle
    muscles = db.execute(select(Muscle)).scalars().all()
    types = {m.structure_type for m in muscles}
    assert StructureType.tendon.value in types
    assert StructureType.fascia.value in types
    assert StructureType.ligament.value in types
    # plantar fascia must be fascia, not a muscle
    pf = db.execute(select(Muscle).where(Muscle.slug == "plantar-fascia")).scalar_one()
    assert pf.structure_type == StructureType.fascia.value


def test_validation_flags_missing_anatomy(db, seeded):
    ex = _make_exercise(db, seeded, with_muscles=False)
    issues = validate_exercise(db, ex)
    codes = {i.code for i in issues}
    assert "missing_anatomy" in codes


def test_validation_flags_unknown_licensing(db, seeded):
    ex = _make_exercise(db, seeded, with_source=True)
    src = db.execute(select(Source).where(Source.license == LicenseStatus.unknown)).scalar()
    assert src is not None
    issues = validate_exercise(db, ex)
    assert any(i.code == "licensing_unknown" and i.item_type == ReviewItemType.licensing_unknown
               for i in issues)


def test_validation_sweep_queues_issues(db, seeded):
    _make_exercise(db, seeded, with_muscles=False)
    stats = run_validation_sweep(db)
    assert stats["checked"] >= 1
    assert stats["issues"] >= 1
    assert db.execute(select(ReviewQueueItem).where(
        ReviewQueueItem.status == ReviewItemStatus.open)).scalars().first() is not None


def test_conflict_detection_records_disagreement(db, seeded):
    from app.pipeline.validate import detect_anatomy_conflicts
    from app.models import SourceDocument
    ex = _make_exercise(db, seeded)
    srcs = db.execute(select(Source).limit(2)).scalars().all()
    d1 = SourceDocument(source_id=srcs[0].id, url="https://a.example/x", title="A")
    d2 = SourceDocument(source_id=srcs[1].id, url="https://b.example/y", title="B")
    db.add_all([d1, d2]); db.flush()
    db.add(Provenance(exercise_id=ex.id, field_name="muscles",
                      value='["levator-scapulae"]', origin=DataOrigin.source_fact,
                      source_document_id=d1.id))
    db.add(Provenance(exercise_id=ex.id, field_name="muscles",
                      value='["upper-trapezius"]', origin=DataOrigin.source_fact,
                      source_document_id=d2.id))
    db.commit()
    conflicts = detect_anatomy_conflicts(db, ex)
    assert len(conflicts) == 1
    assert set(conflicts[0]["difference"]) == {"levator-scapulae", "upper-trapezius"}


def test_review_merge_action_via_api(db, seeded, client):
    ex = _make_exercise(db, seeded, name="Merge Source Exercise")
    ex2 = _make_exercise(db, seeded, name="Merge Source Exercise 2",
                          slug="quality-test-2")
    db.commit()
    item = ReviewQueueItem(item_type=ReviewItemType.duplicate_pair,
                           exercise_id=ex.id, related_exercise_id=ex2.id,
                           payload={"similarity": 0.95})
    db.add(item); db.commit()

    r = client.post(f"/api/v1/review/{item.id}/action",
                    json={"action": "merge", "note": "same exercise"},
                    headers=AUTH)
    assert r.status_code == 200
    assert r.json()["status"] == ReviewItemStatus.merged.value
    db.refresh(ex); db.refresh(ex2)
    assert ex2.merged_into_id == ex.id
    assert "Merge Source Exercise 2" in (ex.aliases or [])
    audit = db.execute(select(AuditLog).where(
        AuditLog.action == "review_merge")).scalars().first()
    assert audit is not None


def test_review_merge_can_keep_related_record(db, seeded, client):
    """Reviewer picks B as the canonical survivor; primary merges into related."""
    ex = _make_exercise(db, seeded, name="Keep Related A", slug="keep-related-a")
    ex2 = _make_exercise(db, seeded, name="Keep Related B", slug="keep-related-b")
    db.commit()
    item = ReviewQueueItem(item_type=ReviewItemType.duplicate_pair,
                           exercise_id=ex.id, related_exercise_id=ex2.id,
                           payload={"similarity": 0.9})
    db.add(item); db.commit()
    r = client.post(f"/api/v1/review/{item.id}/action",
                    json={"action": "merge", "edits": {"keep": "related"}},
                    headers=AUTH)
    assert r.status_code == 200
    db.refresh(ex); db.refresh(ex2)
    assert ex.merged_into_id == ex2.id
    assert "Keep Related A" in (ex2.aliases or [])


def test_review_approve_flow(db, seeded, client):
    ex = _make_exercise(db, seeded)
    item = ReviewQueueItem(item_type=ReviewItemType.low_confidence,
                           exercise_id=ex.id, payload={"code": "low_confidence"})
    db.add(item); db.commit()
    r = client.post(f"/api/v1/review/{item.id}/action",
                    json={"action": "approve"}, headers=AUTH)
    assert r.status_code == 200
    db.refresh(ex)
    assert ex.review_status == ReviewStatus.approved


def test_low_confidence_exercise_is_queued(db, seeded):
    ex = _make_exercise(db, seeded)
    ex.confidence = 0.4
    db.commit()
    stats = run_validation_sweep(db)
    items = db.execute(select(ReviewQueueItem).where(
        ReviewQueueItem.exercise_id == ex.id)).scalars().all()
    assert any(i.item_type == ReviewItemType.low_confidence for i in items)
