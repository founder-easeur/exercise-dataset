"""Crawl job tracking."""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    DateTime, Enum, ForeignKey, Integer, String, Text, UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base
from app.enums import CrawlJobStatus, CrawlMode, CrawlUrlStatus


class CrawlJob(Base):
    __tablename__ = "crawl_jobs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    source_id: Mapped[int | None] = mapped_column(
        ForeignKey("sources.id"), nullable=True, index=True
    )
    mode: Mapped[CrawlMode] = mapped_column(Enum(CrawlMode, name="crawl_mode"))
    status: Mapped[CrawlJobStatus] = mapped_column(
        Enum(CrawlJobStatus, name="crawl_job_status"),
        default=CrawlJobStatus.queued, index=True,
    )
    config: Mapped[dict] = mapped_column(JSONB, default=dict)
    stats: Mapped[dict] = mapped_column(JSONB, default=dict)
    started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    finished_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    error: Mapped[str | None] = mapped_column(Text, nullable=True)

    urls: Mapped[list["CrawlUrl"]] = relationship(
        back_populates="job", cascade="all, delete-orphan"
    )


class CrawlUrl(Base):
    __tablename__ = "crawl_urls"
    __table_args__ = (
        UniqueConstraint("crawl_job_id", "url", name="uq_crawl_url"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    crawl_job_id: Mapped[int] = mapped_column(
        ForeignKey("crawl_jobs.id", ondelete="CASCADE"), index=True
    )
    url: Mapped[str] = mapped_column(String(800), index=True)
    status: Mapped[CrawlUrlStatus] = mapped_column(
        Enum(CrawlUrlStatus, name="crawl_url_status"),
        default=CrawlUrlStatus.discovered, index=True,
    )
    http_status: Mapped[int | None] = mapped_column(Integer, nullable=True)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)
    content_hash: Mapped[str | None] = mapped_column(String(64), nullable=True)
    discovered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )
    fetched_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    job: Mapped["CrawlJob"] = relationship(back_populates="urls")
