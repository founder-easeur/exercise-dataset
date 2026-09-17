"""Autonomous research query generation from the taxonomy.

Generates high-quality search queries by combining body regions, muscles,
joints and exercise-type contexts — prioritising the small/overlooked
structures this project exists to cover.
"""
from __future__ import annotations

from itertools import product

REGION_TERMS = {
    "neck": ["neck", "cervical", "cervical spine"],
    "jaw": ["jaw", "temporomandibular", "TMJ"],
    "shoulder": ["shoulder", "scapular", "rotator cuff"],
    "upper-back": ["upper back", "thoracic"],
    "chest": ["chest", "pectoral"],
    "lower-back": ["lower back", "lumbar", "low back"],
    "elbow": ["elbow"],
    "forearm": ["forearm"],
    "wrist": ["wrist", "carpal"],
    "hand": ["hand", "finger", "thumb"],
    "hip": ["hip", "deep hip", "pelvis"],
    "knee": ["knee", "patellofemoral"],
    "calf": ["calf", "lower leg", "shin"],
    "ankle": ["ankle", "hindfoot"],
    "foot": ["foot", "plantar", "toe"],
}

CONTEXT_TERMS = [
    "stretch", "stretching exercises", "mobility exercises", "range of motion exercises",
    "physiotherapy exercises", "rehabilitation exercises", "strengthening exercises",
    "exercises for pain", "warm up", "cool down",
]

# Extra targeted queries for clinically-important small structures.
STRUCTURE_QUERIES = [
    "levator scapulae stretch",
    "scalene stretch",
    "suboccipital release",
    "deep neck flexor strengthening",
    "chin tuck exercise",
    "serratus anterior activation",
    "lower trapezius exercise",
    "rotator cuff internal rotation band",
    "rotator cuff external rotation band",
    "sleeper stretch",
    "cross body shoulder stretch",
    "wrist extensor stretch tennis elbow",
    "eccentric wrist extension",
    "de Quervain stretch",
    "median nerve glide",
    "ulnar nerve glide",
    "radial nerve glide",
    "piriformis stretch",
    "hip flexor stretch",
    "90 90 hip stretch",
    "gluteus medius strengthening",
    "iliopsoas stretch",
    "popliteus stretch",
    "VMO strengthening",
    "terminal knee extension",
    "soleus stretch",
    "eccentric heel drop achilles",
    "tibialis posterior strengthening",
    "peroneal tendon exercises",
    "ankle dorsiflexion mobility",
    "plantar fascia stretch",
    "short foot exercise",
    "toe yoga",
    "big toe mobility",
    "diaphragmatic breathing",
    "pelvic floor activation",
    "scapular retraction exercise",
    "thoracic rotation mobility",
    "tmj jaw exercises",
    "carpal tunnel stretching",
]


def generate_queries(muscles: list[dict], limit: int = 400) -> list[dict]:
    """Generate research queries, prioritising small/overlooked structures.

    Each item: {query, muscle_slug?, region_slug?, context}
    """
    queries: list[dict] = []

    # 1. Structure-targeted queries (highest value).
    for m in sorted(muscles, key=lambda x: (not x.get("is_small_overlooked"), x["name"])):
        for ctx in ("stretch", "stretching exercises", "mobility exercises",
                    "rehabilitation exercises", "physiotherapy exercises"):
            queries.append({
                "query": f"{m['name'].lower()} {ctx}",
                "muscle_slug": m["slug"],
                "region_slug": m.get("region"),
                "context": ctx,
            })

    # 2. Region x context queries.
    for region_slug, terms in REGION_TERMS.items():
        for term, ctx in product(terms, CONTEXT_TERMS):
            queries.append({
                "query": f"{term} {ctx}",
                "muscle_slug": None,
                "region_slug": region_slug,
                "context": ctx,
            })

    # 3. Curated structure-specific classics.
    for q in STRUCTURE_QUERIES:
        queries.append({"query": q, "muscle_slug": None, "region_slug": None,
                        "context": "curated-targeted"})

    # De-duplicate while keeping priority order (small structures first).
    seen: set[str] = set()
    out: list[dict] = []
    for q in queries:
        key = q["query"].strip().lower()
        if key not in seen:
            seen.add(key)
            out.append(q)
    return out[:limit]
