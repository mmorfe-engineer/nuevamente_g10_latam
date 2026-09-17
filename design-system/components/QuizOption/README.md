# QuizOption
Opción de respuesta del Visualizador de Quiz Neón con cuatro estados: reposo, hover, correcta con cita y fallida con justificación.

| Estado | Clase | Borde / fondo | Nota |
| --- | --- | --- | --- |
| Reposo | `nm-opt` | `line` / `bg-800` | — |
| Hover / foco | `:hover`, `.is-hover` | `cyber` + `glow-cyber` | la letra pasa a `cyber` |
| Correcta | `.is-correct` | `success` / `success-bg` | **"Correcto."** + cita en `font-mono` |
| Fallida | `.is-wrong` | `danger` / `danger-bg` | **"No exactamente."** + por qué, sin culpar |

- Tras responder se revelan ambas: la elegida y la correcta. El glow desaparece al resolverse.
- Cada nota de acierto lleva cita verificable (norma + requisito). Las citas de la vista previa son de ejemplo: el motor RAG debe insertar la referencia exacta del documento ingerido.
- El estado también se anuncia con texto ("Correcto" / "No exactamente"), nunca solo por color.
