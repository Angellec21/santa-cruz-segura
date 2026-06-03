import asyncio
import os
import time
from collections import defaultdict
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.exc import OperationalError, DatabaseError
from backend.routers import auth, usuarios, reportes, zonas, alertas, dashboard, ia
from backend.websocket.manager import manager

app = FastAPI(
    title="Santa Cruz Segura Predictiva",
    version="1.0.0",
    description="Plataforma colaborativa de predicción del delito para Santa Cruz, Bolivia",
)

app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate limiting en memoria: max 15 peticiones/minuto por IP en rutas de auth
_rl: dict[str, list[float]] = defaultdict(list)
_RL_PATHS = {"/auth/login", "/auth/register"}
_RL_LIMIT = 15
_RL_WINDOW = 60.0


@app.middleware("http")
async def rate_limit(request: Request, call_next):
    if request.url.path in _RL_PATHS:
        ip = request.client.host if request.client else "unknown"
        key = f"{request.url.path}:{ip}"
        now = time.monotonic()
        _rl[key] = [t for t in _rl[key] if now - t < _RL_WINDOW]
        if len(_rl[key]) >= _RL_LIMIT:
            return JSONResponse(
                status_code=429,
                content={"detail": "Demasiadas solicitudes. Espera un momento."},
            )
        _rl[key].append(now)
    return await call_next(request)


@app.exception_handler(OperationalError)
@app.exception_handler(DatabaseError)
async def db_error_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=503,
        content={"detail": "Base de datos no disponible. Intenta en unos segundos."},
    )


@app.get("/health", tags=["infra"])
async def health():
    return {"status": "ok", "ws_connections": manager.count}


@app.on_event("startup")
async def warmup_cache():
    async def _warm():
        await asyncio.sleep(4)
        try:
            from backend.database import SessionLocal
            from backend.services.zona_service import listar_zonas
            from backend.services.alerta_service import listar_alertas
            from backend.utils import cache
            from sqlalchemy import text
            db = SessionLocal()
            try:
                zonas = listar_zonas(db)
                cache.set("zonas:list", zonas)
                intensidad_map = {"bajo": 0.3, "medio": 0.5, "alto": 0.8, "critico": 1.0}
                rows = db.execute(text("""
                    SELECT r.latitud, r.longitud, z.nivel_riesgo
                    FROM reporte r JOIN zona_caliente z ON z.id_zona = r.id_zona
                """)).mappings().all()
                cache.set("zonas:heatmap:all", [
                    {"lat": float(r.latitud), "lng": float(r.longitud),
                     "intensity": intensidad_map.get(r.nivel_riesgo, 0.3)}
                    for r in rows
                ])
                cache.set("alertas:list", listar_alertas(db))
            finally:
                db.close()
        except Exception:
            pass
    asyncio.create_task(_warm())



app.include_router(auth.router)
app.include_router(usuarios.router)
app.include_router(reportes.router)
app.include_router(zonas.router)
app.include_router(alertas.router)
app.include_router(dashboard.router)
app.include_router(ia.router)

_WS_PING_INTERVAL = 25.0


@app.websocket("/ws/mapa")
async def websocket_mapa(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            try:
                await asyncio.wait_for(websocket.receive_text(), timeout=_WS_PING_INTERVAL)
            except asyncio.TimeoutError:
                await websocket.send_text('{"tipo":"ping"}')
    except (WebSocketDisconnect, Exception):
        manager.disconnect(websocket)


os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
