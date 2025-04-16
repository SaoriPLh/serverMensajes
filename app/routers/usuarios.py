from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, models, database

router = APIRouter(prefix="/usuarios", tags=["usuarios"])

@router.post("/", response_model=schemas.Usuario)
def crear_usuario(usuario: schemas.UsuarioCrear, db: Session = Depends(database.get_db)):
    nuevo_usuario = models.Usuario(nombre=usuario.nombre)
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

@router.get("/{usuario_id}", response_model=schemas.Usuario)
def obtener_usuario(usuario_id: int, db: Session = Depends(database.get_db)):
    return db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()

@router.post("/login")
def login_usuario(nombre: str, db: Session = Depends(database.get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.nombre == nombre).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

