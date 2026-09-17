# 🏆 Entregables Oficiales — Plataforma No Country (Hackathon ONE G10)
**Proyecto:** NuevaMente — Plataforma Inteligente de Adaptación Pedagógica de Documentación Técnica  
**Project Manager & Coordinador General:** Martin Morfe  
**Repositorio Oficial:** [https://github.com/mmorfe-engineer/nuevamente_g10_latam](https://github.com/mmorfe-engineer/nuevamente_g10_latam)  
**Infraestructura:** Oracle Cloud Infrastructure (OCI) Always Free ($0.00 USD)

---

Este documento contiene los textos, especificaciones y enlaces listos para ser copiados y pegados directamente por el PM (**Martin Morfe**) en los formularios de entrega de la plataforma No Country.

---

## 📋 TAREA 1: Documentación del Proyecto

### 📌 Formato para el Formulario de la Plataforma
*(Copiar y pegar en la caja de texto o campo Markdown de la Tarea 1)*

```markdown
# NuevaMente — Adaptación Pedagógica Inteligente de Documentación Técnica

## 1. Propuesta de Valor y Problema
En la industria tecnológica y EdTech, la documentación de arquitectura, redes e infraestructura crece a un ritmo acelerado y suele ser densa y abstracta. Adaptar manualmente este contenido a diferentes perfiles (desde principiantes hasta directores) requiere semanas de trabajo instruccional.
**NuevaMente** resuelve este cuello de botella transformando cualquier documento técnico (PDF, Markdown o Texto plano) en contenidos educativos interactivos y personalizados (Flashcards 3D, Quizzes con retroalimentación inmediata, Guías Prácticas y Resúmenes Ejecutivos) en menos de 10 segundos, con 0% de costo de infraestructura y 100% de anclaje a fuentes verificables.

## 2. Arquitectura de la Solución (RAG + Multi-Agente + OCI Always Free + Neon PostgreSQL)
- **Capa 1: Ingestión Multiformato y Corpus Normativo:** Ingestión y procesamiento de 7 documentos canónicos (1,132 páginas) en 3,020 chunks con síntesis bilingüe LexForja, deduplicación por hash SHA-256 y glosario de términos canónicos (`src/ingestion/`).
- **Capa 2: Vector Store & Retrieval:** ChromaDB persistente en disco con embeddings semánticos `all-MiniLM-L6-v2`, 3,018 fragmentos indexados y cálculo de *Grounding Score* (>85% anclaje verificable a la fuente técnica).
- **Capa 3: Persistencia Híbrida Cloud & Local:** Doble capa de datos: SQLite WAL local para latencia cero + Neon Serverless PostgreSQL 18.6 sincronizado por HTTPS + buckets de Oracle Cloud Infrastructure Object Storage (`nuevamente-documentos-origen` y `nuevamente-contenidos-educativos`) bajo el umbral estricto de $0.00 USD.
- **Capa 4: Orquestación Generativa y Multi-Agente:** Compatibilidad y fallback automático con **NVIDIA NIM (DeepSeek v4)**, **Mistral AI (`mistral-small-latest`)** y **Google Gemini**, gobernados por contratos estrictos Pydantic v2 y orquestación multi-agente con **LangGraph** (Investigador RAG -> Redactor Pedagógico -> Crítico Pedagógico).
- **Capa 5: Frontend Design System Dark Enterprise:** UI construida en Streamlit con tokens y CSS del Design System oficial de NuevaMente: 4 TrackCards NIST NICE, Flashcards con perspectiva 3D interactiva, barra de calificación SuperMemo SM-2 de 6 grados, quizzes con citas verificables, glosario canónico parentético (*Término [Canonical English]*) y tablero PMO.

## 3. Diferenciales de Alto Impacto
1. **Algoritmo de Repetición Espaciada (SuperMemo SM-2):** Cálculo científico del Factor de Facilidad (EF), intervalos y días para el próximo repaso según las calificaciones del usuario (0 a 5).
2. **Orquestación Multi-Agente con LangGraph:** Sistema colegiado con traza visual paso a paso que investiga, redacta y somete a crítica de calidad el contenido generado.
3. **Corpus Real Ingerido:** 1,132 páginas de normativas reales (NIST SP 800-53, CIS OCI Benchmark, PCI-DSS v4.0, ISO/IEC 27001, OWASP Top 10) transformadas en micro-aprendizajes interactivos.
4. **Nomenclatura Canónica Auditada:** Regla parentética estricta para evitar discrepancias de traducción técnica en exámenes internacionales y auditorías.
5. **Arquitectura $0.00 USD de por vida:** Despliegue en OCI Always Free y Neon PostgreSQL Free Tier.

## 4. Enlaces de Documentación Completa
- Documento de Iniciación PRINCE2 (PID / Living Document): [docs/tarea1_documentacion.md](https://github.com/mmorfe-engineer/nuevamente_g10_latam/blob/main/docs/tarea1_documentacion.md)
- Estructura Desglosada de Trabajo (EDT 5 Sprints): [docs/EDT_PLAN_DE_TRABAJO_5_SPRINTS.md](https://github.com/mmorfe-engineer/nuevamente_g10_latam/blob/main/docs/EDT_PLAN_DE_TRABAJO_5_SPRINTS.md)
- Arquitectura OCI Always Free: [deploy/OCI_ALWAYS_FREE_ARCHITECTURE.md](https://github.com/mmorfe-engineer/nuevamente_g10_latam/blob/main/deploy/OCI_ALWAYS_FREE_ARCHITECTURE.md)
```

---

## 🎬 TAREA 2: Video Demo del Proyecto

- **Formato Requerido:** Enlace de YouTube (Duración: 2:30 a 3:00 min máximo).
- **Guion Técnico Paso a Paso:** Disponible íntegro en [`docs/GUION_VIDEO_DEMO_3_MINUTOS.md`](https://github.com/mmorfe-engineer/nuevamente_g10_latam/blob/main/docs/GUION_VIDEO_DEMO_3_MINUTOS.md).
- **Estructura del Video para Grabación:**
  1. `0:00 - 0:30`: Presentación del problema, Squad y propuesta de valor de NuevaMente ("Normativa densa, mente nueva").
  2. `0:30 - 1:15`: Carga de documento técnico y persistencia en Neon PostgreSQL 18 y OCI Object Storage.
  3. `1:15 - 2:00`: Ejecución del motor con LangGraph Multi-Agente (DeepSeek v4 / Mistral AI) y cálculo de Repetición Espaciada SM-2.
  4. `2:00 - 2:30`: Interacción con Flashcards 3D en el Design System oficial, evaluación de Quiz con citas verificadas y exportación a Anki (.csv).
  5. `2:30 - 3:00`: Tablero PMO, validación de costo $0.00 en OCI/Neon y cierre de impacto.

*Nota para el PM:* Al finalizar la grabación y subida a YouTube, colocar la URL pública aquí:
`https://www.youtube.com/watch?v=PENDIENTE_SUBIDA_YOUTUBE`

---

## 🛠️ TAREA 3: Herramientas y Tecnologías del Equipo

Seleccionar y registrar las siguientes tecnologías en el formulario de la plataforma:

### 🧠 Inteligencia Artificial y RAG
- **NVIDIA NIM API** (Modelo `deepseek-ai/deepseek-v4-flash-0731` con razonamiento profundo)
- **Mistral AI API** (`mistral-small-latest` para síntesis andragógica de baja latencia)
- **Google Gemini API** (Modelo `gemini-1.5-flash`)
- **LangGraph** (Orquestación del ciclo multi-agente: Investigador, Redactor, Crítico)
- **ChromaDB** (Almacén vectorial local persistente para indexación semántica)
- **Sentence Transformers** (Modelo de embeddings `all-MiniLM-L6-v2`)
- **Pydantic v2** (Validación estricta de esquemas y contratos de datos JSON)
- **PyPDF / PyMuPDF** (Extractores de documentos PDF y Markdown)

### ☁️ Cloud & Persistencia (Always Free)
- **Oracle Cloud Infrastructure (OCI) Always Free** (Capa de costo $0.00 permanente)
- **Neon Serverless PostgreSQL 18.6** (Base de datos relacional serverless sincronizada por HTTPS)
- **OCI Object Storage** (Buckets: `nuevamente-documentos-origen` y `nuevamente-contenidos-educativos`)
- **OCI Compute Ampere A1 Flex** (4 OCPUs Arm, 24 GB RAM para alojamiento de microservicios)
- **OCI Python SDK (`oci`)** (Integración programática con signing keys RSA)
- **SQLite 3 WAL** (Persistencia relacional local de ultra baja latencia)

### 💻 Frontend & Experiencia de Usuario
- **Streamlit** (Framework interactivo Python para aplicaciones de datos e IA)
- **NuevaMente Design System** (Tokens CSS Dark Enterprise: `#070B14`, `#7456F7`, `#22E4F2`, `#C74634`)
- **CSS3 3D Transforms** (Flashcards 3D con perspectiva e interacción de volteo)
- **SuperMemo SM-2 Rating Bar** (Controles de retención mnemotécnica de 6 grados)

### ⚙️ DevOps, Calidad & Metodología
- **Python 3.11**
- **Pytest** (34 tests automatizados pasando al 100% con aislamiento en memoria)
- **Git & GitHub** (Flujo de ramas, commits convencionales y auditoría estricta)
- **PRINCE2 Agile & Scrum** (Tablero WBS en 5 Sprints, gestión de tolerancias)

---

## 🔗 TAREA 4: Enlaces del Proyecto

Copiar y pegar los siguientes enlaces directos:

1. **Repositorio Oficial en GitHub:**  
   `https://github.com/mmorfe-engineer/nuevamente_g10_latam`
2. **Documentación Oficial del Proyecto (PRINCE2):**  
   `https://github.com/mmorfe-engineer/nuevamente_g10_latam/blob/main/docs/tarea1_documentacion.md`
3. **Plan de Trabajo y WBS (5 Sprints):**  
   `https://github.com/mmorfe-engineer/nuevamente_g10_latam/blob/main/docs/EDT_PLAN_DE_TRABAJO_5_SPRINTS.md`
4. **Guion Oficial del Video Demo (3 min):**  
   `https://github.com/mmorfe-engineer/nuevamente_g10_latam/blob/main/docs/GUION_VIDEO_DEMO_3_MINUTOS.md`
5. **Especificación de Arquitectura OCI Always Free:**  
   `https://github.com/mmorfe-engineer/nuevamente_g10_latam/blob/main/deploy/OCI_ALWAYS_FREE_ARCHITECTURE.md`
6. **Enlace al Video Demo de YouTube:**  
   `https://www.youtube.com/watch?v=PENDIENTE_SUBIDA_YOUTUBE` *(Actualizar tras grabar)*

