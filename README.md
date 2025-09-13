# Orchestrated AI File Pipeline

## Prerequisites

### Redis (Upstash)
- Ensure you have an Upstash Redis instance.
- Create environment variables in `.env`:
  ```dotenv
  UPSTASH_REDIS_REST_URL=<your-upstash-url>
  UPSTASH_REDIS_REST_TOKEN=<your-upstash-token>
  ```

### Postgres (Neon)
- You can use Neon Postgres serverless.
- Set in `.env`:
  ```dotenv
  DATABASE_URL=<your-neon-connection-string>
  ```

### AI Gateway
- Install your AI Gateway SDK (example placeholder):
  ```bash
  npm install ai-gateway-sdk
  ```
- Set your API key or OIDC in `.env`:
  ```dotenv
  AI_GATEWAY_API_KEY=<your-api-key>
  ```

## Installation

### Backend
```bash
cd backend
python -m venv .venv
. .venv/Scripts/activate    # Windows PowerShell
pip install -r requirements.txt
```

### Frontend (Next.js + shadcn UI)
```bash
cd frontend
npm install               # installs Next.js, React, Tailwind, ESLint
# install UI & integrations
npm install @shadcn/ui @upstash/redis pg ai-gateway-sdk socket.io-client
npm install -D @types/socket.io-client
npx shadcn@latest add sidebar-16  # or sidebar-11 / sidebar-12
```

## Dependencies

### Backend (Python)
Install using the `requirements.txt`:
```bash
python -m venv .venv
. .venv/Scripts/activate  # Windows PowerShell
pip install -r requirements.txt
```
`requirements.txt` contains:
```
redis==4.5.1
pydantic==1.10.9
psycopg2-binary==2.9.7
python-dotenv==1.0.0
fastapi==0.95.0
uvicorn==0.23.2
```

### Frontend (Node)
```bash
npm install
npm install @shadcn/ui @upstash/redis pg ai-gateway-sdk socket.io-client
npm install -D @types/socket.io-client
```  

## Environment Examples
### Root `.env.example`
```dotenv
UPSTASH_REDIS_REST_URL=
UPSTASH_REDIS_REST_TOKEN=
DATABASE_URL=
AI_GATEWAY_API_KEY=
```
### Frontend `.env.local.example`
```dotenv
NEXT_PUBLIC_WS_URL=ws://localhost:8000
```

## Running Locally

1. Start Redis Streams setup:
   ```bash
   cd backend/infra
   python init_redis_streams.py
   ```
2. Launch Orchestrator API server:
   ```bash
   cd backend
   uvicorn orchestrator:app --reload
   ```
3. Run Next.js Frontend:
   ```bash
   cd frontend
   npm run dev
   ```

Open http://localhost:3000 for your control panel with six real-time chat interfaces.