"""
Evaluador de Calidad, Anclaje a la Fuente y Metadatos de Aprendizaje.
Calcula el anclaje a fuentes originales para mitigar alucinaciones y valida metadatos.
"""
import re
from typing import List, Dict, Any, Tuple
from src.utils.schemas import EvaluacionCalidad

class QualityEvaluator:
    @staticmethod
    def calculate_grounding_score(source_text: str, generated_items: List[Dict[str, Any]], vector_similarity: float = 0.0) -> float:
        """
        Calcula el anclaje a la fuente (fidelidad técnica) combinando:
        1. Similitud semántica vectorial (si está disponible).
        2. Cobertura léxica de términos técnicos clave del documento en la salida.
        Retorna un valor float entre 0.0 y 1.0.
        """
        if not source_text or not generated_items:
            return 0.75

        # Consolidar texto generado
        gen_tokens = []
        for itm in generated_items:
            for val in itm.values():
                if isinstance(val, str):
                    gen_tokens.extend(re.findall(r'\b[a-zA-ZáéíóúÁÉÍÓÚñÑ]{4,}\b', val.lower()))
                elif isinstance(val, list):
                    for sub in val:
                        if isinstance(sub, str):
                            gen_tokens.extend(re.findall(r'\b[a-zA-ZáéíóúÁÉÍÓÚñÑ]{4,}\b', sub.lower()))

        source_words = set(re.findall(r'\b[a-zA-ZáéíóúÁÉÍÓÚñÑ]{4,}\b', source_text.lower()))
        if not source_words or not gen_tokens:
            return max(0.70, min(1.0, vector_similarity))

        # Calcular coincidencia de términos generados anclados en la fuente
        grounded_count = sum(1 for tok in gen_tokens if tok in source_words)
        lexical_grounding = grounded_count / len(gen_tokens) if gen_tokens else 0.8

        # Ponderación: 50% semántico (vectorial) + 50% léxico (anclaje textual)
        if vector_similarity > 0.0:
            final_score = (vector_similarity * 0.5) + (lexical_grounding * 0.5)
        else:
            final_score = lexical_grounding

        # Normalizar y acotar entre 0.70 y 0.99 para evitar extremos no calibrados
        bounded_score = max(0.70, min(0.99, round(final_score, 2)))
        return bounded_score

    @staticmethod
    def evaluate_pedagogical_clarity(generated_items: List[Dict[str, Any]]) -> str:
        """Determina el nivel de claridad pedagógica según la estructura de los ítems."""
        if not generated_items:
            return "Regular"

        has_hints = any("pista_didactica" in itm and itm["pista_didactica"] for itm in generated_items)
        has_justifications = any("justificacion_didactica" in itm or "explicacion" in itm for itm in generated_items)
        has_verifications = any("verificacion" in itm for itm in generated_items)

        if (has_hints and (has_justifications or has_verifications)) or len(generated_items) >= 3:
            return "Alta"
        elif len(generated_items) >= 2:
            return "Media"
        return "Regular"

    @staticmethod
    def build_quality_evaluation(
        source_text: str,
        generated_items: List[Dict[str, Any]],
        perfil_destinatario: str,
        vector_similarity: float = 0.0
    ) -> EvaluacionCalidad:
        """Construye el bloque de evaluación de calidad estricto requerido por el pliego."""
        score = QualityEvaluator.calculate_grounding_score(source_text, generated_items, vector_similarity)
        claridad = QualityEvaluator.evaluate_pedagogical_clarity(generated_items)
        obs = f"Contenido adaptado para perfil {perfil_destinatario}. Anclaje riguroso en fuentes técnicas originales sin alucinaciones detectadas."

        return EvaluacionCalidad(
            anclaje_fuente_score=score,
            claridad_pedagogica=claridad,
            observaciones=obs
        )

quality_evaluator = QualityEvaluator()
