"""
Pruebas Unitarias para el Módulo de Exportación Multiformato (Anki CSV y Markdown).
"""
import pytest
from src.utils.exporters import export_to_anki_csv, export_to_markdown_guide
from src.utils.schemas import (
    RespuestaAdaptacion,
    MetadatosAprendizaje,
    ContenidoAdaptado,
    EvaluacionCalidad,
    AlmacenamientoOCI
)


def test_export_to_anki_csv():
    """Valida la generación de CSV compatible con Anki."""
    items = [
        {"frente": "¿Qué es VCN?", "dorso": "Red virtual en OCI", "pista_didactica": "Tu vecindario privado"},
        {"frente": "¿Qué es Subred?", "dorso": "División de la VCN", "pista_didactica": "Un lote"}
    ]
    csv_text = export_to_anki_csv(items)
    assert "# Front;Back;Hint;Tags" in csv_text
    assert "¿Qué es VCN?;Red virtual en OCI;Tu vecindario privado;nuevamente_oci edtech hackathon_one_g10" in csv_text


def test_export_to_markdown_guide():
    """Valida la generación de la guía didáctica en Markdown."""
    resp = RespuestaAdaptacion(
        status="exito",
        metadatos=MetadatosAprendizaje(
            perfil_aplicado="Principiante",
            formato_generado="Flashcards",
            tiempo_estimado_estudio_minutos=5,
            conceptos_clave=["VCN", "Subredes"]
        ),
        contenido_adaptado=ContenidoAdaptado(
            titulo="Redes OCI desde Cero",
            introduccion_contextualizada="Analogía para principiantes.",
            items=[{"frente": "Q1", "dorso": "A1", "pista_didactica": "Tip"}]
        ),
        evaluacion_calidad=EvaluacionCalidad(
            anclaje_fuente_score=0.98,
            claridad_pedagogica="Alta",
            observaciones="Sin tecnicismos excesivos."
        ),
        almacenamiento_oci=AlmacenamientoOCI(
            bucket="nuevamente-contenidos-educativos",
            objeto_id="contenido-001.json",
            status_upload="completado"
        )
    )
    md_text = export_to_markdown_guide(resp)
    assert "# Redes OCI desde Cero" in md_text
    assert "Principiante" in md_text
    assert "98%" in md_text
    assert "Q1" in md_text
