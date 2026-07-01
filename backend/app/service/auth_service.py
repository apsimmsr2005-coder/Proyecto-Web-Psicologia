import base64
import hashlib
import hmac
import json
import os
import time

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.repository.usuario_repository import UsuarioRepository


SECRET_KEY = os.getenv("SECRET_KEY", "saludmente-dev-secret")
TOKEN_TTL_SECONDS = 60 * 60 * 8
security = HTTPBearer()


def hash_password(contrasena):
    return hashlib.sha256(contrasena.encode("utf-8")).hexdigest()


def _b64url_encode(value):
    return base64.urlsafe_b64encode(value).decode("utf-8").rstrip("=")


def _b64url_decode(value):
    padding = "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode(value + padding)


class AuthService:
    """Servicio de autenticacion y generacion de tokens firmados."""

    def __init__(self):
        self.repo = UsuarioRepository()

    def login(self, correo, contrasena):
        usuario = self.repo.get_by_correo(correo)
        if not usuario or not usuario.activo:
            return None
        if usuario.contrasena_hash != hash_password(contrasena):
            return None
        return usuario

    def create_token(self, usuario):
        payload = {
            "sub": usuario.id,
            "correo": usuario.correo,
            "rol": usuario.rol,
            "exp": int(time.time()) + TOKEN_TTL_SECONDS,
        }
        payload_bytes = json.dumps(payload, separators=(",", ":")).encode("utf-8")
        payload_part = _b64url_encode(payload_bytes)
        signature = hmac.new(
            SECRET_KEY.encode("utf-8"),
            payload_part.encode("utf-8"),
            hashlib.sha256,
        ).digest()
        return f"{payload_part}.{_b64url_encode(signature)}"

    def verify_token(self, token):
        try:
            payload_part, signature_part = token.split(".", 1)
            expected_signature = hmac.new(
                SECRET_KEY.encode("utf-8"),
                payload_part.encode("utf-8"),
                hashlib.sha256,
            ).digest()
            received_signature = _b64url_decode(signature_part)
            if not hmac.compare_digest(expected_signature, received_signature):
                return None

            payload = json.loads(_b64url_decode(payload_part))
            if payload.get("exp", 0) < int(time.time()):
                return None
            return payload
        except Exception:
            return None


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    service = AuthService()
    payload = service.verify_token(credentials.credentials)
    if not payload:
        raise HTTPException(status_code=401, detail="Token invalido o vencido")

    usuario = service.repo.get(payload["sub"])
    if not usuario or not usuario.activo:
        raise HTTPException(status_code=401, detail="Usuario no autorizado")
    return usuario


def require_admin(usuario=Depends(get_current_user)):
    if usuario.rol != "admin":
        raise HTTPException(status_code=403, detail="Solo administradores")
    return usuario
