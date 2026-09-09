# DECISIONS.md — Easeur Exercise Knowledge Base

Architecture and product decisions, with rationale. Companion to the final
implementation report (`docs/implementation-report.md`). Dates are 2026-09.

---

## D1 — Modular monolith, no microservices

**Decision.** One FastAPI application contains taxonomy, pipeline, review and
export logic as internal modules (`app/services/*`, `app/pipeline/*`). Crawler
and API share one process boundary (crawler runs are CLI-triggered jobs, not a
separate service). Frontend is a single Next.js app.

**Why.** Team size and data volume (hundreds of sources, tens of thousands of
records) don't justify distribution. A monolith keeps provenance/review
transactions ACID across pipeline and queue tables, which is the core product
guarantee.

**Rejected.** Crawler-as-a-service / message queue (Celery, Kafka): added
operational surface with no benefit at this scale. Long live crawls run via
`python -m app.cli pipeline crawl` in a worker container if needed.

## D2 — PostgreSQL + SQLAlchemy 2.0 (typed) + Alembic from day one

**Decision.** Real relational DB with migrations, unique constraints and
(native) PostgreSQL array columns for aliases/AI-field lists. Enum types are
database-level (`Enum(...)`), not free strings.

**Why.** Dedup/merge, provenance chains and audit logs rely on FK integrity;
SQLite was rejected because enum/array behavior and transaction semantics
diverge. Alembic migrations ship and are exercised by the test suite
(`command.upgrade(head)` in conftest), so migration drift is caught in CI.

## D3 — Provenance is a first-class table, not a column

**Decision.** `provenance` rows record (exercise, field, value, origin,
source_document, ai_model, confidence). Origins:
`source_fact | normalized | curated | ai_inference | human_reviewed`.

**Why.** The spec's central requirement ("distinguish human-verified vs
AI-suggested vs machine-parsed") is field-level, not record-level: one exercise
can have source-fact instructions and an AI-suggested difficulty. Record-level
flags can't express that.

## D4 — Extraction confidence ladder; AI is enrichment, never the parser

**Decision.** Fixed confidence by extraction method: JSON-LD 0.90 → structured
HTML 0.80 → table 0.72 → semantic HTML 0.62 → plain text 0.45 → AI 0.40.
Any record with `ai_inference` provenance enters `pending_review` regardless of
score; AI candidates per run are hard-capped (`ai_max_candidates_per_run=25`).

**Why.** Predictable confidence semantics auditable in code; prevents the
failure mode where AI-generated content silently dominates the dataset. When no
AI key is configured the pipeline runs fully deterministic.

## D5 — Dedup ladder with conservative auto-merge

**Decision.** Stages: exact (normalized name) → alias → structured comparison
(name similarity × anatomy overlap × category) → no embedding/semantic stage in
v0.1 (see Limitations). Auto-merge only at ≥ 0.99 total similarity **and**
compatible regions. Everything ≥ 0.72 (or ≥ 0.60 with an alias hit) queues for
human review; reviewer can choose which record survives
(`edits.keep = primary | related`).

**Why.** A wrong auto-merge destroys provenance from one source and is hard to
detect later. Tuned after observing 196 noisy pairs at a 0.60 threshold
(e.g. "Internal Rotation" vs "External Rotation" at 0.8+ name similarity but
conflicting anatomy) — anatomy incompatibility now suppresses scores.

## D6 — Conflicts are recorded, never silently resolved

**Decision.** When two source documents disagree on a field (e.g. different
muscle lists), a `data_conflicts` row stores both values with both source
references. Nothing picks a winner automatically; resolution happens through
the review queue and is audit-logged.

## D7 — Licensing posture is conservative and explicit

**Decision.** Every source carries license / commercial-use / attribution
fields. Unknown → excluded from redistribution posture and flagged. The corpus
stores **structured facts, metadata and bounded excerpts with links** — never
full article text. Exercise **media** is never scraped from sources: visuals
are (a) project-owned AI-generated illustrations (`backend/media/exercises/`,
tracked in `app/media_registry.py` with license metadata `ai-generated`, served
under `/static/exercises/`, exposed via the `media[]` API field and exports),
and (b) animated SVG movement previews rendered client-side from structured
data (position + movement pattern + target regions — code, not media). A
future `media_assets` table can hold source-licensed photos/GIFs when a source
explicitly permits reuse; the serializer contract (`kind/url/license/credit`)
is shaped for that. Every exercise additionally carries outbound
`exercise_references` — official demonstration pages (exact source document
for aggregated records; authoritative program pages per body region for
curated ones) — so users can always verify the movement at the source, where
the original images/GIFs/videos live.

**Why.** workout.easeur.com is commercial; "ask forgiveness" scraping is not an
option. Facts themselves are not copyrightable, but expression — including
photos and GIFs — is, so imagery is generated or rendered, never copied.

## D8 — Crawler: replay corpus + live mode, robots-first, SSRF-guarded

**Decision.** The pipeline has two modes: **live** (HTTP fetch with robots.txt
check, per-domain rate limiting ≥ 3 s, identified UA
`EaseurExerciseBot/1.0 (+https://easeur.com/bot)`, no JS execution, disk cache)
and **replay** (deterministic from `backend/corpus/` snapshots, used for tests
and reproducible ingests). All URLs pass SSRF validation (scheme/host allow,
private/link-local/metadata IP block, DNS resolution pinning, port allow-list,
CRLF rejection); robots.txt responses are snapshotted per domain for audit.

**Why.** Reproducibility: a corpus replay produces byte-identical results in
CI without network. The robots-404 case is treated as allow (per RFC 9309) but
recorded.

## D9 — Anatomy taxonomy is an owned dataset, extended by structure type

**Decision.** 16 body regions / 29 muscle groups / 121 structures seeded from
`app/taxonomy/anatomy_data.py`, with `structure_type` distinguishing muscle /
tendon / ligament / fascia / nerve. Small-and-overlooked structures (levator
scapulae, deep neck flexors, pelvic floor, intrinsic foot…) are explicitly
flagged `is_small_overlooked` and drive coverage reporting.

**Why.** The spec's core differentiator vs generic exercise databases is
anatomical completeness; owning the taxonomy (rather than linking out) lets
coverage gaps be measured and guides crawling priorities.

## D10 — Consumers read the API only; versions pin snapshots

**Decision.** EaseurWorkout (future) consumes `/api/v1/*` exclusively — no DB
access, ever. Default listing serves `status=approved` only; research endpoints
(`?status=all`, provenance include) serve the review UI. Dataset versions are
content-hashed snapshots (`dataset_versions`) with JSON/JSONL/CSV export
endpoints.

## D11 — Review queue + audit log are the trust boundary

**Decision.** All uncertain outcomes (duplicate pairs, conflicts,
low-confidence, unknown licensing, medical-claim language) converge on one
`review_queue` with priority and typed items; actions (approve/reject/merge/
split/flag/dismiss) write `audit_log` rows with actor + notes. Merges keep both
names (loser name → alias of winner) and re-point sources.

## D12 — Frontend: Next.js App Router, server-first, dark/light by default

**Decision.** Server Components fetch the API directly for content pages;
interactive pages (explorer, review, coverage) are client components using the
relative `/api/v1` path proxied by a Next rewrite (no CORS exposure in the
browser path). Tailwind v4 design tokens, class-based dark mode with
system-preference default and no-flash inline script. No component library —
~15 small owned components (cards, bars, donut, badges, pagination, SVG body
map).

**Why.** Research UI needs bespoke data-dense layouts; a component library
fights more than it helps. The SVG body map is hand-built (2D front/back
silhouette with per-region coverage) to stay dependency-free and themeable.

## D13 — Testing strategy

**Decision.** Backend: pytest against a real PostgreSQL test DB created by
running the actual Alembic migrations; covers API contract, schema, auth,
SSRF/robots, extraction (incl. malformed HTML), dedup ladder, data-quality
sweeps and review flows (66 tests). Frontend: vitest + Testing Library on the
shared components (19 tests) plus `tsc --noEmit` and a production `next build`
gate.

**Why.** Testing against SQLite/mocks would hide enum/array/FK behavior that
this schema depends on.

## D14 — Deployment story for v0.1

**Decision.** `docker-compose.yml` (postgres + api + ui) is the supported
self-host path. CI-grade one-shot runs (seed, aggregate, export) go through
`python -m app.cli` subcommands so every pipeline step is replayable in any
environment.
