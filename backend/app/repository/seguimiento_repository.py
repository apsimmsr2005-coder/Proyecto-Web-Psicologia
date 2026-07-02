from app.config.database import SessionLocal
from app.entity.seguimiento import SeguimientoORM


class SeguimientoRepository:
    """Repositorio encargado del acceso a datos de seguimientos."""

    def __init__(self):
        self.db = SessionLocal()

    def create(self, seguimiento):
        self.db.add(seguimiento)
        self.db.commit()
        self.db.refresh(seguimiento)
        return seguimiento

    def get(self, seguimiento_id):
        return self.db.query(SeguimientoORM).filter_by(id=seguimiento_id).first()

    def get_by_identificador(self, identificador):
        return self.db.query(SeguimientoORM).filter_by(identificador=identificador).first()

    def get_all(self, beneficiario_id=None, completado=None, prioridad=None):
        query = self.db.query(SeguimientoORM)
        if beneficiario_id:
            query = query.filter(SeguimientoORM.beneficiario_id == beneficiario_id)
        if completado is not None:
            query = query.filter(SeguimientoORM.completado == completado)
        if prioridad:
            query = query.filter(SeguimientoORM.prioridad == prioridad.lower())
        return query.order_by(SeguimientoORM.fecha.desc()).all()

    def update(self, seguimiento):
        self.db.commit()
        self.db.refresh(seguimiento)
        return seguimiento

    def delete(self, seguimiento):
        self.db.delete(seguimiento)
        self.db.commit()
        return seguimiento

