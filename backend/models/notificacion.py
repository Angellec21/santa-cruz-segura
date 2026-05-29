from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.database import Base


class Notificacion(Base):
    __tablename__ = "notificacion"

    id_notificacion = Column(Integer, primary_key=True, autoincrement=True)
    id_alerta = Column(Integer, ForeignKey("alerta.id_alerta"), nullable=False)
    titulo = Column(String(150), nullable=False)
    mensaje = Column(Text, nullable=False)
    fecha_envio = Column(DateTime, server_default=func.now())

    alerta = relationship("Alerta", back_populates="notificaciones")
    destinatarios = relationship("UsuarioNotificacion", back_populates="notificacion")
