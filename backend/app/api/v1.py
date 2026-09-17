"""API v1 routers."""
from __future__ import annotations

import json
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from pydantic import BaseModel, Field
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.config import settings
from app.db import get_db
from app.enums import (
    ConflictStatus, CrawlMode, ReviewAction, ReviewItemType,
)
from app.models import (
    AuditLog, CrawlJob, CrawlUrl, DataConflict, Equipment, ExerciseSource,
    ExerciseType, Joint, ReviewQueueItem, Source, SourceDocument,
)
from app.services import export as export_svc
from app.services import query as q
from app.services import review as review_svc
from app.services import serializers as ser
from app.services import stats as stats_svc
from app.api.deps import require_admin

router = APIRouter(prefix="/api/v1", tags=["v1"])


# ---------------------------------------------------------------- exercises
@router.get("/exercises", summary="List/filter exercises (consumer endpoint)")
def list_exercises(
    db: Session = Depends(get_db),
    q_text: str | None = Query(None, alias="q"),
    body_region: str | None = None,
    muscle: str | None = None,
    muscle_group: str | None = None,
    joint: str | None = None,
    exercise_type: str | None = Query(None, alias="type"),
    equipment: str | None = None,
    difficulty: str | None = None,
    position: str | None = None,
    review_status: str = Query("approved", alias="status",
                               description="'approved' (consumer default), comma list, or 'all'"),
    confidence_min: float | None = Query(None, ge=0, le=1),
    source: str | None = None,
    origin: str | None = None,
    sort: str = "name",
    page: int = Query(1, ge=1),
    page_size: int = Query(24, ge=1, le=200),
):
    filters = q.ExerciseFilters(
        q=q_text, body_region=body_region, muscle=muscle, muscle_group=muscle_group,
        joint=joint, exercise_type=exercise_type, equipment=equipment,
        difficulty=difficulty, position=position, review_status=review_status,
        confidence_min=confidence_min, source=source, origin=origin, sort=sort,
    )
    result = q.list_exercises(db, filters, page=page, page_size=page_size)
    return {
        "total": result["total"], "page": result["page"], "page_size": result["page_size"],
        "items": [ser.exercise_summary(e) for e in result["items"]],
    }


@router.get("/exercises/search", summary="Search exercises (alias of list with required q)")
def search_exercises(
    q_text: str = Query(..., alias="q", min_length=2),
    db: Session = Depends(get_db),
    body_region: str | None = None, muscle: str | None = None,
    exercise_type: str | None = Query(None, alias="type"),
    difficulty: str | None = None, review_status: str = Query("all", alias="status"),
    limit: int = Query(20, ge=1, le=100),
):
    filters = q.ExerciseFilters(q=q_text, body_region=body_region, muscle=muscle,
                                exercise_type=exercise_type, difficulty=difficulty,
                                review_status=review_status)
    result = q.list_exercises(db, filters, page=1, page_size=limit)
    return {"total": result["total"], "items": [ser.exercise_summary(e) for e in result["items"]]}


@router.get("/exercises/{id_or_slug}", summary="Exercise detail")
def exercise_detail(id_or_slug: str, include: str | None = Query(None),
                    db: Session = Depends(get_db)):
    ex = q.get_exercise(db, id_or_slug)
    if ex is None or ex.merged_into_id:
        raise HTTPException(404, "exercise not found")
    include_research = "research" in (include or "")
    return ser.exercise_detail(ex, include_research=include_research)


# ------------------------------------------------------------------ muscles
@router.get("/muscles")
def list_muscles(
    db: Session = Depends(get_db),
    q_text: str | None = Query(None, alias="q"),
    region: str | None = None, muscle_group: str | None = None,
    structure_type: str | None = None, small_only: bool = False,
):
    muscles = q.list_muscles(db, q=q_text, region=region, muscle_group=muscle_group,
                             structure_type=structure_type, small_only=small_only)
    coverage = {c["id"]: c for c in stats_svc.muscle_coverage(db)}
    return {"total": len(muscles),
            "items": [ser.muscle_detail(m, coverage=coverage.get(m.id)) for m in muscles]}


@router.get("/muscles/{id_or_slug}")
def muscle_detail(id_or_slug: str, db: Session = Depends(get_db)):
    m = q.get_muscle(db, id_or_slug)
    if m is None:
        raise HTTPException(404, "muscle not found")
    exercises = q.exercises_for_muscle(db, m.id)
    coverage = next((c for c in stats_svc.muscle_coverage(db) if c["id"] == m.id), None)
    return ser.muscle_detail(m, exercises=exercises, coverage=coverage)


# -------------------------------------------------------- regions/joints/etc
@router.get("/body-regions")
def list_regions(db: Session = Depends(get_db)):
    from app.models import BodyRegion
    rows = db.execute(select(BodyRegion).order_by(BodyRegion.sort_order)).scalars().all()
    cov = {c["slug"]: c for c in stats_svc.region_coverage(db)}
    return {"total": len(rows), "items": [
        {"id": r.id, "slug": r.slug, "name": r.name, "description": r.description,
         **{k: v for k, v in cov.get(r.slug, {}).items()
            if k not in ("id", "slug", "name")}} for r in rows]}


@router.get("/body-regions/{slug}")
def region_detail(slug: str, db: Session = Depends(get_db)):
    from app.models import BodyRegion
    r = db.execute(select(BodyRegion).where(BodyRegion.slug == slug)).scalar_one_or_none()
    if r is None:
        raise HTTPException(404, "region not found")
    result = q.list_exercises(db, q.ExerciseFilters(body_region=slug, review_status="all"),
                              page=1, page_size=200)
    cov = next((c for c in stats_svc.region_coverage(db) if c["slug"] == slug), None)
    return {"id": r.id, "slug": r.slug, "name": r.name, "description": r.description,
            "coverage": cov,
            "exercise_count": result["total"],
            "exercises": [ser.exercise_summary(e) for e in result["items"]]}


@router.get("/joints")
def list_joints(db: Session = Depends(get_db)):
    rows = db.execute(select(Joint).order_by(Joint.name)).scalars().all()
    return {"total": len(rows), "items": [
        {"id": j.id, "slug": j.slug, "name": j.name, "joint_type": j.joint_type} for j in rows]}


@router.get("/joints/{id_or_slug}")
def joint_detail(id_or_slug: str, db: Session = Depends(get_db)):
    joint = db.execute(select(Joint).where(
        Joint.slug == id_or_slug if not id_or_slug.isdigit() else Joint.id == int(id_or_slug))
    ).scalar_one_or_none()
    if joint is None:
        raise HTTPException(404, "joint not found")
    result = q.list_exercises(db, q.ExerciseFilters(joint=joint.slug, review_status="all"),
                              page=1, page_size=100)
    return {"id": joint.id, "slug": joint.slug, "name": joint.name,
            "joint_type": joint.joint_type, "exercise_count": result["total"],
            "exercises": [ser.exercise_summary(e) for e in result["items"]]}


@router.get("/equipment")
def list_equipment(db: Session = Depends(get_db)):
    rows = db.execute(select(Equipment).order_by(Equipment.name)).scalars().all()
    return {"total": len(rows), "items": [
        {"id": e.id, "slug": e.slug, "name": e.name} for e in rows]}


@router.get("/exercise-types")
def list_exercise_types(db: Session = Depends(get_db)):
    rows = db.execute(select(ExerciseType).order_by(ExerciseType.sort_order)).scalars().all()
    return {"total": len(rows), "items": [
        {"id": t.id, "slug": t.slug, "name": t.name, "description": t.description}
        for t in rows]}


# -------------------------------------------------------------------- stats
@router.get("/stats/dashboard")
def dashboard(db: Session = Depends(get_db)):
    return stats_svc.dashboard_stats(db)


@router.get("/stats/coverage/muscles")
def coverage_muscles(region: str | None = None, db: Session = Depends(get_db)):
    rows = stats_svc.muscle_coverage(db, region_slug=region)
    return {"total": len(rows),
            "summary": {
                "missing": sum(1 for r in rows if r["status"] == "missing"),
                "limited": sum(1 for r in rows if r["status"] == "limited"),
                "good": sum(1 for r in rows if r["status"] == "good"),
                "excellent": sum(1 for r in rows if r["status"] == "excellent"),
                "needs_review": sum(1 for r in rows if r["status"] == "needs_review"),
            },
            "items": rows}


@router.get("/stats/coverage/regions")
def coverage_regions(db: Session = Depends(get_db)):
    return {"items": stats_svc.region_coverage(db)}


# ------------------------------------------------------------------ sources
@router.get("/sources")
def list_sources(db: Session = Depends(get_db)):
    rows = db.execute(select(Source).order_by(Source.name)).scalars().all()
    items = []
    for s in rows:
        exercise_count = db.scalar(
            select(func.count(func.distinct(ExerciseSource.exercise_id)))
            .where(ExerciseSource.source_id == s.id)) or 0
        doc_count = db.scalar(
            select(func.count()).select_from(SourceDocument)
            .where(SourceDocument.source_id == s.id)) or 0
        job = db.execute(select(CrawlJob).where(CrawlJob.source_id == s.id)
                         .order_by(CrawlJob.started_at.desc())).scalars().first()
        last_crawl = None
        if job:
            last_crawl = {"job_id": job.id, "mode": job.mode.value,
                          "status": job.status.value,
                          "finished_at": job.finished_at.isoformat() if job.finished_at else None}
        items.append(ser.source_detail(s, exercise_count=exercise_count,
                                       document_count=doc_count, last_crawl=last_crawl))
    return {"total": len(items), "items": items}


@router.get("/sources/{slug}")
def source_detail(slug: str, db: Session = Depends(get_db)):
    s = db.execute(select(Source).where(Source.slug == slug)).scalar_one_or_none()
    if s is None:
        raise HTTPException(404, "source not found")
    docs = db.execute(select(SourceDocument).where(SourceDocument.source_id == s.id)
                      .order_by(SourceDocument.fetched_at.desc())).scalars().all()
    count = db.scalar(select(func.count(func.distinct(ExerciseSource.exercise_id)))
                      .where(ExerciseSource.source_id == s.id)) or 0
    return {**ser.source_detail(s, exercise_count=count, document_count=len(docs)),
            "documents": [{"id": d.id, "url": d.url, "title": d.title,
                           "fetched_at": d.fetched_at.isoformat() if d.fetched_at else None,
                           "word_count": d.word_count} for d in docs[:50]]}


# ------------------------------------------------------------------- review
@router.get("/review", summary="Review queue (research UI)")
def review_queue(item_type: str | None = None, status: str = "open",
                 limit: int = Query(100, ge=1, le=500), db: Session = Depends(get_db)):
    items = review_svc.list_queue(db, item_type=item_type, status=status, limit=limit)
    return {"total": len(items), "items": [ser.review_item(i) for i in items]}


class ReviewActionRequest(BaseModel):
    action: str = Field(..., description="approve|reject|edit|merge|split|flag|dismiss")
    note: str | None = None
    edits: dict | None = None


@router.post("/review/{item_id}/action", dependencies=[Depends(require_admin)])
def review_action(item_id: int, body: ReviewActionRequest, db: Session = Depends(get_db),
                  admin: str = Depends(require_admin)):
    try:
        action = ReviewAction(body.action)
    except ValueError:
        raise HTTPException(422, f"unknown action {body.action}")
    item = review_svc.apply_review_action(db, item_id, action, actor=admin,
                                          note=body.note, edits=body.edits)
    if item is None:
        raise HTTPException(404, "review item not found")
    return ser.review_item(item)


@router.get("/conflicts")
def conflicts(status: str = "open", db: Session = Depends(get_db)):
    rows = db.execute(select(DataConflict).where(
        DataConflict.status == ConflictStatus(status))).scalars().all()
    return {"total": len(rows), "items": [ser.conflict(c) for c in rows]}


@router.get("/duplicates", summary="Open duplicate pairs with comparison")
def duplicates(db: Session = Depends(get_db)):
    from app.enums import ReviewItemStatus
    items = db.execute(select(ReviewQueueItem).where(
        ReviewQueueItem.item_type == ReviewItemType.duplicate_pair,
        ReviewQueueItem.status == ReviewItemStatus.open)).scalars().all()
    out = []
    for i in items:
        a = q.get_related_exercise(db, i.exercise_id) if i.exercise_id else None
        b = q.get_related_exercise(db, i.related_exercise_id) if i.related_exercise_id else None
        out.append({
            "review_item_id": i.id,
            "similarity": (i.payload or {}).get("similarity"),
            "stage": (i.payload or {}).get("stage"),
            "components": (i.payload or {}).get("components"),
            "exercise_a": ser.exercise_summary(a) if a else None,
            "exercise_b": ser.exercise_summary(b) if b else None,
            "reason": i.reason,
        })
    return {"total": len(out), "items": out}


@router.get("/audit", dependencies=[Depends(require_admin)])
def audit_log(limit: int = 100, db: Session = Depends(get_db)):
    rows = db.execute(select(AuditLog).order_by(AuditLog.created_at.desc())
                      .limit(limit)).scalars().all()
    return {"total": len(rows), "items": [
        {"id": a.id, "actor": a.actor, "action": a.action,
         "entity_type": a.entity_type, "entity_id": a.entity_id, "details": a.details,
         "created_at": a.created_at.isoformat()} for a in rows]}


# ------------------------------------------------------------------- export
@router.get("/export")
def export_dataset(
    dataset: str = Query("exercises"),
    fmt: str = Query("json", pattern="^(json|jsonl|csv)$"),
    include_pending: bool = False,
    origin: str | None = None,
    db: Session = Depends(get_db),
):
    media = {"json": "application/json", "jsonl": "application/x-ndjson",
             "csv": "text/csv"}
    try:
        if dataset == "exercises":
            payload = export_svc.export_exercises(db, fmt, approved_only=True,
                                                  origin=origin,
                                                  include_pending=include_pending)
        elif dataset in ("muscles", "body-regions", "joints", "equipment", "exercise-types"):
            payload = export_svc.export_taxonomy(db, dataset, fmt)
        else:
            raise HTTPException(400, f"unknown dataset {dataset}")
    except ValueError as exc:
        raise HTTPException(400, str(exc))
    filename = f"{dataset}{'-all' if include_pending else ''}.{fmt}"
    return Response(content=payload, media_type=media[fmt],
                    headers={"Content-Disposition": f'attachment; filename="{filename}"'})


@router.get("/datasets")
def dataset_versions(db: Session = Depends(get_db)):
    from app.models import DatasetVersion
    rows = db.execute(select(DatasetVersion).order_by(DatasetVersion.created_at.desc())
                      ).scalars().all()
    return {"total": len(rows), "items": [
        {"id": v.id, "version": v.version, "label": v.label, "notes": v.notes,
         "stats": v.stats, "diff": v.diff,
         "created_at": v.created_at.isoformat()} for v in rows]}


# ----------------------------------------------------------- admin pipeline
class CrawlRequest(BaseModel):
    mode: str = "replay"
    sources: list[str] | None = None
    max_pages: int | None = Field(None, ge=1, le=200)


@router.post("/admin/crawl", dependencies=[Depends(require_admin)])
def admin_crawl(body: CrawlRequest, db: Session = Depends(get_db),
                admin: str = Depends(require_admin)):
    from app.pipeline.crawler import CrawlRunner
    try:
        mode = CrawlMode(body.mode)
    except ValueError:
        raise HTTPException(422, "mode must be 'live' or 'replay'")
    corpus = Path("corpus") if mode == CrawlMode.replay else None
    runner = CrawlRunner(db, mode, corpus_dir=corpus)
    return runner.run(body.sources, body.max_pages)


@router.post("/admin/dedup", dependencies=[Depends(require_admin)])
def admin_dedup(db: Session = Depends(get_db), admin: str = Depends(require_admin)):
    from app.pipeline.postprocess import run_dedup_scan
    return run_dedup_scan(db)


@router.post("/admin/validate", dependencies=[Depends(require_admin)])
def admin_validate(db: Session = Depends(get_db), admin: str = Depends(require_admin)):
    from app.pipeline.postprocess import run_validation_sweep
    return run_validation_sweep(db)
