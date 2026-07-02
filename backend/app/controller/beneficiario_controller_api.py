from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from app.schemas.beneficiario_schema import (
    BeneficiarioCreate,
    BeneficiarioSchema,
    BeneficiarioUpdate,
)
from app.service.beneficiario_service import BeneficiarioService


router = APIRouter(prefix="/beneficiarios", tags=["Beneficiarios"])
service = BeneficiarioService()


@router.post("/", response_model=BeneficiarioSchema)
def create_beneficiario(beneficiario: BeneficiarioCreate):
    return service.create_beneficiario(beneficiario)


@router.get("/", response_model=list[BeneficiarioSchema])
def list_beneficiarios(
    search: Optional[str] = Query(default=None),
    estado: Optional[str] = Query(default=None),
):
    return service.list_beneficiarios(search=search, estado=estado)


@router.get("/{beneficiario_id}", response_model=BeneficiarioSchema)
def get_beneficiario(beneficiario_id: int):
    beneficiario = service.get_beneficiario(beneficiario_id)
    if not beneficiario:
        raise HTTPException(status_code=404, detail="Beneficiario no encontrado")
    return beneficiario


@router.put("/{beneficiario_id}", response_model=BeneficiarioSchema)
def update_beneficiario(beneficiario_id: int, beneficiario: BeneficiarioUpdate):
    updated = service.update_beneficiario(beneficiario_id, beneficiario)
    if not updated:
        raise HTTPException(status_code=404, detail="Beneficiario no encontrado")
    return updated


@router.delete("/{beneficiario_id}")
def delete_beneficiario(beneficiario_id: int):
    deleted = service.delete_beneficiario(beneficiario_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Beneficiario no encontrado")
    return {"message": "Beneficiario eliminado"}
