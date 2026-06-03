from __future__ import annotations
from fastapi import APIRouter, Depends, UploadFile, File, Query
from sqlalchemy.orm import Session
from backend.models.usuario import Usuario
from backend.schemas.reporte import ReporteCreate, ReporteResponse, ReporteEstadoUpdate, ReporteGestionResponse
from backend.utils.deps import ROL_AUTORIDAD
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


@router.get("/gestion", response_model=list[ReporteGestionResponse])
def listar_gestion(
    id_zona: int | None = Query(None),
    id_tipo: int | None = Query(None),
    estado: str | None = Query(None),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role([ROL_DIRECTIVO, ROL_AUTORIDAD, ROL_ADMIN])),
):
    """Lista todos los reportes con nombre del reportante. Admins ven nombre aunque sea anónimo."""
    reportes = reporte_service.listar_reportes(db, id_zona, id_tipo, estado, with_evidencias=True)
    es_admin = current_user.rol.nombre == ROL_ADMIN
    resultado = []
    for r in reportes:
        d = ReporteGestionResponse.model_validate(r)
        d.tipo_nombre = r.tipo_incidente.nombre if r.tipo_incidente else None
        d.zona_nombre = r.zona.nombre if r.zona else None
        if es_admin or not r.anonimo:
            d.reporter_nombre   = r.usuario.nombre   if r.usuario else None
            d.reporter_apellido = r.usuario.apellido if r.usuario else None
        else:
            d.reporter_nombre   = "Anónimo"
            d.reporter_apellido = ""
        resultado.append(d)
    return resultado


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
async def subir_evidencia(
    id_reporte: int,
    archivo: UploadFile = File(...),
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    return await reporte_service.guardar_evidencia(id_reporte, archivo, db)
