from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship

from app.infrastructure.database.models.base import Base

class WeeklyNotesModel(Base):
    __tablename__ = "NotasResumenDiarias"

    # Primary keys
    id_student = Column(String(128), primary_key=True, nullable=False)
    id_scale = Column(Integer, primary_key=True, nullable=False)
    fecha = Column(Date, primary_key=True, nullable=False)

    # Time variables
    anio = Column(Integer, nullable=False)
    semana = Column(Integer, nullable=False)
    mes = Column(Integer, nullable=False)

    # Actual statistics
    notas_correctas = Column(Integer, default=0)
    notas_incorrectas = Column(Integer, default=0)