from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.config.database import Base


class SesionORM(Base):
    """Entidad ORM para sesiones de atencion psicologica."""

    __tablename__ = "sesiones_tb"

    id = Column(Integer, primary_key=True, index=True)
    identificador = Column(String(20), unique=True, nullable=False, index=True)
    beneficiario_id = Column(Integer, ForeignKey("beneficiarios_tb.id"), nullable=False)
    terapeuta_id = Column(Integer, ForeignKey("usuarios_tb.id"), nullable=False)
    fecha = Column(Date, nullable=False)
    hora = Column(String(5), nullable=False)
    modalidad = Column(String(20), nullable=False, default="presencial")
    estado = Column(String(20), nullable=False, default="programada")
    notas = Column(String(500), default="")

    beneficiario = relationship("BeneficiarioORM", back_populates="sesiones")
    terapeuta = relationship("UsuarioORM", back_populates="sesiones")
    seguimientos = relationship("SeguimientoORM", back_populates="sesion")

    def __repr__(self):
        return f"Sesion({self.identificador}, fecha={self.fecha}, estado={self.estado})"