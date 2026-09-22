"""
Pruebas de regresión automatizadas para el ciclo de vida de sesiones y estado (DEF-02, DEF-06).
Garantiza:
1. reset_adaptation_session() purga exhaustivamente claves dinámicas de tarjetas y resultados.
2. Aislamiento estricto: Documento A no contamina a Documento B.
3. El banner de métricas rotula honestamente el lote acotado de ADR-012.
"""
from pathlib import Path
import pytest
from streamlit.testing.v1 import AppTest

APP_PATH = str(Path(__file__).resolve().parent.parent / "ui" / "app.py")


def test_session_state_reset_function_logic():
    """Prueba unitaria de la lógica de purga de reset_adaptation_session."""
    from ui.app import reset_adaptation_session

    # Simular claves residuales que antes generaban bleeding
    mock_state = {
        "ultima_respuesta": {"dummy": "data"},
        "ultimo_request": {"doc": "A"},
        "ultimo_trace": {"chunks_indexados": 10},
        "current_chunk_offset": 40,
        "card_flipped_0": True,
        "card_flipped_1": False,
        "card_graded_0": {"status": "Alcanzado", "quality": 5},
        "card_graded_1": {"status": "En desarrollo", "quality": 3},
        "doc_titulo": "Doc A",
        "doc_contenido": "Contenido A",
    }

    # 1. Reset conservando documento
    reset_adaptation_session(clear_document=False, state=mock_state)

    assert "ultima_respuesta" not in mock_state
    assert "ultimo_request" not in mock_state
    assert "ultimo_trace" not in mock_state
    assert mock_state["current_chunk_offset"] == 0
    assert "card_flipped_0" not in mock_state
    assert "card_flipped_1" not in mock_state
    assert "card_graded_0" not in mock_state
    assert "card_graded_1" not in mock_state
    assert mock_state["doc_titulo"] == "Doc A"
    assert mock_state["doc_contenido"] == "Contenido A"

    # 2. Reset limpiando documento
    reset_adaptation_session(clear_document=True, state=mock_state)
    assert "doc_titulo" not in mock_state
    assert "doc_contenido" not in mock_state


def test_ui_e2e_document_reset_cleans_flashcard_state():
    """Valida mediante AppTest que presionar Adaptar Nuevo Documento limpia tarjetas y vuelve al inicio."""
    at = AppTest.from_file(APP_PATH, default_timeout=45)
    at.run()
    assert not at.exception

    # 1. Cargar caso canónico
    btn_canonico = [b for b in at.button if "Caso Canónico Oracle" in b.label][0]
    btn_canonico.click().run()
    assert not at.exception

    # 2. Generar material
    btn_generar = [b for b in at.button if "Generar Material Didáctico" in b.label][0]
    btn_generar.click().run()
    assert not at.exception
    assert "ultima_respuesta" in at.session_state

    # 3. Voltear tarjeta 0 y calificar
    btn_flip = [b for b in at.button if "Voltear Tarjeta" in b.label or "Ver Frente" in b.label]
    if btn_flip:
        btn_flip[0].click().run()
    btn_alc = [b for b in at.button if "Alcanzado" in b.label]
    if btn_alc:
        btn_alc[0].click().run()

    # 4. Accionar Adaptar Nuevo Documento
    btn_reset = [b for b in at.button if "Adaptar Nuevo Documento" in b.label][0]
    btn_reset.click().run()
    assert not at.exception

    # 5. Comprobar que ultima_respuesta ya no existe y no quedan claves residuales de tarjetas
    assert "ultima_respuesta" not in at.session_state
    assert "card_flipped_0" not in at.session_state
    assert "card_graded_0" not in at.session_state
    assert at.session_state["current_chunk_offset"] == 0

    # 6. Comprobar que la estación de bienvenida se renderiza limpia
    all_markdown = " ".join([m.value for m in at.markdown])
    assert "Estación de Ingesta y Transformación Documental" in all_markdown


def test_ui_kpi_banner_labels_active_batch_adr012():
    """Valida que el banner de KPIs generados rotula con precisión 'Fragmentos del Lote Activo (ADR-012)'."""
    at = AppTest.from_file(APP_PATH, default_timeout=45)
    at.run()
    assert not at.exception

    btn_canonico = [b for b in at.button if "Caso Canónico Oracle" in b.label][0]
    btn_canonico.click().run()
    btn_generar = [b for b in at.button if "Generar Material Didáctico" in b.label][0]
    btn_generar.click().run()
    assert not at.exception

    all_markdown = " ".join([m.value for m in at.markdown])
    assert "Fragmentos del Lote Activo (ADR-012)" in all_markdown
    assert "Fragmentos del Corpus" not in all_markdown
