from app.config.database import SessionLocal
from app.entity.usuario import UsuarioORM


class UsuarioRepository:
    """Repositorio encargado del acceso a datos de usuarios."""

    def __init__(self):
        self.db = SessionLocal()

    def create(self, usuario):
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def get(self, usuario_id):
        return self.db.query(UsuarioORM).filter_by(id=usuario_id).first()

    def get_by_identificador(self, identificador):
        return self.db.query(UsuarioORM).filter_by(identificador=identificador).first()

    def get_by_correo(self, correo):
        return self.db.query(UsuarioORM).filter_by(correo=correo).first()

    def get_all(self):
        return self.db.query(UsuarioORM).order_by(UsuarioORM.id).all()

    def update(self, usuario):
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def delete(self, usuario):
        self.db.delete(usuario)
        self.db.commit()
        return usuario
