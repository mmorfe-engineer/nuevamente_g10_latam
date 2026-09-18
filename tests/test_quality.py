"""Pruebas para el Evaluador de Calidad y Anclaje a la Fuente."""
from src.quality.evaluator import quality_evaluator

def test_grounding_score_calculation():
    source = "La válvula de recirculación de aceite debe inspeccionarse cada 500 horas de operación continua."
    items = [
        {"frente": "¿Cada cuánto inspeccionar la válvula de aceite?", "dorso": "Cada 500 horas de operación continua."}
    ]
    score = quality_evaluator.calculate_grounding_score(source, items, vector_similarity=0.92)
    assert 0.70 <= score <= 1.0

def test_pedagogical_clarity_evaluation():
    items = [
        {"frente": "Q1", "dorso": "A1", "pista_didactica": "P1", "justificacion_didactica": "J1"},
        {"frente": "Q2", "dorso": "A2", "pista_didactica": "P2", "justificacion_didactica": "J2"}
    ]
    clarity = quality_evaluator.evaluate_pedagogical_clarity(items)
    assert clarity in ["Alta", "Media"]

def test_build_quality_evaluation():
    source = "Manual técnico de operación y mantenimiento preventivo."
    items = [{"frente": "Operación", "dorso": "Mantenimiento preventivo"}]
    calidad = quality_evaluator.build_quality_evaluation(source, items, "Principiante")
    assert calidad.anclaje_fuente_score >= 0.70
    assert calidad.claridad_pedagogica in ["Alta", "Media", "Regular"]
    assert "Principiante" in calidad.observaciones
