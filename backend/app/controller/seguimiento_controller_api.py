from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from app.schemas.seguimiento_schema import (
    SeguimientoCreate,
    SeguimientoSchema,
    SeguimientoUpdate,
)
from app.service.auth_service import get_current_user
from app.service.seguimiento_service import SeguimientoService


router = APIRouter(
    prefix="/seguimientos",
    tags=["Seguimientos"],
    dependencies=[Depends(get_current_user)],
)
service = SeguimientoService()


@router.post("/", response_model=SeguimientoSchema)
def create_seguimiento(seguimiento: SeguimientoCreate):
    try:
        return service.create_seguimiento(seguimiento)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("/", response_model=list[SeguimientoSchema])
def list_seguimientos(
    beneficiario_id: Optional[int] = Query(default=None),
    completado: Optional[bool] = Query(default=None),
    prioridad: Optional[str] = Query(default=None),
):
    return service.list_seguimientos(
        beneficiario_id=beneficiario_id,
        completado=completado,
        prioridad=prioridad,
    )


@router.get("/{seguimiento_id}", response_model=SeguimientoSchema)
def get_seguimiento(seguimiento_id: int):
    seguimiento = service.get_seguimiento(seguimiento_id)
    if not seguimiento:
        raise HTTPException(status_code=404, detail="Seguimiento no encontrado")
    return seguimiento


@router.put("/{seguimiento_id}", response_model=SeguimientoSchema)
def update_seguimiento(seguimiento_id: int, seguimiento: SeguimientoUpdate):
    try:
        updated = service.update_seguimiento(seguimiento_id, seguimiento)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    if not updated:
        raise HTTPException(status_code=404, detail="Seguimiento no encontrado")
    return updated


@router.delete("/{seguimiento_id}")
def delete_seguimiento(seguimiento_id: int):
    deleted = service.delete_seguimiento(seguimiento_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Seguimiento no encontrado")
    return {"message": "Seguimiento eliminado"}

