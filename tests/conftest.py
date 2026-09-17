import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["CHROMA_PERSIST_DIR"] = "/tmp/test_chroma_db"
os.environ["APP_ENV"] = "testing"

# Configure engine with StaticPool so all in-memory connections share the exact same DB
test_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

from src.storage import database
from src.storage import models  # noqa: F401
database.engine = test_engine
database.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
database.Base.metadata.create_all(bind=test_engine)

@pytest.fixture(scope="session", autouse=True)
def configure_test_database():
    """Aisla completamente los tests en memoria para nunca tocar data/nuevamente.db."""
    from config.settings import settings
    settings.APP_ENV = "testing"
    database.Base.metadata.create_all(bind=test_engine)
    yield
