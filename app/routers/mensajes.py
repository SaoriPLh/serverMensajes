from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, models, database
from datetime import datetime
from typing import List
from typing import Optional
import asyncio


router = APIRouter(
    prefix="/mensajes",
    tags=["mensajes"]
)

@router.post("/", response_model=schemas.Mensaje)
def crear_mensaje(mensaje: schemas.MensajeCrear, db: Session = Depends(database.get_db)):
    # Validar que ambos usuarios existan
    autor = db.query(models.Usuario).filter(models.Usuario.id == mensaje.de_usuario_id).first()
    receptor = db.query(models.Usuario).filter(models.Usuario.id == mensaje.para_usuario_id).first()

    if not autor or not receptor:
        raise HTTPException(status_code=404, detail="Usuario remitente o destinatario no encontrado")

    nuevo_mensaje = models.Mensaje(
        contenido=mensaje.contenido,
        fecha=datetime.now(),
        de_usuario_id=mensaje.de_usuario_id,
        para_usuario_id=mensaje.para_usuario_id
    )

    db.add(nuevo_mensaje)
    db.commit()
    db.refresh(nuevo_mensaje)

    return nuevo_mensaje


@router.get("/recibidos/{usuario_id}", response_model=List[schemas.Mensaje])
def obtener_mensajes_recibidos(usuario_id: int, db: Session = Depends(database.get_db)):
    return db.query(models.Mensaje).filter(models.Mensaje.para_usuario_id == usuario_id).all()



@router.get("/recibidos/{usuario_id}/esperar-nuevo", response_model=Optional[schemas.Mensaje])
async def esperar_nuevo_mensaje(usuario_id: int, ultimo_id: int = 0, db: Session = Depends(database.get_db)):
    timeout = 30  # tiempo máximo de espera en segundos
    tiempo_espera = 0

    while tiempo_espera < timeout:
        mensaje_nuevo = db.query(models.Mensaje)\
            .filter(models.Mensaje.para_usuario_id == usuario_id)\
            .order_by(models.Mensaje.id.desc())\
            .first()

        if mensaje_nuevo and mensaje_nuevo.id > ultimo_id:
            return mensaje_nuevo

        await asyncio.sleep(2)
        tiempo_espera += 2

    return None  # Si no hay mensaje nuevo, responder None (null)
