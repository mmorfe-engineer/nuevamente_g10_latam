# Flashcard3D
Tarjeta de estudio con volteo 3D: anverso = pregunta + pista mnemotécnica; reverso = explicación canónica + fuente citada + fuerza de retención.

**Anatomía**
1. Meta: rótulo `overline` (ruta · posición) y sello `nm-oci` si el contenido es de Oracle Cloud.
2. Anverso: pregunta en `font-display` 20/28; pista al pie sobre `bg-700`, palabra "Pista" en `quantum-soft`.
3. Reverso: explicación en `body` con al menos un `CanonicalTerm`; fuente en `font-mono` y color `success`; anillo `RetentionMeter` pequeño arriba a la derecha.
4. Debajo de la tarjeta, al voltear, aparece `SM2Rating`.

**Comportamiento**
- Voltea con clic, Enter o Espacio (`.is-flipped`), 600 ms. Con `prefers-reduced-motion`, el consumidor cambia el giro por un fundido.
- Hover: borde `cyber`. Volumen permanente: `elev-3d`.
- La fuente es obligatoria: una tarjeta sin cita no se publica.
