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
database_url = settings.DATABASE_URL

# Asegurar directorio si es SQLite
if database_url.startswith("sqlite"):
    db_path = database_url.replace("sqlite:///", "")
    if db_path and db_path != ":memory:":
        os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
    
    # Habilitar SQLite en modo seguro para concurrencia básica
    engine = create_engine(
        database_url,
        echo=settings.DB_ECHO,
        connect_args={"check_same_thread": False}
    )

    # Activar llaves foráneas y modo WAL en SQLite
    @event.listens_for(Engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.close()
else:
    # PostgreSQL / Supabase
    engine = create_engine(
        database_url,
        echo=settings.DB_ECHO,
        pool_pre_ping=True
    )

# Fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Crea todas las tablas en la base de datos de manera idempotente."""
    # Importar modelos aquí para registrar metadatos en Base
    from src.storage import models  # noqa: F401
    Base.metadata.create_all(bind=engine)
    logger.info("Esquema relacional de NuevaMente inicializado exitosamente.")


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
