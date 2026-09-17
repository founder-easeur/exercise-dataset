"""Management CLI.

Usage:  python -m app.cli <command>
"""
from __future__ import annotations

import logging
from pathlib import Path

import typer
from sqlalchemy import select

from app.config import settings
from app.db import Base, SessionLocal, engine
from app.log import configure_logging, log_event

cli = typer.Typer(name="easeur", help="Easeur Exercise Knowledge Base management")
pipeline_cli = typer.Typer(help="Pipeline operations")
cli.add_typer(pipeline_cli, name="pipeline")

log = logging.getLogger("easeur.cli")


@cli.command("init-db")
def init_db() -> None:
    """Run migrations (alembic upgrade head)."""
    from alembic import command
    from alembic.config import Config
    cfg = Config(Path(__file__).parent.parent / "alembic.ini")
    command.upgrade(cfg, "head")
    typer.echo("database migrated to head")


@cli.command("seed")
def seed() -> None:
    """Seed taxonomy, sources and curated exercises."""
    from app.services.seeder import run_full_seed
    db = SessionLocal()
    try:
        result = run_full_seed(db)
        typer.echo(f"seeded: {result}")
    finally:
        db.close()


@cli.command("drop-all")
def drop_all() -> None:
    """Drop all tables (dev only!)."""
    if typer.confirm("Drop ALL tables?"):
        Base.metadata.drop_all(engine)
        typer.echo("dropped")


@pipeline_cli.command("crawl")
def crawl(mode: str = typer.Option("replay", help="live|replay"),
          sources: str = typer.Option("", help="comma-separated source slugs"),
          max_pages: int = typer.Option(0, help="0 = use config default")) -> None:
    """Run a controlled crawl job (live HTTP or replay corpus)."""
    from app.enums import CrawlMode
    from app.pipeline.crawler import CrawlRunner
    db = SessionLocal()
    try:
        runner = CrawlRunner(
            db, CrawlMode(mode),
            corpus_dir=Path(__file__).parent.parent / "corpus" if mode == "replay" else None)
        result = runner.run(
            [s for s in sources.split(",") if s] or None,
            max_pages or None)
        typer.echo(result)
    finally:
        db.close()


@pipeline_cli.command("postprocess")
def postprocess() -> None:
    """Dedup scan + validation sweep."""
    from app.pipeline.postprocess import run_full_postprocess
    db = SessionLocal()
    try:
        typer.echo(run_full_postprocess(db))
    finally:
        db.close()


@pipeline_cli.command("report")
def report(out: Path = typer.Option(Path("../docs/data-quality-report.md"))) -> None:
    """Generate docs/data-quality-report.md."""
    from app.pipeline.report import generate_report
    db = SessionLocal()
    try:
        content = generate_report(db)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(content)
        typer.echo(f"report written to {out}")
    finally:
        db.close()


@pipeline_cli.command("run-all")
def run_all(mode: str = "replay", max_pages: int = 0) -> None:
    """Seed (if needed) -> crawl -> postprocess -> report."""
    from app.enums import RecordOrigin
    from app.models import Exercise
    from app.pipeline.crawler import CrawlRunner
    from app.pipeline.postprocess import run_full_postprocess
    from app.pipeline.report import generate_report
    from app.services.seeder import run_full_seed
    db = SessionLocal()
    try:
        existing = db.scalar(select(Exercise.id).limit(1))
        if not existing:
            typer.echo(run_full_seed(db))
        from app.enums import CrawlMode
        runner = CrawlRunner(db, CrawlMode(mode),
                             corpus_dir=Path(__file__).parent.parent / "corpus"
                             if mode == "replay" else None)
        typer.echo(runner.run(None, max_pages or None))
        typer.echo(run_full_postprocess(db))
        out = Path(__file__).parent.parent.parent / "docs" / "data-quality-report.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(generate_report(db))
        typer.echo(f"report -> {out}")
    finally:
        db.close()


@cli.command("export")
def export(dataset: str = typer.Option("exercises"),
           fmt: str = typer.Option("json", help="json|jsonl|csv"),
           out: Path = typer.Option(None),
           include_pending: bool = typer.Option(False)) -> None:
    """Export datasets to exports/."""
    from app.services.export import export_exercises, export_taxonomy
    db = SessionLocal()
    try:
        if dataset == "exercises":
            payload = export_exercises(db, fmt, include_pending=include_pending)
        else:
            payload = export_taxonomy(db, dataset, fmt)
        out = out or (Path(__file__).parent.parent.parent / "exports" / f"{dataset}.{fmt}")
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(payload)
        typer.echo(f"exported -> {out}")
    finally:
        db.close()


@cli.command("snapshot")
def snapshot(version: str = typer.Argument(...), label: str = typer.Option(""),
             notes: str = typer.Option("")) -> None:
    """Create a dataset version snapshot."""
    from app.services.export import snapshot_version
    db = SessionLocal()
    try:
        v = snapshot_version(db, version, label or None, notes or None)
        typer.echo(f"created dataset version {v.version} (id={v.id})")
    finally:
        db.close()


@cli.command("serve")
def serve(host: str = "0.0.0.0", port: int = 8000, reload: bool = False) -> None:
    """Run the API server (dev convenience; use uvicorn in production)."""
    import uvicorn
    uvicorn.run("app.main:app", host=host, port=port, reload=reload)


if __name__ == "__main__":
    configure_logging()
    cli()
