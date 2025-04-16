from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)

    mensajes_enviados = relationship("Mensaje", back_populates="autor", foreign_keys="Mensaje.de_usuario_id")
    mensajes_recibidos = relationship("Mensaje", back_populates="destinatario", foreign_keys="Mensaje.para_usuario_id")


class Mensaje(Base):
    __tablename__ = "mensajes"

    id = Column(Integer, primary_key=True, index=True)
    contenido = Column(String)
    fecha = Column(DateTime)

    de_usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    para_usuario_id = Column(Integer, ForeignKey("usuarios.id"))

    autor = relationship("Usuario", foreign_keys=[de_usuario_id], back_populates="mensajes_enviados")
    destinatario = relationship("Usuario", foreign_keys=[para_usuario_id], back_populates="mensajes_recibidos")
