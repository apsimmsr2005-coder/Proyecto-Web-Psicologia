from app.entity.sesion import SesionORM
from app.repository.beneficiario_repository import BeneficiarioRepository
from app.repository.sesion_repository import SesionRepository
from app.repository.usuario_repository import UsuarioRepository


ESTADOS_VALIDOS = {"programada", "realizada", "cancelada"}
MODALIDADES_VALIDAS = {"presencial", "virtual", "telefonica"}


class SesionService:
    """Logica de negocio para sesiones psicologicas."""

    def __init__(self):
        self.repo = SesionRepository()
        self.beneficiario_repo = BeneficiarioRepository()
        self.usuario_repo = UsuarioRepository()

    def _validar_relaciones(self, beneficiario_id, terapeuta_id):
        beneficiario = self.beneficiario_repo.get(beneficiario_id)
        if not beneficiario:
            raise ValueError("Beneficiario no encontrado")
        if beneficiario.estado == "cerrado":
            raise ValueError("No se pueden registrar sesiones para casos cerrados")

        terapeuta = self.usuario_repo.get(terapeuta_id)
        if not terapeuta or not terapeuta.activo:
            raise ValueError("Terapeuta no encontrado o inactivo")
        if terapeuta.rol not in {"terapeuta", "admin"}:
            raise ValueError("El usuario asignado no puede atender sesiones")
        return beneficiario, terapeuta

    def _validar_estado_modalidad(self, estado, modalidad):
        if estado.lower() not in ESTADOS_VALIDOS:
            raise ValueError("Estado de sesion invalido")
        if modalidad.lower() not in MODALIDADES_VALIDAS:
            raise ValueError("Modalidad de sesion invalida")

    def create_sesion(self, data):
        self._validar_estado_modalidad(data.estado, data.modalidad)
        beneficiario, _ = self._validar_relaciones(data.beneficiario_id, data.terapeuta_id)

        if self.repo.get_by_identificador(data.identificador):
            raise ValueError("Ya existe una sesion con ese identificador")
        if self.repo.find_slot(data.terapeuta_id, data.fecha, data.hora):
            raise ValueError("El terapeuta ya tiene una sesion en esa fecha y hora")

        sesion = SesionORM(
            identificador=data.identificador,
            beneficiario_id=data.beneficiario_id,
            terapeuta_id=data.terapeuta_id,
            fecha=data.fecha,
            hora=data.hora,
            modalidad=data.modalidad.lower(),
            estado=data.estado.lower(),
            notas=data.notas,
        )
        resultado = self.repo.create(sesion)

        if beneficiario.estado == "activo":
            beneficiario.estado = "en_seguimiento"
            self.beneficiario_repo.update(beneficiario)
        return resultado

    def get_sesion(self, sesion_id):
        return self.repo.get(sesion_id)

    def list_sesiones(self, estado=None, beneficiario_id=None, terapeuta_id=None):
        return self.repo.get_all(estado=estado, beneficiario_id=beneficiario_id, terapeuta_id=terapeuta_id)

    def update_sesion(self, sesion_id, data):
        sesion = self.repo.get(sesion_id)
        if not sesion:
            return None

        values = data.model_dump(exclude_unset=True)
        beneficiario_id = values.get("beneficiario_id", sesion.beneficiario_id)
        terapeuta_id = values.get("terapeuta_id", sesion.terapeuta_id)
        fecha = values.get("fecha", sesion.fecha)
        hora = values.get("hora", sesion.hora)
        estado = values.get("estado", sesion.estado)
        modalidad = values.get("modalidad", sesion.modalidad)

        self._validar_estado_modalidad(estado, modalidad)
        self._validar_relaciones(beneficiario_id, terapeuta_id)
        if self.repo.find_slot(terapeuta_id, fecha, hora, exclude_id=sesion.id):
            raise ValueError("El terapeuta ya tiene una sesion en esa fecha y hora")

        for field, value in values.items():
            if field in {"estado", "modalidad"}:
                value = value.lower()
            setattr(sesion, field, value)
        return self.repo.update(sesion)

    def delete_sesion(self, sesion_id):
        sesion = self.repo.get(sesion_id)
        if not sesion:
            return None
        return self.repo.delete(sesion)

