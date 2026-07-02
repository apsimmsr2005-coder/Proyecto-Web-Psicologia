from sqlalchemy import Column, Date, DateTime, Integer, String, func
from sqlalchemy.orm import relationship

from app.config.database import Base


class BeneficiarioORM(Base):
    """Entidad ORM para personas beneficiarias del programa comunitario."""

    __tablename__ = "beneficiarios_tb"

    id = Column(Integer, primary_key=True, index=True)
    identificador = Column(String(20), unique=True, nullable=False, index=True)
    nombre = Column(String(80), nullable=False)
    apellido = Column(String(80), nullable=False)
    cedula = Column(String(30), unique=True, nullable=False, index=True)
    fecha_nacimiento = Column(Date, nullable=False)
    direccion = Column(String(200), nullable=False)
    telefono = Column(String(30), nullable=False)
    estado = Column(String(30), nullable=False, default="activo")
    motivo_consulta = Column(String(300), nullable=False)
    nivel_riesgo = Column(String(20), nullable=False, default="bajo")
    creado_en = Column(DateTime, server_default=func.now())

    sesiones = relationship(
        "SesionORM",
        back_populates="beneficiario",
        cascade="all, delete-orphan",
    )
    seguimientos = relationship(
        "SeguimientoORM",
        back_populates="beneficiario",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"Beneficiario({self.identificador}, {self.nombre} {self.apellido})"
