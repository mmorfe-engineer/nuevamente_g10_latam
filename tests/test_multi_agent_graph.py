"""
Pruebas Unitarias para el Sistema Multi-Agente con LangGraph (Diferencial Hackathon ONE G10).
"""
import pytest
from src.utils.schemas import (
    SolicitudAdaptacion,
    PerfilDestinatario,
    FormatoSalida,
    NichoSector,
    NivelDetalle
)
from src.agents.multi_agent_graph import run_langgraph_pipeline, multi_agent_graph


def test_multi_agent_graph_execution():
    """Valida la ejecución del grafo con los 3 agentes (Investigador, Redactor, Crítico)."""
    req = SolicitudAdaptacion(
        documento_titulo="Redes Virtuales VCN",
        documento_contenido=(
            "La Virtual Cloud Network (VCN) de Oracle Cloud Infrastructure es una red privada configurable. "
            "Permite crear subredes públicas y privadas, tablas de enrutamiento y Security Lists."
        ),
        perfil_destinatario=PerfilDestinatario.PRINCIPIANTE,
        formato_salida=FormatoSalida.FLASHCARDS,
        nicho_sector=NichoSector.GENERAL,
        nivel_detalle=NivelDetalle.DIDACTICO
    )

    respuesta, logs = run_langgraph_pipeline(req)

    # Validar que los 3 agentes emitieron logs
    assert any("Investigador RAG" in log for log in logs)
    assert any("Redactor Pedagógico" in log for log in logs)
    assert any("Crítico/Revisor" in log for log in logs)

    # Validar respuesta estructurada
    assert respuesta.status == "exito"
    assert respuesta.metadatos.perfil_aplicado == "Principiante"
    assert len(respuesta.contenido_adaptado.items) > 0
    assert respuesta.evaluacion_calidad.anclaje_fuente_score >= 0.85
    assert "LangGraph" in respuesta.evaluacion_calidad.observaciones
