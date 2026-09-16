"""
Módulo de Algoritmo de Repetición Espaciada (SuperMemo SM-2 / Leitner).
Optimiza la retención a largo plazo calculando el Factor de Facilidad (EF) e intervalos de repaso.
"""
from datetime import datetime, timedelta
from typing import Tuple


def calculate_sm2(
    quality: int,
    repetitions: int = 0,
    previous_interval: int = 1,
    previous_ef: float = 2.5
) -> Tuple[int, int, float, datetime]:
    """
    Calcula el siguiente intervalo de estudio y factor de facilidad según el algoritmo SM-2.
    
    Parámetros:
      - quality (int): Calificación del usuario de 0 a 5:
          5: Respuesta perfecta, esfuerzo nulo (Fácil)
          4: Respuesta correcta con vacilación
          3: Respuesta correcta con dificultad (Bien)
          2: Respuesta incorrecta, pero recordó al ver dorso
          1: Respuesta incorrecta, familiar
          0: Olvido total (Difícil)
      - repetitions (int): Cantidad de veces repasada con éxito consecutivas.
      - previous_interval (int): Intervalo previo en días.
      - previous_ef (float): Factor de facilidad previo (mínimo 1.3).
      
    Retorna:
      - (new_repetitions, new_interval_days, new_ef, next_review_datetime)
    """
    # Restringir calidad a rango 0-5
    quality = max(0, min(5, quality))

    # Actualizar factor de facilidad (EF)
    # Fórmula SM-2: EF' = EF + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
    new_ef = previous_ef + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    new_ef = max(1.3, round(new_ef, 2))

    if quality >= 3:
        # Repaso exitoso
        if repetitions == 0:
            new_interval = 1
        elif repetitions == 1:
            new_interval = 6
        else:
            new_interval = max(1, int(round(previous_interval * new_ef)))
        new_repetitions = repetitions + 1
    else:
        # Olvido o fallo: reiniciar ciclo
        new_repetitions = 0
        new_interval = 1

    next_review = datetime.utcnow() + timedelta(days=new_interval)
    return new_repetitions, new_interval, new_ef, next_review
