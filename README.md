# Orchestrated AI File Pipeline

## Documentation
- [System Blueprint](docs/blueprint.md)
- [Operational Rules](docs/rules.md)

## Overview
- Backend orchestrator consumes Redis stream events, validates each phase, and on failure both publishes an error to Redis and persists it to Postgres (when `DATABASE_URL` is set).
- FastAPI server bridges the `phase_error` Redis channel to a WebSocket at `/ws/errors` for live UI toasts.
- Frontend (Vite + React + shadcn/sonner) shows controls and subscribes to error events.

## Prerequisites
- Redis (Upstash): use the Redis protocol URL (`rediss://...`), not the REST URL/token. Local Redis (`redis://localhost:6379`) also works for development.
- Postgres (optional): set `DATABASE_URL` (e.g., Neon/Cloud/Postgres local) to persist orchestrator failures. Install a driver: `pip install 'psycopg[binary]'` (recommended) or `pip install psycopg2-binary`.

## Environment
Create a `.env` at the repository root:
```dotenv
# Use the Redis protocol URL (rediss://...), not REST URL/token
UPSTASH_REDIS_URL=rediss://:<password>@<host>:<port>

# Optional: enable Postgres error logging
DATABASE_URL=postgresql://user:pass@host:port/db
```

## Backend Setup
```bash
cd backend
python -m venv .venv
# Windows PowerShell
. .venv/Scripts/activate
pip install -r requirements.txt
# Optional Postgres driver for error logging
# pip install 'psycopg[binary]'
```

Initialize Redis streams (creates streams and a consumer group):
```bash
cd backend/infra
python init_redis_streams.py
```

Run the orchestrator (validates phases; publishes and logs failures):
```bash
# from repository root (uses .env at root)
python backend/orchestrator.py
```

Run the FastAPI WebSocket server (bridges `phase_error` → `/ws/errors`):
```bash
uvicorn backend.server:app --host 0.0.0.0 --port 8000 --reload
```

Keep the orchestrator and WebSocket server running in separate terminals.

## Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

- Dev UI: http://localhost:5173
- The ChatPanel auto-connects to `ws://localhost:8000/ws/errors` and raises toast alerts per error event.
- The Control Panel shows Start/Pause/Stop buttons (wired to `http://localhost:3001`). If you’re using the optional `backend-mcp` sample server, run it separately (ts-node/tsc not included here).

## Build for Production
```bash
cd frontend
npm install
npm run build
npm run preview
```

Ensure the orchestrator and FastAPI server are running as above while previewing the UI.

## Notes
- Audit schema example: see `backend/infra/audit_log.sql`.
- Models roster reference: `backend/models_config.py`.
