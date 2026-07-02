from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class BeneficiarioBase(BaseModel):
    """Campos comunes compartidos por Create, Update y Schema (evita repetir)."""
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
    """Datos requeridos al crear: hereda todo tal cual, no agrega ni quita nada."""
    pass


class BeneficiarioUpdate(BaseModel):
    """No hereda de Base: todos los campos son Optional para permitir update parcial (PATCH)."""
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
    """Schema de salida (respuesta de la API): agrega campos generados por la BD."""
    id: int # solo existe una vez creado el registro, por eso no está en Base/Create
    creado_en: Optional[datetime] = None # lo pone la BD (server_default), no el cliente

    # Permite construir este schema directo desde un objeto ORM (BeneficiarioORM), no solo desde un dict
    model_config = ConfigDict(from_attributes=True)
