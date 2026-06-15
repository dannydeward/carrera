from fastapi import FastAPI

from app.database import engine
from app.models.user import User
from app.database import Base
from app.routers.user import router as user_router
from app.models.team import Team
from app.routers.teams import router as team_router
from app.models.carrera import Carrera
from app.routers.carrera import router as carrera_router
from app.routers.ranking import router as ranking_router

app = FastAPI()

Base.metadata.create_all(bind=engine)
app.include_router(user_router)
app.include_router(team_router)
app.include_router(carrera_router)
app.include_router(ranking_router)

@app.get("/")
def inicio():
    return {"mensaje": "Bienvenido a RunFun"}