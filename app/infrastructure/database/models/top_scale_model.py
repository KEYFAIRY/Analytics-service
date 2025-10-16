from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship

from app.infrastructure.database.models.base import Base

class TopScaleModel(Base):
    __tablename__ = "TopEscalasDiarias"

    # Primary keys
    id_student = Column(String(128), primary_key=True, nullable=False)
    id_scale = Column(Integer, primary_key=True, nullable=False)
    fecha = Column(Date, primary_key=True, nullable=False)

    # Time variables
    anio = Column(Integer, nullable=False)
    semana = Column(Integer, nullable=False)
    mes = Column(Integer, nullable=False)
    
    # Actual statistics
    veces_practicada = Column(Integer, default=0)
