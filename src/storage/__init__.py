"""
Módulo de Almacenamiento y Persistencia de NuevaMente.
Integra base de datos relacional (SQLAlchemy 2.0) y OCI Object Storage Always Free.
"""
from src.storage.database import Base, engine, SessionLocal, init_db, reset_db, get_db, get_db_session
from src.storage.models import (
    UserModel,
    TechnicalDocumentModel,
    RAGKnowledgeBaseModel,
    LearningSessionModel,
    FlashcardModel,
    QuizModel,
    QuizQuestionModel
)
from src.storage.repository import (
    UserRepository,
    TechnicalDocumentRepository,
    RAGKnowledgeBaseRepository,
    LearningSessionRepository,
    FlashcardRepository,
    QuizRepository
)
from src.storage.oci_client import oci_storage, OCIStorageClient

__all__ = [
    "Base",
    "engine",
    "SessionLocal",
    "init_db",
    "reset_db",
    "get_db",
    "get_db_session",
    "UserModel",
    "TechnicalDocumentModel",
    "RAGKnowledgeBaseModel",
    "LearningSessionModel",
    "FlashcardModel",
    "QuizModel",
    "QuizQuestionModel",
    "UserRepository",
    "TechnicalDocumentRepository",
    "RAGKnowledgeBaseRepository",
    "LearningSessionRepository",
    "FlashcardRepository",
    "QuizRepository",
    "oci_storage",
    "OCIStorageClient",
]
