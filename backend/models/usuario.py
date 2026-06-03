from sqlalchemy import Column, Integer, String, Boolean, DateTime, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.database import Base


class Usuario(Base):
    __tablename__ = "usuario"

    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    id_junta = Column(Integer, ForeignKey("junta_vecinal.id_junta"), nullable=False)
    id_rol = Column(Integer, ForeignKey("rol.id_rol"), nullable=False)
    nombre = Column(String(80), nullable=False)
    apellido = Column(String(80), nullable=False)
    email = Column(String(120), nullable=False, unique=True)
    telefono = Column(String(20))
    password_hash = Column(String(255), nullable=False)
    latitud = Column(DECIMAL(10, 8))
    longitud = Column(DECIMAL(11, 8))
    activo = Column(Boolean, default=True)
    email_verificado = Column(Boolean, default=False, nullable=False, server_default="0")
    token_verificacion = Column(String(100), nullable=True)
    session_id = Column(String(36), nullable=True)
    fecha_registro = Column(DateTime, server_default=func.now())

    junta = relationship("JuntaVecinal", back_populates="usuarios")
    rol = relationship("Rol", back_populates="usuarios")
    reportes = relationship("Reporte", foreign_keys="Reporte.id_usuario", back_populates="usuario")
    alertas_creadas = relationship("Alerta", back_populates="creador")
    notificaciones = relationship("UsuarioNotificacion", back_populates="usuario")
