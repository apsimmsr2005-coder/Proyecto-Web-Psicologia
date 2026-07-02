from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.config.database import Base


class SeguimientoORM(Base):
    """Entidad ORM para acciones de seguimiento comunitario."""

    __tablename__ = "seguimientos_tb"

    id = Column(Integer, primary_key=True, index=True)
    identificador = Column(String(20), unique=True, nullable=False, index=True)
    beneficiario_id = Column(Integer, ForeignKey("beneficiarios_tb.id"), nullable=False)
    sesion_id = Column(Integer, ForeignKey("sesiones_tb.id"), nullable=True)
    fecha = Column(Date, nullable=False)
    descripcion = Column(String(500), nullable=False)
    accion = Column(String(200), nullable=False)
    prioridad = Column(String(20), nullable=False, default="media")
    completado = Column(Boolean, default=False)

    beneficiario = relationship("BeneficiarioORM", back_populates="seguimientos")
    sesion = relationship("SesionORM", back_populates="seguimientos")

    def __repr__(self):
        return f"Seguimiento({self.identificador}, prioridad={self.prioridad})"

