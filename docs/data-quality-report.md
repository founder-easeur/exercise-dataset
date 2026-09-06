# Data Quality Report

_Generated 2026-09-06 11:04 UTC by the Easeur Exercise Knowledge Base pipeline._

## Sources

- Sources registered: **10**
- Sources with unknown licensing: **2** (conservative default; flagged for review)
- Crawl jobs run: **1** (replay mode)

## Crawl & extraction

- Pages processed: **6**
- Pages failed: **0**
- URLs skipped by robots/policy: **0**
- Exercise candidates extracted: **41**
- Candidates linked to existing exercises (dedup stage 1): **4**
- Candidates rejected during normalization: **1**
- URL status breakdown: `processed`=6

## Exercises

- Normalized exercises (active): **184**
  - Curated: **148** (team-authored, approved)
  - Aggregated from sources: **36**
- Approved: **148** — Pending review: **36**
- Merged duplicates (parked): **0**
- Potential duplicate pairs awaiting review: **55**
- Open data conflicts: **0**
- Low-confidence records (<0.55): **0**
- Records flagged with medical-claim language: **0** (held for clinical review)
- Open review-queue items (all types): **56**

## Anatomical coverage

- Structures in taxonomy: **121** (muscles, tendons, ligaments, fascia, nerves)
- Structures with at least one exercise: **113** (93%)
- Structures with no exercises: **8**

### By body region

| Region | Exercises | Verified | Sources | Muscles covered | Status |
|---|---|---|---|---|---|
| Neck | 17 | 13 | 2 | 8/8 | excellent |
| Jaw / Face | 3 | 3 | 0 | 4/4 | limited |
| Shoulder | 30 | 22 | 2 | 8/8 | excellent |
| Upper Back | 20 | 19 | 1 | 7/7 | good |
| Chest | 8 | 8 | 0 | 2/2 | good |
| Lower Back | 17 | 17 | 0 | 8/8 | good |
| Elbow | 5 | 3 | 1 | 3/6 | good |
| Forearm | 16 | 15 | 1 | 17/17 | good |
| Wrist | 11 | 9 | 1 | 5/5 | good |
| Hand | 16 | 9 | 2 | 4/5 | excellent |
| Hip / Pelvis | 38 | 34 | 1 | 20/22 | good |
| Knee | 16 | 16 | 1 | 5/5 | good |
| Calf / Lower Leg | 25 | 18 | 1 | 12/12 | good |
| Ankle | 21 | 19 | 1 | 1/3 | good |
| Foot | 20 | 16 | 1 | 9/9 | good |
| Whole Body | 7 | 7 | 0 | 0/0 | good |

### Muscles / structures with no exercises yet

Anconeus, Biceps Tendon (Distal), Triceps Tendon (Distal), Hypothenar Muscles, Inferior Gemellus, Sartorius, Anterior Talofibular Ligament, Deltoid (Medial) Ligament of the Ankle

### Limited-coverage structures (1-3 exercises)

Cervical Extensors (3), Levator Scapulae (2), Scalenes (3), Splenius Capitis & Cervicis (1), Sternocleidomastoid (1), Suboccipitals (2), Lateral Pterygoid (2), Masseter (3), Medial Pterygoid (1), Temporalis (1), Supraspinatus (3), Rhomboid Minor (2), Teres Major (1), Pectoralis Minor (2), Multifidus (1), Pelvic Floor Muscles (1), Biceps Brachii (3), Abductor Pollicis Longus (1), Brachioradialis (3), Common Flexor Tendon (Medial Epicondyle) (2), Extensor Carpi Ulnaris (3), Extensor Pollicis (Longus & Brevis) (1), Flexor Carpi Radialis (3), Flexor Carpi Ulnaris (3), Flexor Digitorum Profundus (3), Flexor Pollicis Longus (1), Palmaris Longus (1), Pronator Teres (1), Radial Nerve (1), Supinator (2), Flexor Retinaculum (Transverse Carpal Ligament) (1), Median Nerve (1), Ulnar Nerve (1), Wrist Extensor Group (1), Wrist Flexor Group (2), Adductor Pollicis (3), Interossei (Hand) (3), Thenar Muscles (3), Gluteus Minimus (2), Gracilis (2), Iliotibial Band (Tract) (2), Obturator Externus (1), Obturator Internus (3), Pectineus (2), Quadratus Femoris (1), Sciatic Nerve (1), Semimembranosus (3), Semitendinosus (3), Superior Gemellus (1), Patellar Tendon (1), Popliteus (3), Vastus Intermedius (2), Extensor Digitorum Longus (3), Extensor Hallucis Longus (3), Flexor Hallucis Longus (3), Peroneus Brevis (3), Plantaris (1), Peroneal (Fibular) Tendons (3), Abductor Digiti Minimi (1), Adductor Hallucis (1), Extensor Digitorum Brevis (2), Lumbricals (Foot) (2), Plantar Fascia (3)

## Licensing summary

| License | Sources |
|---|---|
| unknown | 2 |
| public_domain | 3 |
| restricted | 5 |

## Notes & caveats

- Aggregated records store **structured facts + provenance only** — never full copyrighted article text or media.
- Where licensing is unclear, `commercial_use_allowed = unknown` and the exercise is queued for licensing review.
- Medical-claim language detected in source text is flagged and requires review before approval; the pipeline never invents diagnoses or treatments.
- AI enrichment: the deterministic anatomy mapper (`heuristic-anatomy-mapper v1`) performs classification; LLM enrichment is implemented but disabled unless `EASEUR_AI_API_KEY` is configured. All AI/inference output is marked `ai_inference` + `pending_review`.
