from __future__ import annotations
from fastapi import APIRouter, Depends, UploadFile, File, Query
from sqlalchemy.orm import Session
from backend.models.usuario import Usuario
from backend.schemas.reporte import ReporteCreate, ReporteResponse, ReporteEstadoUpdate
from backend.services import reporte_service
from backend.utils.deps import get_db, get_current_user, require_role, ROL_DIRECTIVO, ROL_ADMIN
from backend.websocket.manager import manager

router = APIRouter(prefix="/reportes", tags=["reportes"])


@router.post("", response_model=ReporteResponse, status_code=201)
async def crear(
    data: ReporteCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    reporte = reporte_service.crear_reporte(data, current_user.id_usuario, db)
    zona = reporte.zona
    await manager.broadcast({
        "tipo": "nuevo_reporte",
        "id_reporte": reporte.id_reporte,
        "latitud": float(reporte.latitud),
        "longitud": float(reporte.longitud),
        "tipo_incidente": reporte.tipo_incidente.nombre if reporte.tipo_incidente else "",
        "nivel_zona": zona.nivel_riesgo.value if zona else "bajo",
        "id_zona": reporte.id_zona,
    })
    return reporte


@router.get("/mis", response_model=list[ReporteResponse])
def mis_reportes(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    return reporte_service.listar_reportes(db, id_usuario=current_user.id_usuario)


@router.get("", response_model=list[ReporteResponse])
def listar(
    id_zona: int | None = Query(None),
    id_tipo: int | None = Query(None),
    estado: str | None = Query(None),
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    return reporte_service.listar_reportes(db, id_zona, id_tipo, estado)


@router.put("/{id_reporte}/estado", response_model=ReporteResponse)
def cambiar_estado(
    id_reporte: int,
    data: ReporteEstadoUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_role([ROL_DIRECTIVO, ROL_ADMIN])),
):
    return reporte_service.actualizar_estado(id_reporte, data, db)


@router.post("/{id_reporte}/evidencia", status_code=201)
def subir_evidencia(
    id_reporte: int,
    archivo: UploadFile = File(...),
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    return reporte_service.guardar_evidencia(id_reporte, archivo, db)
