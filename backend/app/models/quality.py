"""Provenance, conflicts, review queue, audit log, AI tracking, dataset versions."""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    DateTime, Enum, Float, ForeignKey, Index, Integer, String, Text, UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base
from app.enums import (
    ConflictStatus, DataOrigin, ReviewAction, ReviewItemStatus, ReviewItemType,
)


class Provenance(Base):
    """Field-level provenance: where each important value came from."""
    __tablename__ = "provenance"
    __table_args__ = (
        Index("ix_provenance_exercise_field", "exercise_id", "field_name"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    exercise_id: Mapped[int] = mapped_column(
        ForeignKey("exercises.id", ondelete="CASCADE"), index=True
    )
    field_name: Mapped[str] = mapped_column(String(80))
    value: Mapped[str | None] = mapped_column(Text, nullable=True)
    origin: Mapped[DataOrigin] = mapped_column(Enum(DataOrigin, name="data_origin"))
    source_document_id: Mapped[int | None] = mapped_column(
        ForeignKey("source_documents.id"), nullable=True, index=True
    )
    ai_model: Mapped[str | None] = mapped_column(String(120), nullable=True)
    ai_model_version: Mapped[str | None] = mapped_column(String(120), nullable=True)
    ai_prompt_version: Mapped[str | None] = mapped_column(String(60), nullable=True)
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )

    exercise: Mapped["Exercise"] = relationship(  # noqa: F821
        back_populates="provenance"
    )
    source_document: Mapped["SourceDocument | None"] = relationship()  # noqa: F821


class DataConflict(Base):
    """Recorded disagreement between sources for the same exercise field."""
    __tablename__ = "data_conflicts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    exercise_id: Mapped[int] = mapped_column(
        ForeignKey("exercises.id", ondelete="CASCADE"), index=True
    )
    field_name: Mapped[str] = mapped_column(String(80))
    values: Mapped[list] = mapped_column(JSONB, default=list)
    source_ids: Mapped[list] = mapped_column(JSONB, default=list)
    status: Mapped[ConflictStatus] = mapped_column(
        Enum(ConflictStatus, name="conflict_status"),
        default=ConflictStatus.open, index=True,
    )
    resolution: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )
    resolved_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )


class ReviewQueueItem(Base):
    __tablename__ = "review_queue"
    __table_args__ = (
        Index("ix_review_queue_type_status", "item_type", "status"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    item_type: Mapped[ReviewItemType] = mapped_column(
        Enum(ReviewItemType, name="review_item_type"), index=True
    )
    status: Mapped[ReviewItemStatus] = mapped_column(
        Enum(ReviewItemStatus, name="review_item_status"),
        default=ReviewItemStatus.open, index=True,
    )
    exercise_id: Mapped[int | None] = mapped_column(
        ForeignKey("exercises.id", ondelete="CASCADE"), nullable=True, index=True
    )
    related_exercise_id: Mapped[int | None] = mapped_column(
        ForeignKey("exercises.id", ondelete="SET NULL"), nullable=True, index=True
    )
    payload: Mapped[dict] = mapped_column(JSONB, default=dict)
    priority: Mapped[int] = mapped_column(Integer, default=5)  # 1 highest
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )
    resolved_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    resolution_note: Mapped[str | None] = mapped_column(Text, nullable=True)


class AuditLog(Base):
    __tablename__ = "audit_log"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    actor: Mapped[str] = mapped_column(String(120), default="system")
    action: Mapped[str] = mapped_column(String(60), index=True)
    entity_type: Mapped[str] = mapped_column(String(60), index=True)
    entity_id: Mapped[int] = mapped_column(Integer, index=True)
    details: Mapped[dict] = mapped_column(JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, index=True
    )


class AiEvent(Base):
    """Every AI (or deterministic-enrichment) operation is tracked."""
    __tablename__ = "ai_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    operation: Mapped[str] = mapped_column(String(80))
    model: Mapped[str] = mapped_column(String(120))
    model_version: Mapped[str | None] = mapped_column(String(120), nullable=True)
    prompt_version: Mapped[str | None] = mapped_column(String(60), nullable=True)
    target_type: Mapped[str] = mapped_column(String(60), default="exercise_candidate")
    target_ref: Mapped[str | None] = mapped_column(String(200), nullable=True)
    fields_generated: Mapped[list] = mapped_column(JSONB, default=list)
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    accepted: Mapped[bool] = mapped_column(default=False)
    review_status: Mapped[str] = mapped_column(String(40), default="pending_review")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )


class DatasetVersion(Base):
    __tablename__ = "dataset_versions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    version: Mapped[str] = mapped_column(String(40), unique=True, index=True)
    label: Mapped[str | None] = mapped_column(String(200), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    stats: Mapped[dict] = mapped_column(JSONB, default=dict)
    diff: Mapped[dict] = mapped_column(JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )
