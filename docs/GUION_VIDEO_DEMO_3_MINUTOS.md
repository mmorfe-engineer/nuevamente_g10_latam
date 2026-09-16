# Guion Oficial del Video Demo (3 Minutos) — Proyecto NuevaMente
## Hackathon ONE G10 (Oracle Next Education & Alura / No Country)
**Tiempo Total Estimado:** 3 minutos exactos (180 segundos)  
**Resolución de Grabación:** 1080p Full HD (60 fps)  
**Tono:** Profesional, dinámico, enfocado en impacto EdTech y suficiencia técnica en Oracle Cloud Infrastructure (OCI).

---

## 🎬 Estructura del Video por Bloques

```text
===================================================================================================
[00:00 - 00:30] BLOQUE 1: El Desafío EdTech y la Propuesta de Valor de NuevaMente
[00:30 - 01:10] BLOQUE 2: Ingestión Técnica, Deduplicación SHA-256 y Persistencia en OCI Object Storage
[01:10 - 01:50] BLOQUE 3: Pipeline RAG en ChromaDB y Adaptación Pedagógica con Gemini 1.5 Flash
[01:50 - 02:30] BLOQUE 4: Experiencia "Deep Dev": Flashcards 3D con SM-2, Quizzes y Exportación Anki
[02:30 - 03:00] BLOQUE 5: Arquitectura Always Free, Tablero PMO y Cierre de Impacto
===================================================================================================
```

---

### [00:00 - 00:30] BLOQUE 1: El Desafío EdTech y la Propuesta de Valor
- **Toma en Pantalla:** Primer plano del presentador con overlay gráfico del título *"NuevaMente · Sistema Inteligente de Adaptación Educativa"*, seguido de una transición rápida hacia la interfaz Cyber-Modern de NuevaMente en `localhost:8501`.
- **Locución del Narrador:**
  > *"¿Sabías que un equipo de ingeniería y diseño instruccional tarda hasta tres semanas en transformar un manual técnico de 50 páginas en material didáctico efectivo? En un mundo donde la nube y el software evolucionan a diario, la educación técnica no puede permitirse ese retraso.*
  > 
  > *Bienvenidos a **NuevaMente**, la plataforma SaaS EdTech desarrollada para el Hackathon ONE Grupo 10. Con NuevaMente, ingerimos cualquier documentación técnica densa y, en cuestión de segundos, la transformamos en experiencias de aprendizaje personalizadas para cuatro audiencias distintas, garantizando fidelidad técnica y cero alucinaciones mediante RAG anclado en Oracle Cloud Infrastructure."*

---

### [00:30 - 01:10] BLOQUE 2: Ingestión, Hash SHA-256 y Persistencia en OCI Always Free
- **Toma en Pantalla:** Puntero del ratón seleccionando en la barra lateral el *"Escenario 1: Redes VCN en OCI"*. Muestra del texto técnico original y clic en *"⚡ Generar Adaptación Pedagógica"*. Transición a la consola de OCI o pestaña de Persistencia mostrando los dos buckets: `nuevamente-documentos-origen` y `nuevamente-contenidos-educativos`.
- **Locución del Narrador:**
  > *"Observemos el flujo en acción. Seleccionamos una documentación oficial sobre Arquitectura de Redes VCN en OCI. Al procesarlo, nuestro motor ejecuta tres acciones clave de infraestructura:*
  > 
  > *Primero: extrae y sanitiza el contenido, calculando un hash criptográfico SHA-256 para evitar duplicidad de procesamiento en nuestra base de datos relacional.*
  > 
  > *Segundo: persiste de forma inmediata el documento fuente original en nuestro bucket 'nuevamente-documentos-origen' dentro de la capa OCI Object Storage Always Free, asegurando trazabilidad y cumplimiento normativo.*
  > 
  > *Tercero: segmenta el documento en fragmentos contextuales de 1000 caracteres con solapamiento, listos para la indexación vectorial."*

---

### [01:10 - 01:50] BLOQUE 3: Pipeline RAG en ChromaDB y Orquestación con Gemini 1.5 Flash
- **Toma en Pantalla:** Pestaña *"Métricas & Grounding RAG"*. Muestra de la métrica de anclaje (98%), barra de progreso verde, ausencia de alucinación y selección del perfil *"Principiante"* vs *"Líder Técnico / Arquitecto"*.
- **Locución del Narrador:**
  > *"Aquí es donde ocurre la magia de la IA Generativa responsable. Los fragmentos se indexan en nuestro Vector Store ChromaDB utilizando embeddings de alta densidad. Cuando el usuario solicita adaptar el contenido para un perfil 'Principiante', nuestro orquestador enruta la consulta recuperando los chunks más relevantes por similitud coseno.*
  > 
  > *Google Gemini 1.5 Flash recibe un system prompt pedagógico fundamentado en la Taxonomía de Bloom. En lugar de conceptos áridos, genera analogías cotidianas: la VCN se explica como un vecindario privado y las Security Lists como guardias de acceso.*
  > 
  > *Y lo más importante: nuestro evaluador de calidad certifica un score de anclaje a la fuente del 98%, garantizando que no existe inventiva ni alucinación."*

---

### [01:50 - 02:30] BLOQUE 4: Experiencia "Deep Dev": Flashcards 3D con SM-2, Quizzes y Anki
- **Toma en Pantalla:** Pestaña *"Contenido Pedagógico Adaptado"*. El cursor pasa sobre las flashcards mostrando el volteo interactivo 3D. El usuario presiona el botón *"🟢 Fácil"* y aparece la notificación con el cálculo SM-2 (+6 días de intervalo). Luego se navega hacia el Quiz interactivo, seleccionando una opción y recibiendo el resplandor neón verde con la justificación técnica. Finaliza mostrando el botón *"🗃️ Exportar a Anki (.csv)"*.
- **Locución del Narrador:**
  > *"La interfaz fue diseñada con una estética 'Deep Dev / Cyber-Modern' en paleta oscura y glassmorphism. Cero aspecto de plantilla genérica.*
  > 
  > *Las Flashcards cuentan con efecto de giro 3D en tiempo real e integran el algoritmo científico de repetición espaciada SuperMemo SM-2. Al calificar nuestra asimilación, el sistema recalcula en la base de datos la próxima fecha óptima de repaso.*
  > 
  > *En el visor de Quizzes, el estudiante recibe retroalimentación visual instantánea con justificación anclada a la fuente y nivel taxonómico de Bloom.*
  > 
  > *Y como diferencial pedagógico: un botón de exportación en un clic hacia Anki CSV y guías didácticas en Markdown estructurado."*

---

### [02:30 - 03:00] BLOQUE 5: Arquitectura Always Free, Tablero PMO y Cierre
- **Toma en Pantalla:** Clic en la pestaña *"🏢 Oficina de Proyecto (PMO & WBS)"*. Muestra de los KPIs de proyecto (88% WBS, 26 tests pasando, costo OCI: $0.00 USD), seguido de la terminal ejecutando `pytest tests/ -v` con 26/26 tests verdes. Placa final con los nombres del equipo y logo de Oracle Next Education.
- **Locución del Narrador:**
  > *"Detrás de esta solución existe una arquitectura de ingeniería rigurosa en 6 capas, respaldada por un Tablero PMO integrado que monitorea el avance del WBS en 5 Sprints bajo metodología PRINCE2 y Scrum.*
  > 
  > *El 100% de la plataforma corre sobre una instancia Ampere A1 de OCI Compute con 4 OCPUs y 24 GB de RAM, con un costo mensual certificado de exactamente CERO dólares.*
  > 
  > *Con 26 pruebas unitarias y de integración automatizadas al 100%, NuevaMente democratiza y acelera la educación técnica en América Latina. Somos el equipo NuevaMente para el Hackathon ONE G10. ¡Muchas gracias!"*

---

## 📋 Lista de Verificación para la Grabación (Checklist)
- [ ] Resolución de pantalla configurada en 1920x1080 (100% DPI scaling).
- [ ] Servidor local activo en `http://localhost:8501`.
- [ ] Base de datos poblada con al menos 1 escenario generado para mostrar biblioteca.
- [ ] Micrófono limpio sin eco de sala.
- [ ] Terminal lista con el comando `venv/bin/pytest tests/ -v`.
- [ ] Exportación en formato MP4 (H.264 / AAC) a 1080p60 para subida a YouTube.
