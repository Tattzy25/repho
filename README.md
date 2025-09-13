# Orchestrated AI File Pipeline

This project moves jobs through multiple phases and reports any failures in real time.

## Prerequisites
- Python 3.10+
- Node.js 18+
- Redis instance (e.g., Upstash) – set `UPSTASH_REDIS_URL` in `.env`
- Postgres database (optional) – set `DATABASE_URL` for persistent error logs

## Backend setup
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Unix or macOS
# .venv\\Scripts\\Activate.ps1  # Windows PowerShell
pip install -r requirements.txt
```
Create `.env` at the project root:
```dotenv
UPSTASH_REDIS_URL=
DATABASE_URL=
```

### Start services
1. Initialise Redis streams
   ```bash
   python infra/init_redis_streams.py
   ```
2. Run the orchestrator
   ```bash
   python orchestrator.py
   ```
3. Launch the API server (WebSocket)
   ```bash
   uvicorn server:app --reload
   ```

## Frontend setup
```bash
cd frontend
npm install
npm run dev
```
Visit the printed URL (usually http://localhost:5173). The control panel lists the commands above and error alerts appear as toasts.
