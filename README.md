# Easeur Exercise Knowledge Base

Structured **stretching · mobility · physiotherapy-oriented · rehabilitation**
exercise dataset with a full anatomy taxonomy, per-field provenance, licensing
posture, human review workflows and a research UI — the data platform behind
[workout.easeur.com](https://workout.easeur.com).

- **API:** FastAPI + PostgreSQL — `http://localhost:8000/api/v1` (OpenAPI at `/docs`)
- **Research UI:** Next.js 15 — `http://localhost:3000` (dark/light)
- **Status:** v0.1.0 — 184 exercises (148 curated + 36 aggregated), 121 anatomical
  structures (93% covered), 10 registered sources, 66 backend + 19 frontend tests

## Quick start (Docker)

```bash
cp .env.example .env
docker compose up --build -d
docker compose exec api python -m app.cli init-db
docker compose exec api python -m app.cli seed
docker compose exec api python -m app.cli pipeline run-all
```

Open <http://localhost:3000> (UI) and <http://localhost:8000/docs> (API).

## Quick start (local)

```bash
# Backend (Python 3.11, PostgreSQL on :5432)
cd backend
python -m venv .venv && .venv/bin/pip install -r requirements.txt -r requirements-dev.txt
.venv/bin/python -m app.cli init-db          # alembic migrations
.venv/bin/python -m app.cli seed             # taxonomy + 148 curated exercises
.venv/bin/python -m app.cli pipeline run-all # replay aggregation + dedup + quality report
.venv/bin/python -m uvicorn app.main:app --port 8000

# Frontend (Node 22)
cd frontend
npm install && npm run dev                   # :3000, proxies /api → :8000
```

## The pipeline

```
registered sources ──► crawler (robots.txt, rate-limited, SSRF-guarded, no JS)
                    ──► extract (JSON-LD ▸ structured HTML ▸ tables ▸ semantic ▸ text)
                    ──► normalize + anatomy mapping (121-structure taxonomy)
                    ──► dedup (exact ▸ alias ▸ structured)   ── auto-merge only ≥0.99
                    ──► validation sweep                     ──► review queue
                    ──► snapshot + exports (JSON / JSONL / CSV)
```

Every aggregated record carries field-level provenance
(`source_fact | normalized | curated | ai_inference | human_reviewed`), a
confidence score, and source-document links. Conflicting source facts are
**recorded, never silently resolved**. AI enrichment (optional, off by default)
is capped, tagged and always review-gated.

**Exercise media** ships licensing-clean: project-owned AI illustrations (one
per body area, served at `/static/exercises/…` and exposed via the `media[]`
API field + exports) plus animated SVG movement previews rendered per exercise
from position/movement/target-region data. No copyrighted photos or GIFs are
copied from sources.

Two crawl modes: **live** and **replay** — v0.1 aggregation ran deterministically
from the stored corpus in `backend/corpus/`.

## Research UI pages

`/` dashboard · `/exercises` explorer (12 filters, search, pagination) ·
`/exercises/[slug]` detail (+ `?research=1` provenance table) · `/muscles` and
`/muscles/[slug]` structure explorer · `/body-map` interactive 2D coverage map ·
`/coverage` gap analysis · `/sources` + `/sources/[slug]` licensing & crawl
status · `/review` duplicate adjudication & queue (admin key) · `/datasets`
versions & exports.

## Configuration

See `.env.example` — database URL, admin API key (`X-API-Key` for review/admin
endpoints; default `dev-admin-key`), crawler politeness, thresholds, optional AI
provider.

## Testing

```bash
cd backend  && .venv/bin/python -m pytest   # 66 tests (real PostgreSQL)
cd frontend && npm test                     # 19 component tests
cd frontend && npx tsc --noEmit && npx next build
```

## Docs

- `CLAUDE.md` — agent guide: repo orientation, non-negotiable rules, run/test commands, incremental-task recipes, gotchas (start here if you're an AI coding agent)
- `DECISIONS.md` — architecture decisions D1–D14 with rationale
- `docs/implementation-report.md` — final report: counts, endpoints, startup, limitations, next steps
- `docs/data-quality-report.md` — generated dataset quality report

## Licensing posture

Facts and structured metadata extracted from authoritative medical sources
(AAOS OrthoInfo, Versus Arthritis, NHS inform, NHS, CDC, MedlinePlus…); bounded
excerpts + outbound links only — no copyrighted article text or media copied.
Sources with unclear terms are flagged `unknown` and excluded from
redistribution until reviewed.
