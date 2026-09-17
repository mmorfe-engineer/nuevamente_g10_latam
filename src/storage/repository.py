"""
Capa de Repositorios (Data Access Objects) para NuevaMente.
Implementa operaciones CRUD y lógica de persistencia desacoplada para las 6 entidades core.
"""
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from sqlalchemy.orm import Session

from src.storage.models import (
    UserModel,
    TechnicalDocumentModel,
    RAGKnowledgeBaseModel,
    LearningSessionModel,
    FlashcardModel,
    QuizModel,
    QuizQuestionModel
)
from src.utils.schemas import (
    UserCreate,
    TechnicalDocumentCreate,
    RAGKnowledgeBaseCreate,
    LearningSessionCreate,
    FlashcardCreate,
    FlashcardUpdateMastery,
    QuizCreate
)


class UserRepository:
    @staticmethod
    def get_by_id(db: Session, user_id: UUID) -> Optional[UserModel]:
        return db.query(UserModel).filter(UserModel.id == user_id).first()

    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[UserModel]:
        return db.query(UserModel).filter(UserModel.email == email).first()

    @staticmethod
    def create(db: Session, user: UserCreate) -> UserModel:
        db_user = UserModel(
            email=user.email,
            full_name=user.full_name,
            role=user.role.value if hasattr(user.role, "value") else str(user.role),
            target_profile_default=(
                user.target_profile_default.value
                if hasattr(user.target_profile_default, "value")
                else str(user.target_profile_default)
            )
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @classmethod
    def get_or_create_default_user(cls, db: Session) -> UserModel:
        email = "demo.estudiante@nuevamente.ai"
        user = cls.get_by_email(db, email)
        if not user:
            user = UserModel(
                email=email,
                full_name="Estudiante Demo ONE G10",
                role="estudiante",
                target_profile_default="Principiante"
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        return user


class TechnicalDocumentRepository:
    @staticmethod
    def create(db: Session, doc: TechnicalDocumentCreate) -> TechnicalDocumentModel:
        db_doc = TechnicalDocumentModel(
            user_id=doc.user_id,
            title=doc.title,
            source_type=doc.source_type,
            raw_content=doc.raw_content,
            content_hash=doc.content_hash,
            char_count=doc.char_count or len(doc.raw_content),
            oci_bucket=doc.oci_bucket,
            oci_object_id=doc.oci_object_id
        )
        db.add(db_doc)
        db.commit()
        db.refresh(db_doc)
        return db_doc

    @staticmethod
    def get_by_id(db: Session, doc_id: UUID) -> Optional[TechnicalDocumentModel]:
        return db.query(TechnicalDocumentModel).filter(TechnicalDocumentModel.id == doc_id).first()

    @staticmethod
    def get_by_hash(db: Session, content_hash: str) -> Optional[TechnicalDocumentModel]:
        return db.query(TechnicalDocumentModel).filter(TechnicalDocumentModel.content_hash == content_hash).first()

    @staticmethod
    def list_all(db: Session, limit: int = 50) -> List[TechnicalDocumentModel]:
        return db.query(TechnicalDocumentModel).order_by(TechnicalDocumentModel.created_at.desc()).limit(limit).all()


class RAGKnowledgeBaseRepository:
    @staticmethod
    def create(db: Session, kb: RAGKnowledgeBaseCreate) -> RAGKnowledgeBaseModel:
        db_kb = RAGKnowledgeBaseModel(
            document_id=kb.document_id,
            collection_name=kb.collection_name,
            chunk_count=kb.chunk_count,
            chunk_strategy=kb.chunk_strategy,
            chunk_size=kb.chunk_size,
            chunk_overlap=kb.chunk_overlap,
            embedding_model=kb.embedding_model,
            status=kb.status.value if hasattr(kb.status, "value") else str(kb.status)
        )
        db.add(db_kb)
        db.commit()
        db.refresh(db_kb)
        return db_kb

    @staticmethod
    def get_by_document_id(db: Session, doc_id: UUID) -> Optional[RAGKnowledgeBaseModel]:
        return db.query(RAGKnowledgeBaseModel).filter(RAGKnowledgeBaseModel.document_id == doc_id).first()

    @staticmethod
    def update_status(db: Session, kb_id: UUID, status: str) -> Optional[RAGKnowledgeBaseModel]:
        kb = db.query(RAGKnowledgeBaseModel).filter(RAGKnowledgeBaseModel.id == kb_id).first()
        if kb:
            kb.status = status
            db.commit()
            db.refresh(kb)
        return kb


class LearningSessionRepository:
    @staticmethod
    def create(db: Session, session_data: LearningSessionCreate) -> LearningSessionModel:
        db_session = LearningSessionModel(
            user_id=session_data.user_id,
            document_id=session_data.document_id,
            perfil_destinatario=(
                session_data.perfil_destinatario.value
                if hasattr(session_data.perfil_destinatario, "value")
                else str(session_data.perfil_destinatario)
            ),
            formato_salida=(
                session_data.formato_salida.value
                if hasattr(session_data.formato_salida, "value")
                else str(session_data.formato_salida)
            ),
            nicho_sector=(
                session_data.nicho_sector.value
                if hasattr(session_data.nicho_sector, "value")
                else str(session_data.nicho_sector)
            ),
            nivel_detalle=(
                session_data.nivel_detalle.value
                if hasattr(session_data.nivel_detalle, "value")
                else str(session_data.nivel_detalle)
            ),
            titulo_adaptado=session_data.titulo_adaptado,
            introduccion_contextualizada=session_data.introduccion_contextualizada,
            tiempo_estimado_minutos=session_data.tiempo_estimado_minutos,
            conceptos_clave=session_data.conceptos_clave,
            anclaje_fuente_score=session_data.anclaje_fuente_score,
            claridad_pedagogica=session_data.claridad_pedagogica,
            observaciones_calidad=session_data.observaciones_calidad,
            oci_bucket=session_data.oci_bucket,
            oci_object_id=session_data.oci_object_id
        )
        db.add(db_session)
        db.commit()
        db.refresh(db_session)
        return db_session

    @staticmethod
    def get_by_id(db: Session, session_id: UUID) -> Optional[LearningSessionModel]:
        return db.query(LearningSessionModel).filter(LearningSessionModel.id == session_id).first()

    @staticmethod
    def list_by_user(db: Session, user_id: UUID) -> List[LearningSessionModel]:
        return (
            db.query(LearningSessionModel)
            .filter(LearningSessionModel.user_id == user_id)
            .order_by(LearningSessionModel.created_at.desc())
            .all()
        )


class FlashcardRepository:
    @staticmethod
    def create_batch(db: Session, cards: List[FlashcardCreate]) -> List[FlashcardModel]:
        db_cards = []
        for c in cards:
            card_model = FlashcardModel(
                session_id=c.session_id,
                user_id=c.user_id,
                front=c.front,
                back=c.back,
                didactic_hint=c.didactic_hint,
                mastery_level=c.mastery_level,
                next_review_at=c.next_review_at
            )
            db.add(card_model)
            db_cards.append(card_model)
        db.commit()
        for card in db_cards:
            db.refresh(card)
        return db_cards

    @staticmethod
    def get_by_session(db: Session, session_id: UUID) -> List[FlashcardModel]:
        return db.query(FlashcardModel).filter(FlashcardModel.session_id == session_id).all()

    @staticmethod
    def update_mastery(
        db: Session, card_id: UUID, mastery_data: FlashcardUpdateMastery
    ) -> Optional[FlashcardModel]:
        card = db.query(FlashcardModel).filter(FlashcardModel.id == card_id).first()
        if card:
            card.mastery_level = mastery_data.mastery_level
            card.next_review_at = mastery_data.next_review_at
            db.commit()
            db.refresh(card)
        return card


class QuizRepository:
    @staticmethod
    def create_quiz_with_questions(db: Session, quiz_data: QuizCreate) -> QuizModel:
        db_quiz = QuizModel(
            session_id=quiz_data.session_id,
            user_id=quiz_data.user_id,
            title=quiz_data.title,
            total_questions=len(quiz_data.questions) or quiz_data.total_questions
        )
        db.add(db_quiz)
        db.flush()  # Obtener ID del quiz para las preguntas

        for q in quiz_data.questions:
            db_question = QuizQuestionModel(
                quiz_id=db_quiz.id,
                question_text=q.question_text,
                options=q.options,
                correct_answer=q.correct_answer,
                explanation=q.explanation,
                didactic_hint=q.didactic_hint,
                bloom_taxonomy_level=(
                    q.bloom_taxonomy_level.value
                    if hasattr(q.bloom_taxonomy_level, "value")
                    else str(q.bloom_taxonomy_level)
                )
            )
            db.add(db_question)

        db.commit()
        db.refresh(db_quiz)
        return db_quiz

    @staticmethod
    def get_by_id(db: Session, quiz_id: UUID) -> Optional[QuizModel]:
        return db.query(QuizModel).filter(QuizModel.id == quiz_id).first()

    @staticmethod
    def get_by_session(db: Session, session_id: UUID) -> Optional[QuizModel]:
        return db.query(QuizModel).filter(QuizModel.session_id == session_id).first()


# ==============================================================================
# REPOSITORIOS LEXFORJA: CORPUS Y GLOSARIO CANÓNICO
# ==============================================================================

class CorpusRepository:
    @staticmethod
    def create_document(db: Session, doc_data: dict) -> "CorpusDocumentoModel":
        from src.storage.models import CorpusDocumentoModel
        doc = CorpusDocumentoModel(
            doc_id=doc_data["doc_id"],
            titulo=doc_data["titulo"],
            archivo_origen=doc_data["archivo_origen"],
            idioma=doc_data.get("idioma", "en"),
            version_normativa=doc_data.get("version_normativa"),
            peso_bytes=doc_data.get("peso_bytes", 0),
            sha256_hash=doc_data["sha256_hash"]
        )
        db.add(doc)
        db.commit()
        db.refresh(doc)
        return doc

    @staticmethod
    def get_document(db: Session, doc_id: str) -> Optional["CorpusDocumentoModel"]:
        from src.storage.models import CorpusDocumentoModel
        return db.query(CorpusDocumentoModel).filter(CorpusDocumentoModel.doc_id == doc_id).first()

    @staticmethod
    def create_chunks(db: Session, chunks_data: List[dict]) -> List["CorpusChunkModel"]:
        from src.storage.models import CorpusChunkModel
        db_chunks = []
        for c in chunks_data:
            chunk = CorpusChunkModel(
                chunk_id=c["chunk_id"],
                doc_id=c["doc_id"],
                pagina_numero=c.get("pagina_numero", 1),
                capitulo_seccion=c.get("capitulo_seccion"),
                contenido_original=c["contenido_original"],
                sintesis_espanol=c["sintesis_espanol"],
                terminos_clave_en=c.get("terminos_clave_en", []),
                terminos_clave_es=c.get("terminos_clave_es", []),
                aplicabilidad_roles=c.get("aplicabilidad_roles", []),
                modifica_a_chunk_id=c.get("modifica_a_chunk_id"),
                version_prioridad=c.get("version_prioridad", 1.0),
                embedding_id=c.get("embedding_id")
            )
            db.add(chunk)
            db_chunks.append(chunk)
        db.commit()
        for chunk in db_chunks:
            db.refresh(chunk)
        return db_chunks

    @staticmethod
    def get_chunks_with_precedence(db: Session, doc_id: Optional[str] = None) -> List["CorpusChunkModel"]:
        """
        Aplica la Regla de Precedencia Determinista de LexForja:
        Si un chunk de enmienda modifica a otro anterior, adquiere prioridad forzada (+1.0)
        y los chunks derogados o modificados se marcan con menor prioridad.
        """
        from src.storage.models import CorpusChunkModel
        query = db.query(CorpusChunkModel)
        if doc_id:
            query = query.filter(CorpusChunkModel.doc_id == doc_id)
        
        chunks = query.all()
        # Identificar IDs que fueron modificados/sustituidos
        modified_ids = {c.modifica_a_chunk_id for c in chunks if c.modifica_a_chunk_id}
        
        # Ordenar: primero los no derogados y con mayor version_prioridad
        def sort_key(c):
            is_superseded = c.chunk_id in modified_ids
            # Si fue modificado por una enmienda más reciente, penalizar prioridad
            effective_priority = 0.1 if is_superseded else c.version_prioridad
            return effective_priority

        return sorted(chunks, key=sort_key, reverse=True)


class GlosarioRepository:
    @staticmethod
    def get_all(db: Session) -> List["GlosarioCiberseguridadModel"]:
        from src.storage.models import GlosarioCiberseguridadModel
        return db.query(GlosarioCiberseguridadModel).all()

    @staticmethod
    def get_by_term_en(db: Session, term_en: str) -> Optional["GlosarioCiberseguridadModel"]:
        from src.storage.models import GlosarioCiberseguridadModel
        return db.query(GlosarioCiberseguridadModel).filter(
            GlosarioCiberseguridadModel.termino_en == term_en
        ).first()

    @staticmethod
    def search(db: Session, term: str) -> List["GlosarioCiberseguridadModel"]:
        from src.storage.models import GlosarioCiberseguridadModel
        pattern = f"%{term}%"
        return db.query(GlosarioCiberseguridadModel).filter(
            (GlosarioCiberseguridadModel.termino_en.ilike(pattern)) |
            (GlosarioCiberseguridadModel.termino_es.ilike(pattern))
        ).all()
