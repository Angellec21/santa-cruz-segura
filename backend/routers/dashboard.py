from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from backend.models.usuario import Usuario
from backend.utils.deps import get_db, get_current_user, require_role, ROL_DIRECTIVO, ROL_ADMIN, ROL_AUTORIDAD

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

_ROLES_DASH = [ROL_DIRECTIVO, ROL_ADMIN, ROL_AUTORIDAD]


@router.get("/resumen")
def resumen(
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_role(_ROLES_DASH)),
):
    rows = db.execute(text("SELECT * FROM v_resumen_barrio")).mappings().all()
    return [dict(r) for r in rows]


@router.get("/tendencia")
def tendencia(
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_role(_ROLES_DASH)),
):
    rows = db.execute(text("""
        SELECT DATE(fecha_reporte) AS fecha, COUNT(*) AS total
        FROM reporte
        WHERE fecha_reporte >= CURDATE() - INTERVAL 29 DAY
        GROUP BY DATE(fecha_reporte)
        ORDER BY fecha
    """)).mappings().all()
    return [dict(r) for r in rows]


@router.get("/tipos")
def tipos(
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_role(_ROLES_DASH)),
):
    rows = db.execute(text("""
        SELECT ti.nombre, COUNT(r.id_reporte) AS total
        FROM tipo_incidente ti
        LEFT JOIN reporte r ON ti.id_tipo = r.id_tipo
            AND r.fecha_reporte >= CURDATE() - INTERVAL 30 DAY
        GROUP BY ti.id_tipo, ti.nombre
        ORDER BY total DESC
    """)).mappings().all()
    return [dict(r) for r in rows]
