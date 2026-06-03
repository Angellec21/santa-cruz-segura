from __future__ import annotations
from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from backend.models.usuario import Usuario
from backend.schemas.zona import ZonaResponse, HeatmapPoint
from backend.services import zona_service
from backend.utils.deps import get_db, get_current_user
from backend.utils import cache

router = APIRouter(prefix="/zonas", tags=["zonas"])


@router.get("", response_model=list[ZonaResponse])
def listar(
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    hit, val = cache.get("zonas:list", ttl=30)
    if hit:
        return val
    result = zona_service.listar_zonas(db)
    cache.set("zonas:list", result)
    return result


@router.get("/heatmap/all")
def heatmap_all(
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    """Devuelve todos los puntos de heatmap en una sola query — reemplaza los 10 requests individuales."""
    hit, val = cache.get("zonas:heatmap:all", ttl=30)
    if hit:
        return val
    intensidad_map = {"bajo": 0.3, "medio": 0.5, "alto": 0.8, "critico": 1.0}
    rows = db.execute(text("""
        SELECT r.latitud, r.longitud, z.nivel_riesgo
        FROM reporte r
        JOIN zona_caliente z ON z.id_zona = r.id_zona
    """)).mappings().all()
    result = [
        {"lat": float(r.latitud), "lng": float(r.longitud),
         "intensity": intensidad_map.get(r.nivel_riesgo, 0.3)}
        for r in rows
    ]
    cache.set("zonas:heatmap:all", result)
    return result


@router.get("/{id_zona}/heatmap", response_model=list[HeatmapPoint])
def heatmap(
    id_zona: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    key = f"zonas:heatmap:{id_zona}"
    hit, val = cache.get(key, ttl=30)
    if hit:
        return val
    result = zona_service.heatmap_zona(id_zona, db)
    cache.set(key, result)
    return result
