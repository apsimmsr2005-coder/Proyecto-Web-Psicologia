from app.entity.usuario import UsuarioORM
from app.repository.usuario_repository import UsuarioRepository
from app.service.auth_service import hash_password


ROLES_VALIDOS = {"admin", "terapeuta"}


class UsuarioService:
    """Logica de negocio para usuarios."""

    def __init__(self):
        self.repo = UsuarioRepository()

    def create_usuario(self, data):
        if data.rol.lower() not in ROLES_VALIDOS:
            raise ValueError("Rol invalido")
        if self.repo.get_by_identificador(data.identificador):
            raise ValueError("Ya existe un usuario con ese identificador")
        if self.repo.get_by_correo(data.correo):
            raise ValueError("Ya existe un usuario con ese correo")

        usuario = UsuarioORM(
            identificador=data.identificador,
            nombre=data.nombre,
            apellido=data.apellido,
            correo=data.correo,
            contrasena_hash=hash_password(data.contrasena),
            rol=data.rol.lower(),
            activo=data.activo,
        )
        return self.repo.create(usuario)

    def get_usuario(self, usuario_id):
        return self.repo.get(usuario_id)

    def list_usuarios(self):
        return self.repo.get_all()

    def update_usuario(self, usuario_id, data):
        usuario = self.repo.get(usuario_id)
        if not usuario:
            return None

        values = data.model_dump(exclude_unset=True)
        if "rol" in values and values["rol"].lower() not in ROLES_VALIDOS:
            raise ValueError("Rol invalido")
        if "correo" in values:
            existente = self.repo.get_by_correo(values["correo"])
            if existente and existente.id != usuario.id:
                raise ValueError("Ya existe un usuario con ese correo")

        for field, value in values.items():
            if field == "contrasena":
                usuario.contrasena_hash = hash_password(value)
            elif field == "rol":
                usuario.rol = value.lower()
            else:
                setattr(usuario, field, value)
        return self.repo.update(usuario)

    def delete_usuario(self, usuario_id):
        usuario = self.repo.get(usuario_id)
        if not usuario:
            return None
        return self.repo.delete(usuario)
