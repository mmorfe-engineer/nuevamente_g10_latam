"""
Pruebas Unitarias para los Contratos de Dominio (Capa 1)
Valida las 6 entidades core de NuevaMente:
1. Users
2. TechnicalDocuments
3. RAGKnowledgeBases
4. LearningSessions
5. Flashcards
6. Quizzes y QuizQuestions
"""
import uuid
from datetime import datetime
import pytest
from pydantic import ValidationError

from src.utils.schemas import (
    PerfilDestinatario,
    FormatoSalida,
    NichoSector,
    NivelDetalle,
    RoleUsuario,
    TaxonomiaBloom,
    EstadoIndexacion,
    UserCreate,
    UserResponse,
    TechnicalDocumentCreate,
    TechnicalDocumentResponse,
    RAGKnowledgeBaseCreate,
    RAGKnowledgeBaseResponse,
    LearningSessionCreate,
    LearningSessionResponse,
    FlashcardCreate,
    FlashcardResponse,
    FlashcardUpdateMastery,
    QuizCreate,
    QuizResponse,
    QuizQuestionCreate,
    QuizQuestionResponse,
    QuizSubmission,
    QuizResult
)


def test_user_schema_validation():
    """Valida la creación y serialización de un usuario."""
    user_data = {
        "email": "estudiante@nuevamente.ai",
        "full_name": "Esteban Morales",
        "role": RoleUsuario.ESTUDIANTE,
        "target_profile_default": PerfilDestinatario.PRINCIPIANTE
    }
    user = UserCreate(**user_data)
    assert user.email == "estudiante@nuevamente.ai"
    assert user.role == RoleUsuario.ESTUDIANTE

    user_resp = UserResponse(
        id=uuid.uuid4(),
        created_at=datetime.utcnow(),
        **user.model_dump()
    )
    assert isinstance(user_resp.id, uuid.UUID)
    assert user_resp.target_profile_default == PerfilDestinatario.PRINCIPIANTE


def test_technical_document_schema_validation():
    """Valida el contrato de documentos técnicos ingresados."""
    doc_create = TechnicalDocumentCreate(
        title="Arquitectura de Redes VCN en OCI",
        source_type="markdown",
        raw_content="Contenido técnico sobre Virtual Cloud Networks, subredes y tablas de ruteo.",
        content_hash="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        char_count=78,
        oci_bucket="nuevamente-documentos-origen",
        oci_object_id="01_oci_vcn_redes.md"
    )
    assert doc_create.title == "Arquitectura de Redes VCN en OCI"
    assert doc_create.oci_bucket == "nuevamente-documentos-origen"

    doc_resp = TechnicalDocumentResponse(
        id=uuid.uuid4(),
        created_at=datetime.utcnow(),
        **doc_create.model_dump()
    )
    assert doc_resp.char_count == 78


def test_rag_knowledge_base_schema_validation():
    """Valida la especificación de indexación RAG con ChromaDB."""
    doc_id = uuid.uuid4()
    rag_kb = RAGKnowledgeBaseCreate(
        document_id=doc_id,
        collection_name=f"col_vcn_{doc_id.hex[:8]}",
        chunk_count=12,
        chunk_strategy="recursive_character",
        chunk_size=1000,
        chunk_overlap=150,
        embedding_model="all-MiniLM-L6-v2",
        status=EstadoIndexacion.INDEXED
    )
    assert rag_kb.chunk_count == 12
    assert rag_kb.status == EstadoIndexacion.INDEXED

    rag_resp = RAGKnowledgeBaseResponse(
        id=uuid.uuid4(),
        created_at=datetime.utcnow(),
        **rag_kb.model_dump()
    )
    assert rag_resp.document_id == doc_id


def test_learning_session_schema_validation():
    """Valida la sesión de aprendizaje y sus metadatos pedagógicos."""
    doc_id = uuid.uuid4()
    user_id = uuid.uuid4()

    session_create = LearningSessionCreate(
        user_id=user_id,
        document_id=doc_id,
        perfil_destinatario=PerfilDestinatario.PRINCIPIANTE,
        formato_salida=FormatoSalida.FLASHCARDS,
        nicho_sector=NichoSector.GENERAL,
        nivel_detalle=NivelDetalle.DIDACTICO,
        titulo_adaptado="Dominando Redes VCN desde Cero",
        introduccion_contextualizada="Imagina una VCN como tu propio barrio privado en la nube de Oracle.",
        tiempo_estimado_minutos=5,
        conceptos_clave=["VCN", "Subredes", "Internet Gateway"],
        anclaje_fuente_score=0.98,
        claridad_pedagogica="Alta",
        observaciones_calidad="Analogías claras sin tecnicismos innecesarios.",
        oci_bucket="nuevamente-contenidos-educativos",
        oci_object_id="contenido-vcn-principiante-flashcards.json"
    )
    assert session_create.anclaje_fuente_score == 0.98
    assert session_create.perfil_destinatario == PerfilDestinatario.PRINCIPIANTE

    session_resp = LearningSessionResponse(
        id=uuid.uuid4(),
        created_at=datetime.utcnow(),
        **session_create.model_dump()
    )
    assert session_resp.tiempo_estimado_minutos == 5


def test_flashcard_schema_and_mastery():
    """Valida la creación y actualización de dominio (SM-2) de flashcards."""
    sess_id = uuid.uuid4()
    card_create = FlashcardCreate(
        session_id=sess_id,
        front="¿Qué es una VCN?",
        back="Es una red privada virtual personalizable en Oracle Cloud.",
        didactic_hint="El terreno cercado donde residen tus servidores.",
        mastery_level=0
    )
    assert card_create.mastery_level == 0

    # Actualización de asimilación SM-2
    mastery_update = FlashcardUpdateMastery(
        mastery_level=4,
        next_review_at=datetime.utcnow()
    )
    assert mastery_update.mastery_level == 4

    # Validación de límites de dominio (0-5)
    with pytest.raises(ValidationError):
        FlashcardUpdateMastery(mastery_level=6)


def test_quiz_and_question_schemas():
    """Valida el quiz con preguntas, opciones y niveles de Taxonomía de Bloom."""
    sess_id = uuid.uuid4()
    q1 = QuizQuestionCreate(
        question_text="¿Cuál es la función principal de una Security List en OCI?",
        options=[
            "A) Balancear tráfico web",
            "B) Filtrar tráfico mediante reglas de entrada y salida",
            "C) Aumentar la velocidad de almacenamiento",
            "D) Crear copias de seguridad de bases de datos"
        ],
        correct_answer="B) Filtrar tráfico mediante reglas de entrada y salida",
        explanation="Las Security Lists actúan como firewalls virtuales a nivel de subred.",
        didactic_hint="Reglas de ingress y egress.",
        bloom_taxonomy_level=TaxonomiaBloom.COMPRENDER
    )

    quiz_create = QuizCreate(
        session_id=sess_id,
        title="Evaluación de Redes VCN",
        total_questions=1,
        questions=[q1]
    )
    assert len(quiz_create.questions) == 1
    assert quiz_create.questions[0].bloom_taxonomy_level == TaxonomiaBloom.COMPRENDER

    # Prueba de envío y resultado de quiz
    q_id = uuid.uuid4()
    submission = QuizSubmission(
        question_id=q_id,
        selected_option="B) Filtrar tráfico mediante reglas de entrada y salida"
    )
    result = QuizResult(
        question_id=submission.question_id,
        is_correct=True,
        correct_answer=q1.correct_answer,
        explanation=q1.explanation,
        bloom_taxonomy_level=q1.bloom_taxonomy_level
    )
    assert result.is_correct is True
