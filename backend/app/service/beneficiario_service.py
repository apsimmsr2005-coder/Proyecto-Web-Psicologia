from app.entity.beneficiario import BeneficiarioORM
from app.repository.beneficiario_repository import BeneficiarioRepository


ESTADOS_VALIDOS = {"activo", "en_seguimiento", "cerrado"}
RIESGOS_VALIDOS = {"bajo", "medio", "alto"}


class BeneficiarioService:
    """Logica de negocio para beneficiarios."""

    def __init__(self):
        self.repo = BeneficiarioRepository()

    def _validar_estado_y_riesgo(self, estado, nivel_riesgo):
        if estado.lower() not in ESTADOS_VALIDOS:
            raise ValueError("Estado de beneficiario invalido")
        if nivel_riesgo.lower() not in RIESGOS_VALIDOS:
            raise ValueError("Nivel de riesgo invalido")

    def create_beneficiario(self, data):
        self._validar_estado_y_riesgo(data.estado, data.nivel_riesgo)
        if self.repo.get_by_identificador(data.identificador):
            raise ValueError("Ya existe un beneficiario con ese identificador") # valida unicidad ANTES de tocar la BD
        if self.repo.get_by_cedula(data.cedula):
            raise ValueError("Ya existe un beneficiario con esa cedula")

        # convierte el schema Pydantic (data) en un objeto ORM
        beneficiario = BeneficiarioORM(
            identificador=data.identificador,
            nombre=data.nombre,
            apellido=data.apellido,
            cedula=data.cedula,
            fecha_nacimiento=data.fecha_nacimiento,
            direccion=data.direccion,
            telefono=data.telefono,
            estado=data.estado.lower(), # normaliza antes de guardar (consistencia en la BD)
            motivo_consulta=data.motivo_consulta,
            nivel_riesgo=data.nivel_riesgo.lower(),
        )
        return self.repo.create(beneficiario)

    def get_beneficiario(self, beneficiario_id):
        return self.repo.get(beneficiario_id)

    def list_beneficiarios(self, search=None, estado=None):
        return self.repo.get_all(search=search, estado=estado)

    def update_beneficiario(self, beneficiario_id, data):
        beneficiario = self.repo.get(beneficiario_id)
        if not beneficiario:
            return None

        values = data.model_dump(exclude_unset=True) # solo los campos que el cliente Sí envió (update parcial real)
        estado = values.get("estado", beneficiario.estado) # si no vino "estado", usa el actual para validar igual
        riesgo = values.get("nivel_riesgo", beneficiario.nivel_riesgo)
        self._validar_estado_y_riesgo(estado, riesgo)

        if "cedula" in values:
            existente = self.repo.get_by_cedula(values["cedula"])
            if existente and existente.id != beneficiario.id:
                raise ValueError("Ya existe un beneficiario con esa cedula")

        for field, value in values.items():
            if field in {"estado", "nivel_riesgo"}:
                value = value.lower()
            setattr(beneficiario, field, value) # aplica cada campo dinámicamente al objeto ORM
        return self.repo.update(beneficiario)

    def delete_beneficiario(self, beneficiario_id):
        beneficiario = self.repo.get(beneficiario_id)
        if not beneficiario:
            return None
        return self.repo.delete(beneficiario)
