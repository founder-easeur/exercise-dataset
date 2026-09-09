"""Core exercise tables and relationships."""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    DateTime, Enum, Float, ForeignKey, Index, Integer, String, Text, UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base
from app.enums import (
    Difficulty, ExerciseRole, RecordOrigin, RegionRole, ReviewStatus,
)


class Exercise(Base):
    __tablename__ = "exercises"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    slug: Mapped[str] = mapped_column(String(160), unique=True, index=True)
    canonical_name: Mapped[str] = mapped_column(String(200), index=True)
    aliases: Mapped[list[str]] = mapped_column(default=list)

    category_id: Mapped[int] = mapped_column(
        ForeignKey("exercise_types.id"), index=True
    )
    movement_pattern: Mapped[str | None] = mapped_column(String(120), nullable=True)
    difficulty: Mapped[Difficulty] = mapped_column(
        Enum(Difficulty, name="difficulty"), default=Difficulty.beginner, index=True
    )
    position: Mapped[str | None] = mapped_column(String(120), nullable=True)

    # Normalized, human-readable content owned by the knowledge base
    instructions: Mapped[str | None] = mapped_column(Text, nullable=True)
    breathing: Mapped[str | None] = mapped_column(Text, nullable=True)
    safety_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    contraindications: Mapped[str | None] = mapped_column(Text, nullable=True)
    clinical_relevance: Mapped[str | None] = mapped_column(Text, nullable=True)
    dosage: Mapped[str | None] = mapped_column(String(200), nullable=True)

    confidence: Mapped[float] = mapped_column(Float, default=0.8, index=True)
    review_status: Mapped[str] = mapped_column(
        Enum(ReviewStatus, name="review_status"),
        default=ReviewStatus.pending_review, index=True,
    )
    origin: Mapped[str] = mapped_column(
        Enum(RecordOrigin, name="record_origin"),
        default=RecordOrigin.aggregated, index=True,
    )
    is_medical_claim: Mapped[bool] = mapped_column(default=False)
    ai_generated_fields: Mapped[list[str]] = mapped_column(default=list)

    # Dedup support
    normalized_name: Mapped[str | None] = mapped_column(
        String(200), index=True, nullable=True
    )
    merged_into_id: Mapped[int | None] = mapped_column(
        ForeignKey("exercises.id"), nullable=True, index=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )

    category: Mapped["ExerciseType"] = relationship(back_populates="exercises")  # noqa: F821
    exercise_muscles: Mapped[list["ExerciseMuscle"]] = relationship(
        back_populates="exercise", cascade="all, delete-orphan"
    )
    body_regions: Mapped[list["ExerciseBodyRegion"]] = relationship(
        back_populates="exercise", cascade="all, delete-orphan"
    )
    joints: Mapped[list["ExerciseJoint"]] = relationship(
        back_populates="exercise", cascade="all, delete-orphan"
    )
    equipment: Mapped[list["ExerciseEquipment"]] = relationship(
        back_populates="exercise", cascade="all, delete-orphan"
    )
    sources: Mapped[list["ExerciseSource"]] = relationship(  # noqa: F821
        back_populates="exercise", cascade="all, delete-orphan"
    )
    references: Mapped[list["ExerciseReference"]] = relationship(
        back_populates="exercise", cascade="all, delete-orphan"
    )
    provenance: Mapped[list["Provenance"]] = relationship(  # noqa: F821
        back_populates="exercise", cascade="all, delete-orphan"
    )
    merged_into: Mapped["Exercise | None"] = relationship(
        remote_side="Exercise.id", foreign_keys=[merged_into_id]
    )

    @property
    def primary_muscles(self) -> list["ExerciseMuscle"]:
        return [em for em in self.exercise_muscles if em.role == ExerciseRole.primary]

    @property
    def is_active(self) -> bool:
        return self.merged_into_id is None and self.review_status != ReviewStatus.rejected


class ExerciseMuscle(Base):
    __tablename__ = "exercise_muscles"
    __table_args__ = (
        UniqueConstraint("exercise_id", "muscle_id", "role", name="uq_ex_muscle_role"),
        Index("ix_ex_muscles_muscle", "muscle_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    exercise_id: Mapped[int] = mapped_column(
        ForeignKey("exercises.id", ondelete="CASCADE"), index=True
    )
    muscle_id: Mapped[int] = mapped_column(ForeignKey("muscles.id"), index=True)
    role: Mapped[ExerciseRole] = mapped_column(
        Enum(ExerciseRole, name="muscle_role"), default=ExerciseRole.primary
    )
    confidence: Mapped[float] = mapped_column(Float, default=0.9)
    origin: Mapped[str] = mapped_column(String(30), default="source_fact")

    exercise: Mapped["Exercise"] = relationship(back_populates="exercise_muscles")
    muscle: Mapped["Muscle"] = relationship()  # noqa: F821


class ExerciseBodyRegion(Base):
    __tablename__ = "exercise_body_regions"
    __table_args__ = (
        UniqueConstraint("exercise_id", "body_region_id", "role", name="uq_ex_region_role"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    exercise_id: Mapped[int] = mapped_column(
        ForeignKey("exercises.id", ondelete="CASCADE"), index=True
    )
    body_region_id: Mapped[int] = mapped_column(ForeignKey("body_regions.id"), index=True)
    role: Mapped[RegionRole] = mapped_column(
        Enum(RegionRole, name="region_role"), default=RegionRole.primary
    )

    exercise: Mapped["Exercise"] = relationship(back_populates="body_regions")
    body_region: Mapped["BodyRegion"] = relationship()  # noqa: F821


class ExerciseJoint(Base):
    __tablename__ = "exercise_joints"
    __table_args__ = (
        UniqueConstraint("exercise_id", "joint_id", name="uq_ex_joint"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    exercise_id: Mapped[int] = mapped_column(
        ForeignKey("exercises.id", ondelete="CASCADE"), index=True
    )
    joint_id: Mapped[int] = mapped_column(ForeignKey("joints.id"), index=True)
    movement: Mapped[str | None] = mapped_column(String(120), nullable=True)

    exercise: Mapped["Exercise"] = relationship(back_populates="joints")
    joint: Mapped["Joint"] = relationship()  # noqa: F821


class ExerciseEquipment(Base):
    __tablename__ = "exercise_equipment"
    __table_args__ = (
        UniqueConstraint("exercise_id", "equipment_id", name="uq_ex_equipment"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    exercise_id: Mapped[int] = mapped_column(
        ForeignKey("exercises.id", ondelete="CASCADE"), index=True
    )
    equipment_id: Mapped[int] = mapped_column(ForeignKey("equipment.id"), index=True)

    exercise: Mapped["Exercise"] = relationship(back_populates="equipment")
    equipment: Mapped["Equipment"] = relationship()  # noqa: F821


class ExerciseVariation(Base):
    """Directed variation/equivalence links between exercises."""
    __tablename__ = "exercise_variations"
    __table_args__ = (
        UniqueConstraint("parent_exercise_id", "variation_exercise_id", name="uq_variation"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    parent_exercise_id: Mapped[int] = mapped_column(
        ForeignKey("exercises.id", ondelete="CASCADE"), index=True
    )
    variation_exercise_id: Mapped[int] = mapped_column(
        ForeignKey("exercises.id", ondelete="CASCADE"), index=True
    )
    variation_type: Mapped[str | None] = mapped_column(String(60), nullable=True)
    note: Mapped[str | None] = mapped_column(Text, nullable=True)

    parent: Mapped["Exercise"] = relationship(foreign_keys=[parent_exercise_id])
    variation: Mapped["Exercise"] = relationship(foreign_keys=[variation_exercise_id])


class ExerciseReference(Base):
    """Curated outbound reference: an authoritative page where this exercise is
    demonstrated (official images/GIFs/videos live there). We link — never
    re-host — source media (DECISIONS.md D7)."""
    __tablename__ = "exercise_references"
    __table_args__ = (
        UniqueConstraint("exercise_id", "url", name="uq_exercise_reference_url"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    exercise_id: Mapped[int] = mapped_column(
        ForeignKey("exercises.id", ondelete="CASCADE"), index=True
    )
    source_id: Mapped[int | None] = mapped_column(
        ForeignKey("sources.id"), nullable=True, index=True
    )
    label: Mapped[str] = mapped_column(String(300))
    url: Mapped[str] = mapped_column(String(800))
    # demonstration = exact page demonstrating this exercise (aggregated docs);
    # program = official exercise program containing it; article = background.
    kind: Mapped[str] = mapped_column(String(30), default="program")
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )

    exercise: Mapped["Exercise"] = relationship(back_populates="references")
    source: Mapped["Source | None"] = relationship()  # noqa: F821
