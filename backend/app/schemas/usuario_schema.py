from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr


class UsuarioBase(BaseModel):
    identificador: str
    nombre: str
    apellido: str
    correo: EmailStr
    rol: str = "terapeuta"
    activo: bool = True


class UsuarioCreate(UsuarioBase):
    contrasena: str


class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    correo: Optional[EmailStr] = None
    rol: Optional[str] = None
    activo: Optional[bool] = None
    contrasena: Optional[str] = None


class UsuarioSchema(UsuarioBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
