from pydantic import BaseModel
from pydantic import BaseModel

class UserCreate(BaseModel):
    nombre: str
    apellido: str
    email: str
    edad: int
    pais: str
    ciudad: str