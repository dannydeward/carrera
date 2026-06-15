from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.user import User
from app.schemas.user import UserCreate

from app.models.team import Team
from app.models.carrera import Carrera

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/usuarios")
def crear_usuario(usuario: UserCreate, db: Session = Depends(get_db)):

    nuevo_usuario = User(
        nombre=usuario.nombre,
        apellido=usuario.apellido,
        email=usuario.email,
        edad=usuario.edad,
        pais=usuario.pais,
        ciudad=usuario.ciudad
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return {
        "mensaje": "Usuario creado correctamente",
        "id": nuevo_usuario.id
    }

@router.get("/usuarios")
def listar_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(User).all()
    return usuarios

@router.get("/usuarios/{usuario_id}/perfil")
def perfil_usuario(
    usuario_id: int,
    db: Session = Depends(get_db)
):

    usuario = db.query(User).filter(
        User.id == usuario_id
    ).first()

    if not usuario:
        return {
            "error": "Usuario no encontrado"
        }


    equipo_nombre = None

    if usuario.equipo_id:

        equipo = db.query(Team).filter(
            Team.id == usuario.equipo_id
        ).first()

        if equipo:
            equipo_nombre = equipo.nombre


    carreras = db.query(Carrera).filter(
        Carrera.usuario_id == usuario_id
    ).all()


    posicion = db.query(User).filter(
        User.km_totales > usuario.km_totales
    ).count() + 1


    return {
        "nombre": usuario.nombre,
        "apellido": usuario.apellido,
        "equipo": equipo_nombre,
        "km_totales": usuario.km_totales,
        "posicion_ranking": posicion,
        "ultimas_carreras": carreras
    }

@router.get("/usuarios/{usuario_id}/estadisticas")
def estadisticas_usuario(
    usuario_id: int,
    db: Session = Depends(get_db)
):

    usuario = db.query(User).filter(
        User.id == usuario_id
    ).first()


    if not usuario:
        return {
            "error": "Usuario no encontrado"
        }


    # Buscar carreras del usuario

    carreras = db.query(Carrera).filter(
        Carrera.usuario_id == usuario_id
    ).all()


    cantidad_carreras = len(carreras)


    # Calcular velocidad promedio

    velocidad_promedio = 0

    if cantidad_carreras > 0:

        suma_velocidades = sum(
            carrera.velocidad
            for carrera in carreras
        )

        velocidad_promedio = round(
            suma_velocidades / cantidad_carreras,
            2
        )


    # Buscar mejor carrera por distancia

    mejor_carrera = 0

    if cantidad_carreras > 0:

        mejor_carrera = max(
            carrera.distancia
            for carrera in carreras
        )


    # Buscar equipo

    equipo_nombre = None

    if usuario.equipo_id:

        equipo = db.query(Team).filter(
            Team.id == usuario.equipo_id
        ).first()

        if equipo:
            equipo_nombre = equipo.nombre



    return {
        "nombre": usuario.nombre,
        "apellido": usuario.apellido,
        "equipo": equipo_nombre,
        "kilometros_totales": usuario.km_totales,
        "cantidad_carreras": cantidad_carreras,
        "velocidad_promedio": velocidad_promedio,
        "mejor_carrera": mejor_carrera
    }