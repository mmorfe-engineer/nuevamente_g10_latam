"""
Motor de Base de Datos Relacional para NuevaMente.
Soporte dual: SQLite (desarrollo local y pruebas) y PostgreSQL (producción / Supabase).
Basado en SQLAlchemy 2.0.
"""
import os
import logging
from contextlib import contextmanager
from typing import Generator
from sqlalchemy import create_engine, event
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy.engine import Engine

from config.settings import settings

logger = logging.getLogger(__name__)

# Base declarativa para todos los modelos ORM
Base = declarative_base()

# Construcción del engine según dialecto
database_url = os.environ.get("DATABASE_URL") or settings.DATABASE_URL

# Asegurar directorio si es SQLite
if database_url.startswith("sqlite"):
    if ":memory:" in database_url:
        db_path = None
    else:
        raw_path = database_url.replace("sqlite:///", "")
        abs_path = os.path.abspath(raw_path)
        dir_path = os.path.dirname(abs_path)

        # Comprobar si el directorio es escribible (en Streamlit Cloud /mount/src es READ-ONLY)
        can_write = False
        try:
            os.makedirs(dir_path, exist_ok=True)
            test_file = os.path.join(dir_path, ".write_test")
            with open(test_file, "w") as f:
                f.write("ok")
            os.remove(test_file)
            can_write = True
        except Exception:
            can_write = False

        if not can_write:
            # Conmutar automáticamente al directorio escribible del contenedor
            safe_db = "/tmp/nuevamente.db"
            database_url = f"sqlite:///{safe_db}"
            logger.warning(f"Directorio {dir_path} es de solo lectura. Conmutando base de datos a: {safe_db}")

    # Habilitar SQLite en modo seguro para concurrencia básica
    engine = create_engine(
        database_url,
        echo=settings.DB_ECHO,
        connect_args={"check_same_thread": False}
    )

    # Activar llaves foráneas y modo WAL en SQLite de forma tolerante a fallos
    @event.listens_for(Engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        try:
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            try:
                cursor.execute("PRAGMA journal_mode=WAL")
            except Exception:
                pass
            cursor.close()
        except Exception as e:
            logger.warning(f"Aviso configurando pragmas SQLite: {e}")
else:
    # PostgreSQL / Neon / Supabase
    engine = create_engine(
        database_url,
        echo=settings.DB_ECHO,
        pool_pre_ping=True
    )

# Fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Crea todas las tablas en la base de datos de manera idempotente y siembra glosario si está vacío."""
    try:
        from src.storage import models  # noqa: F401
        Base.metadata.create_all(bind=engine)
        logger.info("Esquema relacional de NuevaMente inicializado exitosamente.")
    except Exception as e:
        logger.warning(f"Advertencia creando esquema relacional: {e}")

    # Sembrar glosario básico de forma segura si está vacío
    try:
        from src.storage.seed_glossary import seed_glosario_database
        with SessionLocal() as s:
            seed_glosario_database(s)
    except Exception as e:
        logger.debug(f"Aviso sembrando glosario inicial: {e}")


def reset_db():
    """Elimina y recrea todas las tablas (utilidad para tests y reset limpio)."""
    from src.storage import models  # noqa: F401
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    logger.info("Esquema relacional de NuevaMente reiniciado.")


@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    """Generador de sesión transaccional con commit y rollback automático."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"Error en transacción de base de datos: {e}")
        raise
    finally:
        session.close()


def get_db() -> Generator[Session, None, None]:
    """Inyección de dependencia para frameworks y servicios."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
