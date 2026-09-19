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


def test_adaptation_service_large_document_representative_batching_and_progress():
    """Valida la indexación representativa (lote de 80 fragmentos) y reporte dinámico de progreso en documentos extensos."""
    # Documento sintético extenso de ~100,000 caracteres (~120 fragmentos)
    parrafo = (
        "En Oracle Cloud Infrastructure, una Virtual Cloud Network (VCN) define un entorno de red aislado en la nube. "
        "Permite configurar subredes públicas y privadas, enrutamiento CIDR, gateways de internet y tablas de seguridad. "
    )
    doc_extenso = (parrafo * 450)  # ~102,000 caracteres

    req = SolicitudAdaptacion(
        documento_titulo="Manual Extenso de Redes Cloud",
        documento_contenido=doc_extenso,
        perfil_destinatario=PerfilDestinatario.PRINCIPIANTE,
        formato_salida=FormatoSalida.FLASHCARDS,
        nicho_sector=NichoSector.CLOUD_INFRAESTRUCTURA,
        nivel_detalle=NivelDetalle.DIDACTICO
    )

    progreso_capturado = []

    def callback_spy(phase: int, name: str, current: int, total: int, detail: str):
        progreso_capturado.append((phase, name, current, total, detail))

    with get_db_session() as db:
        resp, trace = adaptation_service.process_adaptation(
            req,
            db=db,
            progress_callback=callback_spy,
            max_chunks=80,
            chunk_offset=0
        )

        # 1. Validar que la respuesta sea válida
        assert resp.status == "exito"
        assert len(resp.contenido_adaptado.items) > 0

        # 2. Validar que la partición representativa limitó la indexación a 80 chunks
        assert trace["chunks_indexados"] == 80
        assert trace["total_chunks_doc"] > 80
        assert trace["cobertura_pct"] < 100.0
        assert "Lote representativo #1" in trace["porcion_procesada"]
        assert f"{trace['total_chars_doc']:,}" in trace["porcion_procesada"]

        # 3. Validar que el callback fue invocado para las 4 fases y reportó progreso
        fases_vistas = {p[0] for p in progreso_capturado}
        assert {1, 2, 3, 4}.issubset(fases_vistas)

        # Validar que en la fase 2 se reportó progreso de fragmentos
        progreso_fase2 = [p for p in progreso_capturado if p[0] == 2]
        assert len(progreso_fase2) >= 5
        assert progreso_fase2[-1][2] == 80  # Finalizó en 80 de 80

        # 4. Validar avance al siguiente lote (offset=80)
        resp2, trace2 = adaptation_service.process_adaptation(
            req,
            db=db,
            max_chunks=80,
            chunk_offset=80
        )
        assert trace2["chunks_indexados"] == trace2["total_chunks_doc"] - 80
        assert trace2["chunk_offset"] == 80
        assert "Lote representativo #2" in trace2["porcion_procesada"]

