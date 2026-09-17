"""
Modelos Relacionales SQLAlchemy 2.0 para NuevaMente.
Implementa las 6 entidades core de la plataforma EdTech SaaS:
1. Users (users)
2. TechnicalDocuments (technical_documents)
3. RAGKnowledgeBases (rag_knowledge_bases)
4. LearningSessions (learning_sessions)
5. Flashcards (flashcards)
6. Quizzes y QuizQuestions (quizzes, quiz_questions)
"""
import uuid
from datetime import datetime
from sqlalchemy import (
    Column,
    String,
    Text,
    Integer,
    Float,
    DateTime,
    ForeignKey,
    JSON,
    Uuid
)
from sqlalchemy.orm import relationship

from src.storage.database import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    full_name = Column(String(255), nullable=False)
    role = Column(String(50), default="estudiante", nullable=False)
    target_profile_default = Column(String(100), default="Principiante", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)

    # Relaciones
    documents = relationship("TechnicalDocumentModel", back_populates="user")
    sessions = relationship("LearningSessionModel", back_populates="user")
    flashcards = relationship("FlashcardModel", back_populates="user")
    quizzes = relationship("QuizModel", back_populates="user")

    def to_dict(self):
        return {
            "id": str(self.id),
            "email": self.email,
            "full_name": self.full_name,
            "role": self.role,
            "target_profile_default": self.target_profile_default,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class TechnicalDocumentModel(Base):
    __tablename__ = "technical_documents"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(Uuid(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    title = Column(String(255), nullable=False)
    source_type = Column(String(50), nullable=False)
    raw_content = Column(Text, nullable=False)
    content_hash = Column(String(64), nullable=False, index=True)
    char_count = Column(Integer, default=0, nullable=False)
    oci_bucket = Column(String(100), default="nuevamente-documentos-origen", nullable=False)
    oci_object_id = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relaciones
    user = relationship("UserModel", back_populates="documents")
    rag_kbs = relationship("RAGKnowledgeBaseModel", back_populates="document", cascade="all, delete-orphan")
    sessions = relationship("LearningSessionModel", back_populates="document", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": str(self.id),
            "user_id": str(self.user_id) if self.user_id else None,
            "title": self.title,
            "source_type": self.source_type,
            "content_hash": self.content_hash,
            "char_count": self.char_count,
            "oci_bucket": self.oci_bucket,
            "oci_object_id": self.oci_object_id,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class RAGKnowledgeBaseModel(Base):
    __tablename__ = "rag_knowledge_bases"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(Uuid(as_uuid=True), ForeignKey("technical_documents.id", ondelete="CASCADE"), nullable=False)
    collection_name = Column(String(100), nullable=False, unique=True)
    chunk_count = Column(Integer, default=0, nullable=False)
    chunk_strategy = Column(String(50), default="recursive_character", nullable=False)
    chunk_size = Column(Integer, default=1000, nullable=False)
    chunk_overlap = Column(Integer, default=150, nullable=False)
    embedding_model = Column(String(100), default="all-MiniLM-L6-v2", nullable=False)
    status = Column(String(50), default="pending", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relaciones
    document = relationship("TechnicalDocumentModel", back_populates="rag_kbs")

    def to_dict(self):
        return {
            "id": str(self.id),
            "document_id": str(self.document_id),
            "collection_name": self.collection_name,
            "chunk_count": self.chunk_count,
            "chunk_strategy": self.chunk_strategy,
            "chunk_size": self.chunk_size,
            "chunk_overlap": self.chunk_overlap,
            "embedding_model": self.embedding_model,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class LearningSessionModel(Base):
    __tablename__ = "learning_sessions"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(Uuid(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    document_id = Column(Uuid(as_uuid=True), ForeignKey("technical_documents.id", ondelete="CASCADE"), nullable=False)
    perfil_destinatario = Column(String(100), nullable=False)
    formato_salida = Column(String(100), nullable=False)
    nicho_sector = Column(String(50), default="General", nullable=False)
    nivel_detalle = Column(String(50), default="Didactico", nullable=False)
    titulo_adaptado = Column(String(255), nullable=False)
    introduccion_contextualizada = Column(Text, nullable=False)
    tiempo_estimado_minutos = Column(Integer, default=5, nullable=False)
    conceptos_clave = Column(JSON, default=list, nullable=False)
    anclaje_fuente_score = Column(Float, default=0.95, nullable=False)
    claridad_pedagogica = Column(String(50), default="Alta", nullable=False)
    observaciones_calidad = Column(Text, default="", nullable=False)
    oci_bucket = Column(String(100), default="nuevamente-contenidos-educativos", nullable=False)
    oci_object_id = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relaciones
    user = relationship("UserModel", back_populates="sessions")
    document = relationship("TechnicalDocumentModel", back_populates="sessions")
    flashcards = relationship("FlashcardModel", back_populates="session", cascade="all, delete-orphan")
    quizzes = relationship("QuizModel", back_populates="session", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": str(self.id),
            "user_id": str(self.user_id) if self.user_id else None,
            "document_id": str(self.document_id),
            "perfil_destinatario": self.perfil_destinatario,
            "formato_salida": self.formato_salida,
            "nicho_sector": self.nicho_sector,
            "nivel_detalle": self.nivel_detalle,
            "titulo_adaptado": self.titulo_adaptado,
            "introduccion_contextualizada": self.introduccion_contextualizada,
            "tiempo_estimado_minutos": self.tiempo_estimado_minutos,
            "conceptos_clave": self.conceptos_clave,
            "anclaje_fuente_score": self.anclaje_fuente_score,
            "claridad_pedagogica": self.claridad_pedagogica,
            "observaciones_calidad": self.observaciones_calidad,
            "oci_bucket": self.oci_bucket,
            "oci_object_id": self.oci_object_id,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class FlashcardModel(Base):
    __tablename__ = "flashcards"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(Uuid(as_uuid=True), ForeignKey("learning_sessions.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Uuid(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    front = Column(Text, nullable=False)
    back = Column(Text, nullable=False)
    didactic_hint = Column(Text, nullable=True)
    mastery_level = Column(Integer, default=0, nullable=False)
    next_review_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relaciones
    session = relationship("LearningSessionModel", back_populates="flashcards")
    user = relationship("UserModel", back_populates="flashcards")

    def to_dict(self):
        return {
            "id": str(self.id),
            "session_id": str(self.session_id),
            "user_id": str(self.user_id) if self.user_id else None,
            "front": self.front,
            "back": self.back,
            "didactic_hint": self.didactic_hint,
            "mastery_level": self.mastery_level,
            "next_review_at": self.next_review_at.isoformat() if self.next_review_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class QuizModel(Base):
    __tablename__ = "quizzes"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(Uuid(as_uuid=True), ForeignKey("learning_sessions.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Uuid(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    title = Column(String(255), nullable=False)
    total_questions = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relaciones
    session = relationship("LearningSessionModel", back_populates="quizzes")
    user = relationship("UserModel", back_populates="quizzes")
    questions = relationship("QuizQuestionModel", back_populates="quiz", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": str(self.id),
            "session_id": str(self.session_id),
            "user_id": str(self.user_id) if self.user_id else None,
            "title": self.title,
            "total_questions": self.total_questions,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "questions": [q.to_dict() for q in self.questions] if self.questions else []
        }


class QuizQuestionModel(Base):
    __tablename__ = "quiz_questions"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    quiz_id = Column(Uuid(as_uuid=True), ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False)
    question_text = Column(Text, nullable=False)
    options = Column(JSON, nullable=False)
    correct_answer = Column(String(255), nullable=False)
    explanation = Column(Text, nullable=False)
    didactic_hint = Column(Text, nullable=True)
    bloom_taxonomy_level = Column(String(50), default="Comprender", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relaciones
    quiz = relationship("QuizModel", back_populates="questions")

    def to_dict(self):
        return {
            "id": str(self.id),
            "quiz_id": str(self.quiz_id),
            "question_text": self.question_text,
            "options": self.options,
            "correct_answer": self.correct_answer,
            "explanation": self.explanation,
            "didactic_hint": self.didactic_hint,
            "bloom_taxonomy_level": self.bloom_taxonomy_level,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


# ==============================================================================
# ESTÁNDAR LEXFORJA: INGESTA ASIMÉTRICA Y BASE DE DATOS ENRIQUECIDA
# ==============================================================================

class CorpusDocumentoModel(Base):
    __tablename__ = "corpus_documentos"

    doc_id = Column(String(50), primary_key=True)
    titulo = Column(String(255), nullable=False)
    archivo_origen = Column(String(255), nullable=False)
    idioma = Column(String(10), nullable=False, default="en")
    version_normativa = Column(String(50), nullable=True)
    peso_bytes = Column(Integer, default=0, nullable=False)
    sha256_hash = Column(String(64), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relaciones
    chunks = relationship("CorpusChunkModel", back_populates="documento", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "doc_id": self.doc_id,
            "titulo": self.titulo,
            "archivo_origen": self.archivo_origen,
            "idioma": self.idioma,
            "version_normativa": self.version_normativa,
            "peso_bytes": self.peso_bytes,
            "sha256_hash": self.sha256_hash,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "total_chunks": len(self.chunks) if self.chunks else 0
        }


class CorpusChunkModel(Base):
    __tablename__ = "corpus_chunks"

    chunk_id = Column(String(50), primary_key=True)
    doc_id = Column(String(50), ForeignKey("corpus_documentos.doc_id", ondelete="CASCADE"), nullable=False)
    pagina_numero = Column(Integer, nullable=False, default=1)
    capitulo_seccion = Column(String(255), nullable=True)
    contenido_original = Column(Text, nullable=False)
    sintesis_espanol = Column(Text, nullable=False)
    terminos_clave_en = Column(JSON, nullable=False, default=list)
    terminos_clave_es = Column(JSON, nullable=False, default=list)
    aplicabilidad_roles = Column(JSON, nullable=False, default=list)
    modifica_a_chunk_id = Column(String(50), nullable=True, index=True)
    version_prioridad = Column(Float, default=1.0, nullable=False)
    embedding_id = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relaciones
    documento = relationship("CorpusDocumentoModel", back_populates="chunks")

    def to_dict(self):
        return {
            "chunk_id": self.chunk_id,
            "doc_id": self.doc_id,
            "pagina_numero": self.pagina_numero,
            "capitulo_seccion": self.capitulo_seccion,
            "contenido_original": self.contenido_original,
            "sintesis_espanol": self.sintesis_espanol,
            "terminos_clave_en": self.terminos_clave_en,
            "terminos_clave_es": self.terminos_clave_es,
            "aplicabilidad_roles": self.aplicabilidad_roles,
            "modifica_a_chunk_id": self.modifica_a_chunk_id,
            "version_prioridad": self.version_prioridad,
            "embedding_id": self.embedding_id,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class GlosarioCiberseguridadModel(Base):
    __tablename__ = "glosario_ciberseguridad"

    id = Column(Integer, primary_key=True, autoincrement=True)
    termino_en = Column(String(150), unique=True, nullable=False, index=True)
    termino_es = Column(String(150), nullable=False, index=True)
    definicion_didactica = Column(Text, nullable=False)
    categoria = Column(String(50), default="General", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "termino_en": self.termino_en,
            "termino_es": self.termino_es,
            "definicion_didactica": self.definicion_didactica,
            "categoria": self.categoria,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
