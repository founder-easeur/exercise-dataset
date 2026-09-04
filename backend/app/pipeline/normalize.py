"""Normalization: ExerciseCandidate -> NormalizedExercise bound to the taxonomy."""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from app.enums import Difficulty, ExerciseRole
from app.pipeline.anatomy_mapper import guess_exercise_type, map_text
from app.pipeline.extract import ExerciseCandidate
from app.services.text import normalize_name, slugify

DIFFICULTY_MAP = {
    "easy": Difficulty.beginner, "beginner": Difficulty.beginner,
    "gentle": Difficulty.beginner, "level 1": Difficulty.beginner,
    "intermediate": Difficulty.intermediate, "moderate": Difficulty.intermediate,
    "level 2": Difficulty.intermediate, "medium": Difficulty.intermediate,
    "advanced": Difficulty.advanced, "hard": Difficulty.advanced,
    "level 3": Difficulty.advanced, "difficult": Difficulty.advanced,
}

POSITION_PATTERNS = [
    (re.compile(r"\bsupine\b|\bly(ing|e) on (your )?back\b|\bon your back\b", re.I), "supine"),
    (re.compile(r"\bprone\b|\bly(ing|e) on (your )?front\b|\bon your stomach\b|\bface down\b", re.I), "prone"),
    (re.compile(r"\bside[- ]lying\b|\blie on your side\b|\bon your side\b", re.I), "side-lying"),
    (re.compile(r"\bquadruped\b|\ball fours\b|\bhands and knees\b", re.I), "quadruped"),
    (re.compile(r"\bkneel", re.I), "kneeling"),
    (re.compile(r"\bsit(ting)?\b|\bseated\b|\bchair\b", re.I), "seated"),
    (re.compile(r"\bstand(ing)?\b", re.I), "standing"),
]

GENERIC_NAME_BLOCKLIST = {
    "stretching exercises", "movement and strengthening exercises",
    "how many and how often", "getting started", "warm up", "related media",
    "purpose of program", "target muscles", "exercises", "strengthening exercises",
    "back to top", "when to seek medical attention",
}

MEDICAL_CLAIM_RE = re.compile(
    r"\b(treats?|cures?|heals?|resolves?|eliminates?|repairs?|prevents? (?:arthritis|disease|injury)|"
    r"therapy for (?:disease|arthritis)|relieves? pain|reduces? pain|eases? pain)\b", re.I,
)


@dataclass
class NormalizedExercise:
    name: str
    slug: str
    normalized_name: str
    aliases: list[str]
    category_slug: str
    difficulty: Difficulty
    position: str | None
    instructions: str
    safety_notes: str | None
    muscles: list[tuple[str, ExerciseRole]] = field(default_factory=list)
    regions: list[str] = field(default_factory=list)
    joints: list[str] = field(default_factory=list)
    equipment: list[str] = field(default_factory=list)
    movement_pattern: str | None = None
    is_medical_claim: bool = False
    confidence: float = 0.5
    extraction_method: str = "page_text"
    unmapped_terms: list[str] = field(default_factory=list)
    source_slug: str = ""
    url: str = ""
    ai_generated_fields: list[str] = field(default_factory=list)


def normalize_candidate(cand: ExerciseCandidate) -> NormalizedExercise | None:
    name = (cand.name or "").strip()
    name = re.sub(r"^\d+\s*[.\):]\s*", "", name)  # strip "1." / "2)" list numbering
    name = re.sub(r"\s+", " ", name).strip(" .:-–—")
    if not name or len(name) < 3 or len(name) > 120:
        return None
    if name.lower().rstrip(":").strip() in GENERIC_NAME_BLOCKLIST:
        return None

    blob_parts = [name] + cand.raw_muscles + cand.raw_regions + cand.raw_equipment + cand.instructions + cand.safety
    mapped = map_text(*blob_parts)

    # --- muscles ---
    roles: list[tuple[str, ExerciseRole]] = []
    for slug in mapped.muscles[:8]:
        roles.append((slug, ExerciseRole.stretch_target if "stretch" in (cand.exercise_type or name.lower()) else ExerciseRole.primary))
    # --- regions: prefer regions implied by mapped muscles (less noisy than text)
    regions: list[str] = []
    from app.taxonomy.anatomy_data import MUSCLES
    by_slug = {m["slug"]: m for m in MUSCLES}
    for slug, _ in roles:
        region = by_slug.get(slug, {}).get("region")
        if region and region not in regions:
            regions.append(region)
    if not regions:
        regions = mapped.regions[:3]
    regions = regions[:3]
    # --- equipment ---
    equipment = mapped.equipment[:5]
    # --- type ---
    type_slug = cand.exercise_type or guess_exercise_type(name, " ".join(cand.instructions))
    if type_slug not in {"stretching", "mobility", "rehabilitation", "physiotherapy", "recovery",
                         "warmup", "cooldown", "posture", "balance", "breathing", "strength", "release"}:
        type_slug = "mobility"
    # --- difficulty ---
    difficulty = Difficulty.beginner
    if cand.difficulty:
        difficulty = DIFFICULTY_MAP.get(cand.difficulty.strip().lower(), Difficulty.beginner)
    # --- position ---
    text_blob = " ".join(cand.instructions)
    position = None
    for rx, label in POSITION_PATTERNS:
        if rx.search(text_blob):
            position = label
            break
    # --- instructions ---
    instructions = "\n".join(f"{i+1}. {s}" for i, s in enumerate(cand.instructions[:10])) if cand.instructions else None
    if not instructions:
        return None  # an exercise without instructions is not reviewable content
    safety = "\n".join(cand.safety[:4]) or None
    is_claim = bool(MEDICAL_CLAIM_RE.search(" ".join(cand.instructions + cand.safety)))

    # Confidence: extraction method confidence, adjusted by mapping success
    from app.pipeline.extract import METHOD_CONFIDENCE
    base = METHOD_CONFIDENCE.get(cand.extraction_method, 0.45)
    bonus = 0.08 if roles else 0.0
    bonus += 0.04 if len(cand.instructions) >= 3 else -0.05
    confidence = min(0.95, max(0.25, base + bonus))

    unmapped = []
    for phrase in cand.raw_muscles:
        if not map_text(phrase).muscles:
            unmapped.append(phrase)

    slug = slugify(name)[:150]
    return NormalizedExercise(
        name=name, slug=slug, normalized_name=normalize_name(name),
        aliases=sorted({a.strip().lower() for a in cand.aliases if a and a.strip().lower() != name.lower()})[:6],
        category_slug=type_slug, difficulty=difficulty, position=position,
        instructions=instructions, safety_notes=safety,
        muscles=roles, regions=regions[:3], joints=mapped.joints[:4],
        equipment=equipment, is_medical_claim=is_claim,
        confidence=round(confidence, 2),
        extraction_method=cand.extraction_method,
        unmapped_terms=unmapped[:8],
        source_slug=cand.source_slug, url=cand.url,
        ai_generated_fields=[],
    )
