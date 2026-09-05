# Implementation Report — Easeur Exercise Knowledge Base v0.1.0

**Date:** 2026-09-04 · **Status:** complete, seeded, aggregated, tested, deployable
**Companion docs:** `DECISIONS.md` (rationale), `README.md` (startup), `docs/data-quality-report.md` (generated quality report).

---

## 1. What was built

| Layer | Technology | Location |
|---|---|---|
| API + pipeline + review | Python 3.11, FastAPI, Pydantic v2, SQLAlchemy 2.0, Alembic, PostgreSQL 16 | `backend/` |
| Research UI | Next.js 15 (App Router), TypeScript, Tailwind v4, dark/light | `frontend/` |
| Deployment | Docker Compose (postgres + api + ui) | `docker-compose.yml` |
| Tests | pytest (66) + vitest/RTL (19) | `backend/tests/`, `frontend/src/**/*.test.tsx` |

### Dataset at v0.1.0 (snapshot id 1, content-hashed)

| Metric | Value |
|---|---|
| Active exercises | **184** (148 curated/approved + 36 aggregated/pending_review) |
| Anatomy taxonomy | 16 body regions · 29 muscle groups · **121 structures** (muscles, tendons, ligaments, fascia, nerves) |
| Structures with ≥1 exercise | 113 / 121 (**93%**); 8 missing, 2 need review |
| Registered sources | 10 (4 crawled in v0.1) · 2 unknown-license, flagged |
| Review queue | 55 duplicate pairs + 1 taxonomy item open · **0 auto-merged without review** |
| Conflicts recorded | 0 (none triggered in v0.1 corpus) |
| Exports | `exports/exercises.json` (10,517 lines), `muscles.json`, `body-regions.json` + live JSON/JSONL/CSV endpoints |

### Aggregated corpus (replay mode, `backend/corpus/`)

6 licensed/authoritative pages + per-domain robots.txt snapshots + manifest:

| Page | Source | Exercises extracted |
|---|---|---|
| Shoulder conditioning program | OrthoInfo — AAOS | 18 |
| Knee conditioning program | OrthoInfo — AAOS | 12 |
| Foot & ankle conditioning program | OrthoInfo — AAOS | 10 |
| Neck pain exercises | Versus Arthritis (arthritis-uk.org) | 3 |
| Fingers, hands & wrists exercises | Versus Arthritis (arthritis-uk.org) | 6 |
| Wrist, hand & finger exercises | NHS inform (Scotland) | 12 (incl. dosage) |

Extraction ladder results: 42 candidates accepted (36 created, 6 linked to
existing curated records via dedup), 1 rejected (generic heading), with
per-record provenance (`source_fact`/`normalized`) and bounded text excerpts.

## 2. URLs & endpoints

- API base: `http://localhost:8000/api/v1` · OpenAPI UI: `http://localhost:8000/docs`
- Research UI: `http://localhost:3000` (pages: dashboard `/`, `/exercises`, `/exercises/[slug]?research=1`, `/muscles`, `/muscles/[slug]`, `/body-map`, `/coverage`, `/sources`, `/sources/[slug]`, `/review`, `/datasets`)
- Key API resources: `exercises` (+filters: region, muscle, joint, type, equipment, difficulty, source, origin, status, confidence, sort, search), `muscles`, `body-regions`, `joints`, `equipment`, `exercise-types`, `sources`, `review` (+`POST /review/{id}/action`), `duplicates`, `conflicts`, `audit` (admin), `export`, `datasets`, `stats/dashboard`, `stats/coverage/{muscles,regions}`, `admin/{crawl,dedup,validate}` (admin)
- Auth: consumer endpoints public (default `status=approved`); research/admin via `X-API-Key` (default dev key `dev-admin-key` — rotate via `EASEUR_ADMIN_API_KEY`)

## 3. Startup steps

**Docker (recommended):**

```bash
docker compose up --build -d
docker compose exec api python -m app.cli init-db        # migrations
docker compose exec api python -m app.cli seed            # taxonomy + 148 curated
docker compose exec api python -m app.cli pipeline run-all  # replay-crawl + postprocess + report
# API http://localhost:8000/docs · UI http://localhost:3000
```

**Local (as used for development):**

```bash
# backend
cd backend && python -m venv .venv && .venv/bin/pip install -r requirements.txt -r requirements-dev.txt
#   PostgreSQL 16 on :5432 (easeur/easeur/easeur), then:
.venv/bin/python -m app.cli init-db && .venv/bin/python -m app.cli seed
.venv/bin/python -m app.cli pipeline run-all
.venv/bin/python -m uvicorn app.main:app --port 8000
# frontend
cd frontend && npm install && npm run dev   # :3000, proxies /api → :8000
# tests
cd backend && .venv/bin/python -m pytest    # 66 tests
cd frontend && npm test                     # 19 tests
```

CLI also provides: `pipeline {crawl|postprocess|report|run-all}`, `export --dataset … --fmt {json|jsonl|csv}`, `snapshot vX.Y.Z --label …`, `drop-all`.

## 4. Test coverage summary

- **API contract** (list/filters/pagination/detail/search/exports/statuses/OpenAPI shape)
- **Schema**: all 22 tables via real Alembic migrations; enum values; structure types (plantar fascia ≠ muscle)
- **Auth**: 401 without/with wrong key on review actions, admin endpoints, audit
- **Crawler**: robots disallow enforced (specific agent + wildcard), missing robots ⇒ allow, replay end-to-end incl. robots skip, same-domain link discovery
- **SSRF**: 16 hostile URLs rejected (localhost, private ranges, IPv6, cloud metadata, CRLF, credentials, non-HTTP schemes, DB ports); fetcher refuses private targets; safe URLs pass
- **Extractors**: structured markdown, JSON-LD (valid + invalid), tables, malformed/empty/oversized HTML, pages with no exercises, numbering-stripped normalization, missing fields
- **Dedup**: exact auto-merge, plural/synonym normalization, spec example (Neck Rotation vs Cervical Spine Rotation), alias stage, eversion-vs-inversion non-merge, region-incompatibility penalty, no uncertain auto-merge, existing-pair dedup
- **Data quality**: validation sweep queues missing anatomy/licensing/low-confidence; conflict detection records disagreement with both sources; review merge (both keep-directions), approve flow, audit log entries

## 5. Limitations (known, deliberate)

1. **No semantic/embedding dedup stage** in v0.1 — paraphrase-level duplicates
   (e.g. "Heel Cord Stretch" vs "Gastrocnemius Stretch") queue only if structured
   similarity ≥ 0.72. Planned: sentence-transformer embeddings with a conservative
   review-only threshold.
2. **AI enrichment is wired but disabled** (no provider key configured). All v0.1
   records are deterministic extractions; the AI path is capped, provenance-tagged
   and review-gated by design.
3. **Corpus breadth** — 6 pages / 3 crawled domains at v0.1. Seed lists for NHS
   inform per-joint pages, arthritis-uk.org per-joint pages and PDFs, and
   dynamichealth.nhs.uk lower-back exercises are prepared in
   `crawler.LIVE_SEED_URLS`; live crawling requires permissive egress (the dev
   sandbox allowed pypi/npm/github only, so v0.1 aggregation ran in replay mode
   from stored snapshots).
4. **2 sources have unknown licensing** (flagged in UI/exports, excluded from
   redistribution posture until reviewed); NHS Inform is marked restricted
   (facts-only use).
5. **Body map is stylized 2D** (front/back silhouettes with per-region zones) —
   meets the 2D requirement; no front/side/back full rotation.
6. **Docker Compose is the only packaged deployment**; no k8s manifests, no
   horizontal crawler workers.
7. **Media**: no photos/GIFs are scraped from sources (licensing posture D7).
   Visuals are project-owned AI-generated illustrations (10 shipped, mapped per
   body region with rehabilitation overrides; knee/ankle/whole-body assets land
   in the next batch — lower-limb exercises temporarily use the hip
   illustration) plus client-rendered animated SVG movement previews built from
   structured data. Source-licensed media requires explicit permission and a
   future `media_assets` table.

## 6. Next steps

1. Review the 55 queued duplicate pairs via `/review` (≈30 min of human work;
   audit-logged) → then re-run `pipeline postprocess` + `snapshot v0.2.0`.
2. Expand corpus: arthritis-uk.org per-joint pages + exercise PDFs, NHS inform
   per-joint pages, dynamichealth.nhs.uk lower-back set (seed URLs ready).
3. Add embedding-based dedup stage (review-only threshold) once ≥ 400 records.
4. Enable AI enrichment for targeted fields (difficulty normalization, dosage
   parsing) with the review gate already in place.
5. Schedule weekly `admin/validate` sweeps; add CI (migrations + 66 backend
   tests + frontend build/tests).
6. workout.easeur.com integration against pinned dataset versions via `/api/v1`.

## 7. File map

```
docker-compose.yml            full stack (postgres + api + ui)
.env.example                  all configuration knobs
DECISIONS.md                  D1–D14 architecture decisions & rationale
docs/implementation-report.md this report
docs/data-quality-report.md   generated dataset quality report
backend/app/{models,services,pipeline,api,taxonomy,seed}/…
backend/corpus/               replay corpus (6 pages, manifest, robots snapshots)
backend/alembic/              migrations (initial schema applied)
backend/tests/                66 pytest tests (real PG)
frontend/src/app/             12 routes (dark/light)
frontend/src/components/      shared UI (cards, badges, donut, SVG body map…)
exports/                      exercises/muscles/body-regions JSON snapshots
```
