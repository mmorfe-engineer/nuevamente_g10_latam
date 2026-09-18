"""Pruebas de esquemas Pydantic y contratos de datos oficiales."""
import pytest
from src.utils.schemas import (
    SolicitudAdaptacion,
    RespuestaAdaptacion,
    MetadatosAprendizaje,
    ContenidoAdaptado,
    EvaluacionCalidad,
    AlmacenamientoOCI,
    PerfilDestinatario,
    FormatoSalida
)

def test_solicitud_adaptacion_valida():
    req = SolicitudAdaptacion(
        documento_titulo="VCN OCI",
        documento_contenido="Contenido de prueba de Virtual Cloud Network",
        perfil_destinatario=PerfilDestinatario.PRINCIPIANTE,
        formato_salida=FormatoSalida.FLASHCARDS
    )
    assert req.documento_titulo == "VCN OCI"
    assert req.perfil_destinatario == PerfilDestinatario.PRINCIPIANTE

def test_respuesta_adaptacion_valida():
    resp = RespuestaAdaptacion(
        status="exito",
        metadatos=MetadatosAprendizaje(
            perfil_aplicado="Principiante",
            formato_generado="Flashcards",
            tiempo_estimado_estudio_minutos=5,
            conceptos_clave=["VCN", "Subredes"],
            prerrequisitos=["Conceptos básicos de IP", "Navegación web"]
        ),
        contenido_adaptado=ContenidoAdaptado(
            titulo="Redes desde Cero",
            introduccion_contextualizada="Analogía de prueba",
            items=[{"frente": "Q1", "dorso": "A1", "pista_didactica": "Pista"}]
        ),
        evaluacion_calidad=EvaluacionCalidad(
            anclaje_fuente_score=0.98,
            claridad_pedagogica="Alta",
            observaciones="Sin tecnicismos excesivos"
        ),
        almacenamiento_oci=AlmacenamientoOCI(
            bucket="nuevamente-contenidos-educativos",
            objeto_id="contenido-001.json",
            status_upload="completado"
        )
    )
    assert resp.status == "exito"
    assert resp.metadatos.tiempo_estimado_estudio_minutos == 5
    assert len(resp.metadatos.prerrequisitos) == 2
    assert resp.evaluacion_calidad.anclaje_fuente_score == 0.98

def test_diez_sectores_canonicos_y_reexportacion():
    from src.schemas.adaptation import NichoSector, SolicitudAdaptacion as SolicitudCanonical
    sectores_esperados = [
        "Ciberseguridad", "Agroindustria", "Commodities y energía",
        "Banca y fintech", "Salud", "Manufactura e ingeniería",
        "Cloud e infraestructura", "Logística y comercio exterior",
        "Administración pública", "Telecomunicaciones"
    ]
    for s in sectores_esperados:
        assert any(n.value == s for n in NichoSector)
    
    req = SolicitudCanonical(
        documento_titulo="Manual de Compresor",
        documento_contenido="Mantenimiento preventivo",
        nicho_sector=NichoSector.MANUFACTURA
    )
    assert req.nicho_sector.value == "Manufactura e ingeniería"

