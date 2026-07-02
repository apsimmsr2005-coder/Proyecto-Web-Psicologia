from sqlalchemy import Column, Date, DateTime, Integer, String, func
from sqlalchemy.orm import relationship

from app.config.database import Base


class BeneficiarioORM(Base):
    """Entidad ORM para personas beneficiarias del programa comunitario."""

    __tablename__ = "beneficiarios_tb"

    id = Column(Integer, primary_key=True, index=True)
    identificador = Column(String(20), unique=True, nullable=False, index=True) # único + indexado: búsquedas rápidas por este campo
    nombre = Column(String(80), nullable=False)
    apellido = Column(String(80), nullable=False)
    cedula = Column(String(30), unique=True, nullable=False, index=True) # único + indexado: se consulta seguido y no puede repetirse
    fecha_nacimiento = Column(Date, nullable=False)
    direccion = Column(String(200), nullable=False)
    telefono = Column(String(30), nullable=False)
    estado = Column(String(30), nullable=False, default="activo") # default en Python: si no se envía, SQLAlchemy pone "activo" antes del INSERT
    motivo_consulta = Column(String(300), nullable=False)
    nivel_riesgo = Column(String(20), nullable=False, default="bajo")
    creado_en = Column(DateTime, server_default=func.now()) # default calculado por la BD (no por Python), aplica aunque se inserte fuera del ORM

    # Relación con SesionORM (navegable como beneficiario.sesiones)
    sesiones = relationship(
        "SesionORM",
        # sincroniza con el atributo "beneficiario" definido en SesionORM
        back_populates="beneficiario",
        # si se borra el beneficiario (o se desvincula una sesión), 
        # esa sesión se borra de la BD
        cascade="all, delete-orphan", 
    )
    # Relación con SeguimientoORM (misma lógica que "sesiones")
    seguimientos = relationship(
        "SeguimientoORM",
        back_populates="beneficiario",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"Beneficiario({self.identificador}, {self.nombre} {self.apellido})"
