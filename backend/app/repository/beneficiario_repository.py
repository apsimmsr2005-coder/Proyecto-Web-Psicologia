from sqlalchemy import or_

from app.config.database import SessionLocal
from app.entity.beneficiario import BeneficiarioORM


class BeneficiarioRepository:
    """Repositorio encargado del acceso a datos de beneficiarios."""

    def create(self, beneficiario):
        with SessionLocal() as db:
            db.add(beneficiario)
            db.commit()
            db.refresh(beneficiario)
            return beneficiario

    def get(self, beneficiario_id):
        with SessionLocal() as db:
            return db.query(BeneficiarioORM).filter_by(id=beneficiario_id).first()

    def get_by_identificador(self, identificador):
        with SessionLocal() as db:
            return db.query(BeneficiarioORM).filter_by(identificador=identificador).first()

    def get_by_cedula(self, cedula):
        with SessionLocal() as db:
            return db.query(BeneficiarioORM).filter_by(cedula=cedula).first()

    def get_all(self, search=None, estado=None):
        with SessionLocal() as db:
            query = db.query(BeneficiarioORM)
            if search:
                pattern = f"%{search}%"
                query = query.filter(
                    or_(
                        BeneficiarioORM.nombre.ilike(pattern),
                        BeneficiarioORM.apellido.ilike(pattern),
                        BeneficiarioORM.cedula.ilike(pattern),
                        BeneficiarioORM.identificador.ilike(pattern),
                    )
                )
            if estado:
                query = query.filter(BeneficiarioORM.estado == estado.lower())
            return query.order_by(BeneficiarioORM.id).all()

    def update(self, beneficiario):
        with SessionLocal() as db:
            merged = db.merge(beneficiario)
            db.commit()
            db.refresh(merged)
            return merged

    def delete(self, beneficiario):
        with SessionLocal() as db:
            merged = db.merge(beneficiario)
            db.delete(merged)
            db.commit()
            return beneficiario
