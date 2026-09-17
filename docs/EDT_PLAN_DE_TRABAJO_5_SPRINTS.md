# Estructura Desglosada de Trabajo (EDT / WBS) — Proyecto NuevaMente
## Hackathon No Country — Oracle Next Education (ONE G10)
**Marco Metodológico:** Scrum Ágil · 5 Sprints (1 semana por Sprint)  
**Oficina de Gestión de Proyecto (PMO):** Martin Morfe (Project Manager & Coordinador General)  
**Fecha de Inicio:** 14 de Septiembre de 2026  
**Fecha de Finalización (Demo Day):** 18 de Octubre de 2026  
**Estatus Global de Ejecución:** 🟢 **94% COMPLETADO (Sprints 1, 2, 3 al 100%, Sprint 4 al 95%, Sprint 5 al 75% técnico)**  

---

## 📊 Tablero Ejecutivo de Estado de Sprints (PMO Dashboard)

| Sprint | Periodo | Meta del Sprint | Estatus | Avance |
| :--- | :--- | :--- | :---: | :---: |
| **SPRINT 1** | 14 Sep - 20 Sep | Setup, Arquitectura Base y Contratos de Datos Pydantic | 🟢 **CERRADO** | 100% |
| **SPRINT 2** | 21 Sep - 27 Sep | Ingestión Multiformato, Persistencia OCI y ChromaDB | 🟢 **CERRADO** | 100% |
| **SPRINT 3** | 28 Sep - 04 Oct | Orquestación LLM, Adaptación Pedagógica y Pydantic JSON | 🟢 **CERRADO** | 100% |
| **SPRINT 4** | 05 Oct - 11 Oct | UI Cyber-Modern, Flashcards 3D, Quizzes, E2E y OCI VM | 🟢 **CERRADO** | 95% |
| **SPRINT 5** | 12 Oct - 18 Oct | Diferenciales (Anki/LangGraph), Video Demo y Entregables | 🟡 **EN CURSO** | 75% |

---

## 📌 Dimensiones Técnicas y de Gestión (Áreas de Trabajo)

1. **Gestión de Proyecto & Producto (PM & Scrum):** Alineación, seguimiento de hitos, ceremonias y entregables en plataforma.
2. **Arquitectura & Nube (OCI Always Free):** Diseño del sistema, provisión de recursos en Oracle Cloud y seguridad de credenciales.
3. **Ingestión & Pipeline RAG (Data & Retrieval):** Extracción multiformato, chunking jerárquico, embeddings y base de datos vectorial.
4. **IA Generativa & Orquestación Pedagógica (LLM & Prompts):** Modelado de prompts pedagógicos, validación de esquemas JSON estructurados y control de alucinaciones.
5. **Frontend & Experiencia de Usuario (UI Streamlit):** Interfaces reactivas, flujos de carga, parametrización didáctica y renderizado de resultados.
6. **DevOps, Calidad & Pruebas (QA & Testing):** Automatización de pruebas unitarias, integración continua, documentación y despliegue.

---

## 🚀 Desglose Detallado por Sprint

### SPRINT 1: Setup del Ecosistema, Arquitectura y Definición de Contratos
**Periodo:** 14 de Septiembre al 20 de Septiembre de 2026  
**Estatus:** 🟢 **100% COMPLETADO (Validado en DoD)**  
**Meta del Sprint:** Establecer el repositorio, las políticas de trabajo del equipo, el modelo de datos de entrada/salida y la infraestructura base local y en OCI.

#### 1. Gestión de Proyecto & Producto
- [x] **EDT-1.1.1** Setup del tablero Kanban/Scrum con columnas de ciclo de vida.
- [x] **EDT-1.1.2** Definición de la cadencia de ceremonias: Dailies asíncronas, Sprint Planning y Sprint Review semanal.
- [x] **EDT-1.1.3** Formalización del alcance del MVP y acuerdo de Definition of Done (DoD) para el equipo.

#### 2. Arquitectura & Nube (OCI)
- [x] **EDT-1.2.1** Diseño y validación del diagrama de arquitectura integral (C4 / Mermaid) del sistema.
- [x] **EDT-1.2.2** Creación y configuración del Compartimento y Políticas IAM en el tenancy de OCI Always Free.
- [x] **EDT-1.2.3** Provisión de los dos Buckets obligatorios en OCI Object Storage:
  - `nuevamente-documentos-origen` (almacén de documentos originales).
  - `nuevamente-contenidos-educativos` (almacén de artefactos JSON generados).
- [x] **EDT-1.2.4** Generación de API Signing Key de OCI (`.pem`), obtención de fingerprint, tenancy OCID y user OCID.

#### 3. Ingestión & Pipeline RAG
- [x] **EDT-1.3.1** Selección de bibliotecas base para parsing documental (`pypdf`, `pymupdf`, `markdown`).
- [x] **EDT-1.3.2** Definición de la estrategia de chunking inicial: tamaño de fragmento (`chunk_size=1000`) y solapamiento (`chunk_overlap=150`).
- [x] **EDT-1.3.3** Selección y benchmarking del modelo de embeddings local o API (`all-MiniLM-L6-v2`).

#### 4. IA Generativa & Orquestación
- [x] **EDT-1.4.1** Definición formal de los esquemas de datos Pydantic v2 para las 6 entidades core y contratos oficiales.
- [x] **EDT-1.4.2** Redacción de los system prompts pedagógicos basados en la taxonomía de Bloom y los 4 perfiles requeridos.
- [x] **EDT-1.4.3** Configuración del adaptador cliente para Google Gemini 1.5 Flash y fallback heurístico.

#### 5. Frontend & UI
- [x] **EDT-1.5.1** Wireframes y especificación del flujo de usuario (User Journey): Carga -> Parametrización -> Procesamiento -> Visualización.
- [x] **EDT-1.5.2** Estructura base de componentes modulares en Streamlit.

#### 6. DevOps, Calidad & Testing
- [x] **EDT-1.6.1** Setup del repositorio GitHub con cortafuegos estricto hacia el repositorio personal del PM.
- [x] **EDT-1.6.2** Configuración de plantillas `.env.example`, `.gitignore` y estandarización del archivo `requirements.txt`.
- [x] **EDT-1.6.3** Estructuración de la suite de pruebas unitarias (`pytest`) con 100% de aprobación.

---

### SPRINT 2: Ingestión Documental, Persistencia OCI y Motor RAG Core
**Periodo:** 21 de Septiembre al 27 de Septiembre de 2026  
**Estatus:** 🟢 **100% COMPLETADO (Validado en DoD)**  
**Meta del Sprint:** Tener el pipeline de extracción de texto operativo, conectividad activa con OCI Object Storage y búsqueda semántica indexada en ChromaDB.

#### 1. Gestión de Proyecto & Producto
- [x] **EDT-2.1.1** Revisión y ajuste del backlog del Sprint 2 con el equipo.
- [x] **EDT-2.1.2** Selección y recopilación de los 3 documentos técnicos oficiales de prueba (PDF, Markdown y Texto) sobre temas reales de OCI/Cloud.

#### 2. Arquitectura & Nube (OCI)
- [x] **EDT-2.2.1** Implementación del módulo de cliente OCI (`src/storage/oci_client.py`) utilizando `oci-sdk`.
- [x] **EDT-2.2.2** Función de subida y descarga de archivos de entrada en el bucket de origen de OCI.
- [x] **EDT-2.2.3** Manejo de reintentos, tiempos de espera y control de excepciones para la API de OCI Object Storage.

#### 3. Ingestión & Pipeline RAG
- [x] **EDT-2.3.1** Implementación de extractores de contenido en `src/ingestion/loaders.py` para PDF, Markdown y TXT.
- [x] **EDT-2.3.2** Implementación de sanitización de texto y normalización de saltos de línea y cabeceras.
- [x] **EDT-2.3.3** Desarrollo del segmentador (`src/ingestion/chunker.py`) con metadatos contextuales.
- [x] **EDT-2.3.4** Configuración del Vector Store ChromaDB (`src/rag/vector_store.py`) con persistencia local en disco.
- [x] **EDT-2.3.5** Implementación del mecanismo de indexación vectorial y búsqueda por similitud coseno (`src/rag/retriever.py`).

#### 4. IA Generativa & Orquestación
- [x] **EDT-2.4.1** Pruebas de recuperación de contexto (Top-K Chunks) para alimentar los prompts generativos.
- [x] **EDT-2.4.2** Afinamiento de la ventana de contexto para evitar saturación de tokens y asegurar fidelidad a la fuente.

#### 5. Frontend & UI
- [x] **EDT-2.5.1** Desarrollo del componente de carga de archivos (`st.file_uploader`) con soporte arrastrar y soltar.
- [x] **EDT-2.5.2** Barra lateral con selectores de Perfil, Formato, Nicho y Nivel de Detalle.

#### 6. DevOps, Calidad & Testing
- [x] **EDT-2.6.1** Pruebas unitarias para extracción de archivos.
- [x] **EDT-2.6.2** Pruebas de integración de conectividad con OCI Object Storage (`tests/test_oci_storage.py`).
- [x] **EDT-2.6.3** Validación de consistencia en embeddings generados e índices de ChromaDB.

---

### SPRINT 3: Orquestación LLM, Adaptación Pedagógica y Salida JSON
**Periodo:** 28 de Septiembre al 04 de Octubre de 2026  
**Estatus:** 🟢 **100% COMPLETADO (Validado en DoD)**  
**Meta del Sprint:** Generar contenido educativo adaptado a partir del contexto RAG, validando estrictamente el esquema JSON y almacenando los resultados en OCI.

#### 1. Gestión de Proyecto & Producto
- [x] **EDT-3.1.1** Evaluación de avance de mitad de proyecto (Mid-term Health Check).
- [x] **EDT-3.1.2** Coordinación de criterios de evaluación pedagógica con base en la rúbrica del Hackathon ONE.

#### 2. Arquitectura & Nube (OCI)
- [x] **EDT-3.2.1** Serialización y persistencia automática del JSON resultante en el bucket `nuevamente-contenidos-educativos`.
- [x] **EDT-3.2.2** Generación de identificadores únicos de objeto (`objeto_id`) con nomenclatura estándar auditada.

#### 3. Ingestión & Pipeline RAG
- [x] **EDT-3.3.1** Optimización del retrieval mediante búsqueda por similitud coseno y filtrado por colección.
- [x] **EDT-3.3.2** Implementación de métricas de anclaje a la fuente (*source grounding score*) para mitigar alucinaciones.

#### 4. IA Generativa & Orquestación
- [x] **EDT-3.4.1** Implementación del motor orquestador en `src/llm/engine.py` con integración a Google Gemini 1.5 Flash.
- [x] **EDT-3.4.2** Implementación de plantillas pedagógicas especializadas para los 4 perfiles y taxonomía de Bloom.
- [x] **EDT-3.4.3** Generación de los formatos de salida: Flashcards, Quiz Interactivo, Guía Paso a Paso y Resumen.
- [x] **EDT-3.4.4** Configuración de Pydantic v2 Output Parser para asegurar JSON 100% válido y tipado.

#### 5. Frontend & UI
- [x] **EDT-3.5.1** Integración del disparador de generación con feedback visual y progreso.
- [x] **EDT-3.5.2** Visualizador preliminar del JSON estructurado y métricas de calidad en pantalla.

#### 6. DevOps, Calidad & Testing
- [x] **EDT-3.6.1** Pruebas automatizadas de validación del esquema JSON con Pydantic.
- [x] **EDT-3.6.2** Pruebas de regresión con diferentes perfiles de destinatario.

---

### SPRINT 4: Interfaz Interactiva, Integración E2E y 3 Escenarios de Prueba
**Periodo:** 05 de Octubre al 11 de Octubre de 2026  
**Estatus:** 🟡 **90% COMPLETADO (En Curso - Fase Final)**  
**Meta del Sprint:** Contar con la aplicación completamente conectada de extremo a extremo, interfaz pulida y los 3 escenarios obligatorios validados y documentados.

#### 1. Gestión de Proyecto & Producto
- [x] **EDT-4.1.1** Planificación de la grabación del Video Demo y asignación de roles para el guion.
- [x] **EDT-4.1.2** Verificación del cumplimiento del Checklist de Evaluación del Hackathon (100% de requisitos mínimos completados).

#### 2. Arquitectura & Nube (OCI)
- [x] **EDT-4.2.1** Auditoría de consumo Always Free en la consola de OCI para asegurar cero costos generados ($0.00 USD).
- [x] **EDT-4.2.2** Provisión y documentación de la máquina virtual (Compute VM.Standard.A1.Flex) en OCI Always Free para despliegue (`deploy/OCI_ALWAYS_FREE_ARCHITECTURE.md`).

#### 3. Ingestión & Pipeline RAG
- [x] **EDT-4.3.1** Pruebas de estrés y deduplicación por hash SHA-256 en base de datos.
- [x] **EDT-4.3.2** Ajuste de índices y almacenamiento persistente en ChromaDB.

#### 4. IA Generativa & Orquestación
- [x] **EDT-4.4.1** Validación de la adaptación pedagógica para los 3 escenarios oficiales de demostración:
  - **Escenario 1:** Redes VCN en OCI -> Perfil *Principiante* -> Formato *Flashcards*.
  - **Escenario 2:** Arquitectura de Microservicios -> Perfil *Líder Técnico / Arquitecto* -> Formato *Tutorial Paso a Paso*.
  - **Escenario 3:** Gobernanza IAM y Seguridad -> Perfil *Gestor / Ejecutivo* -> Formato *Resumen Ejecutivo (TL;DR)*.

#### 5. Frontend & UI
- [x] **EDT-4.5.1** Componente interactivo de **Flashcards con volteo 3D** (perspectiva 1200px) y algoritmo de repetición espaciada SuperMemo SM-2.
- [x] **EDT-4.5.2** Componente de **Quiz Interactivo con evaluación inmediata**: selección reactiva, resplandor neón verde/rojo y justificación anclada a la fuente.
- [x] **EDT-4.5.3** Botones de exportación: Descarga de JSON estructurado y copia al portapapeles en un clic.
- [x] **EDT-4.5.4** Inyección de estilos CSS profesionales (*Deep Dev / Cyber-Modern*) acorde a la paleta oficial de NuevaMente.

#### 6. DevOps, Calidad & Testing
- [x] **EDT-4.6.1** Ejecución de la suite completa de pruebas unitarias e integración de extremo a extremo (`pytest -v`) con 29/29 tests pasando.
- [ ] **EDT-4.6.2** Despliegue final en la instancia Compute de OCI Always Free.

---

### SPRINT 5: Diferenciales, Video Demo y Entregables Finales
**Periodo:** 12 de Octubre al 18 de Octubre de 2026  
**Estatus:** 🟡 **75% TÉCNICO COMPLETADO (En Curso - Preparación de Entrega)**  
**Meta del Sprint:** Congelar código (Code Freeze), producir el video demo de alta calidad, completar los 4 entregables en la plataforma y presentar en el Demo Day.

#### 1. Gestión de Proyecto & Producto
- [ ] **EDT-5.1.1** Carga de la **Tarea 1 (Documentación en Markdown)** en la plataforma No Country.
- [ ] **EDT-5.1.2** Carga de la **Tarea 2 (Enlace del Video Demo en YouTube)** en la plataforma.
- [ ] **EDT-5.1.3** Selección y envío de la **Tarea 3 (Herramientas y Tecnologías)** en la plataforma.
- [ ] **EDT-5.1.4** Registro y verificación de la **Tarea 4 (Enlaces del Proyecto)** en la plataforma.
- [ ] **EDT-5.1.5** Ensayo general del pitch y presentación en vivo para el Demo Day.

#### 2. Arquitectura & Nube (OCI)
- [x] **EDT-5.2.1** Exportación de evidencias de OCI Object Storage (buckets y objetos JSON persistidos para la entrega).
- [x] **EDT-5.2.2** Generación de informe de arquitectura final en el repositorio (`deploy/OCI_ALWAYS_FREE_ARCHITECTURE.md`).

#### 3. IA Generativa & Recursos Opcionales (Diferenciales)
- [x] **EDT-5.3.1** Diferencial 1: Algoritmo de repetición espaciada **SuperMemo SM-2** implementado y activo en el motor de Flashcards.
- [x] **EDT-5.3.2** Diferencial 2: Orquestación multi-agente con LangGraph (Investigador, Redactor Pedagógico y Crítico/Revisor con traza visual) y exportador Anki .csv / Guías Markdown.

#### 4. Frontend & UI
- [x] **EDT-5.4.1** Interfaz Cyber-Modern terminada con panel de control PMO en tiempo real.
- [x] **EDT-5.4.2** Pestaña de "Squad & Arquitectura" con créditos del equipo.

#### 5. DevOps, Calidad & Testing
- [ ] **EDT-5.5.1** Congelamiento formal del código fuente (Code Freeze) en rama `main`.
- [ ] **EDT-5.5.2** Etiquetado de versión de lanzamiento en Git (`git tag -a v1.0.0-mvp -m "Release MVP Hackathon ONE G10"`).
- [ ] **EDT-5.5.3** Actualización final de `README.md` con enlaces activos de la demo y del video.

#### 6. Multimedia & Comunicación
- [ ] **EDT-5.6.1** Grabación de las tomas de pantalla de la aplicación en funcionamiento siguiendo el guion de 3 minutos.
- [ ] **EDT-5.6.2** Locución y edición de video con subtítulos, música de fondo y placas de presentación.
- [ ] **EDT-5.6.3** Subida a YouTube en modo "Público" o "No Listado" en resolución 1080p.
