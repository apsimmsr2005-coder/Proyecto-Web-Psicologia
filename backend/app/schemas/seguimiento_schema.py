from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict


class SeguimientoBase(BaseModel):
    identificador: str
    beneficiario_id: int
    sesion_id: Optional[int] = None
    fecha: date
    descripcion: str
    accion: str
    prioridad: str = "media"
    completado: bool = False


class SeguimientoCreate(SeguimientoBase):
    pass


class SeguimientoUpdate(BaseModel):
    beneficiario_id: Optional[int] = None
    sesion_id: Optional[int] = None
    fecha: Optional[date] = None
    descripcion: Optional[str] = None
    accion: Optional[str] = None
    prioridad: Optional[str] = None
    completado: Optional[bool] = None


class SeguimientoSchema(SeguimientoBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

