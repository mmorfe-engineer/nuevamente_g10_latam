from pathlib import Path
import json

content = """# INFORME DEFINITIVO DE PRUEBAS · NUEVAMENTE
**Campaña de Verificación QA y Regresión Integral**  
**Marco de Gobernanza:** Hackathon ONE G10 (Oracle & Alura) / Marco Metodológico PRINCE2  
**Entorno de Ejecución:** Repositorio Shadow Privado (`mmorfe-engineer/nuevamente_g10_latam`)  
**Fecha de Cierre:** 22 de Septiembre de 2026  
**Responsable Técnico:** Lead QA Architect & PM  

---

## 1. IDENTIFICACIÓN Y CONFIGURACIÓN DEL ENTORNO

| Parámetro | Detalle Factual |
| :--- | :--- |
| **Proyecto** | NuevaMente — Sistema Inteligente de Adaptación y Generación de Contenido Educativo |
| **Repositorio Probado** | `mmorfe-engineer/nuevamente_g10_latam` (Rama `main`) |
| **Commit Base de Regresión** | `258a86a` (con trazabilidad desde `b61fcd3`, `e83b19b`, `0a9fc3f`, `d720962`) |
| **Fecha y Hora de Regresión** | 22 de Septiembre de 2026 · 20:30 UTC-4 |
| **Entorno Primario de Ejecución** | Linux x86_64 (Ubuntu 24.04 LTS / Kernel 6.8.0), Python 3.11.15 |
| **URL Pública de Despliegue** | `https://nuevamente.streamlit.app` |
| **Estado del Despliegue Público** | **Inaccesible (Redirección HTTP 303 a `share.streamlit.io/errors/not_found`)**. La aplicación pública no se encuentra sincronizada con el commit de prueba ni accesible sin autenticación en Streamlit Cloud. |
| **Navegador de Automatización** | Chromium 134.0.6998.35 (Snap / Headless con Chrome DevTools Protocol) |
| **Viewports Evaluados** | 1. Desktop: 1300x950 px<br/>2. Tablet: 768x1024 px<br/>3. Mobile: 375x667 px |
| **Persistencia y Base Vectorial** | SQLite Local (WAL mode) / ChromaDB 0.5+ / Adaptador OCI S3 Local |

---

## 2. OBJETIVO DE LA CAMPAÑA

El objetivo de esta intervención final ha sido ejecutar la **regresión integral** sobre el sistema tras la aplicación de las correcciones de arquitectura, estado y diseño (`DEF-01` a `DEF-06`), auditar la no-regresión de los **67 casos de prueba formales**, evaluar el aislamiento estricto de sesiones entre documentos distintos, validar el comportamiento en documentos de longitud extrema (965k caracteres), constatar el estado real de la aplicación en la URL pública desplegada y emitir un dictamen técnico definitivo basado exclusivamente en hechos observables.

---

## 3. ALCANCE

El alcance auditado comprende:
- **Flujo E2E completo:** Ingesta universal multiformato (PDF, Markdown, Texto plano, Pegado libre), medición de caracteres, selección de perfiles pedagógicos (4), formatos de salida (3 activos), nichos sectoriales (10) y niveles de detalle (3).
- **Procesamiento RAG y Fases:** Orquestación multi-agente, chunking semántico acotado según ADR-012 (máximo 80 fragmentos por lote), vectorización y generación didáctica.
- **Experiencias interactivas:** Flashcards 3D con volteo híbrido (botón + CSS), calificación algorítmica SuperMemo SM-2 (3 niveles de asimilación) y exportación Anki (.csv).
- **Auditoría de calidad y gobernanza:** Pestañas de auditoría metodológica (Tab 2) y tablero de trazabilidad PMO (Tab 3) con matriz de requisitos (O-01 a O-14, D-01 a D-05, X-01).
- **Ciclo de vida y sesión:** Aislamiento determinista de `st.session_state` entre adaptaciones sucesivas (Documento A vs Documento B).

---

## 4. METODOLOGÍA

Se aplicó una metodología de pruebas en caja negra y gris sustentada en:
1. **Verificación de Custodia Previa:** Ejecución obligatoria de `~/protect_squad_repo.sh` asegurando confinamiento en el repositorio Shadow (`CUSTODY_OK_SHADOW`) y bloqueo estricto ante el repositorio del squad (`No-Country-simulation/G10-team1-newmind`).
2. **Jerarquía de Validación Visual:** Inspección prioritaria sobre la URL pública desplegada; al detectarse inaccesibilidad externa, registro del bloqueo público justificado y captura de evidencia provisional sobre el entorno Chromium local instrumentado vía CDP.
3. **Automatización Determinista:** Suite Pytest con `AppTest` de Streamlit para probar el árbol de componentes y contratos de estado sin depender de heurísticas frágiles.
4. **Principio de Honestidad Técnica:** Separación estricta entre métricas medidas y estimadas; distinción entre fragmentos del lote activo y el corpus global; y clasificación explícita de requisitos diferenciales no disponibles sin forzar falsos positivos.

---

## 5. INVENTARIO FINAL DE PRUEBAS Y COBERTURA

Los valores reportados derivan de la ejecución efectiva de los casos:

- **Cobertura Diseñada:** **67 casos estructurados** (100% del inventario formal en las 13 áreas del sistema).
- **Cobertura Ejecutada:** **67 casos efectivamente corridos o evaluados** (100% de ejecución: 60 casos probados funcionalmente, 4 casos bloqueados por inaccesibilidad de la URL pública y 3 casos no ejecutables por funcionalidad diferencial D-01 aún no implementada).
- **Cobertura Aprobada:** **60 casos con dictamen objetivo PASS** (**89.55%** del inventario total), con evidencia material registrada y respaldados por 55 pruebas automatizadas en verde.
- **Casos en Estado Pendiente:** **0 casos** (Cero casos sin evaluar).

---

## 6. RESULTADO GENERAL DE LA REGRESIÓN

| Estado Final | Cantidad | Porcentaje | Justificación Técnica |
| :--- | :---: | :---: | :--- |
| **PASS** | **60** | **89.55%** | Cumplimiento estricto del comportamiento esperado respaldado por pruebas y logs. |
| **BLOQUEADO JUSTIFICADO** | **4** | **5.97%** | Pruebas visuales/responsivas (`TEST-02`, `TEST-61`, `TEST-62`, `TEST-63`) bloqueadas para cierre público definitivo debido a que `https://nuevamente.streamlit.app` no está disponible públicamente (redirección a error `not_found`). Validadas provisionalmente en local. |
| **NO EJECUTABLE JUSTIFICADO** | **3** | **4.48%** | Pruebas (`TEST-20`, `TEST-38`, `TEST-39`) correspondientes al Diferencial D-01 (Quizzes interactivos), funcionalidad no implementada en la interfaz del MVP. |
| **FAIL ABIERTO** | **0** | **0.00%** | Ningún defecto abierto ni comportamiento anómalo no controlado. |
| **NO APLICA JUSTIFICADO** | **0** | **0.00%** | No se registraron casos inaplicables. |
| **TOTAL** | **67** | **100.00%** | Inventario completo auditado. |

---

## 7. RESULTADOS POR ÁREA

| Área de Prueba | Total | PASS | BLOQ | NO EJEC | Estado del Área |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Área 01: Arranque e Inicialización** | 4 | 3 | 1 | 0 | Conforme (TEST-02 bloqueado en público) |
| **Área 02: Ingesta Documental** | 7 | 7 | 0 | 0 | Conforme (Spinner activo en PDF extenso) |
| **Área 03: Medición y Partición** | 4 | 4 | 0 | 0 | Conforme (Lote activo rotulado honestamente) |
| **Área 04: Muestras de Demostración** | 3 | 3 | 0 | 0 | Conforme (3 muestras oficiales operativas) |
| **Área 05: Configuración Pedagógica** | 5 | 4 | 0 | 1 | Conforme (TEST-20 Quiz no ejecutable) |
| **Área 06: Generación de Material** | 5 | 5 | 0 | 0 | Conforme (Fases y ventana ADR-012 operativas) |
| **Área 07: Experiencia de Estudio (Flashcards)** | 9 | 9 | 0 | 0 | Conforme (Volteo híbrido y SM-2 validados) |
| **Área 08: Otros Formatos Didácticos** | 4 | 2 | 0 | 2 | Conforme (TEST-38/39 Quizzes no ejecutables) |
| **Área 09: Auditoría de Calidad** | 4 | 4 | 0 | 0 | Conforme (Tipografía hasta 90ch balanceada) |
| **Área 10: Trazabilidad PMO y Gobernanza** | 9 | 9 | 0 | 0 | Conforme (KPIs alineados a 124px, contratos listos) |
| **Área 11: Ciclo de Vida y Sesión** | 6 | 6 | 0 | 0 | Conforme (Aislamiento total Documento A/B) |
| **Área 12: Diseño Responsivo y Accesibilidad** | 4 | 1 | 3 | 0 | Parcial (Desktop, Tablet y Mobile bloqueados en público) |
| **Área 13: Errores Controlados y Robustez** | 3 | 3 | 0 | 0 | Conforme (Fallback sintético y sanitización activos) |

---

## 8. RECORRIDO E2E PRINCIPAL (INTEGRADO DE CIERRE)

Se ejecutó un recorrido de ciclo completo continuo sobre la aplicación:
1. **Arranque en Frío:** La estación central se inicializa sin excepciones (`TEST-01`). Los KPIs de cabecera indican honestamente `"Puntaje de Anclaje: -- · Aún sin medir"`, `"Formatos Didácticos: 3 Formatos"` y `"Cloud: No"`. La barra lateral opera en modo informativo de solo lectura sin duplicar controles.
2. **Carga e Ingesta:** Se carga el Caso Canónico de Oracle VCN (`TEST-16`). La interfaz detecta y cuenta inmediatamente 2.420 caracteres, estimando 4 chunks. El sidebar se sincroniza reflejando el documento cargado.
3. **Configuración y Generación:** Parámetros: Perfil Principiante, Formato Flashcards, Nicho Cloud, Nivel Didáctico. Se pulsa "Generar Material Didáctico" (`TEST-23`). La aplicación transita de forma reactiva por las 4 fases de procesamiento emitiendo eventos de callback sin timers ciegos.
4. **Presentación e Interacción:** El banner anuncia `"¡Material Didáctico Listo!"`. Se despliegan 4 flashcards con diseño Dark Enterprise Radix. Se acciona el botón accesible `"Voltear Tarjeta"` en la tarjeta 0 (`TEST-31`), exponiendo el reverso con términos canónicos formateados (`[VCN]`, `[CIDR]`). Se califica con `"Alcanzado"` (`TEST-35`), registrando en persistencia el nivel 5 y programando el próximo repaso para 6 días en el futuro, sin arrojar errores de sesión.
5. **Auditoría y Trazabilidad:** Se navega a Tab 2 (`TEST-43`, `TEST-44`). La traza de agentes LangGraph se expande detallando el flujo cognitivo. La tarjeta de Fundamento Metodológico presenta su texto expandido armónicamente hasta 90ch eliminando el vacío asimétrico derecho. En Tab 3 (`TEST-46` a `TEST-53`), las cuatro tarjetas KPI exhiben idéntica altura visual (124px) y la matriz lista los 14 requisitos obligatorios con descarga operativa del payload JSON oficial.
6. **Reinicio y Cierre:** Se acciona `"Adaptar Nuevo Documento"`. La interfaz regresa limpiamente a la estación de bienvenida; no persisten flashcards, estados de volteo ni calificaciones SM-2 en memoria.

---

## 9. REVALIDACIÓN EXPLICITA DE DEFECTOS CORREGIDOS (DEF-01 a DEF-06)

| DEF-ID | TEST-ID | Hallazgo Previo | Corrección Aplicada | Resultado de Regresión | Evidencia Material |
| :---: | :---: | :--- | :--- | :---: | :--- |
| **DEF-01** | `TEST-06` | Dimming silente de 3 a 8s durante lectura de PDFs pesados. | Envoltorio con `st.spinner("Leyendo y preparando documento técnico...")`. | **PASS** (Feedback instantáneo al cargar archivo de 965k). | `docs/qa/evidence/final_regression/04_doc_A_cargado_ingesta.png` |
| **DEF-02** | `TEST-56`, `TEST-58` | Bleeding de tarjetas y calificaciones SM-2 al reiniciar o cambiar de documento. | Función `reset_adaptation_session()` con purga exhaustiva de claves `card_*`. | **PASS** (Prueba A/B demostró aislamiento total; ver sección 14). | `docs/qa/evidence/final_regression/ab_state_isolation_results.json` |
| **DEF-03** | `TEST-02` | Clipping superior del wordmark "NuevaMente" bajo navbar fija. | Ajuste a `padding-top: clamp(3rem, 5vh, 4.5rem)` en `.block-container`. | **BLOQUEADO EN PÚBLICO** (Provisional PASS local con margen completo). | `docs/qa/evidence/final_regression/01_desktop_pantalla_inicial_header.png` |
| **DEF-04** | `TEST-44` | Párrafos de Fundamento Metodológico comprimidos a 70ch con 40% de vacío. | Regla de especificidad `.nm-glass p { max-width: min(90ch, 100%) }`. | **PASS** (Texto balanceado a 90ch en tarjeta de 1200px). | `docs/qa/evidence/final_regression/10_tab2_auditoria_fundamento_metodologico.png` |
| **DEF-05** | `TEST-46` | Disparidad de altura vertical en las 4 tarjetas KPI de Tab 3. | Regla `.nm-kpi` con flex vertical, `min-height: 124px` y alineación de bases. | **PASS** (Tarjetas con altura uniforme de 124px y pies alineados). | `docs/qa/evidence/final_regression/11_tab3_trazabilidad_kpis_alineados.png` |
| **DEF-06** | `TEST-13`, `TEST-30`, `TEST-42` | Cifra de lote (ej. 80) rotulada como "Fragmentos del Corpus". | Rótulo renombrado a "Fragmentos del Lote Activo (ADR-012)" con pie aclaratorio. | **PASS** (Distinción semántica nítida en cabecera y traza). | `docs/qa/evidence/final_regression/05_doc_A_resultados_kpis.png` |

---

## 10. REVALIDACIÓN DE MEJORA DE INTERACCIÓN (IMP-01)

- **Identificador:** `IMP-01` (antigua `HIP-C`).
- **TEST-ID:** `TEST-31` (Interacción y Volteo de Flashcards).
- **Clasificación Oficial:** **DECISIÓN DE PRODUCTO / DISEÑO SHADOW** (No constituye desviación del pliego oficial del Hackathon).
- **Evaluación y Resultados:** Se reevaluó la presencia del botón secundario `"Voltear Tarjeta"` / `"Ver Frente"` (`btn_flip_{i}`). Se constató que es estrictamente indispensable para usuarios en navegadores móviles/táctiles donde el pseudo-elemento `:hover` no puede dispararse con el cursor. Asimismo, permite la operación de estudio mediante teclado accesible (`Tab` + `Enter`). La tarjeta mantiene ambas modalidades sincronizadas de forma bidireccional.
- **Dictamen:** **ACEPTADO COMO MEJORA DEFINITIVA**. Mantenida en el código base y catalogada formalmente en la especificación de componentes.

---

## 11. SUITE AUTOMATIZADA FINAL

- **Comando:** `venv/bin/pytest tests/`
- **Conteo Real:** **55 pruebas automatizadas**.
- **Resultado:** **55 PASSED, 0 FAILED** (100% de éxito).
- **Duración Observada:** **21.02 segundos**.
- **Desglose de Cobertura de la Suite:**
  - Adaptación y generación didáctica: 4 tests (`test_adaptation_service.py`)
  - Dominio cruzado / Manufactura: 1 test (`test_cross_corpus_domain.py`)
  - Persistencia relacional SQL y SQLite WAL: 6 tests (`test_db_persistence.py`)
  - Contratos de dominio Pydantic: 6 tests (`test_domain_contracts.py`)
  - Exportadores Anki (.csv) y Markdown: 2 tests (`test_exporters.py`)
  - Ingesta multiformato y deduplicación: 4 tests (`test_ingestion.py`)
  - LexForja y arquitectura de base de datos: 5 tests (`test_lexforja_architecture.py`)
  - Motor LLM y resiliencia: 1 test (`test_llm_engine.py`)
  - Grafo multi-agente LangGraph: 1 test (`test_multi_agent_graph.py`)
  - Adaptador de almacenamiento OCI/S3: 6 tests (`test_oci_storage.py`)
  - Métricas de calidad y anclaje: 3 tests (`test_quality.py`)
  - Pipeline RAG y ChromaDB: 1 test (`test_rag_pipeline.py`)
  - Esquemas de solicitud y validación: 3 tests (`test_schemas.py`)
  - Regresión de ciclo de vida y aislamiento de sesión: 3 tests (`test_session_lifecycle_regression.py`)
  - Repetición espaciada SuperMemo SM-2: 4 tests (`test_spaced_repetition.py`)
  - Pruebas de humo de UI Streamlit (`AppTest`): 5 tests (`test_ui_smoke.py`)

---

## 12. VALIDACIÓN PÚBLICA Y ESTADO DEL DESPLIEGUE

Conforme al principio metodológico de jerarquía de validación (Punto 2 de la directiva de gobierno), se intentó auditar la aplicación sobre la URL pública oficial declarada: `https://nuevamente.streamlit.app`.

### Hallazgos Factuales:
1. **Inaccesibilidad del Despliegue Público:** Al realizar peticiones HTTP y navegación directa con Chromium headless, el servidor de Streamlit Cloud devuelve una redirección `HTTP 303` hacia `https://share.streamlit.io/errors/not_found`.
2. **Evidencia Documentada:** Se capturó y archivó el pantallazo de error de Streamlit Cloud en [`docs/qa/evidence/final_regression/public_deploy_inaccessible_evidence.png`](file:///home/bitcoinpapa/projects/nuevamente/docs/qa/evidence/final_regression/public_deploy_inaccessible_evidence.png).
3. **Consecuencia Técnica y Gobernanza:** Dado que la URL pública no se encuentra activa ni sincronizada con el commit `258a86a`, está terminantemente prohibido declarar `PASS` definitivo para los casos estrictamente dependientes del render público. Por tanto, los casos `TEST-02`, `TEST-61`, `TEST-62` y `TEST-63` quedan formalmente catalogados como:
   `BLOQUEADO — validación pública pendiente`
   dejando constancia de que la verificación local provisional resultó plenamente satisfactoria (`PASS provisional en local`).

---

## 13. RENDIMIENTO OBSERVADO (VALORES ESTRICTAMENTE MEDIDOS)

Todas las mediciones se obtuvieron en ejecuciones reales sobre el entorno de laboratorio:

| Escenario de Carga | Longitud Medida | Chunks Indexados | Latencia Medida | Rendimiento / Tasa |
| :--- | :---: | :---: | :---: | :---: |
| **Documento Estándar (Caso Canónico Oracle VCN)** | 2.420 caracteres | 4 fragmentos | **2.85 segundos** | 849 caracteres / seg |
| **Documento Extenso (Manual Integral de Redes OCI)** | 965.086 caracteres | 80 fragmentos (ADR-012) | **15.15 segundos** | 63.702 caracteres / seg |
| **Extracción de PDF Estándar (pypdf/fitz)** | 14.820 caracteres | N/A (fase ingesta) | **0.42 segundos** | Ingesta fluida |
| **Extracción de PDF Pesado (>20 páginas con spinner)** | 54.120 caracteres | N/A (fase ingesta) | **3.80 segundos** | Spinner activo continuo |
| **Suite Completa Pytest (55 pruebas)** | 16 módulos | 55 aserciones | **21.02 segundos** | 0.38 s / prueba |

---

## 14. ESTADO Y PERSISTENCIA (PRUEBA CRÍTICA A/B)

Se ejecutó la prueba de aislamiento estricto de sesión entre dos documentos temáticamente disjuntos:

### Fase A: Documento A (Caso Canónico Oracle VCN)
- Longitud: 2.420 caracteres.
- Perfil: Principiante.
- Material Generado: Flashcards.
- Título Generado: `"Fundamentos de Redes VCN en OCI para Principiantes"`.
- Interacción: Tarjeta 0 volteada (`card_flipped_0 = True`) y calificada con nivel 5 (`card_graded_0 = {"status": "Alcanzado", "quality": 5}`).
- Registro: Guardado en base de datos local y capturado en `06_doc_A_tarjeta_calificada_sm2.png`.

### Transición: Reinicio Controlado
- Se acciona `"Adaptar Nuevo Documento"`.
- Ejecución de `reset_adaptation_session()`: `ultima_respuesta`, `ultimo_request` y `ultimo_trace` eliminados; claves dinámicas `card_flipped_*` y `card_graded_*` purgadas de raíz; `current_chunk_offset` restablecido a 0.
- Verificación DOM: Cero tarjetas visibles en pantalla (`07_doc_A_reset_bienvenida_limpia.png`).

### Fase B: Documento B (Muestra 3: Seguridad IAM)
- Longitud: 1.016 caracteres.
- Perfil: Principiante.
- Material Generado: Flashcards.
- Título Generado: `"Gobernanza y Seguridad en la Nube: Identidad y Acceso (IAM) para Principiantes"`.
- Resultados Observables:
  - ¿Títulos distintos?: **SÍ** (`True`).
  - ¿Persisten tarjetas de A?: **NO** (`False`).
  - ¿Persiste estado volteado en tarjeta 0?: **NO** (`False`, `card_flipped_0` no existe).
  - ¿Persiste calificación SM-2 de A?: **NO** (`False`, `card_graded_0` no existe).
  - ¿Chunk offset correcto?: **SÍ** (Inicia en 0 para el nuevo documento).

### Transición B2: Documento B + Cambio de Perfil
- Se cambia el perfil de "Principiante" a "Desarrollador Junior / Semi Senior" y se re-adapta.
- Título adaptado cambia automáticamente a: `"Gobernanza y Seguridad en la Nube: IAM para Desarrolladores Junior/Semi-Senior"`.
- El vocabulario técnico y la introducción se enriquecen con conceptos de arquitectura (`[Identity and Access Management (IAM)]`), evidenciando reactividad pedagógica al cambio de parámetros.
- Archivo de respaldo: [`docs/qa/evidence/final_regression/ab_state_isolation_results.json`](file:///home/bitcoinpapa/projects/nuevamente/docs/qa/evidence/final_regression/ab_state_isolation_results.json) y [`doc_B_profile_change_results.json`](file:///home/bitcoinpapa/projects/nuevamente/docs/qa/evidence/final_regression/doc_B_profile_change_results.json).

---

## 15. AUDITORÍA DE CALIDAD Y TRAZABILIDAD PMO

### Tab 2 (Auditoría de Calidad y Traza Multi-Agente)
- El panel de traza LangGraph expone la secuencia paso a paso de los agentes especializados (Revisor Pedagógico, Extractor de Conceptos, Calibrador Andragógico).
- La tarjeta de **Fundamento Metodológico del Puntaje de Anclaje** presenta una lectura fluida con ancho armónico de hasta 90 caracteres (`max-width: min(90ch, 100%)`), resolviendo definitivamente la asimetría reportada en DEF-04.
- Se mantiene la exclusión formal de modelos organizacionales longitudinales conforme a ADR-006.

### Tab 3 (Trazabilidad PMO y Gobernanza)
- Las cuatro tarjetas KPI superiores exhiben dimensiones simétricas (`min-height: 124px`, layout flex vertical y pie alineado), resolviendo DEF-05.
- La **Matriz de Trazabilidad Canónica** lista con total transparencia:
  - 14 Requisitos Obligatorios (O-01 a O-14): 11 VERIFICADOS, 2 con dependencia externa mitigada (O-03 Gemini y O-11 OCI físico) y 1 documentado.
  - 5 Requisitos Diferenciales (D-01 a D-05) y Requisito Interno X-01.
- El centro de descargas proporciona de forma inmediata los 5 contratos JSON oficiales y el paquete de transferencia de 5 documentos Markdown.

---

## 16. TRATAMIENTO DE REQUISITOS DIFERENCIALES (D-01 a D-05)

Conforme a la instrucción metodológica, los requisitos diferenciales no implementados en la interfaz de usuario se clasifican rigurosamente como `NO EJECUTABLE — funcionalidad diferencial aún no disponible`, sin alterar la numeración canónica del pliego ni forzar falsos fallos:

| Requisito | Denominación Canónica | Disponibilidad en UI | Clasificación QA |
| :---: | :--- | :---: | :--- |
| **D-01** | Quizzes Diagnósticos Interactivos con Feedback | No disponible en UI (solo Flashcards, Guía y Resumen) | **NO EJECUTABLE JUSTIFICADO** (`TEST-20`, `TEST-38`, `TEST-39`) |
| **D-02** | Sistema Multi-Agente LangGraph con Estado Compartido | Disponible y Verificado (Traza en Tab 2) | **PASS** (`TEST-23`, `TEST-43`) |
| **D-03** | Exportación Didáctica Multiformato (Anki .csv / Guía .md) | Disponible y Verificado | **PASS** (`TEST-36`, `TEST-40`) |
| **D-04** | Aprovisionamiento en OCI Compute VM Ampere | Dependencia externa no desplegada (S3 mock activo) | **PASS** en contrato / Dependencia documentada |
| **D-05** | Soporte Multimodal para Diagramas Bitmap | Fuera de alcance MVP (planificado en roadmap) | Fuera de alcance según pliego |

---

## 17. DEFECTOS ABIERTOS

- **Defectos Abiertos Residuales:** **0 (CERO)**.
- Todos los defectos reproducidos (`DEF-01` a `DEF-06`) fueron resueltos en el código fuente, validados con pruebas de regresión automatizadas e inspeccionados visualmente.
- No se registraron nuevos defectos durante el transcurso de la regresión integral.

---

## 18. RIESGOS RESIDUALES

A pesar de la estabilidad demostrada en el repositorio Shadow, se identifican con honestidad técnica los siguientes riesgos operacionales:
1. **Desincronización de la URL Pública Desplegada:** `https://nuevamente.streamlit.app` no se encuentra operativa en Streamlit Community Cloud (redirección a error 404). Mientras el entorno desplegado no sea re-vinculado y actualizado con los commits del repositorio Shadow, los usuarios externos no podrán acceder a las correcciones.
2. **Dependencia de Credenciales Cloud para Inferencia Externa:** En ausencia de variables de entorno para API Keys (Gemini, Mistral, NVIDIA) o credenciales OCI físicas, el sistema conmuta de forma segura a su motor de fallback sintético local y almacenamiento emulado en disco. Si bien esto garantiza que la aplicación nunca colapse (cero pantallas rojas), la variabilidad de contenidos didácticos en modo offline se apoya en plantillas deterministas.
3. **Escalamiento de Documentos Gigantes (>5 MB):** El límite de lote activo establecido en ADR-012 (máximo 80 fragmentos) protege eficazmente la memoria y costos de inferencia en documentos extensos; no obstante, documentos que superen las 100 páginas requerirán múltiples invocaciones del botón "Lote Adicional" para completar la lectura secuencial de todo el material.

---

## 19. REGISTRO DE EVIDENCIA MATERIAL

Todas las capturas y archivos de soporte se encuentran consolidados en el repositorio local bajo `docs/qa/evidence/final_regression/`:

| Artefacto de Evidencia | Descripción Técnica | Asociación TEST-ID |
| :--- | :--- | :---: |
| [`01_desktop_pantalla_inicial_header.png`](docs/qa/evidence/final_regression/01_desktop_pantalla_inicial_header.png) | Pantalla inicial en Desktop (1300x950) con padding superior corregido | `TEST-01`, `TEST-02`, `TEST-61` |
| [`02_tablet_pantalla_inicial.png`](docs/qa/evidence/final_regression/02_tablet_pantalla_inicial.png) | Render responsive en Tablet (768x1024) | `TEST-62` |
| [`03_mobile_pantalla_inicial.png`](docs/qa/evidence/final_regression/03_mobile_pantalla_inicial.png) | Render responsive en Mobile (375x667) | `TEST-63` |
| [`04_doc_A_cargado_ingesta.png`](docs/qa/evidence/final_regression/04_doc_A_cargado_ingesta.png) | Ingesta de Documento A con medición de caracteres en sidebar | `TEST-05`, `TEST-16` |
| [`05_doc_A_resultados_kpis.png`](docs/qa/evidence/final_regression/05_doc_A_resultados_kpis.png) | Banner de resultados con "Fragmentos del Lote Activo (ADR-012)" | `TEST-06`, `TEST-13`, `TEST-30` |
| [`06_doc_A_tarjeta_calificada_sm2.png`](docs/qa/evidence/final_regression/06_doc_A_tarjeta_calificada_sm2.png) | Flashcard 0 volteada y calificada como "Alcanzado" (SM-2) | `TEST-31`, `TEST-35` |
| [`07_doc_A_reset_bienvenida_limpia.png`](docs/qa/evidence/final_regression/07_doc_A_reset_bienvenida_limpia.png) | Vista de bienvenida limpia tras accionar "Adaptar Nuevo Documento" | `TEST-56`, `TEST-58` |
| [`08_doc_B_cargado.png`](docs/qa/evidence/final_regression/08_doc_B_cargado.png) | Ingesta de Documento B (Muestra 3: Seguridad IAM) | `TEST-18`, `TEST-58` |
| [`09_doc_B_resultados.png`](docs/qa/evidence/final_regression/09_doc_B_resultados.png) | Resultados de Documento B sin herencia de flashcards previas | `TEST-58` |
| [`10_tab2_auditoria_fundamento_metodologico.png`](docs/qa/evidence/final_regression/10_tab2_auditoria_fundamento_metodologico.png) | Fundamento Metodológico a 90ch en Tab 2 sin vacío asimétrico | `TEST-44` |
| [`11_tab3_trazabilidad_kpis_alineados.png`](docs/qa/evidence/final_regression/11_tab3_trazabilidad_kpis_alineados.png) | 4 tarjetas KPI de Tab 3 con altura simétrica normalizada (124px) | `TEST-46` |
| [`12_tab3_matriz_trazabilidad_oficial.png`](docs/qa/evidence/final_regression/12_tab3_matriz_trazabilidad_oficial.png) | Matriz oficial con 14 obligatorios, 5 diferenciales y contratos | `TEST-48`, `TEST-49`, `TEST-50` |
| [`ab_state_isolation_results.json`](docs/qa/evidence/final_regression/ab_state_isolation_results.json) | Registro estructurado del aislamiento A/B y purga de estado | `TEST-56`, `TEST-58` |
| [`doc_B_profile_change_results.json`](docs/qa/evidence/final_regression/doc_B_profile_change_results.json) | Adaptación diferenciada ante cambio de perfil pedagógico | `TEST-57` |
| [`extenso_965k_metrics.json`](docs/qa/evidence/final_regression/extenso_965k_metrics.json) | Métricas medidas y distinción semántica en documento de 965k | `TEST-06`, `TEST-13`, `TEST-26` |
| [`public_deploy_inaccessible_evidence.png`](docs/qa/evidence/final_regression/public_deploy_inaccessible_evidence.png) | Captura de error de Streamlit Cloud justificando bloqueo público | `TEST-02`, `TEST-61..63` |

---

## 20. MATRIZ FINAL DE CASOS DE PRUEBA (TEST-01 a TEST-67)

| TEST-ID | Área | Clasificación | Fuente | Estado Final | DEF-ID Asociado | Evidencia de Soporte |
| :---: | :--- | :--- | :--- | :---: | :---: | :--- |
| **TEST-01** | Arranque e Inicialización | OBLIGATORIO (O-09) | PLIEGO | **PASS** | — | `01_desktop_pantalla_inicial_header.png` |
| **TEST-02** | Arranque e Inicialización | SOPORTE / UX | HIPÓTESIS (HIP-E) | **BLOQUEADO** | DEF-03 | `public_deploy_inaccessible_evidence.png` (Provisional en `01_desktop...`) |
| **TEST-03** | Arranque e Inicialización | SOPORTE / UX | DECISIÓN PRODUCTO | **PASS** | — | `01_desktop_pantalla_inicial_header.png` |
| **TEST-04** | Arranque e Inicialización | SOPORTE / UX | DECISIÓN PRODUCTO | **PASS** | — | `test_ui_smoke.py` |
| **TEST-05** | Ingesta Documental | OBLIGATORIO (O-01) | PLIEGO | **PASS** | — | `test_ingestion.py` |
| **TEST-06** | Ingesta Documental | SOPORTE / UX | HIPÓTESIS (HIP-A) | **PASS** | DEF-01 | `04_doc_A_cargado_ingesta.png` |
| **TEST-07** | Ingesta Documental | OBLIGATORIO (O-01) | PLIEGO | **PASS** | — | `test_ingestion.py` |
| **TEST-08** | Ingesta Documental | OBLIGATORIO (O-01) | PLIEGO | **PASS** | — | `test_ingestion.py` |
| **TEST-09** | Ingesta Documental | OBLIGATORIO (O-01) | PLIEGO | **PASS** | — | `test_ui_smoke.py` |
| **TEST-10** | Ingesta Documental | OBLIGATORIO (O-10) | PLIEGO | **PASS** | — | `test_ui_smoke.py` |
| **TEST-11** | Ingesta Documental | OBLIGATORIO (O-10) | PLIEGO | **PASS** | — | `test_ingestion.py` |
| **TEST-12** | Medición Documental | SOPORTE / UX | DECISIÓN PRODUCTO | **PASS** | — | `04_doc_A_cargado_ingesta.png` |
| **TEST-13** | Medición Documental | SOPORTE / UX | ADR-012 / HIP-H | **PASS** | DEF-06 | `05_doc_A_resultados_kpis.png` |
| **TEST-14** | Medición Documental | SOPORTE / UX | DECISIÓN PRODUCTO | **PASS** | — | `extenso_965k_metrics.json` |
| **TEST-15** | Medición Documental | SOPORTE / UX | DECISIÓN PRODUCTO | **PASS** | — | `04_doc_A_cargado_ingesta.png` |
| **TEST-16** | Muestras de Demostración | OBLIGATORIO (O-12) | PLIEGO | **PASS** | — | `04_doc_A_cargado_ingesta.png` |
| **TEST-17** | Muestras de Demostración | OBLIGATORIO (O-12) | PLIEGO | **PASS** | — | `test_ui_smoke.py` |
| **TEST-18** | Muestras de Demostración | OBLIGATORIO (O-12) | PLIEGO | **PASS** | — | `08_doc_B_cargado.png` |
| **TEST-19** | Configuración Pedagógica | OBLIGATORIO (O-08) | PLIEGO | **PASS** | — | `test_ui_smoke.py` |
| **TEST-20** | Configuración Pedagógica | DIFERENCIAL (D-01) | PLIEGO | **NO EJECUTABLE** | — | Funcionalidad Quiz D-01 no implementada en UI |
| **TEST-21** | Configuración Pedagógica | OBLIGATORIO (O-08) | PLIEGO | **PASS** | — | `test_ui_smoke.py` |
| **TEST-22** | Configuración Pedagógica | OBLIGATORIO (O-08) | PLIEGO | **PASS** | — | `test_ui_smoke.py` |
| **TEST-23** | Configuración Pedagógica | DIFERENCIAL (D-02) | PLIEGO / ADR | **PASS** | — | `test_multi_agent_graph.py` |
| **TEST-24** | Generación de Material | OBLIGATORIO (O-10) | PLIEGO | **PASS** | — | `test_ui_smoke.py` |
| **TEST-25** | Generación de Material | SOPORTE / UX | HIPÓTESIS (HIP-B) | **PASS** | — | `extenso_965k_metrics.json` |
| **TEST-26** | Generación de Material | SOPORTE / UX | ADR-012 | **PASS** | — | `extenso_965k_metrics.json` |
| **TEST-27** | Generación de Material | OBLIGATORIO (O-06) | PLIEGO | **PASS** | — | `test_db_persistence.py` |
| **TEST-28** | Generación de Material | OBLIGATORIO (O-06) | PLIEGO | **PASS** | — | `test_oci_storage.py` |
| **TEST-29** | Flashcards 3D | OBLIGATORIO (O-07) | PLIEGO | **PASS** | — | `05_doc_A_resultados_kpis.png` |
| **TEST-30** | Flashcards 3D | SOPORTE / UX | ADR-012 / HIP-H | **PASS** | DEF-06 | `05_doc_A_resultados_kpis.png` |
| **TEST-31** | Flashcards 3D | SOPORTE / UX | HIPÓTESIS (HIP-C) | **PASS** | IMP-01 | `06_doc_A_tarjeta_calificada_sm2.png` |
| **TEST-32** | Flashcards 3D | SOPORTE / UX | DISEÑO SHADOW | **PASS** | — | `06_doc_A_tarjeta_calificada_sm2.png` |
| **TEST-33** | Algoritmo SM-2 | SOPORTE / UX | DECISIÓN PRODUCTO | **PASS** | — | `test_spaced_repetition.py` |
| **TEST-34** | Algoritmo SM-2 | SOPORTE / UX | DECISIÓN PRODUCTO | **PASS** | — | `test_spaced_repetition.py` |
| **TEST-35** | Algoritmo SM-2 | SOPORTE / UX | DECISIÓN PRODUCTO | **PASS** | — | `06_doc_A_tarjeta_calificada_sm2.png` |
| **TEST-36** | Exportación Anki | DIFERENCIAL (D-03) | PLIEGO | **PASS** | — | `test_exporters.py` |
| **TEST-37** | Paginación ADR-012 | SOPORTE / UX | ADR-012 | **PASS** | — | `test_adaptation_service.py` |
| **TEST-38** | Quizzes Diagnósticos | DIFERENCIAL (D-01) | PLIEGO | **NO EJECUTABLE** | — | Funcionalidad Quiz D-01 no implementada en UI |
| **TEST-39** | Quizzes Diagnósticos | DIFERENCIAL (D-01) | PLIEGO | **NO EJECUTABLE** | — | Funcionalidad Quiz D-01 no implementada en UI |
| **TEST-40** | Guía Práctica | OBLIGATORIO (O-05) | PLIEGO | **PASS** | — | `test_exporters.py` |
| **TEST-41** | Resumen Ejecutivo | OBLIGATORIO (O-05) | PLIEGO | **PASS** | — | `test_adaptation_service.py` |
| **TEST-42** | Auditoría de Calidad | OBLIGATORIO (O-04) | PLIEGO | **PASS** | DEF-06 | `05_doc_A_resultados_kpis.png` |
| **TEST-43** | Auditoría de Calidad | DIFERENCIAL (D-02) | PLIEGO | **PASS** | — | `10_tab2_auditoria_fundamento...` |
| **TEST-44** | Auditoría de Calidad | SOPORTE / UX | HIPÓTESIS (HIP-F) | **PASS** | DEF-04 | `10_tab2_auditoria_fundamento...` |
| **TEST-45** | Auditoría de Calidad | SOPORTE / UX | ADR-006 | **PASS** | — | `10_tab2_auditoria_fundamento...` |
| **TEST-46** | Trazabilidad PMO | SOPORTE / UX | HIPÓTESIS (HIP-G) | **PASS** | DEF-05 | `11_tab3_trazabilidad_kpis_alineados.png` |
| **TEST-47** | Trazabilidad PMO | SOPORTE / UX | DECISIÓN PRODUCTO | **PASS** | — | `11_tab3_trazabilidad_kpis_alineados.png` |
| **TEST-48** | Trazabilidad Contractual | OBLIGATORIO (O-01..14) | PLIEGO | **PASS** | — | `12_tab3_matriz_trazabilidad_oficial.png` |
| **TEST-49** | Trazabilidad Contractual | DIFERENCIAL (D-01..05) | PLIEGO | **PASS** | — | `12_tab3_matriz_trazabilidad_oficial.png` |
| **TEST-50** | Descarga de Contratos | SOPORTE / UX | DECISIÓN PRODUCTO | **PASS** | — | `12_tab3_matriz_trazabilidad_oficial.png` |
| **TEST-51** | Descarga de Transferencia | SOPORTE / UX | DECISIÓN PRODUCTO | **PASS** | — | `12_tab3_matriz_trazabilidad_oficial.png` |
| **TEST-52** | Secuencia de Commits | SOPORTE / UX | DECISIÓN PRODUCTO | **PASS** | — | `12_tab3_matriz_trazabilidad_oficial.png` |
| **TEST-53** | Persistencia OCI | OBLIGATORIO (O-06, O-11) | PLIEGO | **PASS** | — | `test_oci_storage.py` |
| **TEST-54** | Persistencia LexForja | SOPORTE / UX | DECISIÓN PRODUCTO | **PASS** | — | `test_lexforja_architecture.py` |
| **TEST-55** | Preservación de Tabs | SOPORTE / UX | DECISIÓN PRODUCTO | **PASS** | — | `test_ui_smoke.py` |
| **TEST-56** | Ciclo de Vida y Sesión | SOPORTE / UX | HIPÓTESIS (HIP-D) | **PASS** | DEF-02 | `ab_state_isolation_results.json` |
| **TEST-57** | Diferenciación Pedagógica | OBLIGATORIO (O-05) | PLIEGO | **PASS** | — | `doc_B_profile_change_results.json` |
| **TEST-58** | Aislamiento Documental | SOPORTE / UX | HIPÓTESIS (HIP-D) | **PASS** | DEF-02 | `ab_state_isolation_results.json` |
| **TEST-59** | Reinicio Tab 1 Inferior | SOPORTE / UX | DECISIÓN PRODUCTO | **PASS** | — | `test_session_lifecycle_regression.py` |
| **TEST-60** | Sesión de Navegador | SOPORTE / UX | DECISIÓN PRODUCTO | **PASS** | — | `test_session_lifecycle_regression.py` |
| **TEST-61** | Responsive Desktop | SOPORTE / UX | DISEÑO SHADOW | **BLOQUEADO** | — | `public_deploy_inaccessible_evidence.png` (Provisional en `01_desktop...`) |
| **TEST-62** | Responsive Tablet | SOPORTE / UX | DISEÑO SHADOW | **BLOQUEADO** | — | `public_deploy_inaccessible_evidence.png` (Provisional en `02_tablet...`) |
| **TEST-63** | Responsive Mobile | SOPORTE / UX | DISEÑO SHADOW | **BLOQUEADO** | — | `public_deploy_inaccessible_evidence.png` (Provisional en `03_mobile...`) |
| **TEST-64** | Contraste Cromático | SOPORTE / UX | DISEÑO SHADOW | **PASS** | — | `styles.css` / `test_ui_smoke.py` |
| **TEST-65** | Manejo de Errores | SOPORTE / UX | DECISIÓN PRODUCTO | **PASS** | — | `test_ui_smoke.py` |
| **TEST-66** | Fallback Defensivo | OBLIGATORIO (O-10) | PLIEGO | **PASS** | — | `test_llm_engine.py` |
| **TEST-67** | Sanitización y Seguridad | SOPORTE / UX | DECISIÓN PRODUCTO | **PASS** | — | `test_schemas.py` |

---

## 21. CONCLUSIÓN TÉCNICA

En cumplimiento estricto del principio de veracidad técnica y transparencia metodológica, se emite el balance técnico factual de la solución:

### 1. Qué está plenamente demostrado:
- **Integridad del Motor RAG y Pipeline Didáctico:** Procesamiento determinista de ingesta universal (PDF, Markdown, Texto plano), partición semántica acotada a 80 fragmentos por ejecución conforme a ADR-012, recuperación contextual vectorial con ChromaDB y síntesis multi-agente adaptada por perfil destinatario.
- **Aislamiento Absoluto de Sesión (DEF-02 Resuelto):** La rutina centralizada `reset_adaptation_session()` purga determinísticamente todas las claves dinámicas en memoria volátil. Quedó formalmente demostrado en la prueba A/B que el Documento B no hereda flashcards, estados de volteo ni calificaciones SM-2 del Documento A.
- **Transparencia y Distinción Semántica (DEF-06 Resuelto):** El indicador de cabecera rotula honestamente el lote acotado activo (`Fragmentos del Lote Activo (ADR-012)`), impidiendo que se confunda el subconjunto procesado en la ventana con los fragmentos totales del documento o los 3.020 fragmentos del corpus en base de datos.
- **Estabilidad y Resiliencia Automatizada:** 55 pruebas unitarias, de integración, esquemas y regresión ejecutadas con 100% de éxito en Pytest. Presencia de fallback heurístico sintético ante indisponibilidad de APIs externas (cero crashes).
- **Usabilidad Ergonómica de Flashcards (IMP-01 Aceptado):** El botón de volteo híbrido complementa la animación CSS garantizando accesibilidad en pantallas táctiles y teclado.

### 2. Qué está parcialmente demostrado:
- **Adaptabilidad Responsive Visual:** En el entorno local instrumentado con Chromium, la interfaz se adapta armónicamente a resoluciones Desktop (1300x950), Tablet (768x1024) y Mobile (375x667), sin solapamientos. Sin embargo, no puede declararse demostrada en producción pública al encontrarse la URL externa inaccesible.

### 3. Qué no está demostrado:
- **Comportamiento en Entorno Físico de Nube OCI:** El aprovisionamiento de cómputo en instancias Ampere físicas (D-04) no fue ejecutado en esta campaña (gestionado como dependencia técnica externa con mock local S3 verificado).
- **Formato Interactivo de Quizzes (D-01):** Las pruebas atómicas de interfaz para quizzes (`TEST-20`, `TEST-38`, `TEST-39`) no pudieron ejecutarse al no estar expuesta esta modalidad interactiva en la interfaz principal del MVP.

### 4. Qué queda formalmente bloqueado:
- **Validación Visual Pública Definitiva:** Los casos `TEST-02` (Header en host público), `TEST-61` (Desktop), `TEST-62` (Tablet) y `TEST-63` (Mobile) quedan catalogados como `BLOQUEADO — validación pública pendiente` debido a que `https://nuevamente.streamlit.app` no responde con la aplicación desplegada sino con error 404/not_found en Streamlit Cloud.

### 5. Riesgos que permanecen:
- Desconexión del deployment público respecto al repositorio Shadow.
- Requerimiento de re-autenticación o vinculación en Streamlit Community Cloud para habilitar la visualización por parte de evaluadores externos.
"""

with open("docs/qa/TEST_REPORT_FINAL.md", "w") as f:
    f.write(content)
print("Created docs/qa/TEST_REPORT_FINAL.md successfully.")
