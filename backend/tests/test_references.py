"""Reference-link tests: coverage, idempotency, API exposure."""
from __future__ import annotations

from sqlalchemy import func, select

from app.models import Exercise, ExerciseReference
from app.services.seeder import seed_references


def _active_without_references(db) -> list[str]:
    return db.execute(
        select(Exercise.slug).where(
            Exercise.merged_into_id.is_(None),
            ~Exercise.id.in_(select(ExerciseReference.exercise_id).distinct()),
        )
    ).scalars().all()


def test_every_exercise_gets_a_reference(db, seeded):
    missing = _active_without_references(db)
    assert missing == [], f"exercises without references: {missing[:10]}"
    total = db.execute(select(func.count()).select_from(ExerciseReference)).scalar()
    assert total >= 184  # at least one each, usually more


def test_seed_references_idempotent(db, seeded):
    before = db.execute(select(func.count()).select_from(ExerciseReference)).scalar()
    seed_references(db)
    after = db.execute(select(func.count()).select_from(ExerciseReference)).scalar()
    assert before == after


def test_aggregated_references_point_at_source_documents(db, seeded):
    """Aggregated records reference the exact page they were extracted from."""
    from app.enums import Difficulty, RecordOrigin, ReviewStatus
    from app.models import ExerciseSource, ExerciseType, Source, SourceDocument
    src = db.execute(select(Source).where(Source.slug == "orthoinfo-aaos")).scalar_one()
    cat = db.execute(select(ExerciseType).limit(1)).scalar_one()
    doc = SourceDocument(source_id=src.id,
                         url="https://www.orthoinfo.org/recovery/test-page/",
                         title="Test Program")
    db.add(doc)
    db.flush()
    ex = Exercise(slug="agg-ref-test", canonical_name="Aggregated Ref Test",
                  normalized_name="aggregated ref test", category_id=cat.id,
                  difficulty=Difficulty.beginner,
                  instructions="1. Do it slowly.", review_status=ReviewStatus.pending_review,
                  origin=RecordOrigin.aggregated, confidence=0.8)
    db.add(ex)
    db.flush()
    db.add(ExerciseSource(exercise_id=ex.id, source_id=src.id, source_document_id=doc.id))
    db.commit()

    seed_references(db)
    refs = db.execute(select(ExerciseReference).where(
        ExerciseReference.exercise_id == ex.id)).scalars().all()
    assert refs
    demo = next((r for r in refs if r.kind == "demonstration"), None)
    assert demo is not None, "aggregated record should reference its source document"
    assert demo.url == "https://www.orthoinfo.org/recovery/test-page/"
    assert demo.source.slug == "orthoinfo-aaos"


def test_curated_references_are_authoritative_programs(db, seeded):
    """Curated records get official program pages for their region."""
    from app.enums import RecordOrigin
    cur = db.execute(select(Exercise).where(
        Exercise.origin == RecordOrigin.curated,
        Exercise.slug == "levator-scapulae-stretch")).scalar_one()
    refs = db.execute(select(ExerciseReference).where(
        ExerciseReference.exercise_id == cur.id)).scalars().all()
    assert refs
    neck_ref = next((r for r in refs if "neck" in r.url), None)
    assert neck_ref is not None, "expected a neck program reference"
    assert neck_ref.source.slug == "versus-arthritis"
    assert neck_ref.kind == "program"


def test_references_exposed_in_detail_api(client, seeded):
    slug = client.get("/api/v1/exercises").json()["items"][0]["slug"]
    detail = client.get(f"/api/v1/exercises/{slug}").json()
    assert "references" in detail
    assert detail["references"], "detail should include at least one reference"
    r = detail["references"][0]
    assert r["url"].startswith("https://")
    assert r["label"]
    assert r["kind"] in ("demonstration", "program", "article")
    assert r["authority"] == "high"  # all mapped sources are high-authority
