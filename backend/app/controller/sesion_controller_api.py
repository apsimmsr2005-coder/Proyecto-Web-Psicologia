from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from app.schemas.sesion_schema import SesionCreate, SesionSchema, SesionUpdate
from app.service.auth_service import get_current_user
from app.service.sesion_service import SesionService


router = APIRouter(
    prefix="/sesiones",
    tags=["Sesiones"],
    dependencies=[Depends(get_current_user)],
)
service = SesionService()


@router.post("/", response_model=SesionSchema)
def create_sesion(sesion: SesionCreate):
    try:
        return service.create_sesion(sesion)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("/", response_model=list[SesionSchema])
def list_sesiones(
    estado: Optional[str] = Query(default=None),
    beneficiario_id: Optional[int] = Query(default=None),
    terapeuta_id: Optional[int] = Query(default=None),
):
    return service.list_sesiones(
        estado=estado,
        beneficiario_id=beneficiario_id,
        terapeuta_id=terapeuta_id,
    )


@router.get("/{sesion_id}", response_model=SesionSchema)
def get_sesion(sesion_id: int):
    sesion = service.get_sesion(sesion_id)
    if not sesion:
        raise HTTPException(status_code=404, detail="Sesion no encontrada")
    return sesion


@router.put("/{sesion_id}", response_model=SesionSchema)
def update_sesion(sesion_id: int, sesion: SesionUpdate):
    try:
        updated = service.update_sesion(sesion_id, sesion)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    if not updated:
        raise HTTPException(status_code=404, detail="Sesion no encontrada")
    return updated


@router.delete("/{sesion_id}")
def delete_sesion(sesion_id: int):
    deleted = service.delete_sesion(sesion_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Sesion no encontrada")
    return {"message": "Sesion eliminada"}

