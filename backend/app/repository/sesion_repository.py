from sqlalchemy import and_

from app.config.database import SessionLocal
from app.entity.sesion import SesionORM


class SesionRepository:
    """Repositorio encargado del acceso a datos de sesiones."""

    def __init__(self):
        self.db = SessionLocal()

    def create(self, sesion):
        self.db.add(sesion)
        self.db.commit()
        self.db.refresh(sesion)
        return sesion

    def get(self, sesion_id):
        return self.db.query(SesionORM).filter_by(id=sesion_id).first()

    def get_by_identificador(self, identificador):
        return self.db.query(SesionORM).filter_by(identificador=identificador).first()

    def get_all(self, estado=None, beneficiario_id=None, terapeuta_id=None):
        query = self.db.query(SesionORM)
        if estado:
            query = query.filter(SesionORM.estado == estado.lower())
        if beneficiario_id:
            query = query.filter(SesionORM.beneficiario_id == beneficiario_id)
        if terapeuta_id:
            query = query.filter(SesionORM.terapeuta_id == terapeuta_id)
        return query.order_by(SesionORM.fecha.desc(), SesionORM.hora).all()

    def find_slot(self, terapeuta_id, fecha, hora, exclude_id=None):
        query = self.db.query(SesionORM).filter(
            and_(
                SesionORM.terapeuta_id == terapeuta_id,
                SesionORM.fecha == fecha,
                SesionORM.hora == hora,
                SesionORM.estado != "cancelada",
            )
        )
        if exclude_id:
            query = query.filter(SesionORM.id != exclude_id)
        return query.first()

    def update(self, sesion):
        self.db.commit()
        self.db.refresh(sesion)
        return sesion

    def delete(self, sesion):
        self.db.delete(sesion)
        self.db.commit()
        return sesion

