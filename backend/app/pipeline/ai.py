"""Selective AI enrichment with full provenance.

AI is NEVER the default parser. It runs only:
  - when AI_API_KEY is configured, AND
  - on a bounded number of low-confidence / ambiguous candidates
    (settings.ai_max_candidates_per_run), AND
  - output is always recorded as origin=ai_inference, status=pending_review.

When no LLM is configured (the default, and the case in the offline build
sandbox), the deterministic anatomy mapper in `anatomy_mapper.py` performs
classification and is honestly labelled as a deterministic heuristic.
"""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass

import httpx

from app.config import settings

log = logging.getLogger("easeur.ai")

ENRICHMENT_SYSTEM_PROMPT = (
    "You are a physiotherapy data extraction assistant. Given an exercise "
    "description, return strict JSON with keys: muscles (list of anatomical "
    "structure names, precise and conservative), body_regions (list), "
    "equipment (list), exercise_type (one of: stretching, mobility, "
    "rehabilitation, physiotherapy, recovery, warmup, cooldown, posture, "
    "balance, breathing, strength, release), difficulty (beginner|intermediate|"
    "advanced), confidence (0-1). Only include information supported by the "
    "text. Never invent medical claims."
)
PROMPT_VERSION = settings.ai_prompt_version


@dataclass
class AiEnrichment:
    fields: dict
    model: str
    model_version: str | None
    prompt_version: str
    confidence: float | None


class AiEnricher:
    """OpenAI-compatible chat-completion enrichment client."""

    def __init__(self) -> None:
        self.enabled = bool(settings.ai_api_key and settings.ai_api_base)
        self.model = settings.ai_model

    def enrich_candidate(self, name: str, text: str) -> AiEnrichment | None:
        if not self.enabled:
            return None
        try:
            resp = httpx.post(
                f"{settings.ai_api_base}/chat/completions",
                headers={"Authorization": f"Bearer {settings.ai_api_key}"},
                json={
                    "model": self.model,
                    "temperature": 0,
                    "response_format": {"type": "json_object"},
                    "messages": [
                        {"role": "system", "content": ENRICHMENT_SYSTEM_PROMPT},
                        {"role": "user", "content": f"Exercise: {name}\n\nDescription:\n{text[:3000]}"},
                    ],
                },
                timeout=45,
            )
            resp.raise_for_status()
            data = json.loads(resp.json()["choices"][0]["message"]["content"])
            return AiEnrichment(
                fields=data, model=self.model,
                model_version=None, prompt_version=PROMPT_VERSION,
                confidence=float(data.get("confidence", 0.5)) or None,
            )
        except Exception as exc:  # noqa: BLE001
            log.warning("AI enrichment failed for %r: %s", name, exc)
            return None
