"""Text normalisation helpers shared by seeder, extractor and dedup."""
from __future__ import annotations

import re
import unicodedata

_STOPWORDS = {
    "exercise", "exercises", "stretch", "stretches", "stretching", "the", "a", "an",
    "with", "for", "and", "of", "your", "side", "both", "sides", "left", "right",
}

_SINGULARS = {
    "rotations": "rotation", "circles": "circle", "turns": "turn", "raises": "raise",
    "curls": "curl", "extensions": "extension", "drops": "drop", "swings": "swing",
    "slides": "slide", "squeezes": "squeeze", "pushups": "pushup", "push": "push",
    "marches": "march", "lifts": "lift", "bends": "bend", "twists": "twist",
    "glides": "glide", "holds": "hold", "rolls": "roll", "drills": "drill",
}


def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()
    return value or "unnamed"


def normalize_name(name: str) -> str:
    """Canonical form for name comparison (dedup stage 2)."""
    name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii").lower()
    name = re.sub(r"[^a-z0-9\s]", " ", name)
    tokens = [t for t in name.split() if t]
    tokens = [_SINGULARS.get(t, t) for t in tokens]
    tokens = [t for t in tokens if t not in _STOPWORDS]
    return " ".join(tokens)


def name_tokens(name: str) -> set[str]:
    return set(normalize_name(name).split())


def jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def truncate(text: str | None, limit: int = 1200) -> str | None:
    if text is None:
        return None
    text = text.strip()
    if len(text) <= limit:
        return text
    return text[:limit].rsplit(" ", 1)[0] + " …"


def strip_html(html: str) -> str:
    """Very small, safe HTML->text fallback. BeautifulSoup is the primary path."""
    html = re.sub(r"(?is)<(script|style|noscript)[^>]*>.*?</\1>", " ", html)
    html = re.sub(r"(?s)<!--.*?-->", " ", html)
    html = re.sub(r"(?s)<br\s*/?>", "\n", html)
    html = re.sub(r"(?s)</p>", "\n\n", html)
    text = re.sub(r"(?s)<[^>]+>", " ", html)
    text = text.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    text = text.replace("&nbsp;", " ").replace("&quot;", '"').replace("&#39;", "'")
    return re.sub(r"[ \t]+", " ", text).strip()
