"""
Prueba de humo automatizada para la interfaz de usuario (ui/app.py).
Utiliza streamlit.testing.v1.AppTest para garantizar que:
1. La aplicación arranca sin excepciones ni tracebacks.
2. Los cuatro parámetros de control (Perfil, Formato, Nicho Sectorial, Nivel de Detalle) se renderizan en la estación central.
3. La barra lateral opera en modo de solo lectura (un solo punto de escritura, cero duplicación).
4. El cambio de modo de ingesta (archivo vs texto libre) no genera desbordes ni errores.
5. La vista principal no contiene bloques estáticos acoplados a sectores específicos.
6. Los KPIs iniciales muestran honestamente 'Aún sin medir' y existen exactamente 3 muestras oficiales (O-12).
"""
from pathlib import Path
import pytest
from streamlit.testing.v1 import AppTest

APP_PATH = str(Path(__file__).resolve().parent.parent / "ui" / "app.py")


def test_ui_smoke_startup_and_four_parameters():
    """Verifica que ui/app.py arranca de forma limpia y renderiza los cuatro parámetros de control en la estación central."""
    at = AppTest.from_file(APP_PATH, default_timeout=30)
    at.run()

    # 1. Cero excepciones en el arranque inicial
    assert not at.exception, f"Excepción al arrancar ui/app.py: {[e.message for e in at.exception]}"

    # 2. Los cuatro parámetros de control deben existir en la estación central
    selectboxes = at.selectbox
    assert len(selectboxes) >= 4, f"Faltan selectboxes en la estación central: {[sb.label for sb in selectboxes]}"

    labels = [sb.label for sb in selectboxes]
    assert any("Perfil del Destinatario" in l for l in labels), "Falta parámetro 1: Perfil del Destinatario"
    assert any("Formato Didáctico" in l for l in labels), "Falta parámetro 2: Formato Didáctico"
    assert any("Nicho / Sector" in l for l in labels), "Falta parámetro 3: Nicho / Sector"
    assert any("Nivel de Detalle" in l for l in labels), "Falta parámetro 4: Nivel de Detalle"

    # 3. Principio de un solo punto de escritura: La barra lateral no debe duplicar inputs
    sidebar_selectboxes = at.sidebar.selectbox
    assert len(sidebar_selectboxes) == 0, "La barra lateral no debe tener selectboxes compitiendo con la estación central"


def test_ui_smoke_all_ingestion_modes_do_not_throw_out_of_range():
    """Verifica que cambiar el modo de ingesta no provoca StreamlitValueOutOfRangeError ni errores de estado."""
    at = AppTest.from_file(APP_PATH, default_timeout=30)
    at.run()
    assert not at.exception, "Fallo en arranque inicial"

    modo_radios = [r for r in at.radio if "Método de Entrada" in r.label]
    assert len(modo_radios) >= 1, "Falta selector de Modo de Ingesta por radio"
    modo_radio = modo_radios[0]

    for modo in modo_radio.options:
        modo_radio.set_value(modo)
        at.run()
        assert not at.exception, f"Fallo al seleccionar '{modo}': {[e.message for e in at.exception]}"

        # Verificar que los cuatro parámetros siguen renderizados
        labels = [sb.label for sb in at.selectbox]
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
    """Verifica que la estación de ingesta, los KPIs honestos y las 3 muestras canónicas funcionan."""
    at = AppTest.from_file(APP_PATH, default_timeout=30)
    at.run()
    assert not at.exception

    # 1. Comprobar que los KPIs de motor muestran 'Aún sin medir' en frío
    all_markdown = " ".join([m.value for m in at.markdown])
    assert "Puntaje de Anclaje" in all_markdown
    assert "Aún sin medir" in all_markdown, "El KPI inicial debe mostrar honestamente 'Aún sin medir'"
    assert "3 Formatos" in all_markdown
    assert "Corpus SQL" not in all_markdown, "El KPI de biblioteca 'Corpus SQL' no debe estar en el banner superior"

    # 2. Comprobar la presencia de la Estación de Ingesta
    assert "Estación de Ingesta y Transformación Documental" in all_markdown

    # 3. Comprobar exactamente las 3 muestras oficiales
    btn_canonico = [b for b in at.button if "Caso Canónico Oracle" in b.label]
    assert len(btn_canonico) == 1, "No se encontró el botón del caso canónico de Oracle VCN"
    btn_m2 = [b for b in at.button if "Muestra 2: VCN Arquitecto" in b.label]
    assert len(btn_m2) == 1, "No se encontró el botón de Muestra 2"
    btn_m3 = [b for b in at.button if "Muestra 3: Seguridad IAM" in b.label]
    assert len(btn_m3) == 1, "No se encontró el botón de Muestra 3"

    # 4. Probar clic en el caso canónico
    btn_canonico[0].click().run()
    assert not at.exception


def test_ui_grading_flow_sm2():
    """Valida el flujo de estudio interactivo, volteo de tarjetas y calificación SM-2 en 3 niveles sin DetachedInstanceError."""
    at = AppTest.from_file(APP_PATH, default_timeout=45)
    at.run()
    assert not at.exception

    # 1. Cargar el caso canónico
    btn_canonico = [b for b in at.button if "Caso Canónico Oracle" in b.label][0]
    btn_canonico.click().run()
    assert not at.exception

    # 2. Pulsar botón principal de generación
    btn_generar = [b for b in at.button if "Generar Material Didáctico" in b.label][0]
    btn_generar.click().run()
    assert not at.exception

    all_text = " ".join([m.value for m in at.markdown] + [c.value for c in at.caption])
    # Anuncio de resultados listo
    assert "¡Material Didáctico Listo!" in all_text, "Debe mostrarse el banner anunciador de resultados"
    # Nota de representatividad pedagógica
    assert "muestra representativa de 4 tarjetas" in all_text, "Falta nota de control de carga cognitiva"

    # 3. Probar volteo de la primera tarjeta
    btn_flip = [b for b in at.button if "Voltear Tarjeta" in b.label or "Ver Frente" in b.label]
    assert len(btn_flip) >= 1, "Debe existir al menos un botón de volteo"
    btn_flip[0].click().run()
    assert not at.exception

    # 4. Probar los 3 botones de asimilación por competencia (SM-2)
    btn_no = [b for b in at.button if "No alcanzado" in b.label]
    btn_dev = [b for b in at.button if "En desarrollo" in b.label]
    btn_alc = [b for b in at.button if "Alcanzado" in b.label]

    assert len(btn_no) >= 1, "Debe existir botón 🔴 No alcanzado"
    assert len(btn_dev) >= 1, "Debe existir botón 🟡 En desarrollo"
    assert len(btn_alc) >= 1, "Debe existir botón 🟢 Alcanzado"

    # Ejecutar clic en 'Alcanzado' y validar que no arroja DetachedInstanceError ni excepción
    btn_alc[0].click().run()
    assert not at.exception, f"Error al calificar SM-2: {[e.message for e in at.exception]}"

    # Verificar que el retorno del cronograma de repaso quedó renderizado
    markdown_after_grade = " ".join([m.value for m in at.markdown])
    assert "Próximo repaso:" in markdown_after_grade, "El cronograma de repaso debe persistir visible en la tarjeta"
    assert "Alcanzado" in markdown_after_grade

