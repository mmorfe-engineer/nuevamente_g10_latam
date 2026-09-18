"""
Contrato oficial literal del pliego ONE G10 / Oracle Next Education & Alura.
Reexporta todas las clases y esquemas de datos canónicos desde src.utils.schemas.
"""
from src.utils.schemas import (
    PerfilDestinatario,
    FormatoSalida,
    NichoSector,
    NivelDetalle,
    SolicitudAdaptacion,
    FlashcardItem,
    QuizItem,
    TutorialStepItem,
    MetadatosAprendizaje,
    ContenidoAdaptado,
    EvaluacionCalidad,
    AlmacenamientoOCI,
    RespuestaAdaptacion,
)

__all__ = [
    "PerfilDestinatario",
    "FormatoSalida",
    "NichoSector",
    "NivelDetalle",
    "SolicitudAdaptacion",
    "FlashcardItem",
    "QuizItem",
    "TutorialStepItem",
    "MetadatosAprendizaje",
    "ContenidoAdaptado",
    "EvaluacionCalidad",
    "AlmacenamientoOCI",
    "RespuestaAdaptacion",
]
