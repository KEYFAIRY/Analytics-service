from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship

from app.infrastructure.database.models.base import Base

class MusicalMistakesModel(Base):
    __tablename__ = "ProgresoErroresPosturales"

    id_student = Column(String(128), nullable=False, primary_key=True)
    id_scale = Column(Integer, nullable=False, primary_key=True)
    date = Column(Date, nullable=False, primary_key=True)
    year = Column(Integer, nullable=False)
    week = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    mistake_amount = Column(Integer, nullable=False)