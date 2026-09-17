"""Exercise candidate extraction.

Extraction order (deterministic first):
    JSON-LD -> structured HTML -> tables -> semantic HTML -> page text -> AI (fallback)

Returns ExerciseCandidate objects with an `extraction_method` so provenance can
distinguish how each field was obtained. Text stored from sources is bounded and
sanitised — we keep structured facts, not full copyrighted articles.
"""
from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass, field

from bs4 import BeautifulSoup

from app.services.text import strip_html, truncate

log = logging.getLogger("easeur.extract")

EXERCISE_NAME_RE = re.compile(
    r"(stretch|exercise|mobili[sz]ation|rotation|flexion|extension|raise|curl|"
    r"glide|circle|tilt|tuck|bridge|pose|breathing|squeeze|march|swing|slide|"
    r"release|traction|hang|sit|squat|lunge|twist|bend|walk|pickup|scrunch|"
    r"balance|push|pull|drop|hop)", re.I,
)

INSTRUCTION_HINTS = re.compile(r"(step|instruction|how to|direction|follow|technique|to do)", re.I)
SAFETY_HINTS = re.compile(
    r"(stop|pain|hurt|discomfort|dizzy|caution|careful|safe|avoid|do not|don't|"
    r"warning|doctor|clinician|therapist|medical)", re.I,
)
MIN_SECTION_WORDS = 8

# methods ranked by trust
METHOD_CONFIDENCE = {
    "jsonld": 0.90, "structured_html": 0.80, "table": 0.72,
    "semantic_html": 0.62, "page_text": 0.45, "ai": 0.40,
}


@dataclass
class ExerciseCandidate:
    name: str
    url: str
    source_slug: str
    extraction_method: str = "page_text"
    confidence: float = 0.45
    aliases: list[str] = field(default_factory=list)
    raw_muscles: list[str] = field(default_factory=list)      # phrases pre-mapping
    raw_regions: list[str] = field(default_factory=list)
    raw_equipment: list[str] = field(default_factory=list)
    exercise_type: str | None = None
    difficulty: str | None = None
    instructions: list[str] = field(default_factory=list)
    safety: list[str] = field(default_factory=list)
    extra: dict = field(default_factory=dict)


def _clean(s: str | None) -> str | None:
    if not s:
        return None
    s = re.sub(r"\s+", " ", s).strip()
    return s or None


def parse_markdown(md: str) -> BeautifulSoup:
    """Replay mode: corpus pages are markdown; render to HTML for uniform parsing."""
    from markdown_it import MarkdownIt
    html = MarkdownIt("commonmark").render(md)
    return BeautifulSoup(html, "html.parser")


def parse_html(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, "html.parser")


def page_title(soup: BeautifulSoup) -> str | None:
    if soup.title and soup.title.get_text(strip=True):
        return _clean(soup.title.get_text())
    h1 = soup.find("h1")
    return _clean(h1.get_text()) if h1 else None


# ---------------------------------------------------------------- 1. JSON-LD
def extract_jsonld(soup: BeautifulSoup, url: str, source_slug: str) -> list[ExerciseCandidate]:
    out: list[ExerciseCandidate] = []
    for tag in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(tag.string or "")
        except (json.JSONDecodeError, TypeError):
            continue
        items = data if isinstance(data, list) else [data]
        for item in items:
            if not isinstance(item, dict):
                continue
            graph = item.get("@graph")
            for node in ([item] + graph if graph else [item]):
                if not isinstance(node, dict):
                    continue
                types = node.get("@type", "")
                types = types if isinstance(types, list) else [types]
                tset = {str(t).lower() for t in types}
                if not ({"exerciseaction", "exercise", "howto", "physicalactivity",
                         "physicalactivitycategory"} & tset):
                    continue
                name = _clean(node.get("name") or node.get("headline"))
                if not name:
                    continue
                howto = node.get("step") or node.get("supply") or []
                steps: list[str] = []
                if isinstance(howto, list):
                    for st in howto:
                        if isinstance(st, dict):
                            steps.append(_clean(st.get("text") or st.get("name") or ""))
                        else:
                            steps.append(_clean(str(st)))
                muscles = node.get("target", [])
                if isinstance(muscles, str):
                    muscles = [muscles]
                out.append(ExerciseCandidate(
                    name=name, url=url, source_slug=source_slug,
                    extraction_method="jsonld",
                    confidence=METHOD_CONFIDENCE["jsonld"],
                    raw_muscles=[_clean(str(m)) for m in muscles or [] if _clean(str(m))],
                    instructions=[s for s in steps if s],
                ))
    return out


# ------------------------------------------------------- 2/4. HTML structure
def _sectionize(soup: BeautifulSoup) -> list[tuple[str, list[str]]]:
    """Split page into (heading, [paragraph/list text]) sections."""
    sections: list[tuple[str, list[str]]] = []
    current_name: str | None = None
    current: list[str] = []

    def flush() -> None:
        nonlocal current, current_name
        if current_name and current:
            sections.append((current_name, current))
        current, current_name = [], None

    for el in soup.find_all(["h1", "h2", "h3", "h4", "p", "ul", "ol", "li", "table"]):
        if el.name in ("h1", "h2", "h3", "h4"):
            level = int(el.name[1])
            text = _clean(el.get_text()) or ""
            text = re.sub(r"^\d+\s*[.\):]\s*", "", text)  # "3. Heel Cord Stretch" -> "Heel Cord Stretch"
            if level <= 2 and current_name is not None:
                flush()
            if text:
                current_name = text
            continue
        if el.name == "li" and el.find(["ul", "ol"]):
            continue  # nested list handled at parent level
        if el.name in ("ul", "ol") and el.parent and el.parent.name == "li":
            continue
        text = _clean(el.get_text(" ", strip=True))
        if text:
            current.append(text)
    flush()
    return sections


def _looks_like_exercise_heading(heading: str) -> bool:
    if not heading or len(heading) > 120 or len(heading) < 4:
        return False
    if EXERCISE_NAME_RE.search(heading):
        return True
    return False


def _extract_fielded_section(lines: list[str]) -> dict[str, list[str]]:
    """Pull 'Main muscles targeted: X' / 'Equipment needed: Y' style lines."""
    fields: dict[str, list[str]] = {}
    key_map = [
        (re.compile(r"main muscles?\s*targeted|muscles?\s*worked|targets?\s*the", re.I), "muscles"),
        (re.compile(r"you should feel", re.I), "feel"),
        (re.compile(r"equipment\s*needed|equipment:", re.I), "equipment"),
        (re.compile(r"level\s*of\s*difficulty|difficulty", re.I), "difficulty"),
        (re.compile(r"steps\s*to\s*follow|how\s*to\s*do\s*it|instructions?\s*[:\s]?$", re.I), "steps_start"),
    ]
    for line in lines:
        for rx, key in key_map:
            m = rx.search(line)
            if m:
                tail = _clean(line[m.end():].lstrip(" :-–—"))
                if tail:
                    fields.setdefault(key, []).append(tail)
                break
    return fields


def extract_structured(soup: BeautifulSoup, url: str, source_slug: str,
                       method: str = "structured_html") -> list[ExerciseCandidate]:
    """Headed sections that look like exercises, with fielded metadata."""
    out: list[ExerciseCandidate] = []
    for heading, lines in _sectionize(soup):
        if not _looks_like_exercise_heading(heading):
            continue
        body_words = sum(len(l.split()) for l in lines)
        if body_words < MIN_SECTION_WORDS:
            continue
        fields = _extract_fielded_section(lines)
        raw_muscles = list(fields.get("muscles", [])) + list(fields.get("feel", []))
        # instruction-like lines: long-ish lines or list steps after "steps" hint
        instructions = [l for l in lines
                        if len(l.split()) >= 5 and l not in raw_muscles
                        and not re.match(r"(you should feel|equipment|level of difficulty)", l, re.I)]
        safety = [l for l in lines if SAFETY_HINTS.search(l) and l not in instructions[:1]]
        cand = ExerciseCandidate(
            name=heading, url=url, source_slug=source_slug,
            extraction_method=method, confidence=METHOD_CONFIDENCE[method],
            raw_muscles=raw_muscles, raw_equipment=fields.get("equipment", []),
            difficulty=_clean(fields["difficulty"][0]) if fields.get("difficulty") else None,
            instructions=[truncate(t, 300) for t in instructions[:10]],
            safety=[truncate(t, 300) for t in safety[:4]],
        )
        if fields.get("feel"):
            cand.extra["feel"] = fields["feel"]
        out.append(cand)
    return out


# --------------------------------------------------------------- 3. tables
def extract_tables(soup: BeautifulSoup, url: str, source_slug: str) -> list[ExerciseCandidate]:
    out: list[ExerciseCandidate] = []
    for table in soup.find_all("table"):
        headers = [_clean(th.get_text()) for th in table.find_all("th")]
        if not headers or not any(h and EXERCISE_NAME_RE.search(h) for h in headers):
            continue
        name_idx = next((i for i, h in enumerate(headers) if h and re.search(r"exercise|name|stretch", h, re.I)), None)
        if name_idx is None:
            continue
        for row in table.find_all("tr"):
            cells = [_clean(td.get_text(" ", strip=True)) for td in row.find_all("td")]
            if len(cells) <= name_idx or not cells[name_idx]:
                continue
            cand = ExerciseCandidate(
                name=cells[name_idx], url=url, source_slug=source_slug,
                extraction_method="table", confidence=METHOD_CONFIDENCE["table"],
            )
            for i, h in enumerate(headers):
                if not h or i >= len(cells) or not cells[i]:
                    continue
                if re.search(r"muscle|target", h, re.I):
                    cand.raw_muscles.append(cells[i])
                elif re.search(r"equipment", h, re.I):
                    cand.raw_equipment.append(cells[i])
                elif re.search(r"how|step|instruct|rep", h, re.I):
                    cand.instructions.append(truncate(cells[i], 300))
            if cand.instructions or cand.raw_muscles:
                out.append(cand)
    return out


# ---------------------------------------------------------- 5. plain text
def extract_text_fallback(text: str, url: str, source_slug: str) -> list[ExerciseCandidate]:
    """Last deterministic resort: pull exercise-name-like sentences with nearby steps."""
    out: list[ExerciseCandidate] = []
    lines = [l.strip() for l in re.split(r"[\n\r]+", text) if l.strip()]
    for i, line in enumerate(lines):
        line_n = _clean(line) or ""
        if 5 <= len(line_n) <= 110 and EXERCISE_NAME_RE.search(line_n):
            follow = [l for l in lines[i + 1:i + 5] if len(l.split()) >= 5][:4]
            if follow:
                out.append(ExerciseCandidate(
                    name=line_n.rstrip(" .:-"), url=url, source_slug=source_slug,
                    extraction_method="page_text", confidence=METHOD_CONFIDENCE["page_text"],
                    instructions=[truncate(l, 300) for l in follow],
                ))
    return out


def extract_candidates(html_or_md: str, url: str, source_slug: str, *,
                       is_markdown: bool = False) -> list[ExerciseCandidate]:
    """Full deterministic extraction pipeline for one document."""
    soup = parse_markdown(html_or_md) if is_markdown else parse_html(html_or_md)

    candidates: list[ExerciseCandidate] = []
    seen_names: set[str] = set()

    def add_all(cands: list[ExerciseCandidate]) -> None:
        for c in cands:
            key = c.name.lower()
            if key in seen_names:
                continue
            seen_names.add(key)
            candidates.append(c)

    # Deterministic ladder
    if not is_markdown:
        add_all(extract_jsonld(soup, url, source_slug))
    add_all(extract_structured(soup, url, source_slug, "structured_html"))
    add_all(extract_tables(soup, url, source_slug))
    if not candidates:
        add_all(extract_structured(soup, url, source_slug, "semantic_html"))
    if not candidates:
        text = strip_html(html_or_md) if not is_markdown else html_or_md
        add_all(extract_text_fallback(text, url, source_slug))

    log.debug("extracted %d candidates from %s", len(candidates), url)
    return candidates
