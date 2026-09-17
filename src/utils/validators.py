"""
Módulo de Validadores y Normalización de Nomenclatura — Estándar LexForja.
Asegura la preservación canónica de términos técnicos:
Regla obligatoria: Término en Español [Término Canónico en Inglés]
"""
import re
from typing import List, Dict, Tuple, Any, Optional

# Patrón regex que detecta: Cualquier texto en español seguido de [Término Canónico en Inglés]
PARENTHETICAL_REGEX = re.compile(r'([A-Za-zÁÉÍÓÚáéíóúñÑ0-9\s\-\/\(\)]+?)\s*\[([A-Za-z0-9\s\-\/\(\)\.\_\:]+)\]')


class LexForjaValidator:
    """Validador de calidad y consistencia técnica según el estándar LexForja."""

    @staticmethod
    def extract_parenthetical_pairs(text: str) -> List[Tuple[str, str]]:
        """Extrae todas las tuplas (término_es, término_en) que cumplen con la regla parentética."""
        if not text:
            return []
        matches = PARENTHETICAL_REGEX.findall(text)
        return [(m[0].strip(), m[1].strip()) for m in matches if len(m[0].strip()) > 2 and len(m[1].strip()) > 2]

    @staticmethod
    def validate_text_nomenclature(text: str, expected_terms_en: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Evalúa si un texto técnico pedagógico cumple con la regla de nomenclatura parentética.
        Retorna:
          - is_valid: True si contiene al menos una entidad canónica o no requiere
          - parenthetical_count: cantidad de términos normalizados encontrados
          - extracted_pairs: pares encontrados
          - compliance_score: 0.0 a 1.0 de apego a la norma
        """
        pairs = LexForjaValidator.extract_parenthetical_pairs(text)
        count = len(pairs)
        
        score = min(1.0, count / 2.0) if count > 0 else 0.0
        
        return {
            "is_valid": count > 0,
            "parenthetical_count": count,
            "extracted_pairs": [{"termino_es": p[0], "termino_en": p[1]} for p in pairs],
            "compliance_score": round(score, 2)
        }

    @staticmethod
    def enforce_parenthetical_terms(text: str, glossary_pairs: List[Dict[str, str]]) -> str:
        """
        Inyecta automáticamente los corchetes con el término canónico en inglés
        si el texto generado en español menciona el concepto pero omitió la referencia canónica.
        glossary_pairs: list of dicts with keys 'termino_es' and 'termino_en'
        """
        if not text or not glossary_pairs:
            return text

        enriched_text = text
        for item in glossary_pairs:
            t_es = item.get("termino_es", "").strip()
            t_en = item.get("termino_en", "").strip()
            if not t_es or not t_en:
                continue

            # Si ya contiene el término en inglés entre corchetes, no duplicar
            if f"[{t_en}]" in enriched_text:
                continue

            # Buscar mención aislada en español (case-insensitive) y reemplazar con Término [Término EN]
            pattern = re.compile(rf'\b({re.escape(t_es)})\b(?!\s*\[)', re.IGNORECASE)
            enriched_text = pattern.sub(rf'\1 [{t_en}]', enriched_text, count=2)

        return enriched_text


lexforja_validator = LexForjaValidator()
