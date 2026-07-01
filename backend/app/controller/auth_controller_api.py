from fastapi import APIRouter, HTTPException

from app.schemas.auth_schema import LoginRequest, LoginResponse
from app.service.auth_service import AuthService


router = APIRouter(prefix="/auth", tags=["Autenticacion"])
service = AuthService()


@router.post("/login", response_model=LoginResponse)
def login(data: LoginRequest):
    usuario = service.login(data.correo, data.contrasena)
    if not usuario:
        raise HTTPException(status_code=401, detail="Credenciales invalidas")
    token = service.create_token(usuario)
    return {"access_token": token, "token_type": "bearer", "usuario": usuario}
