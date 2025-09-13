# Interface Controls

The client now provides **Start**, **Pause**, and **Stop** buttons for managing the service.

## Start
- Sends `POST /start` to the backend.
- Initiates processing on the server.

## Pause
- Sends `POST /pause` to the backend.
- Temporarily halts processing while retaining state.

## Stop
- Sends `POST /stop` to the backend.
- Terminates processing and resets state.

Ensure the backend server from `backend-mcp/src/index.ts` is running on port 3001 before using the client.
