from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class BeneficiarioBase(BaseModel):
    identificador: str
    nombre: str
    apellido: str
    cedula: str
    fecha_nacimiento: date
    direccion: str
    telefono: str
    estado: str = "activo"
    motivo_consulta: str
    nivel_riesgo: str = "bajo"


class BeneficiarioCreate(BeneficiarioBase):
    pass


class BeneficiarioUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    cedula: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    estado: Optional[str] = None
    motivo_consulta: Optional[str] = None
    nivel_riesgo: Optional[str] = None


class BeneficiarioSchema(BeneficiarioBase):
    id: int
    creado_en: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
