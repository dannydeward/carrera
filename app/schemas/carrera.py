from pydantic import BaseModel


class CarreraCreate(BaseModel):
    usuario_id: int
    distancia: float
    tiempo_minutos: int