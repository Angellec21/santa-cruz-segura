from sqlalchemy import Column, Integer, String, Text, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.database import Base
import enum


class TipoAlerta(str, enum.Enum):
    preventiva = "preventiva"
    reactiva = "reactiva"
    informativa = "informativa"


class EstadoAlerta(str, enum.Enum):
    activa = "activa"
    resuelta = "resuelta"
    expirada = "expirada"


class Alerta(Base):
    __tablename__ = "alerta"

    id_alerta = Column(Integer, primary_key=True, autoincrement=True)
    id_zona = Column(Integer, ForeignKey("zona_caliente.id_zona"), nullable=False)
    id_junta = Column(Integer, ForeignKey("junta_vecinal.id_junta"), nullable=False)
    id_creador = Column(Integer, ForeignKey("usuario.id_usuario"), nullable=False)
    titulo = Column(String(150), nullable=False)
    descripcion = Column(Text)
    tipo = Column(Enum(TipoAlerta), nullable=False)
    estado = Column(Enum(EstadoAlerta), default=EstadoAlerta.activa)
    fecha_inicio = Column(DateTime, server_default=func.now())
    fecha_fin = Column(DateTime)

    zona = relationship("ZonaCaliente", back_populates="alertas")
    junta = relationship("JuntaVecinal", back_populates="alertas")
    creador = relationship("Usuario", back_populates="alertas_creadas")
    notificaciones = relationship("Notificacion", back_populates="alerta")
