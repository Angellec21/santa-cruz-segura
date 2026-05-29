from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.database import Base


class UsuarioNotificacion(Base):
    __tablename__ = "usuario_notificacion"

    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"), primary_key=True)
    id_notificacion = Column(Integer, ForeignKey("notificacion.id_notificacion"), primary_key=True)
    leida = Column(Boolean, default=False)
    fecha_lectura = Column(DateTime)

    usuario = relationship("Usuario", back_populates="notificaciones")
    notificacion = relationship("Notificacion", back_populates="destinatarios")
