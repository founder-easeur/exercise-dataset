"""Deterministic anatomy mapping: free text -> taxonomy references.

This is the default classification/enrichment engine. It is fully
deterministic (no LLM): every match is traceable to a taxonomy alias. When an
LLM key is configured, `app.pipeline.ai` may enrich what this mapper cannot —
but always with ai_inference provenance and review status.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from functools import lru_cache

# word-boundary-safe alias -> slug
import app.taxonomy.anatomy_data as anatomy_data
import app.taxonomy.reference_data as reference_data


@dataclass
class AnatomyIndex:
    muscles: dict[str, str]          # alias(lower) -> muscle slug
    regions: dict[str, str]
    joints: dict[str, str]
    equipment: dict[str, str]
    types: dict[str, str]


@lru_cache(maxsize=1)
def build_index() -> AnatomyIndex:
    def add(target: dict, slug: str, name: str, aliases) -> None:
        target[re.sub(r"\s+", " ", name.lower()).strip()] = slug
        for a in aliases or []:
            target[re.sub(r"\s+", " ", a.lower()).strip()] = slug

    idx = AnatomyIndex(muscles={}, regions={}, joints={}, equipment={}, types={})
    for m in anatomy_data.MUSCLES:
        add(idx.muscles, m["slug"], m["name"], m.get("aliases"))
    for g in anatomy_data.MUSCLE_GROUPS:
        add(idx.muscles, g["slug"], g["name"], None)
    for r in anatomy_data.BODY_REGIONS:
        add(idx.regions, r["slug"], r["name"], None)
    for j in reference_data.JOINTS:
        add(idx.joints, j["slug"], j["name"], j.get("aliases"))
    for e in reference_data.EQUIPMENT:
        add(idx.equipment, e["slug"], e["name"], e.get("aliases"))
    for t in reference_data.EXERCISE_TYPES:
        add(idx.types, t["slug"], t["name"], None)
    # Extra domain synonyms (curated by the team)
    idx.muscles.update({
        "glute med": "gluteus-medius", "glutes": "gluteus-maximus",
        "hamstring": "biceps-femoris", "hamstrings": "biceps-femoris",
        "quadricep": "rectus-femoris", "quads": "rectus-femoris",
        "calves": "gastrocnemius", "calf": "soleus", "calf muscle": "gastrocnemius",
        "it band": "iliotibial-band", "itband": "iliotibial-band",
        "rotator cuff": "supraspinatus", "rotator cuff muscles": "supraspinatus",
        "deltoid": "deltoid-lateral", "delts": "deltoid-lateral",
        "traps": "upper-trapezius", "trapezius": "upper-trapezius",
        "abs": "rectus-abdominis", "core": "transversus-abdominis",
        "hip flexor": "iliopsoas", "hip flexors": "iliopsoas",
        "psoas": "iliopsoas", "adductor": "adductor-longus", "adductors": "adductor-longus",
        "tibialis anterior muscle": "tibialis-anterior", "shin muscle": "tibialis-anterior",
        "wrist flexors": "flexor-carpi-radialis", "wrist extensors": "extensor-carpi-radialis",
        "forearm flexors": "flexor-carpi-radialis", "forearm extensors": "extensor-carpi-radialis",
        "deep neck flexor": "deep-neck-flexors", "neck flexors": "deep-neck-flexors",
        "suboccipital": "suboccipitals", "scalene": "scalenes",
        "tfl": "tensor-fasciae-latae", "ql": "quadratus-lumborum",
        "scm": "sternocleidomastoid", "levator": "levator-scapulae",
        "pecs": "pectoralis-major", "pec": "pectoralis-major",
        "lats": "latissimus-dorsi", "vmo": "vastus-medialis",
        "peroneals": "peroneus-longus", "peroneus": "peroneus-longus",
        "fibularis": "peroneus-longus", "posterior tibialis": "tibialis-posterior",
        "tibialis posterior muscle": "tibialis-posterior",
        "intrinsic foot muscles": "abductor-hallucis", "foot intrinsics": "abductor-hallucis",
        "plantar aponeurosis": "plantar-fascia",
        "achilles": "achilles-tendon", "achilles tendon": "achilles-tendon",
    })
    idx.regions.update({
        "cervical": "neck", "cervicals": "neck", "thoracic": "upper-back",
        "lumbar": "lower-back", "low back": "lower-back", "t-spine": "upper-back",
        "scapular": "shoulder", "shoulder blade": "shoulder", "gluteal": "hip",
        "buttock": "hip", "buttocks": "hip", "pelvis": "hip", "groin": "hip",
        "carpal": "wrist", "tmc": "hand", "digits": "hand", "fingers": "hand",
        "lower leg": "calf", "shin": "calf", "hindfoot": "ankle", "rearfoot": "ankle",
        "plantar": "foot", "toes": "foot", "tspine": "upper-back",
    })
    idx.equipment.update({
        "no equipment": "bodyweight", "none": "bodyweight", "band": "resistance-band",
        "thera-band": "resistance-band", "therapy band": "resistance-band",
        "exercise band": "resistance-band", "elastic band": "resistance-band",
        "roller": "foam-roller", "foamroller": "foam-roller", "tennis ball": "massage-ball",
        "ball": "massage-ball", "lacrosse ball": "massage-ball", "golf ball": "massage-ball",
        "broomstick": "stick", "cane": "stick", "towel roll": "towel",
        "weight": "dumbbell", "dumbbells": "dumbbell", "hand weights": "dumbbell",
        "swiss ball": "stability-ball", "physioball": "stability-ball",
        "block": "yoga-block", "door frame": "doorway", "doorjamb": "doorway",
        "stairs": "step", "curb": "step", "countertop": "table", "desk": "table",
    })
    idx.types.update({
        "stretch": "stretching", "static stretch": "stretching",
        "flexibility": "stretching", "rom": "mobility", "range of motion": "mobility",
        "strengthening": "strength", "strengthen": "strength", "activation": "strength",
        "smr": "release", "self myofascial release": "release",
        "self-myofascial release": "release", "mobilisation": "mobility",
        "mobilization": "mobility", "warm-up": "warmup", "warm up": "warmup",
        "cool-down": "cooldown", "cool down": "cooldown", "theraband exercise": "physiotherapy",
        "nerve glide": "rehabilitation", "nerve floss": "rehabilitation",
        "balance exercise": "balance", "proprioception": "balance",
        "postural": "posture", "breathing exercise": "breathing",
    })
    return idx


@dataclass
class MatchResult:
    muscles: list[str] = field(default_factory=list)
    regions: list[str] = field(default_factory=list)
    joints: list[str] = field(default_factory=list)
    equipment: list[str] = field(default_factory=list)
    types: list[str] = field(default_factory=list)


def _scan(text: str, table: dict[str, str]) -> list[str]:
    """Longest-alias-first scan with word boundaries. Returns unique slugs, ordered."""
    if not text:
        return []
    hay = " " + re.sub(r"[^a-z0-9]+", " ", text.lower()) + " "
    hits: list[tuple[int, str]] = []
    for alias, slug in table.items():
        needle = " " + re.sub(r"[^a-z0-9]+", " ", alias) + " "
        if needle in hay:
            hits.append((-len(alias), slug))
    out: list[str] = []
    seen: set[str] = set()
    for _, slug in sorted(hits):
        if slug not in seen:
            seen.add(slug)
            out.append(slug)
    return out


def map_text(*texts: str | None) -> MatchResult:
    """Map arbitrary text to taxonomy references using the deterministic index."""
    idx = build_index()
    blob = "\n".join(t for t in texts if t)
    return MatchResult(
        muscles=_scan(blob, idx.muscles),
        regions=_scan(blob, idx.regions),
        joints=_scan(blob, idx.joints),
        equipment=_scan(blob, idx.equipment),
        types=_scan(blob, idx.types),
    )


def map_muscle_phrase(phrase: str) -> list[str]:
    """Map a phrase like 'wrist extensors' or 'Infraspinatus, teres minor'."""
    return map_text(phrase).muscles


def guess_exercise_type(name: str, text: str | None) -> str | None:
    m = map_text(name, *( [text] if text else [] ))
    if m.types:
        return m.types[0]
    low = (name or "").lower()
    if "stretch" in low or "flexibility" in low:
        return "stretching"
    if "glide" in low or "mobil" in low or "circle" in low or "rotation" in low:
        return "mobility"
    if "balance" in low:
        return "balance"
    if "breath" in low:
        return "breathing"
    return None
