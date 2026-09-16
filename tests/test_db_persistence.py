"""
Pruebas Unitarias de Persistencia Relacional y Almacenamiento (Capa 2).
Valida:
- Inicialización y reseteo del esquema relacional (SQLAlchemy 2.0).
- Operaciones CRUD y relaciones en las 6 entidades core.
- Integración con OCI Object Storage Always Free.
"""
import uuid
from datetime import datetime
import pytest

from src.storage.database import reset_db, get_db_session
from src.storage.repository import (
    UserRepository,
    TechnicalDocumentRepository,
    RAGKnowledgeBaseRepository,
    LearningSessionRepository,
    FlashcardRepository,
    QuizRepository
)
from src.storage.oci_client import oci_storage
from src.utils.schemas import (
    UserCreate,
    RoleUsuario,
    PerfilDestinatario,
    FormatoSalida,
    NichoSector,
    NivelDetalle,
    TechnicalDocumentCreate,
    RAGKnowledgeBaseCreate,
    EstadoIndexacion,
    LearningSessionCreate,
    FlashcardCreate,
    FlashcardUpdateMastery,
    QuizCreate,
    QuizQuestionCreate,
    TaxonomiaBloom
)


@pytest.fixture(scope="module", autouse=True)
def setup_database():
    """Inicializa un esquema relacional limpio para la suite de pruebas."""
    reset_db()
    yield
    # Cleanup opcional si es necesario


def test_user_repository_crud():
    """Valida la creación y búsqueda de usuarios."""
    with get_db_session() as db:
        user_in = UserCreate(
            email=f"arquitecto_{uuid.uuid4().hex[:6]}@nuevamente.ai",
            full_name="Líder de Arquitectura",
            role=RoleUsuario.DOCENTE,
            target_profile_default=PerfilDestinatario.ARQUITECTO
        )
        user = UserRepository.create(db, user_in)
        assert user.id is not None
        assert user.email == user_in.email

        fetched = UserRepository.get_by_id(db, user.id)
        assert fetched is not None
        assert fetched.full_name == "Líder de Arquitectura"
        assert fetched.role == "docente"

        # Validar usuario demo por defecto
        default_user = UserRepository.get_or_create_default_user(db)
        assert default_user is not None
        assert default_user.email == "demo.estudiante@nuevamente.ai"


def test_technical_document_and_deduplication():
    """Valida la persistencia de documentos técnicos y búsqueda por hash SHA-256."""
    with get_db_session() as db:
        doc_hash = f"hash_{uuid.uuid4().hex}"
        doc_in = TechnicalDocumentCreate(
            title="Manual de Arquitectura Cloud OCI",
            source_type="pdf",
            raw_content="Oracle Cloud Infrastructure ofrece alta disponibilidad y aislamiento multinivel.",
            content_hash=doc_hash,
            char_count=87,
            oci_bucket="nuevamente-documentos-origen",
            oci_object_id="docs/oci-manual.pdf"
        )
        doc = TechnicalDocumentRepository.create(db, doc_in)
        assert doc.id is not None
        assert doc.content_hash == doc_hash

        # Recuperación por hash
        doc_by_hash = TechnicalDocumentRepository.get_by_hash(db, doc_hash)
        assert doc_by_hash is not None
        assert doc_by_hash.id == doc.id
        assert doc_by_hash.title == "Manual de Arquitectura Cloud OCI"


def test_rag_knowledge_base_persistence():
    """Valida la indexación y control de estado de la base vectorial RAG."""
    with get_db_session() as db:
        doc_in = TechnicalDocumentCreate(
            title="Documento Base RAG",
            source_type="md",
            raw_content="Contenido de prueba para indexación RAG con embeddings.",
            content_hash=uuid.uuid4().hex
        )
        doc = TechnicalDocumentRepository.create(db, doc_in)

        col_name = f"col_{uuid.uuid4().hex[:8]}"
        kb_in = RAGKnowledgeBaseCreate(
            document_id=doc.id,
            collection_name=col_name,
            chunk_count=8,
            chunk_strategy="recursive_character",
            chunk_size=1000,
            chunk_overlap=150,
            embedding_model="all-MiniLM-L6-v2",
            status=EstadoIndexacion.PENDING
        )
        kb = RAGKnowledgeBaseRepository.create(db, kb_in)
        assert kb.status == "pending"

        # Actualizar estado a indexado
        updated_kb = RAGKnowledgeBaseRepository.update_status(db, kb.id, "indexed")
        assert updated_kb.status == "indexed"


def test_learning_session_and_flashcards():
    """Valida la sesión de aprendizaje y creación/actualización de flashcards (SM-2)."""
    with get_db_session() as db:
        user = UserRepository.get_or_create_default_user(db)
        doc_in = TechnicalDocumentCreate(
            title="Seguridad e IAM en OCI",
            source_type="md",
            raw_content="Políticas de acceso basadas en grupos, compartimentos y principios de menor privilegio.",
            content_hash=uuid.uuid4().hex
        )
        doc = TechnicalDocumentRepository.create(db, doc_in)

        session_in = LearningSessionCreate(
            user_id=user.id,
            document_id=doc.id,
            perfil_destinatario=PerfilDestinatario.PRINCIPIANTE,
            formato_salida=FormatoSalida.FLASHCARDS,
            nicho_sector=NichoSector.GENERAL,
            nivel_detalle=NivelDetalle.DIDACTICO,
            titulo_adaptado="Seguridad Cloud Explicada para Principiantes",
            introduccion_contextualizada="Las políticas IAM son las llaves maestras de tu edificio en la nube.",
            tiempo_estimado_minutos=6,
            conceptos_clave=["IAM", "Compartimentos", "Políticas"],
            anclaje_fuente_score=0.97,
            claridad_pedagogica="Alta",
            observaciones_calidad="Analogías claras.",
            oci_bucket="nuevamente-contenidos-educativos",
            oci_object_id="contenido-seguridad-001.json"
        )
        session = LearningSessionRepository.create(db, session_in)
        assert session.id is not None
        assert session.perfil_destinatario == "Principiante"

        # Crear flashcards
        cards_in = [
            FlashcardCreate(
                session_id=session.id,
                user_id=user.id,
                front="¿Qué es una política IAM en OCI?",
                back="Es un documento declarativo que define quién tiene qué acceso a cuáles recursos.",
                didactic_hint="Sintaxis: Allow <group> to <verb> <resource-type> in <compartment>",
                mastery_level=0
            ),
            FlashcardCreate(
                session_id=session.id,
                user_id=user.id,
                front="¿Para qué sirve un Compartimento?",
                back="Para organizar y aislar lógicamente los recursos dentro de un tenancy.",
                didactic_hint="Piensa en carpetas o departamentos de una empresa.",
                mastery_level=0
            )
        ]
        created_cards = FlashcardRepository.create_batch(db, cards_in)
        assert len(created_cards) == 2

        # Actualización de asimilación SM-2
        card_to_update = created_cards[0]
        updated_card = FlashcardRepository.update_mastery(
            db,
            card_to_update.id,
            FlashcardUpdateMastery(mastery_level=5, next_review_at=datetime.utcnow())
        )
        assert updated_card.mastery_level == 5


def test_quiz_and_questions_persistence():
    """Valida la creación de un Quiz con preguntas relacionales y taxonomía de Bloom."""
    with get_db_session() as db:
        user = UserRepository.get_or_create_default_user(db)
        doc_in = TechnicalDocumentCreate(
            title="Bases de Datos Autónomas",
            source_type="txt",
            raw_content="Oracle Autonomous Database se autogestiona, autoasegura y autorepara.",
            content_hash=uuid.uuid4().hex
        )
        doc = TechnicalDocumentRepository.create(db, doc_in)

        session_in = LearningSessionCreate(
            user_id=user.id,
            document_id=doc.id,
            perfil_destinatario=PerfilDestinatario.JUNIOR_MID,
            formato_salida=FormatoSalida.QUIZ,
            titulo_adaptado="Evaluación Técnica: Autonomous Database",
            introduccion_contextualizada="Ponte a prueba sobre las capacidades de automatización en la nube.",
            conceptos_clave=["Autonomous DB", "Machine Learning", "Alta Disponibilidad"]
        )
        session = LearningSessionRepository.create(db, session_in)

        q1 = QuizQuestionCreate(
            question_text="¿Cuáles son los 3 pilares de Oracle Autonomous Database?",
            options=[
                "A) Autogestión, Autoaseguramiento y Autoreparación",
                "B) Solo MySQL, solo Redis y solo Kafka",
                "C) Redimensionamiento manual con parada",
                "D) Migración obligatoria a servidores locales"
            ],
            correct_answer="A) Autogestión, Autoaseguramiento y Autoreparación",
            explanation="La base autónoma utiliza machine learning para parches y tuning sin intervención humana.",
            bloom_taxonomy_level=TaxonomiaBloom.RECORDAR
        )

        quiz_in = QuizCreate(
            session_id=session.id,
            user_id=user.id,
            title="Quiz Autónomo 1",
            total_questions=1,
            questions=[q1]
        )
        quiz = QuizRepository.create_quiz_with_questions(db, quiz_in)
        assert quiz.id is not None
        assert len(quiz.questions) == 1
        assert quiz.questions[0].bloom_taxonomy_level == "Recordar"


def test_oci_storage_interaction_with_db():
    """Valida la interacción entre el cliente OCI Object Storage Always Free y las entidades."""
    # Subida de documento original
    raw_bytes = b"# Documento Tecnico OCI Always Free\nContenido verificado."
    res_upload = oci_storage.upload_raw_document("doc_test_oci.md", raw_bytes, "text/markdown")
    assert res_upload["status"] in ["completado", "emulado_local"]
    assert res_upload["bucket"] == "nuevamente-documentos-origen"

    # Subida de JSON educativo
    json_payload = {
        "titulo": "Prueba de Contenido",
        "items": [{"frente": "Q", "dorso": "A"}]
    }
    res_json = oci_storage.upload_educational_json("test-output.json", json_payload)
    assert res_json.bucket == "nuevamente-contenidos-educativos"
    assert "completado" in res_json.status_upload
