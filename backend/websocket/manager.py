from __future__ import annotations
import json
from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self._active: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self._active.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self._active.remove(websocket)

    async def broadcast(self, event: dict):
        payload = json.dumps(event)
        for ws in list(self._active):
            try:
                await ws.send_text(payload)
            except Exception:
                self._active.remove(ws)


manager = ConnectionManager()
