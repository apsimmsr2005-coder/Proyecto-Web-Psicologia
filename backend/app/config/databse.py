"""
Configuracion de SQLAlchemy.

El proyecto usa MySQL por defecto mediante SQLAlchemy ORM. Si se requiere otra
conexion, se puede definir la variable de ambiente DATABASE_URL.
"""

import os
from datetime import date
from hashlib import sha256

from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url
from sqlalchemy.orm import declarative_base, sessionmaker


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://root:root@localhost:3306/saludmente_db",
)


def ensure_mysql_database_exists(database_url):
    """Crea la base de datos MySQL indicada en DATABASE_URL si no existe."""

    url = make_url(database_url)
    if not url.drivername.startswith("mysql") or not url.database:
        return

    database_name = url.database.replace("`", "")
    server_url = url.set(database=None)
    server_engine = create_engine(server_url, echo=False)

    with server_engine.connect() as connection:
        connection.execute(
            text(
                f"CREATE DATABASE IF NOT EXISTS `{database_name}` "
                "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
            )
        )
        connection.commit()

    server_engine.dispose()


ensure_mysql_database_exists(DATABASE_URL)

connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, echo=False, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


def init_db():
    """Crea todas las tablas definidas por las entidades ORM."""

    from app.entity.beneficiario import BeneficiarioORM
    from app.entity.sesion import SesionORM
    from app.entity.seguimiento import SeguimientoORM
    from app.entity.usuario import UsuarioORM

    Base.metadata.create_all(bind=engine)


def seed_db():
    """Inserta datos iniciales para poder probar el sistema de inmediato."""

    from app.entity.beneficiario import BeneficiarioORM
    from app.entity.sesion import SesionORM
    from app.entity.seguimiento import SeguimientoORM
    from app.entity.usuario import UsuarioORM

    db = SessionLocal()
    try:
        if db.query(UsuarioORM).filter_by(correo="admin@sistema.com").first():
            return

        admin = UsuarioORM(
            identificador="USR-001",
            nombre="Admin",
            apellido="Sistema",
            correo="admin@sistema.com",
            contrasena_hash=sha256("admin123".encode("utf-8")).hexdigest(),
            rol="admin",
            activo=True,
        )
        terapeuta = UsuarioORM(
            identificador="USR-002",
            nombre="Laura",
            apellido="Mendez",
            correo="laura@sistema.com",
            contrasena_hash=sha256("terapeuta123".encode("utf-8")).hexdigest(),
            rol="terapeuta",
            activo=True,
        )
        beneficiario = BeneficiarioORM(
            identificador="BEN-001",
            nombre="Carlos",
            apellido="Vargas",
            cedula="1-1111-1111",
            fecha_nacimiento=date(2002, 5, 18),
            direccion="Puntarenas centro",
            telefono="8888-0000",
            estado="en_seguimiento",
            motivo_consulta="Ansiedad asociada a desempleo familiar",
            nivel_riesgo="medio",
        )

        db.add_all([admin, terapeuta, beneficiario])
        db.commit()
        db.refresh(terapeuta)
        db.refresh(beneficiario)

        sesion = SesionORM(
            identificador="SES-001",
            beneficiario_id=beneficiario.id,
            terapeuta_id=terapeuta.id,
            fecha=date.today(),
            hora="09:00",
            modalidad="presencial",
            estado="realizada",
            notas="Primera entrevista y definicion de plan de seguimiento.",
        )
        db.add(sesion)
        db.commit()
        db.refresh(sesion)

        seguimiento = SeguimientoORM(
            identificador="SEG-001",
            beneficiario_id=beneficiario.id,
            sesion_id=sesion.id,
            fecha=date.today(),
            descripcion="Llamar en una semana para valorar evolucion emocional.",
            accion="Llamada de seguimiento",
            prioridad="media",
            completado=False,
        )
        db.add(seguimiento)
        db.commit()
    finally:
        db.close()
