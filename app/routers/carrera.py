from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.carrera import Carrera
from app.models.user import User
from app.models.team import Team
from app.schemas.carrera import CarreraCreate


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.post("/carreras")
def registrar_carrera(
    carrera: CarreraCreate,
    db: Session = Depends(get_db)
):

    usuario = db.query(User).filter(
        User.id == carrera.usuario_id
    ).first()


    if not usuario:
        return {
            "error": "Usuario no encontrado"
        }


    # ===============================
    # VALIDACION ANTI-TRAMPA
    # ===============================

    tiempo_horas = carrera.tiempo_minutos / 60

    velocidad = carrera.distancia / tiempo_horas


    if velocidad > 25:
        return {
            "error": "Velocidad inválida",
            "velocidad_detectada": round(velocidad, 2)
        }


    # ===============================
    # CREAR CARRERA
    # ===============================

    nueva_carrera = Carrera(
        usuario_id=carrera.usuario_id,
        distancia=carrera.distancia,
        tiempo_minutos=carrera.tiempo_minutos,
        velocidad=round(velocidad, 2)
    )


    db.add(nueva_carrera)


    # ===============================
    # ACTUALIZAR KM DEL USUARIO
    # ===============================

    usuario.km_totales += carrera.distancia



    # ===============================
    # ACTUALIZAR KM DEL EQUIPO
    # ===============================

    if usuario.equipo_id:

        equipo = db.query(Team).filter(
            Team.id == usuario.equipo_id
        ).first()


        if equipo:
            equipo.km_totales += carrera.distancia



    db.commit()
    db.refresh(nueva_carrera)


    return {
        "mensaje": "Carrera registrada",
        "km_sumados": carrera.distancia,
        "velocidad": round(velocidad, 2),
        "fecha": nueva_carrera.fecha
    }




@router.get("/usuarios/{usuario_id}/carreras")
def historial_carreras(
    usuario_id: int,
    db: Session = Depends(get_db)
):

    carreras = db.query(Carrera).filter(
        Carrera.usuario_id == usuario_id
    ).all()


    return carreras
