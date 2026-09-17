# NuevaMente

**Plataforma Inteligente de Transposición Andragógica.** NuevaMente convierte documentación técnica densa —NIST, CIS Benchmarks, PCI DSS, manuales de arquitectura OCI— en rutas de aprendizaje adaptativo por rol: flashcards con repetición espaciada SM-2, quizzes con retroalimentación citada, tutoriales y checklists. Estética *Deep Dev / Cyber-Modern*, Dark Enterprise por defecto.

---

## 1. Manifiesto y ADN de marca

### El nombre
**Nueva·Mente** se lee de tres formas a la vez:
- **Nuevamente** — el adverbio de la repetición espaciada: volver sobre lo aprendido en el momento óptimo.
- **Nueva mente** — la renovación cognitiva del adulto que aprende (andragogía de Knowles): el mismo empleado, una comprensión nueva.
- **Mente nueva** — la inteligencia artificial que lee por ti el manual de 1.000 páginas y lo devuelve en tu idioma.

Wordmark: "Nueva" en `ink` + "Mente" en `quantum-soft`, una sola palabra, `font-display` 700, sin espacio. No hay isotipo aún; hasta que exista, la marca es solo tipográfica.

### Manifiesto
> Las normas que protegen a un banco no fallan por estar mal escritas. Fallan porque nadie las termina de leer.
> Creemos que el cumplimiento se construye en la mente de quien atiende la taquilla, escribe la regla de firewall o firma el plan de continuidad.
> Por eso tomamos el documento más denso, lo respetamos palabra por palabra y lo devolvemos como algo que se puede aprender, repasar y demostrar.
> Cada respuesta con su fuente. Cada término en tu idioma y en el de la consola. Cada avance, medible.
> **Normativa densa, mente nueva.**

### Arquetipo
- **Primario — El Sabio:** rigor, fuentes, precisión normativa. Nunca opina sin cita.
- **Secundario — El Mago (Hacedor Tecnológico):** la transformación visible: 1.000 páginas → 24 tarjetas → una insignia verificable.

### Tono de voz
| Somos | No somos |
| --- | --- |
| Rigurosos: citamos control y versión (`PCI DSS v4.0 · Req. 7.2.4`) | Alarmistas ("¡tu banco está en peligro!") |
| Accesibles: una idea por frase, verbos concretos | Condescendientes ("es muy fácil") |
| Institucionales ante un director de banco | Burocráticos o llenos de siglas sin explicar |
| Motivadores con el talento junior | Infantiles: sin emojis en la interfaz |

**Reglas de escritura**
- Tuteo en la experiencia de aprendizaje; usted en materiales B2B formales.
- Nomenclatura Canónica Bilingüe en la primera mención: *Lista de Seguridad [Security List]* (ver componente CanonicalTerm).
- Errores sin culpa: "No exactamente" en vez de "Incorrecto".
- Prometer lo verificable. Evitar "0 % alucinaciones" en copy público: preferir **"cada respuesta con cita verificable a su fuente"**. Una cifra absoluta es la primera que un juez técnico o un auditor intenta refutar.

### Taglines
1. **B2B —** *Del manual de mil páginas al equipo que cumple.*
2. **B2B —** *Cumplimiento que se aprende, no que se archiva.*
3. **Talento —** *Aprende la nube en tu idioma. Opérala en el suyo.*

Firma de marca (portada, cierre de pitch): *Normativa densa, mente nueva.*

### Elevator pitch (30 s)
> Cada banco tiene cientos de páginas de NIST, CIS y PCI DSS que su gente no alcanza a leer, y esa brecha termina en incidentes y hallazgos de auditoría. NuevaMente ingiere esos documentos y, con IA que cita cada respuesta, los convierte en rutas por rol: el cajero aprende a detectar phishing, el desarrollador a endurecer su red en Oracle Cloud y el CISO a ejecutar Confianza Cero. Repetición espaciada para que no se olvide, evaluación Kirkpatrick para demostrarlo, y todo desplegado en OCI Always Free: capacitación medible con costo de infraestructura cero.

---

## 2. Fundamentos visuales

### Paleta (Dark Enterprise)
| Token | HEX (oscuro) | Nombre | Uso exacto |
| --- | --- | --- | --- |
| `bg-900` | #070B14 | Vacío Profundo | Fondo de página |
| `bg-800` | #0D1322 | Placa Base | Tarjetas, flashcards, opciones |
| `bg-700` | #151D31 | Capa Elevada | Inputs, pistas, barras vacías |
| `quantum` | #7456F7 | Violeta Cuántico | IA: botón primario, progreso, anillo de retención |
| `quantum-soft` | #B3A4FF | Violeta Legible | Texto violeta, "Mente" del wordmark |
| `cyber` | #22E4F2 | Cian Centinela | Hover, foco, término canónico, ruta Operaciones |
| `oracle` | #C74634 | Rojo Nube | Sello OCI; solo relleno o borde |
| `amber` | #F5A524 | Ámbar Consola | Advertencias, nivel 4, ruta Arquitecto |
| `success` | #10D98A | Esmeralda | Acierto, tests pasando |
| `danger` | #FF5C7A | Carmesí | Fallo, brecha |

**Proporción:** 80 % neutros oscuros · 12 % violeta · 6 % cian · 2 % Oracle/ámbar. El rojo Oracle es un sello, no un color de marca: si aparece más de una vez por pantalla, sobra.
**Tema claro (Light Docs):** para exportes PDF y lectura larga; mismos nombres de token con valores reajustados a ≥4.5:1 sobre blanco.

### Tipografía (Google Fonts, gratuitas)
- **Space Grotesk** (`font-display`, 500–700) — encabezados con personalidad técnica.
- **Inter** (`font-sans`, 400–600) — cuerpo e interfaz.
- **JetBrains Mono** (`font-mono`, 500–600) — comandos OCI, IDs de control, cifras de KPI y porcentajes.

```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@500;600&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
```

### Efectos UI
- **Glassmorphism:** `background: var(--glass); backdrop-filter: blur(var(--blur-glass)); border: 1px solid var(--glass-line); border-radius: var(--radius-lg)`. Solo en paneles que flotan sobre contenido (tablero, modales, KPI); nunca en texto largo.
- **Glow neón:** `glow-cyber` y `glow-quantum` son estados, no decoración: aparecen en hover, foco o selección y desaparecen al resolverse.
- **Volumen 3D:** `elev-3d` + `perspective: 1200px` solo en flashcards y modales.
- **Movimiento:** 150–200 ms en hover; 600 ms en el volteo de la flashcard. Respetar `prefers-reduced-motion`.
- **Evitar:** degradados violeta-azul de fondo, texto con glow, más de un elemento brillando a la vez.

### Iconografía
Iconos de trazo (estilo Lucide, 1.8 px, esquinas redondeadas), en `currentColor` del contexto. Tamaños 16/20/24. Sin emojis en la interfaz ni en insignias.

### Accesibilidad
Texto ≥4.5:1 en ambos temas; bordes de control e iconos ≥3:1. El estado nunca depende solo del color: acierto/fallo, retención y riesgo siempre llevan palabra.

---

## 3. Mapa de este sistema
- **Sistema de Skills** (sección siguiente): rutas NIST NICE, insignias Kirkpatrick y visualización SM-2.
- **Componentes:** Button, CanonicalTerm, Flashcard3D, SM2Rating, RetentionMeter, QuizOption, MasteryBadge, TrackCard, KPICard. Todo el CSS vive en `components/bundle.css` y lee solo variables de `tokens.css`.
