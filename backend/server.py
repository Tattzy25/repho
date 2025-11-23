import os
import asyncio
import json
import redis.asyncio as redis
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Set
from dotenv import load_dotenv

load_dotenv()
load_env = os.getenv
redis_url = os.getenv("UPSTASH_REDIS_URL")
if redis_url is None:
    raise RuntimeError(
        "UPSTASH_REDIS_URL is not set. Use the Redis URL (rediss://...) from Upstash, not the REST URL/token."
    )

r = redis.from_url(redis_url, decode_responses=True)
CHANNEL_ERROR = "phase_error"

app = FastAPI()

class ConnectionManager:
    def __init__(self) -> None:
        self.active: Set[WebSocket] = set()

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active.add(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        self.active.discard(websocket)

    async def broadcast(self, message: str) -> None:
        for ws in list(self.active):
            try:
                await ws.send_text(message)
            except Exception:
                self.active.discard(ws)

manager = ConnectionManager()

@app.on_event("startup")
async def redis_listener() -> None:
    async def reader() -> None:
        pubsub = r.pubsub()
        await pubsub.subscribe(CHANNEL_ERROR)
        try:
            async for msg in pubsub.listen():
                if msg["type"] == "message":
                    await manager.broadcast(msg["data"])
        finally:
            await pubsub.close()
    asyncio.create_task(reader())

@app.websocket("/ws/errors")
async def websocket_endpoint(websocket: WebSocket) -> None:
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive; messages are sent from redis_listener
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
