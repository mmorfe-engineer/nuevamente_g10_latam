"""
Prueba de humo automatizada para la interfaz de usuario (ui/app.py).
Utiliza streamlit.testing.v1.AppTest para garantizar que:
1. La aplicación arranca sin excepciones ni tracebacks.
2. Los cuatro parámetros de control (Perfil, Formato, Nicho Sectorial, Nivel de Detalle) se renderizan siempre.
3. Ningún modo de ingesta desencadena StreamlitValueOutOfRangeError ni desborde de índices.
4. La vista principal no contiene bloques estáticos acoplados a ningún sector específico (como NIST NICE fijo).
"""
from pathlib import Path
import pytest
from streamlit.testing.v1 import AppTest

APP_PATH = str(Path(__file__).resolve().parent.parent / "ui" / "app.py")


def test_ui_smoke_startup_and_four_parameters():
    """Verifica que ui/app.py arranca de forma limpia y renderiza los cuatro parámetros de control."""
    at = AppTest.from_file(APP_PATH, default_timeout=30)
    at.run()

    # 1. Cero excepciones en el arranque inicial
    assert not at.exception, f"Excepción al arrancar ui/app.py: {[e.message for e in at.exception]}"

    # 2. Los cuatro parámetros de control deben existir en la barra lateral
    sidebar_selectboxes = at.sidebar.selectbox
    assert len(sidebar_selectboxes) >= 5, "Faltan selectboxes en la barra lateral"

    labels = [sb.label for sb in sidebar_selectboxes]
    assert any("Modo de Ingesta" in l for l in labels), "Falta selector de Modo de Ingesta"
    assert any("Perfil del Destinatario" in l for l in labels), "Falta parámetro 1: Perfil del Destinatario"
    assert any("Formato Pedagógico" in l for l in labels), "Falta parámetro 2: Formato Pedagógico"
    assert any("Nicho / Sector" in l for l in labels), "Falta parámetro 3: Nicho / Sector"
    assert any("Nivel de Detalle" in l for l in labels), "Falta parámetro 4: Nivel de Detalle"


def test_ui_smoke_all_ingestion_modes_do_not_throw_out_of_range():
    """Verifica que cambiar el modo de ingesta no provoca StreamlitValueOutOfRangeError."""
    at = AppTest.from_file(APP_PATH, default_timeout=30)
    at.run()
    assert not at.exception, "Fallo en arranque inicial"

    modo_selector = at.sidebar.selectbox[0]
    opciones_ingesta = modo_selector.options

    for modo in opciones_ingesta:
        modo_selector.select(modo)
        at.run()
        assert not at.exception, f"Fallo al seleccionar '{modo}': {[e.message for e in at.exception]}"

        # Verificar que los cuatro parámetros siguen renderizados
        labels = [sb.label for sb in at.sidebar.selectbox]
        assert any("Perfil" in l for l in labels), f"Falta Perfil en modo {modo}"
        assert any("Formato" in l for l in labels), f"Falta Formato en modo {modo}"
        assert any("Nicho" in l for l in labels), f"Falta Nicho en modo {modo}"
        assert any("Detalle" in l for l in labels), f"Falta Detalle en modo {modo}"


def test_ui_no_static_sector_blocks_on_main_screen():
    """Garantiza el Principio de Agnosticismo: la vista principal no tiene bloques fijos de ningún sector."""
    at = AppTest.from_file(APP_PATH, default_timeout=30)
    at.run()
    assert not at.exception

    # Inspeccionar todos los textos renderizados en markdown y títulos
    all_markdown_texts = [m.value for m in at.markdown]
    joined_text = " ".join(all_markdown_texts).lower()

    # No debe existir el bloque estático de Rutas NIST NICE en la vista principal
    assert "rutas de especialización y certificación nist nice" not in joined_text, (
        "Se detectó bloque estático NIST NICE incrustado en la pantalla principal"
    )
    assert "ruta a · operativo" not in joined_text, "Se detectó tarjeta fija de Ruta A Operativo"
    assert "ruta d · gobernanza" not in joined_text, "Se detectó tarjeta fija de Ruta D Gobernanza"


def test_ui_smoke_welcome_station_and_canonical_demo_button():
    """Verifica que la estación de ingesta O-01 y el botón de muestra canónica O-12 están presentes y funcionan."""
    at = AppTest.from_file(APP_PATH, default_timeout=30)
    at.run()
    assert not at.exception

    # 1. Comprobar que los KPIs de motor (Puntaje de Anclaje) están visibles
    all_markdown = " ".join([m.value for m in at.markdown])
    assert "Puntaje de Anclaje (O-08)" in all_markdown
    assert "Tiempo de Adaptación" in all_markdown
    assert "Formatos Interactivos (O-06)" in all_markdown
    assert "Corpus SQL" not in all_markdown, "El KPI de biblioteca 'Corpus SQL' aún sigue presente"

    # 2. Comprobar la presencia de la Estación de Ingesta O-01
    assert "Estación de Ingesta y Transformación Documental (Pliego O-01)" in all_markdown

    # 3. Comprobar el botón de carga del caso canónico de Oracle VCN (O-12)
    btn_canonico = [b for b in at.button if "Caso Canónico Oracle" in b.label]
    assert len(btn_canonico) == 1, "No se encontró el botón del caso canónico de Oracle VCN"
    btn_canonico[0].click().run()
    assert not at.exception

