"""Anatomy taxonomy + equipment / exercise-type reference tables."""
from __future__ import annotations

from sqlalchemy import Boolean, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base
from app.enums import StructureType


class BodyRegion(Base):
    __tablename__ = "body_regions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    slug: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(120))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    muscle_groups: Mapped[list["MuscleGroup"]] = relationship(back_populates="body_region")
    muscles: Mapped[list["Muscle"]] = relationship(back_populates="body_region")
    joints: Mapped[list["Joint"]] = relationship(back_populates="body_region")


class MuscleGroup(Base):
    __tablename__ = "muscle_groups"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    slug: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(120))
    body_region_id: Mapped[int] = mapped_column(ForeignKey("body_regions.id"), index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    # A group may itself be a clinically-meaningful unit (e.g. "rotator cuff")
    is_clinical_unit: Mapped[bool] = mapped_column(Boolean, default=False)

    body_region: Mapped["BodyRegion"] = relationship(back_populates="muscle_groups")
    muscles: Mapped[list["Muscle"]] = relationship(back_populates="muscle_group")


class Muscle(Base):
    """An anatomical structure target. `structure_type` distinguishes real muscles
    from tendons/ligaments/fascia/nerves so we never mislabel anatomy."""
    __tablename__ = "muscles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(160))
    latin_name: Mapped[str | None] = mapped_column(String(160), nullable=True)
    structure_type: Mapped[str] = mapped_column(
        String(30), default=StructureType.muscle.value, index=True
    )
    muscle_group_id: Mapped[int | None] = mapped_column(
        ForeignKey("muscle_groups.id"), index=True, nullable=True
    )
    body_region_id: Mapped[int | None] = mapped_column(
        ForeignKey("body_regions.id"), index=True, nullable=True
    )
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    # Flag for the project's focus: small / commonly-overlooked structures
    is_small_overlooked: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    search_aliases: Mapped[list[str]] = mapped_column(default=list)

    muscle_group: Mapped["MuscleGroup | None"] = relationship(back_populates="muscles")
    body_region: Mapped["BodyRegion | None"] = relationship(back_populates="muscles")


class Joint(Base):
    __tablename__ = "joints"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    slug: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(120))
    joint_type: Mapped[str | None] = mapped_column(String(60), nullable=True)
    body_region_id: Mapped[int | None] = mapped_column(
        ForeignKey("body_regions.id"), index=True, nullable=True
    )
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    search_aliases: Mapped[list[str]] = mapped_column(default=list)

    body_region: Mapped["BodyRegion | None"] = relationship(back_populates="joints")


class Equipment(Base):
    __tablename__ = "equipment"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    slug: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(120))


class ExerciseType(Base):
    """Extensible exercise category/type taxonomy (stretching, mobility, ...)."""
    __tablename__ = "exercise_types"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    slug: Mapped[str] = mapped_column(String(60), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(120))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    exercises: Mapped[list["Exercise"]] = relationship(  # noqa: F821
        back_populates="category"
    )

