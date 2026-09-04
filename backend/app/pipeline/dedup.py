"""Deduplication pipeline.

    exact match -> normalized text -> aliases -> structured similarity
              -> (semantic similarity: deterministic proxy) -> human review

Only near-exact matches (>= duplicate_auto_merge_threshold with compatible
anatomy) are auto-merged; everything else becomes a review-queue duplicate pair.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from difflib import SequenceMatcher

from app.services.text import jaccard, normalize_name


@dataclass
class DuplicateCandidate:
    a_id: int
    b_id: int
    a_name: str
    b_name: str
    score: float
    components: dict
    stage: str                 # exact | normalized | alias | structural
    recommendation: str        # auto_merge | review | keep_separate


def name_similarity(a: str, b: str) -> float:
    na, nb = normalize_name(a), normalize_name(b)
    if na == nb:
        return 1.0
    j = jaccard(set(na.split()), set(nb.split()))
    s = SequenceMatcher(None, na, nb).ratio()
    return round(max(j, s), 3)


def anatomy_overlap(a_muscles: set[str], b_muscles: set[str]) -> float:
    if not a_muscles and not b_muscles:
        return 0.5  # both empty: neutral evidence
    if not a_muscles or not b_muscles:
        return 0.25
    return jaccard(a_muscles, b_muscles)


def region_compatible(a_regions: set[str], b_regions: set[str]) -> bool:
    if not a_regions or not b_regions:
        return True
    return bool(a_regions & b_regions)


def compare_pair(a, b, *, auto_merge_threshold: float = 0.99) -> DuplicateCandidate | None:
    """Compare two exercise-like records. `a`/`b` need attributes:
    id, canonical_name, aliases, muscle_slugs (set), region_slugs (set)."""
    sim = name_similarity(a.canonical_name, b.canonical_name)
    alias_hit = bool(set(x.lower() for x in (a.aliases or [])) &
                     set(x.lower() for x in (b.aliases or [])) |
                     ({a.canonical_name.lower()} & set(x.lower() for x in (b.aliases or []))) |
                     ({b.canonical_name.lower()} & set(x.lower() for x in (a.aliases or []))))
    anat = anatomy_overlap(set(a.muscle_slugs or []), set(b.muscle_slugs or []))
    compat_region = region_compatible(set(a.region_slugs or []), set(b.region_slugs or []))

    stage, score = "normalized", sim
    if alias_hit:
        stage, score = "alias", max(sim, 0.85)
    struct = round(0.55 * sim + 0.45 * anat, 3)
    if struct > score:
        stage, score = "structural", struct

    if not compat_region:
        score = round(score * 0.6, 3)

    recommendation = "keep_separate"
    if score >= auto_merge_threshold and compat_region:
        recommendation = "auto_merge"
    elif score >= 0.72 or (alias_hit and score >= 0.60):
        recommendation = "review"

    if recommendation == "keep_separate":
        return None
    return DuplicateCandidate(
        a_id=a.id, b_id=b.id, a_name=a.canonical_name, b_name=b.canonical_name,
        score=score, stage=stage, recommendation=recommendation,
        components={"name_similarity": sim, "alias_match": alias_hit,
                    "muscle_overlap": anat, "regions_compatible": compat_region,
                    "structural_similarity": struct},
    )


def find_duplicate_pairs(records: list, *, auto_merge_threshold: float = 0.99,
                         existing_pairs: set[tuple[int, int]] | None = None) -> list[DuplicateCandidate]:
    """All-pairs scan (dataset is small; O(n^2) with n<10k is fine and simple)."""
    existing_pairs = existing_pairs or set()
    out: list[DuplicateCandidate] = []
    recs = sorted(records, key=lambda r: r.id)
    for i, a in enumerate(recs):
        if getattr(a, "merged_into_id", None):
            continue
        for b in recs[i + 1:]:
            if getattr(b, "merged_into_id", None):
                continue
            key = (min(a.id, b.id), max(a.id, b.id))
            if key in existing_pairs:
                continue
            cand = compare_pair(a, b, auto_merge_threshold=auto_merge_threshold)
            if cand:
                out.append(cand)
    return out
