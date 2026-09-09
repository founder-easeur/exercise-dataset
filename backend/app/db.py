"""Database engine / session management (SQLAlchemy 2.0)."""
from __future__ import annotations

from collections.abc import Generator

from sqlalchemy import JSON, String, create_engine
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import settings


class Base(DeclarativeBase):
    # Resolve `Mapped[list[str]]` / `Mapped[dict]` annotations to PG types.
    type_annotation_map = {
        list[str]: ARRAY(String),
        list: JSONB(),
        dict: JSONB(),
    }


def _engine_kwargs() -> dict:
    kwargs: dict = {"pool_pre_ping": True}
    url = settings.database_url
    if url.startswith("sqlite"):
        kwargs["connect_args"] = {"check_same_thread": False}
    else:
        kwargs["pool_size"] = 10
        kwargs["max_overflow"] = 20
        # Explicit UTF-8 client encoding: taxonomy/seed data contains non-ASCII
        # names; servers initialized without a locale (SQL_ASCII) would otherwise
        # crash psycopg2 with UnicodeEncodeError.
        kwargs["connect_args"] = {"options": "-c client_encoding=UTF8"}
    return kwargs


engine = create_engine(settings.database_url, **_engine_kwargs())
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency: one session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
