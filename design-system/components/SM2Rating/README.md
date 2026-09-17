# SM2Rating
Barra de autoevaluación de calidad de respuesta *q* de 0 a 5 del algoritmo SuperMemo SM-2; alimenta el cálculo del próximo repaso.

- Seis botones iguales (0–5) con número en `font-mono` y etiqueta corta. Se usan números, no estrellas: SM-2 incluye el 0 y cinco estrellas no lo representan.
- Filete inferior semántico: 0–2 `danger` (se reinicia la repetición), 3 `amber`, 4–5 `success`.
- Seleccionado: fondo `quantum`, texto blanco. Hover: `glow-cyber`.
- Tras elegir, la línea inferior confirma el efecto en lenguaje llano ("Próximo repaso óptimo · en 6 días" o "Se repite hoy").
- Teclado: atajos 0–5 los provee el consumidor.
- Los días de la vista previa son ilustrativos; el intervalo real sale de `SM-2` (ver sección Sistema de Skills).
