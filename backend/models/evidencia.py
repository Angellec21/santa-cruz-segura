from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.database import Base
import enum


class TipoArchivo(str, enum.Enum):
    imagen = "imagen"
    video = "video"
    audio = "audio"


class Evidencia(Base):
    __tablename__ = "evidencia"

    id_evidencia = Column(Integer, primary_key=True, autoincrement=True)
    id_reporte = Column(Integer, ForeignKey("reporte.id_reporte"), nullable=False)
    tipo_archivo = Column(Enum(TipoArchivo), nullable=False)
    ruta_archivo = Column(String(255), nullable=False)
    nombre_original = Column(String(255))
    fecha_subida = Column(DateTime, server_default=func.now())

    reporte = relationship("Reporte", back_populates="evidencias")
