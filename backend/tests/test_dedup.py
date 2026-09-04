"""Deduplication tests: exact, alias, similar-but-different, uncertain."""
from __future__ import annotations

from dataclasses import dataclass, field

from app.pipeline.dedup import compare_pair, find_duplicate_pairs, name_similarity
from app.services.text import normalize_name


@dataclass
class Rec:
    id: int
    canonical_name: str
    aliases: list = field(default_factory=list)
    muscle_slugs: set = field(default_factory=set)
    region_slugs: set = field(default_factory=set)
    category_slug: str | None = None
    merged_into_id: int | None = None


def test_exact_duplicate_automerge():
    a = Rec(1, "Neck Rotation", muscle_slugs={"splenius-capitis"}, region_slugs={"neck"})
    b = Rec(2, "Neck Rotation", muscle_slugs={"splenius-capitis"}, region_slugs={"neck"})
    pair = compare_pair(a, b)
    assert pair is not None
    assert pair.recommendation == "auto_merge"
    assert pair.score >= 0.99


def test_plural_and_synonym_normalized():
    assert normalize_name("Neck Rotations") == normalize_name("Neck Rotation")
    assert normalize_name("Cervical Rotation Stretch") == "cervical rotation"
    assert normalize_name("Neck Turn Exercise") == "neck turn"


def test_spec_example_family_is_detected():
    a = Rec(1, "Neck Rotation", muscle_slugs={"splenius-capitis"}, region_slugs={"neck"})
    b = Rec(2, "Cervical Spine Rotation",
            muscle_slugs={"splenius-capitis"}, region_slugs={"neck"})
    pair = compare_pair(a, b)
    assert pair is not None and pair.recommendation in ("review", "auto_merge")


def test_alias_duplicate_detected():
    a = Rec(1, "Chin Tuck", aliases=["head retraction"], muscle_slugs={"deep-neck-flexors"})
    b = Rec(2, "Head Retraction", muscle_slugs={"deep-neck-flexors"})
    pair = compare_pair(a, b)
    assert pair is not None and pair.stage == "alias"
    assert pair.recommendation in ("review", "auto_merge")


def test_different_exercises_similar_names_low_score():
    a = Rec(1, "Resistance Band Ankle Eversion",
            muscle_slugs={"peroneus-longus"}, region_slugs={"ankle"})
    b = Rec(2, "Resistance Band Ankle Inversion",
            muscle_slugs={"tibialis-posterior"}, region_slugs={"ankle"})
    pair = compare_pair(a, b)
    # eversion vs inversion: high name similarity but conflicting anatomy
    if pair is not None:
        assert pair.recommendation != "auto_merge"
    else:
        assert name_similarity(a.canonical_name, b.canonical_name) < 0.72


def test_uncertain_match_not_automerged():
    a = Rec(1, "External Rotation", muscle_slugs={"infraspinatus"}, region_slugs={"shoulder"})
    b = Rec(2, "External Rotation with Arm Abducted",
            muscle_slugs={"infraspinatus", "teres-minor"}, region_slugs={"shoulder"})
    pair = compare_pair(a, b)
    assert pair is None or pair.recommendation in ("review", "keep_separate")
    assert pair is None or pair.recommendation != "auto_merge"


def test_incompatible_regions_reduce_score():
    a = Rec(1, "Circles", muscle_slugs={}, region_slugs={"wrist"})
    b = Rec(2, "Ankle Circles", muscle_slugs={}, region_slugs={"ankle"})
    pair = compare_pair(a, b)
    if pair is not None:
        assert pair.score < 0.7


def test_find_duplicate_pairs_dedupes_existing():
    recs = [Rec(1, "Neck Rotation", muscle_slugs={"x"}, region_slugs={"neck"}),
            Rec(2, "Neck Rotation", muscle_slugs={"x"}, region_slugs={"neck"}),
            Rec(3, "Deep Squat", muscle_slugs={"glutes"}, region_slugs={"hip"})]
    pairs = find_duplicate_pairs(recs, existing_pairs={(1, 2)})
    assert all((p.a_id, p.b_id) != (1, 2) for p in pairs)
