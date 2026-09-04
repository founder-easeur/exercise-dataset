"""Test fixtures: isolated test database (real PostgreSQL) + API client."""
from __future__ import annotations

import os

# Must be set before any app import (settings are cached at import time).
os.environ.setdefault("EASEUR_DATABASE_URL", "postgresql+psycopg2://easeur:easeur@127.0.0.1:5432/easeur_test")
os.environ.setdefault("EASEUR_ADMIN_API_KEY", "test-admin-key")

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from sqlalchemy import create_engine, text  # noqa: E402
from sqlalchemy.orm import sessionmaker  # noqa: E402

from app.db import Base, get_db  # noqa: E402


@pytest.fixture(scope="session")
def engine():
    engine = create_engine(os.environ["EASEUR_DATABASE_URL"], pool_pre_ping=True)
    # Run real migrations so the migration chain itself is tested.
    from alembic import command
    from alembic.config import Config
    cfg = Config(os.path.join(os.path.dirname(os.path.dirname(__file__)), "alembic.ini"))
    command.upgrade(cfg, "head")
    yield engine
    engine.dispose()


@pytest.fixture()
def db(engine):
    """Fresh transactional-ish session: truncate all tables after each test."""
    Session = sessionmaker(bind=engine, expire_on_commit=False)
    session = Session()
    yield session
    session.rollback()
    session.close()
    # Truncate everything for test isolation.
    with engine.begin() as conn:
        conn.execute(text(
            "TRUNCATE TABLE exercise_muscles, exercise_body_regions, exercise_joints, "
            "exercise_equipment, exercise_variations, exercise_sources, provenance, "
            "data_conflicts, review_queue, audit_log, ai_events, dataset_versions, "
            "crawl_urls, crawl_jobs, source_documents, sources, exercises, muscles, "
            "muscle_groups, body_regions, joints, equipment, exercise_types RESTART IDENTITY CASCADE"))


@pytest.fixture()
def client(db):
    from app.main import app
    app.dependency_overrides[get_db] = lambda: db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture()
def seeded(db):
    """Seed taxonomy + sources + curated exercises into the test DB."""
    from app.services.seeder import run_full_seed
    return run_full_seed(db)


AUTH = {"X-API-Key": "test-admin-key"}
