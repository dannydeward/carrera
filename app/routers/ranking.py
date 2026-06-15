from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.user import User
from app.models.team import Team

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Ranking de corredores individuales
@router.get("/ranking/usuarios")
def ranking_usuarios(db: Session = Depends(get_db)):

    usuarios = db.query(User).order_by(
        User.km_totales.desc()
    ).all()

    return usuarios


# Ranking de equipos
@router.get("/ranking/equipos")
def ranking_equipos(db: Session = Depends(get_db)):

    equipos = db.query(Team).order_by(
        Team.km_totales.desc()
    ).all()

    return equipos