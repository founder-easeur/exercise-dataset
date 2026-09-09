"""Authoritative reference pages per body region.

Every curated exercise gets at least one outbound reference to an official,
high-authority page where the exercise (or its program) is demonstrated with
images/GIFs/videos. Aggregated exercises reference the exact source document
they were extracted from (see services/seeder.seed_references).

We LINK to these pages; we never copy their media (DECISIONS.md D7).
"""
from __future__ import annotations

# source_slug -> (label, url, kind)
_AR = "https://www.arthritis-uk.org/information-and-support/living-with-arthritis/health-and-wellbeing/exercising-with-arthritis/exercises-for-healthy-joints"
_OI = "https://www.orthoinfo.org/recovery"
_NI = "https://www.nhsinform.scot/illnesses-and-conditions/muscle-bone-and-joints"

#: region slug -> list of (source_slug, label, url, kind)
REGION_REFERENCES: dict[str, list[tuple[str, str, str, str]]] = {
    "neck": [
        ("versus-arthritis", "Neck exercises — Versus Arthritis", f"{_AR}/exercises-for-the-neck/", "program"),
        ("nhs-inform-scotland", "Exercises for neck problems — NHS inform", f"{_NI}/neck-and-back-problems-and-conditions/exercises-for-neck-problems", "program"),
    ],
    "jaw": [
        ("versus-arthritis", "Exercises for healthy joints (incl. jaw) — Versus Arthritis", f"{_AR}/", "program"),
    ],
    "shoulder": [
        ("orthoinfo-aaos", "Rotator cuff & shoulder conditioning program — OrthoInfo (AAOS)", f"{_OI}/rotator-cuff-and-shoulder-conditioning-program/", "program"),
        ("versus-arthritis", "Shoulder exercises — Versus Arthritis", f"{_AR}/exercises-for-the-shoulders/", "program"),
    ],
    "chest": [
        ("orthoinfo-aaos", "Rotator cuff & shoulder conditioning program — OrthoInfo (AAOS)", f"{_OI}/rotator-cuff-and-shoulder-conditioning-program/", "program"),
    ],
    "upper-back": [
        ("versus-arthritis", "Back exercises — Versus Arthritis", f"{_AR}/exercises-for-the-back/", "program"),
    ],
    "lower-back": [
        ("versus-arthritis", "Back exercises — Versus Arthritis", f"{_AR}/exercises-for-the-back/", "program"),
        ("nhs-uk", "Back pain — NHS", "https://www.nhs.uk/conditions/back-pain/", "article"),
    ],
    "elbow": [
        ("versus-arthritis", "Elbow exercises — Versus Arthritis", f"{_AR}/exercises-for-the-elbows/", "program"),
    ],
    "forearm": [
        ("versus-arthritis", "Fingers, hands & wrists exercises — Versus Arthritis", f"{_AR}/exercises-for-the-fingers-hands-and-wrists/", "program"),
        ("nhs-inform-scotland", "Exercises for wrist, hand & finger problems — NHS inform", f"{_NI}/arm-shoulder-and-hand-problems-and-conditions/exercises-for-wrist-hand-and-finger-problems", "program"),
    ],
    "wrist": [
        ("nhs-inform-scotland", "Exercises for wrist, hand & finger problems — NHS inform", f"{_NI}/arm-shoulder-and-hand-problems-and-conditions/exercises-for-wrist-hand-and-finger-problems", "program"),
        ("versus-arthritis", "Fingers, hands & wrists exercises — Versus Arthritis", f"{_AR}/exercises-for-the-fingers-hands-and-wrists/", "program"),
    ],
    "hand": [
        ("nhs-inform-scotland", "Exercises for wrist, hand & finger problems — NHS inform", f"{_NI}/arm-shoulder-and-hand-problems-and-conditions/exercises-for-wrist-hand-and-finger-problems", "program"),
        ("versus-arthritis", "Fingers, hands & wrists exercises — Versus Arthritis", f"{_AR}/exercises-for-the-fingers-hands-and-wrists/", "program"),
    ],
    "hip": [
        ("versus-arthritis", "Hip exercises — Versus Arthritis", f"{_AR}/exercises-for-the-hips/", "program"),
        ("nhs-inform-scotland", "Exercises for hip problems — NHS inform", f"{_NI}/leg-foot-and-hip-problems-and-conditions/exercises-for-hip-problems", "program"),
    ],
    "knee": [
        ("orthoinfo-aaos", "Knee conditioning program — OrthoInfo (AAOS)", f"{_OI}/knee-conditioning-program/", "program"),
        ("versus-arthritis", "Knee exercises — Versus Arthritis", f"{_AR}/exercises-for-the-knees/", "program"),
        ("nhs-inform-scotland", "Exercises for knee problems — NHS inform", f"{_NI}/leg-foot-and-hip-problems-and-conditions/exercises-for-knee-problems", "program"),
    ],
    "calf": [
        ("versus-arthritis", "Toes, feet & ankles exercises — Versus Arthritis", f"{_AR}/exercises-for-the-toes-feet-and-ankles/", "program"),
    ],
    "ankle": [
        ("orthoinfo-aaos", "Foot & ankle conditioning program — OrthoInfo (AAOS)", f"{_OI}/foot-and-ankle-conditioning-program/", "program"),
        ("versus-arthritis", "Toes, feet & ankles exercises — Versus Arthritis", f"{_AR}/exercises-for-the-toes-feet-and-ankles/", "program"),
        ("nhs-inform-scotland", "Exercises for ankle problems — NHS inform", f"{_NI}/leg-foot-and-hip-problems-and-conditions/exercises-for-ankle-problems", "program"),
    ],
    "foot": [
        ("orthoinfo-aaos", "Foot & ankle conditioning program — OrthoInfo (AAOS)", f"{_OI}/foot-and-ankle-conditioning-program/", "program"),
        ("versus-arthritis", "Toes, feet & ankles exercises — Versus Arthritis", f"{_AR}/exercises-for-the-toes-feet-and-ankles/", "program"),
        ("nhs-inform-scotland", "Exercises for foot & toe problems — NHS inform", f"{_NI}/leg-foot-and-hip-problems-and-conditions/exercises-for-foot-and-toe-problems", "program"),
    ],
    "whole-body": [
        ("versus-arthritis", "Exercises for healthy joints — Versus Arthritis", f"{_AR}/", "program"),
    ],
}

#: Fallback when a region has no mapping (should not happen — hub page).
FALLBACK_REFERENCES: list[tuple[str, str, str, str]] = [
    ("versus-arthritis", "Exercises for healthy joints — Versus Arthritis", f"{_AR}/", "program"),
]
