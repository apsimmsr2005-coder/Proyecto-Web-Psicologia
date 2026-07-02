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

# os.getenv: usa la variable de entorno si existe, si no cae en este default local
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://root:root@localhost:3306/saludmente_db",
)


def ensure_mysql_database_exists(database_url):
    """Crea la base de datos MySQL indicada en DATABASE_URL si no existe."""
    
    url = make_url(database_url) # parsea el string de conexión en un objeto manejable (driver, host, db, etc.)
    if not url.drivername.startswith("mysql") or not url.database:
        return # si no es MySQL (ej. sqlite), no hay nada que crear acá

    database_name = url.database.replace("`", "") # limpia backticks por si vinieran en el nombre
    server_url = url.set(database=None) # misma conexión pero SIN especificar base de datos
    server_engine = create_engine(server_url, echo=False) # conecta al SERVIDOR, no a una BD en particular (necesario porque la BD aún no existe)

    with server_engine.connect() as connection:
        connection.execute(
            # text(): SQL crudo, necesario porque CREATE DATABASE no es una operación ORM
            text(
                f"CREATE DATABASE IF NOT EXISTS `{database_name}` "
                "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
            )
        )
        connection.commit()

    server_engine.dispose() # cierra las conexiones de este engine temporal 

# se ejecuta al importar este módulo, antes de crear el engine real
ensure_mysql_database_exists(DATABASE_URL)

connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    # sqlite por defecto bloquea uso multi-hilo; esto lo permite (necesario para FastAPI)
    connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, echo=False, connect_args=connect_args) # engine real, ya apuntando a la BD específica
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False) # fábrica de sesiones (por eso se usa como SessionLocal() en los repos)
Base = declarative_base() # clase base de la que heredan todas las entidades ORM (BeneficiarioORM, etc.)


def init_db():
    """Crea todas las tablas definidas por las entidades ORM."""

    # imports adentro de la función: se necesitan importar las entidades para que
    # SQLAlchemy las "registre" en Base.metadata antes de create_all (si no, no las crea)
    from app.entity.beneficiario import BeneficiarioORM
    from app.entity.sesion import SesionORM
    from app.entity.seguimiento import SeguimientoORM
    from app.entity.usuario import UsuarioORM

    Base.metadata.create_all(bind=engine) # crea las tablas que aún no existan (no toca las que ya existen)


def seed_db():
    """Inserta datos iniciales para poder probar el sistema de inmediato."""

    from app.entity.beneficiario import BeneficiarioORM
    from app.entity.sesion import SesionORM
    from app.entity.seguimiento import SeguimientoORM
    from app.entity.usuario import UsuarioORM

    # sesión manual (no "with"), por eso hay que cerrarla a mano en el finally
    db = SessionLocal()
    try:
        if db.query(UsuarioORM).filter_by(correo="admin@sistema.com").first():
            return # evita duplicar el seed si ya se corrió antes

        admin = UsuarioORM(
            identificador="USR-001",
            nombre="Admin",
            apellido="Sistema",
            correo="admin@sistema.com",
            contrasena_hash=sha256("admin123".encode("utf-8")).hexdigest(), # guarda el hash, nunca la contraseña en texto plano
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

        db.add_all([admin, terapeuta, beneficiario]) # agrupa varios add() en una sola llamada
        db.commit()
        db.refresh(terapeuta) # recupera el "id" generado por la BD, necesario para usarlo abajo (terapeuta_id)
        db.refresh(beneficiario) # idem, necesario para beneficiario_id

        sesion = SesionORM(
            identificador="SES-001",
            beneficiario_id=beneficiario.id, # requiere el refresh anterior: sin id, esto sería None
            terapeuta_id=terapeuta.id,
            fecha=date.today(),
            hora="09:00",
            modalidad="presencial",
            estado="realizada",
            notas="Primera entrevista y definicion de plan de seguimiento.",
        )
        db.add(sesion)
        db.commit()
        db.refresh(sesion) # necesario para sesion.id, usado en seguimiento

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
        db.close() # se ejecuta siempre, incluso si algo falla arriba (evita dejar conexiones abiertas)
