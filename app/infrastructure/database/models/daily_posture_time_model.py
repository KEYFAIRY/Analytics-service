from sqlalchemy import Column, Integer, Numeric, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship

from app.infrastructure.database.models.base import Base

class DailyPosturesModel(Base):
    __tablename__ = "TiempoPosturasDiarias"

    # Primary keys
    id_student = Column(String(128), primary_key=True, nullable=False)
    id_scale = Column(Integer, primary_key=True, nullable=False)
    fecha = Column(Date, primary_key=True, nullable=False)

    # Time variables
    anio = Column(Integer, nullable=False)
    semana = Column(Integer, nullable=False)
    mes = Column(Integer, nullable=False)

    # Actual statistics
    tiempo_total = Column(Numeric, default=0)
    tiempo_mala_postura = Column(Numeric, default=0)
    tiempo_buena_postura = Column(Numeric, default=0)