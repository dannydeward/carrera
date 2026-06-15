from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.team import Team
from app.schemas.team import TeamCreate

from app.models.user import User

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/equipos")
def crear_equipo(equipo: TeamCreate, db: Session = Depends(get_db)):

    nuevo_equipo = Team(
        nombre=equipo.nombre,
        descripcion=equipo.descripcion
    )

    db.add(nuevo_equipo)
    db.commit()
    db.refresh(nuevo_equipo)

    return {
        "mensaje": "Equipo creado",
        "id": nuevo_equipo.id
    }


@router.get("/equipos")
def listar_equipos(db: Session = Depends(get_db)):
    return db.query(Team).all()

@router.post("/equipos/{equipo_id}/unirse/{usuario_id}")
def unirse_equipo(
    equipo_id: int,
    usuario_id: int,
    db: Session = Depends(get_db)
):

    usuario = db.query(User).filter(
        User.id == usuario_id
    ).first()

    if not usuario:
        return {"error": "Usuario no encontrado"}

    equipo = db.query(Team).filter(
        Team.id == equipo_id
    ).first()

    if not equipo:
        return {"error": "Equipo no encontrado"}

    usuario.equipo_id = equipo_id

    db.commit()

    return {
        "mensaje": f"{usuario.nombre} se unió a {equipo.nombre}"
    }

@router.get("/equipos/{equipo_id}")
def ver_equipo(
    equipo_id: int,
    db: Session = Depends(get_db)
):

    equipo = db.query(Team).filter(
        Team.id == equipo_id
    ).first()

    if not equipo:
        return {"error": "Equipo no encontrado"}

    integrantes = db.query(User).filter(
        User.equipo_id == equipo_id
    ).all()

    return {
        "id": equipo.id,
        "nombre": equipo.nombre,
        "descripcion": equipo.descripcion,
        "km_totales": equipo.km_totales,
        "cantidad_integrantes": len(integrantes),
        "integrantes": integrantes
    }
@router.get("/equipos/{equipo_id}/resumen")
def resumen_equipo(
    equipo_id: int,
    db: Session = Depends(get_db)
):

    equipo = db.query(Team).filter(
        Team.id == equipo_id
    ).first()


    if not equipo:
        return {
            "error": "Equipo no encontrado"
        }


    integrantes = db.query(User).filter(
        User.equipo_id == equipo_id
    ).all()


    posicion = db.query(Team).filter(
        Team.km_totales > equipo.km_totales
    ).count() + 1


    lista_integrantes = []

    for usuario in integrantes:

        lista_integrantes.append({
            "nombre": usuario.nombre,
            "apellido": usuario.apellido,
            "km_totales": usuario.km_totales
        })


    return {
        "nombre_equipo": equipo.nombre,
        "descripcion": equipo.descripcion,
        "km_totales": equipo.km_totales,
        "cantidad_integrantes": len(integrantes),
        "posicion_ranking": posicion,
        "integrantes": lista_integrantes
    }