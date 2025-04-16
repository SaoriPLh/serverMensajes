from pydantic import BaseModel
from datetime import datetime
from typing import List

# ----- MENSAJES -----

class MensajeCrear(BaseModel):
    contenido: str
    de_usuario_id: int
    para_usuario_id: int

class Mensaje(BaseModel):
    id: int
    contenido: str
    fecha: datetime
    de_usuario_id: int
    para_usuario_id: int

    class Config:
        from_attributes = True  # Equivalente a orm_mode = True

# ----- USUARIOS -----

#Como nos llegan los datos de los usuarios desde el frontend, no necesitamos el id
class UsuarioCrear(BaseModel):
    nombre: str


#Como guardamos los datos en la base de datos, y lo retornamos al frontend
class Usuario(BaseModel):
    id: int
    nombre: str

    class Config:
        from_attributes = True

#Como guardamos los datos de los usuarios en la base de datos, y lo retornamos al frontend
class UsuarioConMensajes(BaseModel):
    id: int
    nombre: str
    mensajes_enviados: List[Mensaje] = []
    mensajes_recibidos: List[Mensaje] = []

    class Config:
        from_attributes = True
