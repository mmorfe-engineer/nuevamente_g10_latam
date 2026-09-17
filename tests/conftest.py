import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["CHROMA_PERSIST_DIR"] = "/tmp/test_chroma_db"
os.environ["APP_ENV"] = "testing"

@pytest.fixture(scope="session", autouse=True)
def configure_test_database():
    """Aisla completamente los tests en memoria para nunca tocar data/nuevamente.db."""
    from src.storage import database
    test_engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False}
    )
    database.engine = test_engine
    database.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    database.Base.metadata.create_all(bind=test_engine)
    yield
