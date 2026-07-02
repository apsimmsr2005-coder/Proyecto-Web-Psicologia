from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr


class UsuarioBase(BaseModel):
    """Campos comunes, compartidos por Create, Update y Schema."""
    identificador: str
    nombre: str
    apellido: str
    correo: EmailStr # valida formato de email automáticamente (rechaza "correo" inválidos antes de llegar al service)
    rol: str = "terapeuta"
    activo: bool = True


class UsuarioCreate(UsuarioBase):
    contrasena: str # solo en Create: se necesita al registrar, pero nunca se devuelve al cliente (no está en UsuarioSchema)


class UsuarioUpdate(BaseModel):
    """No hereda de Base: todo Optional para permitir update parcial (PATCH)."""
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    correo: Optional[EmailStr] = None
    rol: Optional[str] = None
    activo: Optional[bool] = None
    contrasena: Optional[str] = None # opcional: permite cambiar la contraseña sin obligar a mandarla siempre


class UsuarioSchema(UsuarioBase):
    id: int # solo existe una vez creado el registro

    # Permite construir este schema directo desde un objeto ORM (UsuarioORM)
    model_config = ConfigDict(from_attributes=True)
