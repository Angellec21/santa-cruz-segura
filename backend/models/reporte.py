from sqlalchemy import Column, Integer, Text, DECIMAL, Enum, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.database import Base
import enum


class EstadoReporte(str, enum.Enum):
    pendiente = "pendiente"
    verificado = "verificado"
    resuelto = "resuelto"
    descartado = "descartado"


class Reporte(Base):
    __tablename__ = "reporte"

    id_reporte = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"), nullable=False)
    id_zona = Column(Integer, ForeignKey("zona_caliente.id_zona"), nullable=False)
    id_tipo = Column(Integer, ForeignKey("tipo_incidente.id_tipo"), nullable=False)
    descripcion = Column(Text)
    latitud = Column(DECIMAL(10, 8), nullable=False)
    longitud = Column(DECIMAL(11, 8), nullable=False)
    estado = Column(Enum(EstadoReporte), default=EstadoReporte.pendiente)
    anonimo = Column(Boolean, default=False)
    fecha_incidente = Column(DateTime, nullable=False)
    fecha_reporte = Column(DateTime, server_default=func.now())

    usuario = relationship("Usuario", back_populates="reportes")
    zona = relationship("ZonaCaliente", back_populates="reportes")
    tipo_incidente = relationship("TipoIncidente", back_populates="reportes")
    evidencias = relationship("Evidencia", back_populates="reporte")
