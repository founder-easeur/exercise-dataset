"""Aggregate all curated exercise modules into one dataset."""
from __future__ import annotations

from app.seed.curated.arm import ARM_EXERCISES
from app.seed.curated.general import GENERAL_EXERCISES
from app.seed.curated.hip_knee import HIP_KNEE_EXERCISES
from app.seed.curated.lower_leg_foot import LOWER_LEG_FOOT_EXERCISES
from app.seed.curated.neck_shoulder import NECK_SHOULDER_EXERCISES
from app.seed.curated.torso import TORSO_EXERCISES

ALL_CURATED_EXERCISES: list[dict] = (
    NECK_SHOULDER_EXERCISES
    + ARM_EXERCISES
    + TORSO_EXERCISES
    + HIP_KNEE_EXERCISES
    + LOWER_LEG_FOOT_EXERCISES
    + GENERAL_EXERCISES
)
