from backend.models.junta_vecinal import JuntaVecinal
from backend.models.rol import Rol
from backend.models.usuario import Usuario
from backend.models.tipo_incidente import TipoIncidente
from backend.models.zona_caliente import ZonaCaliente
from backend.models.reporte import Reporte
from backend.models.evidencia import Evidencia
from backend.models.alerta import Alerta
from backend.models.prediccion_ia import PrediccionIA
from backend.models.notificacion import Notificacion
from backend.models.usuario_notificacion import UsuarioNotificacion

__all__ = [
    "JuntaVecinal", "Rol", "Usuario", "TipoIncidente", "ZonaCaliente",
    "Reporte", "Evidencia", "Alerta", "PrediccionIA", "Notificacion",
    "UsuarioNotificacion",
]
