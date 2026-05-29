from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from backend.database import Base


class Rol(Base):
    __tablename__ = "rol"

    id_rol = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(30), nullable=False, unique=True)
    descripcion = Column(Text)

    usuarios = relationship("Usuario", back_populates="rol")
