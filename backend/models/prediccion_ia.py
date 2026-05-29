from sqlalchemy import Column, Integer, String, DECIMAL, Date, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.database import Base


class PrediccionIA(Base):
    __tablename__ = "prediccion_ia"

    id_prediccion = Column(Integer, primary_key=True, autoincrement=True)
    id_zona = Column(Integer, ForeignKey("zona_caliente.id_zona"), nullable=False)
    periodo_inicio = Column(Date, nullable=False)
    periodo_fin = Column(Date, nullable=False)
    nivel_predicho = Column(String(20), nullable=False)
    probabilidad = Column(DECIMAL(5, 4))
    features_json = Column(Text)
    fecha_generacion = Column(DateTime, server_default=func.now())

    zona = relationship("ZonaCaliente", back_populates="predicciones")
