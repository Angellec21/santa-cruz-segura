from sqlalchemy import Column, Integer, String, Text, DECIMAL, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.database import Base


class JuntaVecinal(Base):
    __tablename__ = "junta_vecinal"

    id_junta = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    distrito = Column(String(50), nullable=False)
    descripcion = Column(Text)
    latitud_centro = Column(DECIMAL(10, 8))
    longitud_centro = Column(DECIMAL(11, 8))
    activa = Column(Boolean, default=True)
    fecha_registro = Column(DateTime, server_default=func.now())

    usuarios = relationship("Usuario", back_populates="junta")
    zonas = relationship("ZonaCaliente", back_populates="junta")
    alertas = relationship("Alerta", back_populates="junta")
