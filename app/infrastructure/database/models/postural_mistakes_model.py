from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship

from app.infrastructure.database.models.base import Base

class PosturalMistakesModel(Base):
    __tablename__ = "ProgresoErroresPosturales"

    # Primary keys
    id_student = Column(String(128), primary_key=True, nullable=False)
    id_scale = Column(Integer, primary_key=True, nullable=False)
    fecha = Column(Date, primary_key=True, nullable=False)

    # Time variables
    anio = Column(Integer, nullable=False)
    semana = Column(Integer, nullable=False)
    mes = Column(Integer, nullable=False)

    # Actual statistics
    cantidad_errores = Column(Integer, default=0)