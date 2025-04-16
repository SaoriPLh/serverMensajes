from fastapi import FastAPI
from app import models
from app.database import engine
from app.routers import usuarios
from app.routers import mensajes

app = FastAPI()

#creamos todas las tablas por si no existen

models.Base.metadata.create_all(bind=engine)

app.include_router(usuarios.router)
app.include_router(mensajes.router)


@app.get("/")
def inicio():
    return {"mensaje": "Hola Mundo"}
