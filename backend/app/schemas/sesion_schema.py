from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict


class SesionBase(BaseModel):
    identificador: str
    beneficiario_id: int
    terapeuta_id: int
    fecha: date
    hora: str
    modalidad: str = "presencial"
    estado: str = "programada"
    notas: str = ""


class SesionCreate(SesionBase):
    pass


class SesionUpdate(BaseModel):
    beneficiario_id: Optional[int] = None
    terapeuta_id: Optional[int] = None
    fecha: Optional[date] = None
    hora: Optional[str] = None
    modalidad: Optional[str] = None
    estado: Optional[str] = None
    notas: Optional[str] = None


class SesionSchema(SesionBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

