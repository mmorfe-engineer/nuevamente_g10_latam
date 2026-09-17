"""
Servicio Integral de Adaptación Pedagógica y Orquestación End-to-End (Capa 4).
Coordina:
1. Ingestión y deduplicación con hash SHA-256 en Base de Datos.
2. Almacenamiento del documento fuente en OCI Object Storage Always Free.
3. Segmentación contextual (chunking) e indexación vectorial en ChromaDB.
4. Orquestación RAG y generación con LLMs (Google Gemini 1.5 Flash).
5. Persistencia relacional completa (LearningSession, Flashcards, Quizzes).
"""
import hashlib
import logging
import uuid
from typing import Optional, Dict, Any, Tuple
from sqlalchemy.orm import Session

from config.settings import settings
from src.utils.schemas import (
    SolicitudAdaptacion,
    RespuestaAdaptacion,
    TechnicalDocumentCreate,
    RAGKnowledgeBaseCreate,
    EstadoIndexacion,
    LearningSessionCreate,
    FlashcardCreate,
    QuizCreate,
    QuizQuestionCreate,
    FormatoSalida,
    TaxonomiaBloom
)
from src.storage.database import get_db_session
from src.storage.repository import (
    UserRepository,
    TechnicalDocumentRepository,
    RAGKnowledgeBaseRepository,
    LearningSessionRepository,
    FlashcardRepository,
    QuizRepository
)
from src.storage.oci_client import oci_storage
from src.ingestion.chunker import doc_chunker
from src.rag.vector_store import vector_store
from src.llm.engine import llm_engine

logger = logging.getLogger(__name__)


class AdaptationService:
    def __init__(self):
        self.chunker = doc_chunker
        self.vector_store = vector_store
        self.engine = llm_engine
        self.storage = oci_storage

    def process_adaptation(
        self,
        request: SolicitudAdaptacion,
        user_id: Optional[uuid.UUID] = None,
        db: Optional[Session] = None,
        use_multi_agent: bool = False
    ) -> Tuple[RespuestaAdaptacion, Dict[str, Any]]:
        """
        Ejecuta el ciclo de vida completo de adaptación pedagógica.
        Retorna la respuesta oficial ONE G10 y un diccionario de trazabilidad con los IDs persistidos.
        """
        if db is not None:
            return self._execute_flow(request, user_id, db, use_multi_agent)
        else:
            with get_db_session() as session:
                return self._execute_flow(request, user_id, session, use_multi_agent)

    def _execute_flow(
        self,
        request: SolicitudAdaptacion,
        user_id: Optional[uuid.UUID],
        db: Session,
        use_multi_agent: bool = False
    ) -> Tuple[RespuestaAdaptacion, Dict[str, Any]]:
        # 1. Obtener o crear usuario de la sesión
        if user_id:
            user = UserRepository.get_by_id(db, user_id)
        else:
            user = UserRepository.get_or_create_default_user(db)
        resolved_user_id = user.id if user else None

        # 2. Deduplicación y persistencia del Documento Técnico
        content_bytes = request.documento_contenido.encode("utf-8")
        content_hash = hashlib.sha256(content_bytes).hexdigest()

        doc = TechnicalDocumentRepository.get_by_hash(db, content_hash)
        if not doc:
            # Subir a OCI bucket de documentos origen
            slug_title = "".join(c if c.isalnum() else "_" for c in request.documento_titulo.lower())[:30]
            oci_filename = f"docs/{slug_title}_{content_hash[:8]}.txt"
            self.storage.upload_raw_document(oci_filename, content_bytes, "text/plain")

            doc_create = TechnicalDocumentCreate(
                user_id=resolved_user_id,
                title=request.documento_titulo,
                source_type="text/markdown",
                raw_content=request.documento_contenido,
                content_hash=content_hash,
                char_count=len(request.documento_contenido),
                oci_bucket=settings.OCI_BUCKET_DOCS,
                oci_object_id=oci_filename
            )
            doc = TechnicalDocumentRepository.create(db, doc_create)

        # 3. Chunking e Indexación Vectorial RAG en ChromaDB
        chunks = self.chunker.split_text(request.documento_contenido, source_id=str(doc.id))
        self.vector_store.clear()
        self.vector_store.add_chunks(chunks)

        # Registrar o actualizar estado de la base de conocimiento en la DB
        kb = RAGKnowledgeBaseRepository.get_by_document_id(db, doc.id)
        if not kb:
            kb_create = RAGKnowledgeBaseCreate(
                document_id=doc.id,
                collection_name=f"col_{doc.id.hex[:12]}",
                chunk_count=len(chunks),
                chunk_strategy="recursive_character",
                chunk_size=self.chunker.chunk_size,
                chunk_overlap=self.chunker.chunk_overlap,
                embedding_model=settings.EMBEDDING_MODEL,
                status=EstadoIndexacion.INDEXED
            )
            kb = RAGKnowledgeBaseRepository.create(db, kb_create)
        else:
            RAGKnowledgeBaseRepository.update_status(db, kb.id, EstadoIndexacion.INDEXED.value)

        # 4. Generación Pedagógica con LLM (Modo Estándar o LangGraph Multi-Agente)
        agent_logs = []
        if use_multi_agent:
            from src.agents.multi_agent_graph import run_langgraph_pipeline
            respuesta, agent_logs = run_langgraph_pipeline(request)
        else:
            respuesta = self.engine.adapt_content(request)

        # 5. Persistencia de la Sesión de Aprendizaje en la DB
        session_create = LearningSessionCreate(
            user_id=resolved_user_id,
            document_id=doc.id,
            perfil_destinatario=request.perfil_destinatario,
            formato_salida=request.formato_salida,
            nicho_sector=request.nicho_sector,
            nivel_detalle=request.nivel_detalle,
            titulo_adaptado=respuesta.contenido_adaptado.titulo,
            introduccion_contextualizada=respuesta.contenido_adaptado.introduccion_contextualizada,
            tiempo_estimado_minutos=respuesta.metadatos.tiempo_estimado_estudio_minutos,
            conceptos_clave=respuesta.metadatos.conceptos_clave,
            anclaje_fuente_score=respuesta.evaluacion_calidad.anclaje_fuente_score,
            claridad_pedagogica=respuesta.evaluacion_calidad.claridad_pedagogica,
            observaciones_calidad=respuesta.evaluacion_calidad.observaciones,
            oci_bucket=respuesta.almacenamiento_oci.bucket,
            oci_object_id=respuesta.almacenamiento_oci.objeto_id
        )
        db_session = LearningSessionRepository.create(db, session_create)

        # 6. Persistencia granular de elementos pedagógicos según el formato
        items = respuesta.contenido_adaptado.items
        created_flashcards_count = 0
        created_quiz_id = None

        if request.formato_salida == FormatoSalida.FLASHCARDS:
            cards_to_create = []
            for item in items:
                cards_to_create.append(
                    FlashcardCreate(
                        session_id=db_session.id,
                        user_id=resolved_user_id,
                        front=item.get("frente", "Concepto"),
                        back=item.get("dorso", "Explicación"),
                        didactic_hint=item.get("pista_didactica"),
                        mastery_level=0
                    )
                )
            if cards_to_create:
                saved_cards = FlashcardRepository.create_batch(db, cards_to_create)
                created_flashcards_count = len(saved_cards)

        elif request.formato_salida == FormatoSalida.QUIZ:
            questions_to_create = []
            for item in items:
                questions_to_create.append(
                    QuizQuestionCreate(
                        question_text=item.get("pregunta", "¿Pregunta?"),
                        options=item.get("opciones", ["A", "B", "C", "D"]),
                        correct_answer=item.get("respuesta_correcta", "A"),
                        explanation=item.get("justificacion_didactica", "Fundamentación técnica."),
                        didactic_hint=item.get("pista_didactica"),
                        bloom_taxonomy_level=TaxonomiaBloom.COMPRENDER
                    )
                )
            quiz_create = QuizCreate(
                session_id=db_session.id,
                user_id=resolved_user_id,
                title=respuesta.contenido_adaptado.titulo,
                total_questions=len(questions_to_create),
                questions=questions_to_create
            )
            saved_quiz = QuizRepository.create_quiz_with_questions(db, quiz_create)
            created_quiz_id = str(saved_quiz.id)

        traceability = {
            "user_id": str(resolved_user_id) if resolved_user_id else None,
            "document_id": str(doc.id),
            "session_id": str(db_session.id),
            "kb_id": str(kb.id) if kb else None,
            "flashcards_count": created_flashcards_count,
            "quiz_id": created_quiz_id,
            "oci_raw_object": doc.oci_object_id,
            "oci_output_object": respuesta.almacenamiento_oci.objeto_id,
            "use_multi_agent": use_multi_agent,
            "agent_logs": agent_logs
        }

        return respuesta, traceability


adaptation_service = AdaptationService()
