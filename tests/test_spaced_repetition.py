"""
Pruebas Unitarias para el algoritmo de repetición espaciada SuperMemo SM-2.
"""
from datetime import datetime
import pytest
from src.utils.spaced_repetition import calculate_sm2


def test_sm2_first_successful_review():
    """Valida el primer repaso exitoso (intervalo 1 día)."""
    reps, interval, ef, next_rev = calculate_sm2(quality=4, repetitions=0)
    assert reps == 1
    assert interval == 1
    assert ef >= 1.3
    assert next_rev > datetime.utcnow()


def test_sm2_second_successful_review():
    """Valida el segundo repaso consecutivo exitoso (intervalo 6 días)."""
    reps, interval, ef, next_rev = calculate_sm2(quality=5, repetitions=1, previous_interval=1)
    assert reps == 2
    assert interval == 6
    assert ef >= 2.5


def test_sm2_subsequent_review():
    """Valida repasos posteriores escalados por el factor de facilidad EF."""
    reps, interval, ef, next_rev = calculate_sm2(quality=5, repetitions=2, previous_interval=6, previous_ef=2.6)
    assert reps == 3
    assert interval == 16  # round(6 * 2.6) = 16


def test_sm2_failed_review_resets():
    """Valida que una calificación menor a 3 reinicia el intervalo a 1 día."""
    reps, interval, ef, next_rev = calculate_sm2(quality=1, repetitions=4, previous_interval=20)
    assert reps == 0
    assert interval == 1
    assert ef >= 1.3
