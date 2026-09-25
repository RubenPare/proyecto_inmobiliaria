from sqlalchemy import Column, Integer, String, Float, Text, Boolean
from database import Base


class Propiedad(Base):
    """
    Modelo base de una propiedad. Se amplía a futuro con más unidades
    de negocio (terrenos, campos, naves industriales, etc.) según se
    necesite en cada etapa.
    """
    __tablename__ = "propiedades"

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String(50), nullable=False)        # ej: "Casa", "Departamento", "Terreno", "Campo"
    titulo = Column(String(150), nullable=False)
    descripcion = Column(Text, nullable=True)
    precio = Column(Float, nullable=False)
    ubicacion = Column(String(150), nullable=False)
    imagen_url = Column(String(300), nullable=True)
    activo = Column(Boolean, nullable=False, default=True)