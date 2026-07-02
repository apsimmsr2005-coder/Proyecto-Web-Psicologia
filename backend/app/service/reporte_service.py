from sqlalchemy import func

from app.config.database import SessionLocal
from app.entity.beneficiario import BeneficiarioORM
from app.entity.seguimiento import SeguimientoORM
from app.entity.sesion import SesionORM
from app.entity.usuario import UsuarioORM


class ReporteService:
    """Consultas agregadas para reportes del sistema."""

    def resumen(self):
        with SessionLocal() as db:
            total_beneficiarios = db.query(BeneficiarioORM).count()
            casos_activos = db.query(BeneficiarioORM).filter(BeneficiarioORM.estado != "cerrado").count()
            sesiones_realizadas = db.query(SesionORM).filter_by(estado="realizada").count()
            seguimientos_pendientes = db.query(SeguimientoORM).filter_by(completado=False).count()
            riesgo_alto = db.query(BeneficiarioORM).filter_by(nivel_riesgo="alto").count()
            return {
                "total_beneficiarios": total_beneficiarios,
                "casos_activos": casos_activos,
                "sesiones_realizadas": sesiones_realizadas,
                "seguimientos_pendientes": seguimientos_pendientes,
                "beneficiarios_riesgo_alto": riesgo_alto,
            }

    def beneficiarios_por_estado(self):
        with SessionLocal() as db:
            rows = (
                db.query(BeneficiarioORM.estado, func.count(BeneficiarioORM.id)) # selecciona columna + un conteo, no filas completas
                .group_by(BeneficiarioORM.estado)
                .all()
            )
            # rows es una lista de tuplas: [("activo", 12), ("cerrado", 5), ...]
            return [{"estado": estado, "total": total} for estado, total in rows]

    def sesiones_por_estado(self):
        with SessionLocal() as db:
            rows = (
                db.query(SesionORM.estado, func.count(SesionORM.id))
                .group_by(SesionORM.estado)
                .all()
            )
            return [{"estado": estado, "total": total} for estado, total in rows]

    def carga_terapeutas(self):
        with SessionLocal() as db:
            rows = (
                db.query(
                    UsuarioORM.id,
                    UsuarioORM.nombre,
                    UsuarioORM.apellido,
                    func.count(SesionORM.id), # cuenta sesiones por cada terapeuta (par con el group_by de abajo)
                )
                # outerjoin (LEFT JOIN): trae TODOS los usuarios aunque tengan 0 sesiones.
                .outerjoin(SesionORM, UsuarioORM.id == SesionORM.terapeuta_id)
                .filter(UsuarioORM.rol.in_(["terapeuta", "admin"]))
                .group_by(UsuarioORM.id, UsuarioORM.nombre, UsuarioORM.apellido)
                .all()
            )
            return [
                {
                    "terapeuta_id": usuario_id,
                    "terapeuta": f"{nombre} {apellido}",
                    "total_sesiones": total,
                }
                for usuario_id, nombre, apellido, total in rows
            ]
