from __future__ import annotations
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from backend.models.usuario import Usuario
from backend.schemas.prediccion import PrediccionResponse
from backend.services import ia_service
from backend.utils.deps import get_db, get_current_user, require_role, ROL_DIRECTIVO, ROL_ADMIN, ROL_AUTORIDAD

router = APIRouter(prefix="/ia", tags=["ia"])

_ROLES_IA = [ROL_DIRECTIVO, ROL_ADMIN, ROL_AUTORIDAD]


@router.post("/predecir/{id_zona}", response_model=PrediccionResponse)
def predecir(
    id_zona: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_role(_ROLES_IA)),
):
    return ia_service.predecir_zona(id_zona, db)


@router.get("/predicciones")
def predicciones_actuales(
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    rows = db.execute(text("""
        SELECT p.id_zona, z.nombre AS zona_nombre, z.nivel_riesgo,
               p.nivel_predicho, CAST(p.probabilidad AS FLOAT) AS probabilidad,
               p.periodo_inicio, p.periodo_fin, p.fecha_generacion
        FROM prediccion_ia p
        JOIN zona_caliente z ON z.id_zona = p.id_zona
        WHERE p.id_prediccion = (
            SELECT MAX(p2.id_prediccion) FROM prediccion_ia p2 WHERE p2.id_zona = p.id_zona
        )
        ORDER BY p.fecha_generacion DESC
    """)).mappings().all()
    return [dict(r) for r in rows]
