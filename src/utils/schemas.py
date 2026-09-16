"""
Esquemas Pydantic y Contratos de Datos para NuevaMente.
Cumple estrictamente con la especificación del Hackathon ONE G10 (Páginas 4 y 5 del PDF).
"""
from datetime import datetime
from enum import Enum
from typing import List, Optional, Union, Dict, Any
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict

# --- Enumeraciones de Entrada ---
class PerfilDestinatario(str, Enum):
    PRINCIPIANTE = "Principiante"
    JUNIOR_MID = "Desarrollador Junior / Semi Senior"
    ARQUITECTO = "Líder Técnico / Arquitecto"
    EJECUTIVO = "Gestor / Ejecutivo (No Técnico)"

class FormatoSalida(str, Enum):
    FLASHCARDS = "Flashcards"
    QUIZ = "Quiz Interactivo"
    TUTORIAL = "Guía Práctica Paso a Paso (Tutorial)"
    RESUMEN = "Resumen Ejecutivo (TL;DR)"
    GUION = "Guion de Clase / Video"

class NichoSector(str, Enum):
    FINTECH = "Fintech"
    SALUD = "Salud"
    ECOMMERCE = "E-commerce"
    GENERAL = "General"

class NivelDetalle(str, Enum):
    DIDACTICO = "Didactico"
    TECNICO = "Tecnico"
    EJECUTIVO = "Ejecutivo"

# --- Modelo de Solicitud (Entrada) ---
class SolicitudAdaptacion(BaseModel):
    documento_titulo: str = Field(..., description="Título del documento técnico")
    documento_contenido: str = Field(..., description="Contenido en texto del documento técnico")
    perfil_destinatario: PerfilDestinatario = Field(default=PerfilDestinatario.PRINCIPIANTE)
    formato_salida: FormatoSalida = Field(default=FormatoSalida.FLASHCARDS)
    nicho_sector: NichoSector = Field(default=NichoSector.GENERAL)
    nivel_detalle: NivelDetalle = Field(default=NivelDetalle.DIDACTICO)

# --- Modelos de Elementos Pedagógicos (Items) ---
class FlashcardItem(BaseModel):
    frente: str = Field(..., description="Pregunta o concepto clave")
    dorso: str = Field(..., description="Explicación adaptada pedagógicamente")
    pista_didactica: Optional[str] = Field(None, description="Analogía o pista para facilitar memorización")

class QuizItem(BaseModel):
    pregunta: str = Field(..., description="Pregunta de evaluación")
    opciones: List[str] = Field(..., description="Lista de opciones de respuesta")
    respuesta_correcta: str = Field(..., description="Opción correcta")
    justificacion_didactica: str = Field(..., description="Fundamentación de la respuesta basada en el texto fuente")
    pista_didactica: Optional[str] = Field(None, description="Pista conceptual")

class TutorialStepItem(BaseModel):
    paso: int = Field(..., description="Número de paso")
    titulo_paso: str = Field(..., description="Nombre del paso")
    descripcion: str = Field(..., description="Instrucciones detalladas")
    comando_o_codigo: Optional[str] = Field(None, description="Snippet o comando si aplica")
    verificacion: str = Field(..., description="Cómo verificar que el paso se completó con éxito")

# --- Metadatos y Contenido ---
class MetadatosAprendizaje(BaseModel):
    perfil_aplicado: str = Field(..., description="Perfil del estudiante aplicado")
    formato_generado: str = Field(..., description="Formato pedagógico generado")
    tiempo_estimado_estudio_minutos: int = Field(..., description="Tiempo estimado en minutos")
    conceptos_clave: List[str] = Field(..., description="Conceptos clave extraídos")

class ContenidoAdaptado(BaseModel):
    titulo: str = Field(..., description="Título pedagógico adaptado")
    introduccion_contextualizada: str = Field(..., description="Introducción con analogía acorde al perfil y nicho")
    items: List[Dict[str, Any]] = Field(..., description="Lista de elementos pedagógicos (flashcards, quiz, pasos)")

class EvaluacionCalidad(BaseModel):
    anclaje_fuente_score: float = Field(..., ge=0.0, le=1.0, description="Puntuación de fidelidad al documento (0 a 1)")
    claridad_pedagogica: str = Field(..., description="Nivel de claridad (Alta, Media, Regular)")
    observaciones: str = Field(..., description="Comentarios sobre la adaptación y prevención de alucinaciones")

class AlmacenamientoOCI(BaseModel):
    bucket: str = Field(..., description="Nombre del bucket en OCI Object Storage")
    objeto_id: str = Field(..., description="Nombre del archivo JSON almacenado en OCI")
    status_upload: str = Field(default="completado", description="Estado de la persistencia (completado/emulado)")

# --- Modelo de Respuesta Final (Salida Estructurada) ---
class RespuestaAdaptacion(BaseModel):
    status: str = Field(default="exito", description="Estado de la operación")
    metadatos: MetadatosAprendizaje
    contenido_adaptado: ContenidoAdaptado
    evaluacion_calidad: EvaluacionCalidad
    almacenamiento_oci: AlmacenamientoOCI


# ==============================================================================
# 6 ENTIDADES CORE DE NUEVAMENTE (EdTech SaaS & Persistencia Relacional)
# ==============================================================================

class RoleUsuario(str, Enum):
    ESTUDIANTE = "estudiante"
    DOCENTE = "docente"
    ADMIN = "admin"

class TaxonomiaBloom(str, Enum):
    RECORDAR = "Recordar"
    COMPRENDER = "Comprender"
    APLICAR = "Aplicar"
    ANALIZAR = "Analizar"
    EVALUAR = "Evaluar"
    CREAR = "Crear"

class EstadoIndexacion(str, Enum):
    PENDING = "pending"
    INDEXED = "indexed"
    FAILED = "failed"


# --- Entidad 1: Users ---
class UserBase(BaseModel):
    email: str = Field(..., description="Correo electrónico del usuario")
    full_name: str = Field(..., description="Nombre completo del usuario")
    role: RoleUsuario = Field(default=RoleUsuario.ESTUDIANTE, description="Rol en el sistema")
    target_profile_default: PerfilDestinatario = Field(
        default=PerfilDestinatario.PRINCIPIANTE,
        description="Perfil pedagógico predeterminado"
    )

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(..., description="Identificador único del usuario")
    created_at: datetime = Field(..., description="Fecha de registro")
    updated_at: Optional[datetime] = Field(None, description="Fecha de actualización")


# --- Entidad 2: TechnicalDocuments ---
class TechnicalDocumentBase(BaseModel):
    title: str = Field(..., description="Título del documento técnico")
    source_type: str = Field(..., description="Tipo de fuente (pdf, md, txt, web)")
    raw_content: str = Field(..., description="Texto extraído sanitizado")
    content_hash: str = Field(..., description="Hash SHA-256 del contenido para deduplicación")
    char_count: int = Field(default=0, description="Número de caracteres")
    oci_bucket: str = Field(default="nuevamente-documentos-origen", description="Bucket de origen en OCI")
    oci_object_id: Optional[str] = Field(None, description="Nombre del objeto en OCI Object Storage")

class TechnicalDocumentCreate(TechnicalDocumentBase):
    user_id: Optional[UUID] = Field(None, description="ID del usuario propietario")

class TechnicalDocumentResponse(TechnicalDocumentBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(..., description="Identificador único del documento")
    user_id: Optional[UUID] = Field(None, description="ID del usuario propietario")
    created_at: datetime = Field(..., description="Fecha de ingestión")


# --- Entidad 3: RAGKnowledgeBases ---
class RAGKnowledgeBaseBase(BaseModel):
    collection_name: str = Field(..., description="Nombre de la colección vectorial en ChromaDB")
    chunk_count: int = Field(default=0, description="Cantidad de fragmentos indexados")
    chunk_strategy: str = Field(default="recursive_character", description="Estrategia de fragmentación")
    chunk_size: int = Field(default=1000, description="Tamaño de chunk en caracteres")
    chunk_overlap: int = Field(default=150, description="Solapamiento entre chunks")
    embedding_model: str = Field(default="all-MiniLM-L6-v2", description="Modelo de embeddings")
    status: EstadoIndexacion = Field(default=EstadoIndexacion.PENDING, description="Estado de indexación")

class RAGKnowledgeBaseCreate(RAGKnowledgeBaseBase):
    document_id: UUID = Field(..., description="ID del documento técnico asociado")

class RAGKnowledgeBaseResponse(RAGKnowledgeBaseBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(..., description="Identificador único de la base de conocimiento RAG")
    document_id: UUID = Field(..., description="ID del documento técnico")
    created_at: datetime = Field(..., description="Fecha de indexación")


# --- Entidad 4: LearningSessions ---
class LearningSessionBase(BaseModel):
    perfil_destinatario: PerfilDestinatario = Field(..., description="Perfil del estudiante")
    formato_salida: FormatoSalida = Field(..., description="Formato pedagógico generado")
    nicho_sector: NichoSector = Field(default=NichoSector.GENERAL, description="Nicho o contexto de aplicación")
    nivel_detalle: NivelDetalle = Field(default=NivelDetalle.DIDACTICO, description="Nivel de detalle didáctico")
    titulo_adaptado: str = Field(..., description="Título didáctico adaptado")
    introduccion_contextualizada: str = Field(..., description="Introducción contextualizada con analogía")
    tiempo_estimado_minutos: int = Field(default=5, description="Tiempo estimado de estudio en minutos")
    conceptos_clave: List[str] = Field(default_factory=list, description="Lista de conceptos clave")
    anclaje_fuente_score: float = Field(default=0.95, ge=0.0, le=1.0, description="Score de grounding RAG (0-1)")
    claridad_pedagogica: str = Field(default="Alta", description="Nivel de claridad pedagógica")
    observaciones_calidad: str = Field(default="", description="Observaciones del revisor de calidad")
    oci_bucket: str = Field(default="nuevamente-contenidos-educativos", description="Bucket OCI de resultados")
    oci_object_id: Optional[str] = Field(None, description="Identificador del JSON en OCI")

class LearningSessionCreate(LearningSessionBase):
    user_id: Optional[UUID] = Field(None, description="ID del usuario")
    document_id: UUID = Field(..., description="ID del documento técnico de origen")

class LearningSessionResponse(LearningSessionBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(..., description="Identificador de la sesión de aprendizaje")
    user_id: Optional[UUID] = Field(None, description="ID del usuario")
    document_id: UUID = Field(..., description="ID del documento técnico")
    created_at: datetime = Field(..., description="Fecha de creación")


# --- Entidad 5: Flashcards ---
class FlashcardBase(BaseModel):
    front: str = Field(..., description="Frente: pregunta o concepto técnico clave")
    back: str = Field(..., description="Dorso: explicación pedagógica adaptada")
    didactic_hint: Optional[str] = Field(None, description="Pista mnemotécnica o analogía")
    mastery_level: int = Field(default=0, ge=0, le=5, description="Nivel de asimilación (0 a 5, algoritmo SM-2)")
    next_review_at: Optional[datetime] = Field(None, description="Fecha recomendada para el próximo repaso")

class FlashcardCreate(FlashcardBase):
    session_id: UUID = Field(..., description="ID de la sesión de aprendizaje asociada")
    user_id: Optional[UUID] = Field(None, description="ID del usuario propietario")

class FlashcardUpdateMastery(BaseModel):
    mastery_level: int = Field(..., ge=0, le=5, description="Nuevo nivel de asimilación asignado")
    next_review_at: Optional[datetime] = Field(None, description="Nueva fecha de repaso calculada")

class FlashcardResponse(FlashcardBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(..., description="Identificador único de la flashcard")
    session_id: UUID = Field(..., description="ID de la sesión de aprendizaje")
    user_id: Optional[UUID] = Field(None, description="ID del usuario")
    created_at: datetime = Field(..., description="Fecha de generación")


# --- Entidad 6: Quizzes y QuizQuestions ---
class QuizQuestionBase(BaseModel):
    question_text: str = Field(..., description="Texto del enunciado de la pregunta")
    options: List[str] = Field(..., description="Lista de 4 opciones de respuesta")
    correct_answer: str = Field(..., description="Opción correcta con su texto completo")
    explanation: str = Field(..., description="Justificación pedagógica anclada a la documentación")
    didactic_hint: Optional[str] = Field(None, description="Pista didáctica de apoyo")
    bloom_taxonomy_level: TaxonomiaBloom = Field(
        default=TaxonomiaBloom.COMPRENDER,
        description="Nivel taxonómico de Bloom evaluado"
    )

class QuizQuestionCreate(QuizQuestionBase):
    pass

class QuizQuestionResponse(QuizQuestionBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(..., description="Identificador único de la pregunta")
    quiz_id: UUID = Field(..., description="ID del quiz al que pertenece")
    created_at: datetime = Field(..., description="Fecha de generación")

class QuizBase(BaseModel):
    title: str = Field(..., description="Título didáctico del quiz")
    total_questions: int = Field(default=0, description="Total de preguntas que componen el quiz")

class QuizCreate(QuizBase):
    session_id: UUID = Field(..., description="ID de la sesión de aprendizaje asociada")
    user_id: Optional[UUID] = Field(None, description="ID del usuario")
    questions: List[QuizQuestionCreate] = Field(default_factory=list, description="Lista de preguntas a crear")

class QuizResponse(QuizBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(..., description="Identificador único del quiz")
    session_id: UUID = Field(..., description="ID de la sesión de aprendizaje")
    user_id: Optional[UUID] = Field(None, description="ID del usuario")
    created_at: datetime = Field(..., description="Fecha de creación")
    questions: List[QuizQuestionResponse] = Field(default_factory=list, description="Preguntas del quiz")

class QuizSubmission(BaseModel):
    question_id: UUID = Field(..., description="ID de la pregunta respondida")
    selected_option: str = Field(..., description="Opción seleccionada por el estudiante")

class QuizResult(BaseModel):
    question_id: UUID = Field(..., description="ID de la pregunta evaluada")
    is_correct: bool = Field(..., description="Indica si la respuesta fue correcta")
    correct_answer: str = Field(..., description="Opción correcta esperada")
    explanation: str = Field(..., description="Justificación pedagógica fundamentada")
    bloom_taxonomy_level: TaxonomiaBloom = Field(..., description="Nivel de Bloom correspondiente")
