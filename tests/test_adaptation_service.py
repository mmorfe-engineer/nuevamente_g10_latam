"""
Pruebas de Integración y Servicio (Capa 4).
Valida la orquestación integral de AdaptationService:
- Ingestión, hash y deduplicación.
- Chunking e indexación RAG.
- Generación pedagógica.
- Persistencia en DB (Session, Flashcards, Quizzes) y OCI.
"""
import uuid
import pytest

from src.storage.database import reset_db, get_db_session
from src.utils.schemas import (
    SolicitudAdaptacion,
    PerfilDestinatario,
    FormatoSalida,
    NichoSector,
    NivelDetalle
)
from src.services.adaptation_service import adaptation_service
from src.storage.repository import (
    LearningSessionRepository,
    FlashcardRepository,
    QuizRepository,
    TechnicalDocumentRepository
)


@pytest.fixture(scope="module", autouse=True)
def setup_db():
    reset_db()


def test_adaptation_service_flashcards_flow():
    """Valida el flujo completo generando Flashcards y persistiendo en la DB."""
    req = SolicitudAdaptacion(
        documento_titulo="Arquitectura de Redes VCN en OCI",
        documento_contenido=(
            "La Virtual Cloud Network (VCN) es una red privada y personalizable configurada en Oracle Cloud Infrastructure. "
            "Incluye subredes públicas y privadas, tablas de enrutamiento, Internet Gateways, NAT Gateways y Security Lists "
            "para control de tráfico mediante reglas de entrada y salida."
        ),
        perfil_destinatario=PerfilDestinatario.PRINCIPIANTE,
        formato_salida=FormatoSalida.FLASHCARDS,
        nicho_sector=NichoSector.GENERAL,
        nivel_detalle=NivelDetalle.DIDACTICO
    )

    with get_db_session() as db:
        respuesta, trace = adaptation_service.process_adaptation(req, db=db)

        # Validar respuesta estructurada
        assert respuesta.status == "exito"
        assert respuesta.metadatos.perfil_aplicado == "Principiante"
        assert respuesta.metadatos.formato_generado == "Flashcards"
        assert len(respuesta.contenido_adaptado.items) > 0
        assert respuesta.evaluacion_calidad.anclaje_fuente_score >= 0.85

        # Validar trazabilidad y persistencia
        session_id = uuid.UUID(trace["session_id"])
        saved_session = LearningSessionRepository.get_by_id(db, session_id)
        assert saved_session is not None
        assert saved_session.perfil_destinatario == "Principiante"

        # Validar flashcards guardadas
        saved_cards = FlashcardRepository.get_by_session(db, session_id)
        assert len(saved_cards) == len(respuesta.contenido_adaptado.items)
        assert saved_cards[0].front != ""


def test_adaptation_service_quiz_flow():
    """Valida el flujo completo generando un Quiz y persistiendo en la DB."""
    req = SolicitudAdaptacion(
        documento_titulo="Seguridad y Reglas de Tráfico VCN",
        documento_contenido=(
            "Las Security Lists controlan el tráfico a nivel de subred mediante reglas stateful o stateless. "
            "Los Network Security Groups (NSG) aplican reglas a nivel de VNIC específicas para mayor granularidad."
        ),
        perfil_destinatario=PerfilDestinatario.JUNIOR_MID,
        formato_salida=FormatoSalida.QUIZ,
        nicho_sector=NichoSector.GENERAL,
        nivel_detalle=NivelDetalle.TECNICO
    )

    with get_db_session() as db:
        respuesta, trace = adaptation_service.process_adaptation(req, db=db)

        assert respuesta.status == "exito"
        session_id = uuid.UUID(trace["session_id"])
        saved_quiz = QuizRepository.get_by_session(db, session_id)
        assert saved_quiz is not None
        assert len(saved_quiz.questions) > 0
        assert saved_quiz.questions[0].correct_answer != ""


def test_document_deduplication_in_service():
    """Valida que documentos con el mismo contenido no se dupliquen en la DB."""
    contenido_identico = "Documento de idempotencia para verificar deduplicación por hash SHA-256."
    req = SolicitudAdaptacion(
        documento_titulo="Doc Idempotente",
        documento_contenido=contenido_identico,
        perfil_destinatario=PerfilDestinatario.PRINCIPIANTE,
        formato_salida=FormatoSalida.FLASHCARDS
    )

    with get_db_session() as db:
        _, trace1 = adaptation_service.process_adaptation(req, db=db)
        _, trace2 = adaptation_service.process_adaptation(req, db=db)

        assert trace1["document_id"] == trace2["document_id"]
