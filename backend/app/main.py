"""FastAPI application entrypoint."""
from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app import __version__
from app.api import v1
from app.config import settings
from app.db import Base, engine
from app.log import configure_logging

configure_logging()

app = FastAPI(
    title=settings.app_name,
    version=__version__,
    description=(
        "Structured exercise knowledge base for Easeur — stretching, mobility, "
        "physiotherapy-oriented and rehabilitation exercises with anatomy "
        "taxonomy, provenance, licensing metadata and review workflows. "
        "Consumer endpoints return approved data by default; research "
        "endpoints expose review metadata. Admin endpoints require X-API-Key."
    ),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1.router)

# Project-owned exercise illustrations (see app/media_registry.py for policy).
_MEDIA_DIR = Path(__file__).resolve().parent.parent / "media"
if _MEDIA_DIR.is_dir():
    app.mount("/static", StaticFiles(directory=str(_MEDIA_DIR)), name="media")


@app.get("/health", tags=["meta"])
def health() -> dict:
    return {"status": "ok", "app": settings.app_name, "version": __version__}


@app.get("/", tags=["meta"])
def root() -> dict:
    return {
        "app": settings.app_name,
        "docs": "/docs",
        "api": "/api/v1",
        "consumer_note": "GET /api/v1/exercises returns approved exercises by default",
    }
