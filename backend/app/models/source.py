"""Source registry and crawled documents."""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    DateTime, Enum, Float, ForeignKey, Index, Integer, String, Text, UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base
from app.enums import (
    CommercialUse, LicenseStatus, RobotsStatus, SourceRelationship, SourceType,
    SourceAuthority, CrawlMode,
)


class Source(Base):
    """A registered, controlled source (domain-level)."""
    __tablename__ = "sources"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(200))
    domain: Mapped[str] = mapped_column(String(200), unique=True, index=True)
    homepage_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    source_type: Mapped[SourceType] = mapped_column(
        Enum(SourceType, name="source_type"), default=SourceType.other
    )
    authority: Mapped[SourceAuthority] = mapped_column(
        Enum(SourceAuthority, name="source_authority"),
        default=SourceAuthority.unknown, index=True,
    )
    license: Mapped[LicenseStatus] = mapped_column(
        Enum(LicenseStatus, name="license_status"),
        default=LicenseStatus.unknown, index=True,
    )
    commercial_use_allowed: Mapped[CommercialUse] = mapped_column(
        Enum(CommercialUse, name="commercial_use"), default=CommercialUse.unknown
    )
    attribution_required: Mapped[bool] = mapped_column(default=True)
    license_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    terms_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    robots_status: Mapped[RobotsStatus] = mapped_column(
        Enum(RobotsStatus, name="robots_status"), default=RobotsStatus.unknown
    )
    is_active: Mapped[bool] = mapped_column(default=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )

    documents: Mapped[list["SourceDocument"]] = relationship(back_populates="source")


class SourceDocument(Base):
    """A fetched page/document belonging to a source."""
    __tablename__ = "source_documents"
    __table_args__ = (
        UniqueConstraint("source_id", "url", name="uq_source_doc_url"),
        Index("ix_source_documents_hash", "content_hash"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    source_id: Mapped[int] = mapped_column(ForeignKey("sources.id"), index=True)
    url: Mapped[str] = mapped_column(String(800))
    title: Mapped[str | None] = mapped_column(String(500), nullable=True)
    content_type: Mapped[str | None] = mapped_column(String(120), nullable=True)
    fetch_mode: Mapped[CrawlMode] = mapped_column(
        Enum(CrawlMode, name="crawl_mode"), default=CrawlMode.live
    )
    http_status: Mapped[int | None] = mapped_column(Integer, nullable=True)
    fetched_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )
    content_hash: Mapped[str | None] = mapped_column(String(64), index=True)
    word_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    # Sanitized, bounded text excerpt (never full copyrighted articles)
    text_excerpt: Mapped[str | None] = mapped_column(Text, nullable=True)
    extraction_stats: Mapped[dict] = mapped_column(default=dict)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)

    source: Mapped["Source"] = relationship(back_populates="documents")
    exercise_sources: Mapped[list["ExerciseSource"]] = relationship(
        back_populates="source_document"
    )


class ExerciseSource(Base):
    """Many-to-many: which sources describe an exercise."""
    __tablename__ = "exercise_sources"
    __table_args__ = (
        UniqueConstraint("exercise_id", "source_document_id", name="uq_ex_source_doc"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    exercise_id: Mapped[int] = mapped_column(
        ForeignKey("exercises.id", ondelete="CASCADE"), index=True
    )
    source_id: Mapped[int] = mapped_column(ForeignKey("sources.id"), index=True)
    source_document_id: Mapped[int | None] = mapped_column(
        ForeignKey("source_documents.id"), nullable=True, index=True
    )
    source_relationship: Mapped[SourceRelationship] = mapped_column(
        Enum(SourceRelationship, name="source_relationship"),
        default=SourceRelationship.original,
    )
    license_at_retrieval: Mapped[LicenseStatus] = mapped_column(
        Enum(LicenseStatus, name="license_status_retrieval"),
        default=LicenseStatus.unknown,
    )
    retrieved_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )
    confidence: Mapped[float] = mapped_column(Float, default=0.8)

    exercise: Mapped["Exercise"] = relationship(back_populates="sources")  # noqa: F821
    source: Mapped["Source"] = relationship()
    source_document: Mapped["SourceDocument | None"] = relationship(
        back_populates="exercise_sources"
    )
