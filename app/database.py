#es una función que crea la conexión con la base de datos.

from sqlalchemy import create_engine

#Esto crea una base comun para definir tablas usando clases

# es decir todas nuestras clases heredan de la base que creeemos  como mostramos en la ultima linea
from sqlalchemy.ext.declarative import declarative_base
#una funcion que nos ayuda a crear sesiones es decir para moficiar o interactuar con la bd
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from fastapi import Depends



SQLALCHEMY_DATABASE_URL = "sqlite:///./mensajes.db"

#Conexion a la base de datos
engine = create_engine(
    #SQLite (por defecto) solo permite que una conexión a la base sea usada por el mismo hilo de ejecución (thread).

    #entonces con cheack_same_thread=False le decimos que no se preocupe por eso “Está bien si usas esta conexión en diferentes partes del programa, no te quejes”.
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

#MOLDE para interactuar con la base de datos

#Crea un MOLDE para crear sesiones de base de datos.

#osea que cada que queramos interactuar con la base de datos tendriamos q hacer algo como db = SessionLocal y luego db.save o db.commit

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Base para los modelos todas tus clases como Usuario van a heredar de esto para que se conviertan en tablas.
Base = declarative_base()


#esta funcion nos ayuda a crear una sesion para interactuar con la base de datos 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


