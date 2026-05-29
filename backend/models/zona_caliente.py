from sqlalchemy import Column, Integer, String, DECIMAL, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.database import Base
import enum


class NivelRiesgo(str, enum.Enum):
    bajo = "bajo"
    medio = "medio"
    alto = "alto"
    critico = "critico"


class ZonaCaliente(Base):
    __tablename__ = "zona_caliente"

    id_zona = Column(Integer, primary_key=True, autoincrement=True)
    id_junta = Column(Integer, ForeignKey("junta_vecinal.id_junta"), nullable=False)
    nombre = Column(String(100), nullable=False)
    latitud_centro = Column(DECIMAL(10, 8), nullable=False)
    longitud_centro = Column(DECIMAL(11, 8), nullable=False)
    radio_metros = Column(Integer, default=200)
    nivel_riesgo = Column(Enum(NivelRiesgo), default=NivelRiesgo.bajo)
    total_reportes_30d = Column(Integer, default=0)
    ultima_actualizacion = Column(DateTime, server_default=func.now(), onupdate=func.now())

    junta = relationship("JuntaVecinal", back_populates="zonas")
    reportes = relationship("Reporte", back_populates="zona")
    alertas = relationship("Alerta", back_populates="zona")
    predicciones = relationship("PrediccionIA", back_populates="zona")
