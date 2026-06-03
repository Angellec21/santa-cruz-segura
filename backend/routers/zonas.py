from __future__ import annotations
from fastapi import APIRouter, Depends
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
