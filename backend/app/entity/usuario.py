from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.config.database import Base


class UsuarioORM(Base):
    """Entidad ORM para administradores y terapeutas."""

    __tablename__ = "usuarios_tb"

    id = Column(Integer, primary_key=True, index=True)
    identificador = Column(String(20), unique=True, nullable=False, index=True)
    nombre = Column(String(80), nullable=False)
    apellido = Column(String(80), nullable=False)
    correo = Column(String(120), unique=True, nullable=False, index=True)
    contrasena_hash = Column(String(64), nullable=False)
    rol = Column(String(20), nullable=False, default="terapeuta")
    activo = Column(Boolean, default=True)

    sesiones = relationship("SesionORM", back_populates="terapeuta")

    def __repr__(self):
        return f"Usuario({self.identificador}, {self.correo}, rol={self.rol})"
