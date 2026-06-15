from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class Team(Base):
    __tablename__ = "equipos"

    id = Column(Integer, primary_key=True, index=True)

    nombre = Column(String, unique=True, nullable=False)

    descripcion = Column(String)

    km_totales = Column(Float, default=0)