"""Extraction tests: structured data, JSON-LD, malformed HTML, missing fields."""
from __future__ import annotations

from app.pipeline.extract import (
    extract_candidates, extract_jsonld, extract_structured, extract_tables,
    parse_html,
)

AAOS_MD = """# Program

## 2. Heel Cord Stretch with Bent Knee

**Main muscles worked:** Soleus

_You should feel this stretch in your calf and into your heel_

**Equipment needed:** None

**Step-by-step directions**

- Stand facing a wall with your unaffected leg forward with a slight bend at the knee.
- Keep both heels flat on the floor and press your hips forward toward the wall.
- Hold the stretch for 30 seconds, then relax for 30 seconds. Repeat.

**Tip** Keep your hips centered over both feet.
"""


def test_structured_markdown_extraction():
    cands = extract_candidates(AAOS_MD, "https://x.example/p", "test", is_markdown=True)
    assert len(cands) == 1
    c = cands[0]
    assert c.name == "Heel Cord Stretch with Bent Knee"  # numbering stripped upstream
    assert c.extraction_method == "structured_html"
    assert any("soleus" in m.lower() for m in c.raw_muscles)
    assert len(c.instructions) >= 3
    assert c.confidence >= 0.75


def test_numbering_stripped_in_normalize():
    from app.pipeline.normalize import normalize_candidate
    from app.pipeline.extract import ExerciseCandidate
    cand = ExerciseCandidate(
        name="5. Sleeper Stretch", url="https://x.example", source_slug="s",
        raw_muscles=["Infraspinatus, teres minor"],
        instructions=["Lie on your side with the affected shoulder under you.",
                      "Use your unaffected arm to push your other arm down gently.",
                      "Hold for 30 seconds, then relax."])
    n = normalize_candidate(cand)
    assert n.name == "Sleeper Stretch"
    assert n.slug == "sleeper-stretch"
    assert "infraspinatus" in [s for s, _ in n.muscles]


def test_jsonld_extraction():
    html = """
    <html><body>
    <script type="application/ld+json">
    {"@type": "ExerciseAction", "name": "Seated Neck Rotation",
     "step": [{"@type": "HowToStep", "text": "Sit tall and rotate slowly."},
              {"@type": "HowToStep", "text": "Hold briefly and return."}],
     "target": "sternocleidomastoid"}
    </script>
    </body></html>
    """
    cands = extract_jsonld(parse_html(html), "https://x.example", "s")
    assert len(cands) == 1
    assert cands[0].name == "Seated Neck Rotation"
    assert cands[0].extraction_method == "jsonld"
    assert cands[0].confidence == 0.9
    assert len(cands[0].instructions) == 2


def test_jsonld_invalid_json_ignored():
    html = '<script type="application/ld+json">{invalid json</script>'
    assert extract_jsonld(parse_html(html), "url", "s") == []


def test_table_extraction():
    html = """
    <table>
      <tr><th>Exercise</th><th>Main muscles</th><th>Equipment</th></tr>
      <tr><td>Wrist Extensor Stretch</td><td>wrist extensors</td><td>None</td></tr>
      <tr><td>Wrist Flexor Stretch</td><td>wrist flexors</td><td>None</td></tr>
    </table>
    """
    cands = extract_tables(parse_html(html), "url", "s")
    assert len(cands) == 2
    assert cands[0].extraction_method == "table"
    assert cands[0].raw_muscles == ["wrist extensors"]


def test_malformed_html_does_not_crash():
    htmls = [
        "<html><body><h2>Broken Stretch<h2><p>Unclosed tags everywhere",
        "\x00\x01binary<html><h2>Null bytes</h2>",
        "<div>" + "<p>word " * 5000 + "</div>",
        "",
    ]
    for h in htmls:
        cands = extract_candidates(h, "https://x.example", "s")
        assert isinstance(cands, list)


def test_page_without_exercises_returns_empty():
    html = "<html><body><h1>About Us</h1><p>We are an organisation.</p></body></html>"
    cands = extract_candidates(html, "https://x.example", "s")
    assert cands == []


def test_missing_fields_handled():
    from app.pipeline.normalize import normalize_candidate
    from app.pipeline.extract import ExerciseCandidate
    # no instructions at all -> normalization rejects (nothing reviewable)
    cand = ExerciseCandidate(name="Empty Exercise", url="u", source_slug="s")
    assert normalize_candidate(cand) is None
    # name only + one instruction -> still normalizes with defaults
    cand2 = ExerciseCandidate(name="Simple Move", url="u", source_slug="s",
                              instructions=["Lift the leg slowly and lower it."])
    n = normalize_candidate(cand2)
    assert n is not None
    assert n.difficulty.value == "beginner"
