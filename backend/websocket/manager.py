from __future__ import annotations
import asyncio
import json
from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self._active: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self._active.append(websocket)

    def disconnect(self, websocket: WebSocket):
        try:
            self._active.remove(websocket)
        except ValueError:
            pass

    async def broadcast(self, event: dict):
        if not self._active:
            return
        payload = json.dumps(event)
        snapshot = list(self._active)
        results = await asyncio.gather(
            *[ws.send_text(payload) for ws in snapshot],
            return_exceptions=True,
        )
        for ws, result in zip(snapshot, results):
            if isinstance(result, Exception):
                self.disconnect(ws)

    @property
    def count(self) -> int:
        return len(self._active)


manager = ConnectionManager()
