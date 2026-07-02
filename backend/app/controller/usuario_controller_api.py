from fastapi import APIRouter, Depends, HTTPException

from app.schemas.usuario_schema import UsuarioCreate, UsuarioSchema, UsuarioUpdate
from app.service.auth_service import get_current_user, require_admin
from app.service.usuario_service import UsuarioService


router = APIRouter(prefix="/usuarios", tags=["Usuarios"])
service = UsuarioService()


@router.post("/", response_model=UsuarioSchema, dependencies=[Depends(require_admin)])
# dependencies por endpoint (no en el router, a diferencia de ReporteService): cada ruta
# elige su propio nivel de acceso, algunas solo piden estar logueado, otras piden ser admin
def create_usuario(usuario: UsuarioCreate):
    try:
        return service.create_usuario(usuario)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("/", response_model=list[UsuarioSchema], dependencies=[Depends(get_current_user)])
def list_usuarios():
    # menos restrictivo que los demás: solo pide estar logueado, no ser admin
    return service.list_usuarios()


@router.get("/{usuario_id}", response_model=UsuarioSchema, dependencies=[Depends(require_admin)])
def get_usuario(usuario_id: int):
    usuario = service.get_usuario(usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


@router.put("/{usuario_id}", response_model=UsuarioSchema, dependencies=[Depends(require_admin)])
def update_usuario(usuario_id: int, usuario: UsuarioUpdate):
    try:
        updated = service.update_usuario(usuario_id, usuario)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    if not updated:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return updated


@router.delete("/{usuario_id}", dependencies=[Depends(require_admin)])
def delete_usuario(usuario_id: int):
    deleted = service.delete_usuario(usuario_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"message": "Usuario eliminado"}
