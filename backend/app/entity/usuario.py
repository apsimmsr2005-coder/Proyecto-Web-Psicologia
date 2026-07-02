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
    correo = Column(String(120), unique=True, nullable=False, index=True) # único: no pueden existir dos usuarios con el mismo correo (sirve para login)
    contrasena_hash = Column(String(64), nullable=False)
    rol = Column(String(20), nullable=False, default="terapeuta") # default en Python, no en la BD (a diferencia de creado_en en Beneficiario)
    activo = Column(Boolean, default=True) # permite "desactivar" un usuario sin borrarlo (soft delete)

    # Un terapeuta tiene muchas sesiones. Sin cascade delete
    # (a diferencia de Beneficiario): si se borra el usuario, sus sesiones quedan intactas.
    sesiones = relationship("SesionORM", back_populates="terapeuta")

    def __repr__(self):
        return f"Usuario({self.identificador}, {self.correo}, rol={self.rol})"
