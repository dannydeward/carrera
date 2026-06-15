from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from datetime import datetime

from app.database import Base


class Carrera(Base):

    __tablename__ = "carreras"

    id = Column(Integer, primary_key=True, index=True)

    usuario_id = Column(
        Integer,
        ForeignKey("usuarios.id")
    )

    distancia = Column(Float)

    tiempo_minutos = Column(Integer)

    velocidad = Column(Float)

    fecha = Column(
        DateTime,
        default=datetime.utcnow
    )