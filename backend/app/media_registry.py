"""Exercise illustration registry.

Media policy (DECISIONS.md D7): we do not reuse copyrighted photos/GIFs from
crawled sources. Illustrations shipped with the project are AI-generated for
this project (no third-party rights), tracked with license metadata like any
other asset. The registry maps exercises to assets by body region and exercise
type; every exercise resolves to at least one asset or falls back to the
client-side animated pose diagram (rendered from structured data, not a file).

Source-licensed media (when a source explicitly permits reuse) should be
recorded in a media_assets table in a future version — the serializer contract
below is shaped so those can be added without breaking consumers.
"""
from __future__ import annotations

from pathlib import Path

MEDIA_DIR = Path(__file__).resolve().parent.parent / "media" / "exercises"

#: Per-region illustration files (region slug -> filename).
REGION_ILLUSTRATIONS: dict[str, str] = {
    "neck": "neck.png",
    "jaw": "jaw.png",
    "shoulder": "shoulder.png",
    "chest": "chest.png",
    "upper-back": "upper-back.png",
    "lower-back": "lower-back.png",
    "elbow": "elbow-forearm.png",
    "forearm": "elbow-forearm.png",
    "wrist": "wrist-hand.png",
    "hand": "wrist-hand.png",
    "hip": "hip.png",
    "knee": "knee.png",
    "calf": "ankle-foot.png",
    "ankle": "ankle-foot.png",
    "foot": "ankle-foot.png",
    "whole-body": "whole-body.png",
}

#: Region+type overrides (checked before the region default).
SPECIAL_ILLUSTRATIONS: dict[tuple[str, str], str] = {
    ("shoulder", "rehabilitation"): "rotator-cuff.png",
    ("shoulder", "strengthening"): "rotator-cuff.png",
}

_LICENSE = {
    "kind": "illustration",
    "license": "ai-generated",
    "credit": "AI-generated illustration created for the Easeur Exercise Knowledge Base (no third-party rights)",
    "origin": "generated",
}


def resolve_media(ex) -> list[dict]:
    """Return the media asset list for an Exercise ORM object.

    Deterministic: picks the first body region that has an illustration,
    preferring region+type overrides. ``url`` is served by the API under
    /static/exercises/ (frontend proxies the same path).
    """
    regions: list[str] = []
    try:
        regions = [r.body_region.slug for r in ex.body_regions]
    except Exception:
        regions = []
    category = ex.category.slug if ex.category else None

    filename = None
    for region in regions:
        if category and (region, category) in SPECIAL_ILLUSTRATIONS:
            filename = SPECIAL_ILLUSTRATIONS[(region, category)]
            break
    if filename is None:
        for region in regions:
            if region in REGION_ILLUSTRATIONS:
                filename = REGION_ILLUSTRATIONS[region]
                break
    if filename is None:
        return []  # client renders the data-driven pose diagram only

    return [{
        **_LICENSE,
        "url": f"/static/exercises/{filename}",
        "file": filename,
        "region": region,
    }]


def registry_health() -> dict:
    """Registry self-check: which mapped files exist on disk."""
    files = set(REGION_ILLUSTRATIONS.values()) | set(SPECIAL_ILLUSTRATIONS.values())
    return {
        "assets": sorted(files),
        "missing_on_disk": sorted(f for f in files if not (MEDIA_DIR / f).exists()),
        "regions_covered": sorted(REGION_ILLUSTRATIONS.keys()),
    }
