"""
Prueba de Independencia del Corpus y Agnosticism de Dominio (Sector 6: Manufactura e Ingeniería).
Verifica que el sistema procese un documento de un sector completamente ajeno a ciberseguridad
sin tocar código y con la misma calidad de salida estricta (Cierre de fila X-01).
"""
import json
from pathlib import Path
from src.ingestion.loaders import doc_loader
from src.services.adaptation_service import adaptation_service
from src.utils.schemas import (
    SolicitudAdaptacion,
    PerfilDestinatario,
    FormatoSalida,
    NichoSector,
    NivelDetalle
)

def test_cross_corpus_manufacturing_adaptation():
    doc_path = Path("data/samples/04_manufactura_compresores_industriales.md")
    assert doc_path.exists(), "El documento de muestra de manufactura debe existir."

    content = doc_loader.extract_from_file(doc_path)
    assert len(content) > 500

    solicitud = SolicitudAdaptacion(
        documento_titulo="Manual de Compresores de Tornillo Rotativo Industrial",
        documento_contenido=content,
        perfil_destinatario=PerfilDestinatario.PRINCIPIANTE,
        formato_salida=FormatoSalida.TUTORIAL,
        nicho_sector=NichoSector.MANUFACTURA,
        nivel_detalle=NivelDetalle.DIDACTICO
    )

    respuesta, trace = adaptation_service.process_adaptation(solicitud)

    # Verificaciones estrictas del contrato ONE G10
    assert respuesta.status == "exito"
    assert respuesta.metadatos.perfil_aplicado == PerfilDestinatario.PRINCIPIANTE.value
    assert respuesta.metadatos.formato_generado == FormatoSalida.TUTORIAL.value
    assert respuesta.metadatos.tiempo_estimado_estudio_minutos > 0
    assert len(respuesta.metadatos.conceptos_clave) >= 2
    assert hasattr(respuesta.metadatos, "prerrequisitos")
    assert len(respuesta.metadatos.prerrequisitos) >= 1

    # Verificación de anclaje a la fuente y calidad
    assert respuesta.evaluacion_calidad.anclaje_fuente_score >= 0.70
    assert respuesta.evaluacion_calidad.claridad_pedagogica in ["Alta", "Media"]

    # Verificación de persistencia OCI
    assert respuesta.almacenamiento_oci.bucket == "nuevamente-contenidos-educativos"
    assert respuesta.almacenamiento_oci.objeto_id.endswith(".json")

    # Verificación de contenido adaptado
    items = respuesta.contenido_adaptado.items
    assert len(items) >= 2

    # Auditoría de neutralidad de dominio:
    # No deben aparecer términos ajenos de ciberseguridad inyectados arbitrariamente
    full_text = json.dumps(respuesta.model_dump(), ensure_ascii=False).lower()
    assert "ransomware" not in full_text
    assert "firewall" not in full_text
    assert "phishing" not in full_text

    # Archivar el JSON de evidencia para auditoría de entrega (Checklist X-01)
    output_dir = Path("docs/contratos_referencia")
    output_dir.mkdir(parents=True, exist_ok=True)
    evidence_file = output_dir / "ejemplo_sector6_manufactura.json"
    with open(evidence_file, "w", encoding="utf-8") as f:
        json.dump(respuesta.model_dump(), f, indent=2, ensure_ascii=False)

    assert evidence_file.exists()
    assert evidence_file.stat().st_size > 300
