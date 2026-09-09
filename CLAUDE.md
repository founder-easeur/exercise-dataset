# CLAUDE.md — Agent Guide: Easeur Exercise Knowledge Base

This file orients coding agents (Claude Code and friends) to the repo. Read it
before making changes. Human-facing docs: `README.md` (overview),
`DECISIONS.md` (architecture rationale, D1–D14), `docs/implementation-report.md`
(v0.1.0 report), `docs/data-quality-report.md` (generated dataset stats).

---

## 1. What this project is

A **structured exercise knowledge base** (stretching · mobility · physiotherapy-
oriented · rehabilitation) with full anatomy taxonomy, per-field provenance,
conservative licensing posture, human review workflows, and a research UI.
It is the data platform behind workout.easeur.com (future consumer, **API-only
access — never the database**).

Stack: **FastAPI + SQLAlchemy 2.0 + Alembic + PostgreSQL 16** backend, one
aggregation pipeline module, **Next.js 15 (App Router) + TypeScript + Tailwind
v4** frontend, pytest + vitest tests, Docker Compose deployment.

**Not** a workout app. Not a scraper free-for-all. Quality, provenance and
licensing cleanliness beat record count — every design decision optimizes for
that.

## 2. Non-negotiable rules (violations = rejected PR)

1. **Consumers read `/api/v1/*` only.** No consumer ever touches the DB. Default
   listing serves `status=approved` only.
2. **Never auto-merge uncertain duplicates.** Auto-merge requires total
   similarity ≥ 0.99 **and** region compatibility. Everything ≥ 0.72 (or ≥ 0.60
   with an alias hit) queues for human review. Never lower these thresholds to
   "clean up" the queue.
3. **Never invent or paraphrase medical claims.** Clinical text is recorded
   verbatim from sources, flagged `is_medical_claim`, and review-gated.
4. **Provenance is field-level.** Every key field gets a `provenance` row with
   origin: `source_fact | normalized | curated | ai_inference | human_reviewed`.
   `ai_inference` records are ALWAYS `pending_review`.
5. **AI is selective enrichment, never the default parser.** Hard cap per run
   (`ai_max_candidates_per_run`), model/prompt/fields tracked, disabled by
   default (no API key configured).
6. **Licensing is conservative.** Store structured facts, metadata and bounded
   excerpts + outbound links — never full article text, never scraped photos/
   GIFs. Exercise imagery = project-owned AI illustrations
   (`backend/media/exercises/`) + client-rendered animated SVG previews. Unknown
   license ⇒ flagged, excluded from redistribution.
7. **Conflicts are recorded, never silently resolved** (`data_conflicts` table
   stores both values + both sources; resolution only via review queue).
8. **Aggregated records enter as `pending_review`** — never auto-approved.
9. **Crawler:** respects robots.txt (snapshots stored), identifies itself
   (`EaseurExerciseBot/1.0`), ≥3s per-domain delay, never executes scraped JS,
   SSRF-validates every URL (private/link-local/metadata IPs blocked).
10. **Schema changes go through Alembic migrations**, always. Tests run real
    migrations, so drift is caught.

## 3. Repo map

```
backend/
  app/
    config.py            Settings (env prefix EASEUR_): DB URL, admin key, thresholds
    db.py, models/       SQLAlchemy Base + typed models (22 tables)
    enums.py             All enums — origin, review status, source types, …
    taxonomy/            anatomy_data.py (16 regions/29 groups/121 structures —
                         includes tendons/ligaments/fascia; structure_type column),
                         reference_data.py, source_registry.py (10 sources)
    seed/curated/        148 curated exercises in 6 modules + ALL_CURATED_EXERCISES
    services/            seeder, query (list/get + filters), serializers (API dict
                         shapes), stats, review (queue actions + audit), export
    pipeline/            crawler, fetcher, robots, security (SSRF), extract,
                         anatomy_mapper, normalize, dedup, validate, postprocess,
                         ai, ingest, report
    media_registry.py    region→illustration mapping + license metadata
    api/v1.py            All /api/v1 endpoints (single router file)
    cli.py               init-db | seed | drop-all | export | snapshot | serve |
                         pipeline {crawl|postprocess|report|run-all}
    main.py              FastAPI app + CORS + /static media mount
  alembic/versions/      Migrations (5b4f85af1dfd initial schema)
  corpus/                REPLAY corpus: pages/*.md + manifest.json +
                         www.{domain}.robots.txt snapshots
  media/exercises/       13 AI illustrations (PNG, ~9MB total)
  tests/                 75 pytest tests (real PostgreSQL test DB)
frontend/
  src/app/               Pages: / (dashboard RSC), /exercises (client explorer),
                         /exercises/[slug] (RSC detail, ?research=1 provenance),
                         /muscles, /muscles/[slug], /body-map, /coverage,
                         /sources, /sources/[slug], /review, /datasets
  src/components/        shell (nav), ui (cards/badges/donut/pagination),
                         exercise-card (source chips!), pose-diagram (animated
                         SVG preview), theme (dark/light)
  src/lib/               api.ts (types + client), server-api.ts (RSC fetch),
                         exercise-filters.ts (URL builders — tested)
  tests:                 *.test.tsx collocated; 31 vitest tests
scripts/dev-up.sh        One-command idempotent cold start (see §4)
exports/                 Generated dataset exports (JSON)
docs/                    implementation-report.md, data-quality-report.md (generated)
docker-compose.yml       postgres + api + ui
```

## 4. Running it

```bash
bash scripts/dev-up.sh          # idempotent cold start: venvs, embedded PG
                                # (UTF-8 cluster), migrations, seed, replay
                                # aggregation, snapshot, exports, npm install.
                                # Skips anything already present.

# servers:
(cd backend && .venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000)
(cd frontend && npm run dev)    # http://localhost:3000
```

Ports: **8000** API (OpenAPI at `/docs`), **3000** UI, **5432** PostgreSQL.
DB URL: `postgresql+psycopg2://easeur:easeur@127.0.0.1:5432/easeur`.
Admin key (for review/admin endpoints, `X-API-Key` header): `dev-admin-key`
(override with `EASEUR_ADMIN_API_KEY`).

The UI's `/api/*` and `/static/*` paths are proxied to the backend by a Next.js
rewrite (`frontend/next.config.ts`) — client code uses only relative URLs.

**Docker alternative:** `docker compose up --build -d` then run
`docker compose exec api python -m app.cli init-db && … seed && … pipeline run-all`.

## 5. Environment quirks — read before debugging

- **Always use `backend/.venv/bin/python`.** System python lacks
  `pydantic_settings`. Same for pytest: `cd backend && .venv/bin/python -m pytest`.
- **Env prefix is `EASEUR_`** (e.g. `EASEUR_DATABASE_URL`). See `.env.example`.
- **PostgreSQL runs embedded via `pgserver`** (pip package), not a system
  install. Binaries: `/tmp/pgvenv/lib/python3.11/site-packages/pgserver/pginstall/bin`
  (created by `dev-up.sh`). Data dir: `/home/user/.cache/easeur-pg`.
  When creating a cluster manually you MUST pass `--encoding=UTF8 --locale=C` —
  a default C-locale initdb gives SQL_ASCII and crashes psycopg2 on non-ASCII
  data (taxonomy has em-dashes; fixed in app via `client_encoding=UTF8` in
  `app/db.py`, but keep clusters UTF-8 anyway).
- **Console output is forced UTF-8** in `app/log.py` — some environments default
  to ASCII stdout. Don't remove that reconfigure block.
- **In the Arena/e2b sandbox:** `node_modules`, `backend/.venv`, `/tmp`, and
  `~/.cache` are NOT persisted across sessions; only the git repo + workspace
  files survive. Run `bash scripts/dev-up.sh` after any reset. General web
  egress is blocked (pypi/npm/github only) ⇒ **live crawling impossible; use
  replay mode**. Also beware: the sandbox restore has a glitch that sometimes
  drops recently-created files (seen with `frontend/src/app/coverage/page.tsx`)
  and can roll back `.git` — after any restore, run `git status` and
  `git log --oneline` and reconcile with `origin/arena/01a06df8-exercise-dataset`
  before committing.

## 6. The pipeline (aggregation)

```
registered sources (source_registry.py)
  → crawler (robots.txt checked against corpus snapshots; SSRF-validated;
    rate-limited; UA identified; no JS execution)
  → extract   confidence ladder: jsonld .90 → structured_html .80 → table .72
              → semantic_html .62 → page_text .45 → ai .40
  → normalize (name blocklist for junk headings, numbering strip, aliasing,
    slug generation) + anatomy_mapper (maps raw muscle text → 121-structure
    taxonomy; unmatched terms logged for taxonomy gaps)
  → dedup     exact → alias → structured (name × anatomy × category).
              auto-merge ≥0.99 + region-compatible; review ≥0.72 (alias ≥0.60)
  → validate  missing anatomy / missing source / low confidence (<0.55) /
    licensing unknown / medical claim → review_queue items
  → report    docs/data-quality-report.md (regenerated)
```

Two crawl modes: **replay** (default in dev/CI — reads `backend/corpus/`
manifest + page snapshots; deterministic, byte-identical results) and **live**
(real HTTP; needs egress + robots respect; seeds in `crawler.LIVE_SEED_URLS`).

CLI:
```bash
cd backend
.venv/bin/python -m app.cli pipeline crawl --mode replay   # aggregate from corpus
.venv/bin/python -m app.cli pipeline postprocess           # dedup + validation sweep
.venv/bin/python -m app.cli pipeline report                # regenerate quality report
.venv/bin/python -m app.cli pipeline run-all               # all of the above
.venv/bin/python -m app.cli snapshot v0.2.0 --label "…" --notes "…"   # version pin
.venv/bin/python -m app.cli export --dataset exercises --fmt json     # → exports/
```

**Expected v0.1.0 baseline after a clean replay** (deviation = bug): 148 seeded
curated, 36 aggregated (pending_review), 184 active, 55 duplicate pairs queued,
0 auto-merged, 0 conflicts, 113/121 structures covered, snapshot v0.1.0 id=1.

## 7. Data model essentials

- `exercises` — canonical_name, normalized_name, slug (unique), category,
  difficulty, position, movement_pattern, instructions, dosage, confidence,
  review_status, origin (`curated|aggregated`), merged_into_id, is_medical_claim.
  Merged records stay in the table (soft-merge); queries filter `merged_into_id
  IS NULL`.
- `provenance` — (exercise_id, field_name, value, origin, source_document_id,
  ai_model, confidence). The core trust table.
- `review_queue` — typed items (duplicate_pair, low_confidence, missing_anatomy,
  licensing_unknown, medical_claim, anatomy_conflict…), priority, status.
  Actions via `POST /api/v1/review/{id}/action` (admin):
  `approve|reject|edit|merge|split|flag|dismiss`; merge accepts
  `edits.keep = "primary"|"related"` (which record survives). All actions write
  `audit_log`.
- `sources` — license/commercial-use/attribution/robots posture per domain.
  `source_documents` — fetched pages (bounded excerpt, hash, word count).
- `dataset_versions` — content-hashed snapshots (v0.1.0 = id 1).
- Enum values live in `app/enums.py` and are DB-level `Enum` types.

API serializer contract (do not break without versioning):
`exercise_summary` = {id, slug, name, aliases, type, type_name, difficulty,
position, body_regions, primary_muscles, all_muscles, equipment, confidence,
review_status, origin, is_medical_claim, source_count, **sources[]** (slug,
name, domain, url→original page, authority, license), **media[]** (kind, url,
license, credit, origin)}.

## 8. Common incremental tasks

**Add a new source (live crawling later):**
1. Add entry to `app/taxonomy/source_registry.py` (slug, domain, license
   posture, authority, terms_url). 2. Run the seeder (idempotent by slug) or
   the DB refresh snippet used previously. 3. Add seed URLs to
   `crawler.LIVE_SEED_URLS`. 4. When egress allows, add the page to the replay
   corpus (see next task) OR run `pipeline crawl --mode live`.

**Add a replay-corpus page:** save sanitized markdown to
`backend/corpus/pages/<source>-<topic>.md`, add an entry to
`backend/corpus/manifest.json` (url, file, source_slug, title), drop a
`www.<domain>.robots.txt` snapshot in `backend/corpus/`, then
`pipeline run-all` and confirm the baseline numbers shifted sensibly.

**Adjudicate the 55 duplicate pairs (unblocks v0.2.0):** open `/review` in the
UI (key `dev-admin-key`) — pairs show side-by-side with source links; choose
keep A/B, merge or keep both. Via API: `POST /api/v1/review/{id}/action` with
`{"action":"merge","edits":{"keep":"related"}}`. Afterwards re-run
`pipeline postprocess`, then `snapshot v0.2.0` + exports.

**Add curated exercises:** add a module or extend one in
`backend/app/seed/curated/`, register in `ALL_CURATED_EXERCISES`, re-run
`seed` (idempotent by slug). Curated = approved + `curated` provenance.

**Add an API endpoint:** extend `app/api/v1.py` (single router file). Query
logic in `services/query.py`, dict shape in `services/serializers.py`. Add a
test in `backend/tests/test_api.py`. Admin-protected ⇒ `Depends(require_admin)`.

**Add a UI page:** create `frontend/src/app/<route>/page.tsx`. Use RSC +
`serverGet` for content pages (see `/sources`), client components + `apiGet`
for interactive ones (see `/exercises`). Nav lives in
`src/components/shell.tsx` (NAV array). Use tokens: `card`, `text-muted`,
`border-app` classes; dark mode is class-based — never hardcode colors.
Add vitest tests next to components.

**Extend the anatomy taxonomy:** add to
`app/taxonomy/anatomy_data.py` (respect `structure_type`; small/overlooked
structures get `is_small_overlooked=True`), re-run `seed`, then check
`/coverage` — coverage stats recompute automatically.

**New dataset version:** `app.cli snapshot vX.Y.Z --label … --notes …` then
regenerate `exports/`. Never rewrite an existing version — versions are pins.

## 9. Testing & Definition of Done

```bash
cd backend  && .venv/bin/python -m pytest        # 75 passed (uses real PG:
                                                 #  EASEUR_DATABASE_URL → easeur_test,
                                                 #  runs alembic migrations, truncates
                                                 #  between tests)
cd frontend && npm test                          # 31 passed (vitest + RTL, jsdom)
cd frontend && npx tsc --noEmit                  # must be clean
cd frontend && npx next build                    # must build (run AFTER stopping
                                                 #  `npm run dev` — shared .next dir)
```

Any change is done when: tests pass (with new tests for new behavior), `tsc`
clean, docs updated if behavior/contract changed (this file, DECISIONS.md,
implementation report), and the v0.1.0 baseline (§6) still reproduces after a
clean replay unless the change intentionally moves it.

**Frontend gotchas learned the hard way:**
- `vitest.setup.ts` must keep the explicit `afterEach(cleanup)` — RTL
  auto-cleanup does NOT register without `globals: true`, and leaked DOM made
  tests pass falsely.
- Pages using `useSearchParams()` must be wrapped in `<Suspense>` or
  `next build` fails prerendering.
- `router.replace()` must receive PAGE paths, never `/api/...` paths (the
  rewrite proxy serves them as raw JSON — this bug shipped once; see
  `src/lib/exercise-filters.ts` + its tests).
- Client-side `next build` while `npm run dev` is running corrupts `.next`;
  stop dev first.

**Backend gotchas:** chained `selectinload(A.b).selectinload(B.c)` requires a
real relationship chain — `Exercise.sources.source_document` needs two separate
`selectinload` options (see `services/query.py`). Bulk-deleting ingested data
must respect FK order: review items → conflicts → provenance →
exercise_sources → exercises → crawl jobs → source_documents.

## 10. Current state & known gaps (as of v0.1.0 / 2026-09)

Done: full stack, 184 exercises (148 approved curated + 36 pending aggregated),
121 structures (93% covered), 10 sources, 55 dup pairs awaiting review,
0 conflicts, snapshot v0.1.0, 13/13 illustrations, 106 tests green.

Known gaps (in priority order):
1. 55 duplicate pairs need human adjudication → then approve the 36 pending
   aggregated records → snapshot v0.2.0.
2. Corpus breadth: 6 pages / 3 domains aggregated. Next targets already seeded
   in `LIVE_SEED_URLS`: arthritis-uk.org per-joint pages + PDFs, NHS inform
   per-joint pages, dynamichealth.nhs.uk lower-back set.
3. 8 structures with zero exercises — see `/coverage?filter=missing`; use as
   crawl prioritization.
4. No semantic/embedding dedup stage yet (planned once ≥400 records; review-only
   threshold).
5. AI enrichment wired but disabled by design (needs provider key + policy signoff).
6. Docker Compose is the only packaged deployment; no CI pipeline yet.

Branch: all work goes to `arena/01a06df8-exercise-dataset` (PR #1 → main).
Commit style: imperative subject + body explaining why.
