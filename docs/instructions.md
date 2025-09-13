# Instructions

Logs are stored in Postgres using the logic defined in `backend-mcp/src/db.ts`.
To persist logs in both Postgres and Redis, extend `backend-mcp/src/db.ts` to also write to a Redis client.

# Interface Controls

The client provides **Start**, **Pause**, and **Stop** buttons for managing the service.

## Start
- Sends `POST /start` to the backend.
- Initiates processing on the server.

## Pause
- Sends `POST /pause` to the backend.
- Temporarily halts processing while retaining state.

## Stop
- Sends `POST /stop` to the backend.
- Terminates processing and resets state.

Ensure the backend MCP server from `backend-mcp/src/index.ts` is running on port 3001 before using the client.
