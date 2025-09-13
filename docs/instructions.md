# Instructions

Logs are stored in Postgres using the logic defined in `backend-mcp/src/db.ts`.
To persist logs in both Postgres and Redis, extend `backend-mcp/src/db.ts` to also write to a Redis client.
