from pydantic import BaseModel

from app.schemas.usuario_schema import UsuarioSchema


class LoginRequest(BaseModel):
    correo: str
    contrasena: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    usuario: UsuarioSchema