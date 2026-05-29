from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from backend.database import Base


class TipoIncidente(Base):
    __tablename__ = "tipo_incidente"

    id_tipo = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(60), nullable=False, unique=True)
    descripcion = Column(Text)
    icono = Column(String(50))

    reportes = relationship("Reporte", back_populates="tipo_incidente")
