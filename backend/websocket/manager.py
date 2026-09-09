from __future__ import annotations
import asyncio
from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self._connections: list[WebSocket] = []
        self._loop: asyncio.AbstractEventLoop | None = None

    def set_loop(self, loop: asyncio.AbstractEventLoop) -> None:
        self._loop = loop

    @property
    def count(self) -> int:
        return len(self._connections)

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self._connections.append(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        if websocket in self._connections:
            self._connections.remove(websocket)

    async def _broadcast(self, message: dict) -> None:
        muertas = []
        for ws in self._connections:
            try:
                await ws.send_json(message)
            except Exception:
                muertas.append(ws)
        for ws in muertas:
            self.disconnect(ws)

    def broadcast(self, message: dict) -> None:
        """Programa el envío del mensaje desde código síncrono (routers/services
        corren en un threadpool, no en el event loop donde viven los WebSocket)."""
        if self._loop is None:
            return
        asyncio.run_coroutine_threadsafe(self._broadcast(message), self._loop)


manager = ConnectionManager()
