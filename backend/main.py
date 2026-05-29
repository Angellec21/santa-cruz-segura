from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.routers import auth, usuarios, reportes, zonas, alertas, dashboard, ia
from backend.websocket.manager import manager
import os

app = FastAPI(
    title="Santa Cruz Segura Predictiva",
    version="1.0.0",
    description="Plataforma colaborativa de predicción del delito para Santa Cruz, Bolivia",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(usuarios.router)
app.include_router(reportes.router)
app.include_router(zonas.router)
app.include_router(alertas.router)
app.include_router(dashboard.router)
app.include_router(ia.router)


@app.websocket("/ws/mapa")
async def websocket_mapa(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)


os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
