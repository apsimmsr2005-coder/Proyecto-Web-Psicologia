from app.entity.seguimiento import SeguimientoORM
from app.repository.beneficiario_repository import BeneficiarioRepository
from app.repository.seguimiento_repository import SeguimientoRepository
from app.repository.sesion_repository import SesionRepository


PRIORIDADES_VALIDAS = {"baja", "media", "alta"}


class SeguimientoService:
    """Logica de negocio para acciones de seguimiento."""

    def __init__(self):
        self.repo = SeguimientoRepository()
        self.beneficiario_repo = BeneficiarioRepository()
        self.sesion_repo = SesionRepository()

    def _validar(self, beneficiario_id, sesion_id, prioridad):
        beneficiario = self.beneficiario_repo.get(beneficiario_id)
        if not beneficiario:
            raise ValueError("Beneficiario no encontrado")
        if prioridad.lower() not in PRIORIDADES_VALIDAS:
            raise ValueError("Prioridad invalida")
        if sesion_id:
            sesion = self.sesion_repo.get(sesion_id)
            if not sesion:
                raise ValueError("Sesion no encontrada")
            if sesion.beneficiario_id != beneficiario_id:
                raise ValueError("La sesion no pertenece al beneficiario indicado")
        return beneficiario

    def create_seguimiento(self, data):
        beneficiario = self._validar(data.beneficiario_id, data.sesion_id, data.prioridad)
        if self.repo.get_by_identificador(data.identificador):
            raise ValueError("Ya existe un seguimiento con ese identificador")

        seguimiento = SeguimientoORM(
            identificador=data.identificador,
            beneficiario_id=data.beneficiario_id,
            sesion_id=data.sesion_id,
            fecha=data.fecha,
            descripcion=data.descripcion,
            accion=data.accion,
            prioridad=data.prioridad.lower(),
            completado=data.completado,
        )
        resultado = self.repo.create(seguimiento)

        if beneficiario.estado == "activo":
            beneficiario.estado = "en_seguimiento"
            self.beneficiario_repo.update(beneficiario)
        return resultado

    def get_seguimiento(self, seguimiento_id):
        return self.repo.get(seguimiento_id)

    def list_seguimientos(self, beneficiario_id=None, completado=None, prioridad=None):
        return self.repo.get_all(
            beneficiario_id=beneficiario_id,
            completado=completado,
            prioridad=prioridad,
        )

    def update_seguimiento(self, seguimiento_id, data):
        seguimiento = self.repo.get(seguimiento_id)
        if not seguimiento:
            return None

        values = data.model_dump(exclude_unset=True)
        beneficiario_id = values.get("beneficiario_id", seguimiento.beneficiario_id)
        sesion_id = values.get("sesion_id", seguimiento.sesion_id)
        prioridad = values.get("prioridad", seguimiento.prioridad)
        self._validar(beneficiario_id, sesion_id, prioridad)

        for field, value in values.items():
            if field == "prioridad":
                value = value.lower()
            setattr(seguimiento, field, value)
        return self.repo.update(seguimiento)

    def delete_seguimiento(self, seguimiento_id):
        seguimiento = self.repo.get(seguimiento_id)
        if not seguimiento:
            return None
        return self.repo.delete(seguimiento)

