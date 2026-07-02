from fastapi import APIRouter, Depends

from app.service.auth_service import get_current_user
from app.service.reporte_service import ReporteService


router = APIRouter(
    prefix="/reportes",
    tags=["Reportes"],
    dependencies=[Depends(get_current_user)],
)
service = ReporteService()


@router.get("/resumen")
def resumen():
    return service.resumen()


@router.get("/beneficiarios-por-estado")
def beneficiarios_por_estado():
    return service.beneficiarios_por_estado()


@router.get("/sesiones-por-estado")
def sesiones_por_estado():
    return service.sesiones_por_estado()


@router.get("/carga-terapeutas")
def carga_terapeutas():
    return service.carga_terapeutas()
