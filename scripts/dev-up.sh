#!/usr/bin/env bash
# Cold-start the Easeur Exercise Knowledge Base in this sandbox/VM.
# Idempotent: safe to run repeatedly; skips work that's already done.
#
# Usage:  bash scripts/dev-up.sh          (build: venvs, postgres, seed, npm install)
#         bash scripts/dev-up.sh --serve  (also launch API + UI servers in foreground)
set -euo pipefail
cd "$(dirname "$0")/.."
ROOT=$(pwd)

PG_DATA=/home/user/.cache/easeur-pg
PG_LOG=/home/user/.cache/pg.log
PGVENV=/tmp/pgvenv
PGBIN=$PGVENV/lib/python3.11/site-packages/pgserver/pginstall/bin

log() { printf "\033[1;34m[easeur]\033[0m %s\n" "$*"; }

# ---------- 1. Python environments ----------
if [ ! -x backend/.venv/bin/python ]; then
  log "creating backend venv…"
  python3 -m venv backend/.venv
  backend/.venv/bin/pip install -q -r backend/requirements.txt -r backend/requirements-dev.txt
else
  log "backend venv: present"
fi

# ---------- 2. PostgreSQL (embedded, UTF-8) ----------
if [ ! -x "$PGBIN/pg_ctl" ]; then
  log "installing embedded postgres (pgserver)…"
  python3 -m venv "$PGVENV"
  "$PGVENV/bin/pip" install -q pgserver
fi

if ! "$PGBIN/pg_ctl" -D "$PG_DATA" status >/dev/null 2>&1; then
  if [ ! -f "$PG_DATA/PG_VERSION" ]; then
    log "initialising postgres cluster (UTF-8)…"
    mkdir -p /home/user/.cache
    "$PGBIN/initdb" -D "$PG_DATA" -U easeur --auth=trust --encoding=UTF8 --locale=C >/dev/null
  fi
  log "starting postgres…"
  "$PGBIN/pg_ctl" -D "$PG_DATA" -l "$PG_LOG" start \
    -o "-k $PG_DATA -p 5432" >/dev/null
  sleep 2
else
  log "postgres: running"
fi

for db in easeur easeur_test; do
  "$PGBIN/psql" -h 127.0.0.1 -U easeur -d postgres -tAc \
    "SELECT 1 FROM pg_database WHERE datname='$db'" | grep -q 1 \
    || "$PGBIN/psql" -h 127.0.0.1 -U easeur -d postgres -c "CREATE DATABASE $db OWNER easeur;" >/dev/null
done
log "databases ready (easeur, easeur_test)"

# ---------- 3. Schema + data (skip if already populated) ----------
COUNT=$(cd backend && .venv/bin/python - <<'EOF'
from app.db import engine
from sqlalchemy import text
with engine.connect() as c:
    try:
        print(c.execute(text("select count(*) from exercises")).scalar_one())
    except Exception:
        print(0)
EOF
)
if [ "${COUNT:-0}" -lt 148 ]; then
  log "migrating + seeding + aggregating (deterministic replay)…"
  ( cd backend
    .venv/bin/python -m app.cli init-db
    .venv/bin/python -m app.cli seed
    .venv/bin/python -m app.cli pipeline run-all
    .venv/bin/python -m app.cli snapshot v0.1.0 --label "Initial aggregation" \
      --notes "Curated seed (148) + first controlled aggregation via replay corpus" || true
    for ds in exercises muscles body-regions; do
      .venv/bin/python -m app.cli export --dataset "$ds" --fmt json >/dev/null
    done )
else
  log "database already populated ($COUNT exercises) — skipping seed"
fi

# ---------- 4. Frontend deps ----------
if [ ! -d frontend/node_modules ]; then
  log "installing frontend dependencies…"
  ( cd frontend && npm install --no-audit --no-fund )
else
  log "node_modules: present"
fi

log "build complete."
if [ "${1:-}" = "--serve" ]; then
  log "starting API on :8000 and UI on :3000 (Ctrl-C to stop)…"
  trap 'kill 0' EXIT
  ( cd backend && .venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 ) &
  ( cd frontend && npm run dev ) &
  wait
else
  log "now start the servers:"
  log "  (cd backend && .venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000)"
  log "  (cd frontend && npm run dev)   # http://localhost:3000"
fi
