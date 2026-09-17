# RetentionMeter
Anillo que muestra la Fuerza de Retención estimada de una tarjeta o módulo y la fecha del Próximo Repaso Óptimo.

- Variable CSS `--p` (0–100) controla el arco. Tonos: `quantum` ≥ 85 (Estable), `amber` 70–84 (Repasar hoy), `danger` < 70 (En riesgo).
- El porcentaje siempre va escrito en el centro y el estado en palabras al lado: el color nunca es el único indicador.
- Tamaños: 72 px (tablero) y 48 px `nm-ring--sm` (flashcard).
- Fórmula de la estimación: sección Sistema de Skills → "Visualización SM-2".
