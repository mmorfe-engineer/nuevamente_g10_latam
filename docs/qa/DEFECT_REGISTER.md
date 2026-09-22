# REGISTRO MAESTRO DE DEFECTOS Y MEJORAS · NUEVAMENTE
**Campaña de Verificación QA · Repositorio Shadow (`mmorfe-engineer/nuevamente_g10_latam`)**  
**Fecha de Apertura:** 22 de Septiembre de 2026  
**Última Actualización:** 22 de Septiembre de 2026 (Cierre de Fase Correctiva Prompt 3)  
**Responsable:** Lead QA Architect & PM  

---

## 1. RESUMEN DE ESTADO DE DEFECTOS Y MEJORAS

| DEF-ID | TEST-ID Origen | Área | Severidad | Hipótesis | Causa Raíz | Reprueba | Estado |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **DEF-01** | `TEST-06` | Ingesta Documental | **P1 · ALTO** | HIP-A | Extracción síncrona en script header sin spinner contextual | `TEST-06` (PASS) | **CERRADO** |
| **DEF-02** | `TEST-56`, `TEST-58` | Ciclo de Vida / Sesión | **P0 · CRÍTICO** | HIP-D | Limpieza incompleta de `st.session_state` y bleeding de tarjetas/inputs | `TEST-56`, `TEST-58`, Regresión Pytest (PASS) | **CERRADO** |
| **DEF-03** | `TEST-02` | Arranque / Cabecera | **P2 · MEDIO** | HIP-E | Padding-top insuficiente (`16px`) en `.block-container` vs fixed header | `TEST-02` (PASS) | **CERRADO** |
| **DEF-04** | `TEST-44` | Auditoría de Calidad | **P2 · MEDIO** | HIP-F | Regla CSS global `max-width: 70ch` asimétrica en tarjetas `.nm-glass` | `TEST-44` (PASS) | **CERRADO** |
| **DEF-05** | `TEST-46` | Trazabilidad PMO | **P2 · MEDIO** | HIP-G | Disparidad de altura en `st.columns(4)` por falta de flex/min-height | `TEST-46` (PASS) | **CERRADO** |
| **DEF-06** | `TEST-13`, `TEST-30`, `TEST-42` | Medición / Trazabilidad | **P1 · ALTO** | HIP-H | Rotulado confuso: fragmentos de lote acotado llamados "del Corpus" | `TEST-13`, `TEST-30`, `TEST-42` (PASS) | **CERRADO** |
| **IMP-01** | `TEST-31` | Experiencia de Estudio | **P3 · FORMA** | HIP-C | Incorporación de botón explícito de volteo híbrido en Flashcards | `TEST-31` (PASS) | **ACEPTADO COMO MEJORA** |

---

## 2. FICHAS TÉCNICAS DE DEFECTOS CORREGIDOS

### DEF-01
- **TEST-ID Origen:** `TEST-06`
- **Área:** Ingesta Documental
- **Tipo:** UX / Rendimiento
- **Clasificación:** SOPORTE / UX / ARQUITECTURA
- **Fuente del Criterio:** HIPÓTESIS DE QA (HIP-A)
- **Severidad:** **P1 · ALTO**
- **Descripción:** Durante la carga de archivos PDF pesados (>20 páginas), la interfaz entra en modo dimming de Streamlit durante 3 a 8 segundos sin ningún indicador visual o mensaje que informe que se está extrayendo texto.
- **Causa Raíz:** La extracción síncrona en `ui/app.py` líneas 91-108 y 780-793 se ejecutaba en el flujo principal del script antes de que Streamlit monte un elemento de feedback contextual.
- **Estado de Causa Raíz:** **CONFIRMADA**
- **Corrección Implementada:** Se envolvieron las llamadas de `doc_loader.extract_from_file` tanto en el bloque de sincronización anticipada como en el uploader de Tab 1 dentro de bloques `with st.spinner("Leyendo y preparando documento técnico..."):`.
- **Reprueba Ejecutada:** `TEST-06` (Ingesta de documento extenso) ejecutada exitosamente. El testigo aparece de inmediato durante la lectura.
- **Evidencia:** `docs/qa/evidence/area_02/DEF-01_before.png` y `docs/qa/evidence/area_02/DEF-01_after.png`.
- **Criterio de Cierre Cumplido:** Cero estados de bloqueo silente; feedback contextual inmediato no porcentual y factual.
- **Estado:** **CERRADO**

---

### DEF-02
- **TEST-ID Origen:** `TEST-56`, `TEST-58`
- **Área:** Ciclo de Vida y Sesión
- **Tipo:** Estado / Limpieza Residual
- **Clasificación:** SOPORTE / UX / ARQUITECTURA
- **Fuente del Criterio:** HIPÓTESIS DE QA (HIP-D)
- **Severidad:** **P0 · CRÍTICO**
- **Descripción:** Al presionar "Adaptar Nuevo Documento" (`btn_sidebar_reset`, `btn_tab1_reset`, `btn_tab1_reset_bottom`), la acción solo ejecutaba `del st.session_state["ultima_respuesta"]` y `current_chunk_offset = 0`. No limpiaba `card_flipped_*`, `card_graded_*`, ni el texto previo si se conmutaba de archivo a texto libre, produciendo contaminación cruzada de flashcards y estados residuales.
- **Causa Raíz:**
  1. Ausencia de un método centralizado de invalidación de sesión en `ui/app.py`.
  2. Retención de claves dinámicas `card_flipped_{i}` y `card_graded_{i}` en `st.session_state` entre diferentes documentos.
  3. Falta de hook de invalidación al cargar un nuevo archivo.
- **Estado de Causa Raíz:** **CONFIRMADA**
- **Corrección Implementada:** Se definió la función centralizada `reset_adaptation_session(clear_document: bool = False, state=None)` en `ui/app.py` que purga de forma determinista `ultima_respuesta`, `ultimo_request`, `ultimo_trace`, restablece `current_chunk_offset = 0`, y elimina exhaustivamente todas las claves `card_flipped_*` y `card_graded_*`. Se conectó a los 3 botones de reset y al detector de cambio de archivo.
- **Reprueba Ejecutada:**
  - `TEST-56` y `TEST-58` manuales (PASS).
  - Test automatizado: `tests/test_session_lifecycle_regression.py::test_session_state_reset_function_logic` (PASS).
  - Test E2E de AppTest: `tests/test_session_lifecycle_regression.py::test_ui_e2e_document_reset_cleans_flashcard_state` (PASS).
- **Evidencia:** `docs/qa/evidence/area_07/DEF-02_before.png`, `docs/qa/evidence/area_07/DEF-02_after.png`, y log `docs/qa/evidence/area_07/DEF-02_state_cleanup_regression.log`.
- **Criterio de Cierre Cumplido:** Aislamiento total entre ejecuciones; al accionar reset o cambiar documento, no persisten tarjetas ni calificaciones previas.
- **Estado:** **CERRADO**

---

### DEF-03
- **TEST-ID Origen:** `TEST-02`
- **Área:** Arranque e Inicialización
- **Tipo:** Visual / UX
- **Clasificación:** SOPORTE / UX / ARQUITECTURA
- **Fuente del Criterio:** HIPÓTESIS DE QA (HIP-E) / DISEÑO SHADOW
- **Severidad:** **P2 · MEDIO**
- **Descripción:** En la vista pública de Streamlit, la barra de herramientas del host (`[data-testid="stHeader"]`) tiene una altura de ~56px. Con el padding superior de `.block-container` en `16px`, el marco superior `.nm-glass` quedaba solapado parcialmente o recortado.
- **Causa Raíz:** Regla CSS en `ui/assets/styles.css` línea 179: `padding-top: var(--space-16) !important;` insuficiente para compensar la barra fija de Streamlit Cloud.
- **Estado de Causa Raíz:** **CONFIRMADA**
- **Corrección Implementada:** Se ajustó en `ui/assets/styles.css` la regla de `.block-container` a `padding-top: clamp(3rem, 5vh, 4.5rem) !important;`.
- **Reprueba Ejecutada:** `TEST-02` reejecutada en resoluciones desktop y móvil; el título "NuevaMente" y el subtítulo son 100% visibles y libres de solapamiento.
- **Evidencia:** `docs/qa/evidence/area_01/DEF-03_before.png` y `docs/qa/evidence/area_01/DEF-03_after.png`.
- **Criterio de Cierre Cumplido:** Wordmark institucional completamente visible con respiración superior sin solapamiento bajo el header.
- **Estado:** **CERRADO**

---

### DEF-04
- **TEST-ID Origen:** `TEST-44`
- **Área:** Auditoría de Calidad
- **Tipo:** Visual / Tipografía
- **Clasificación:** SOPORTE / UX / ARQUITECTURA
- **Fuente del Criterio:** HIPÓTESIS DE QA (HIP-F) / DISEÑO SHADOW
- **Severidad:** **P2 · MEDIO**
- **Descripción:** En la tarjeta de "Fundamento Metodológico del Puntaje de Anclaje" en Tab 2, el texto ocupaba solo una franja estrecha a la izquierda, dejando un espacio vacío de más del 40% a la derecha en monitores desktop.
- **Causa Raíz:** Regla global en `ui/assets/styles.css`: `p, .stMarkdown p { max-width: 70ch; }` que forzaba a todos los párrafos dentro de tarjetas anchas a acotarse a 70 caracteres.
- **Estado de Causa Raíz:** **CONFIRMADA**
- **Corrección Implementada:** Se incorporó la regla `.nm-glass p, .nm-glass .stMarkdown p { max-width: min(90ch, 100%) !important; }` en `ui/assets/styles.css`.
- **Reprueba Ejecutada:** `TEST-44` reejecutada; la lectura fluye armónicamente cubriendo hasta 90 caracteres y equilibrando el contenedor de 1200px.
- **Evidencia:** `docs/qa/evidence/area_09/DEF-04_before.png` y `docs/qa/evidence/area_09/DEF-04_after.png`.
- **Criterio de Cierre Cumplido:** Eliminación de la asimetría visual; lectura técnica balanceada y confortable en desktop y tablet.
- **Estado:** **CERRADO**

---

### DEF-05
- **TEST-ID Origen:** `TEST-46`
- **Área:** Trazabilidad PMO
- **Tipo:** Visual / Consistencia
- **Clasificación:** SOPORTE / UX / ARQUITECTURA
- **Fuente del Criterio:** HIPÓTESIS DE QA (HIP-G) / DISEÑO SHADOW
- **Severidad:** **P2 · MEDIO**
- **Descripción:** En Tab 3, las 4 tarjetas KPI ("Cloud en esta Ejecución", "Tests Automatizados", "Almacenamiento", "Corpus en Base de Datos") presentaban alturas verticales diferentes debido a que las descripciones secundarias tenían distinto número de líneas.
- **Causa Raíz:** Falta de flex layout vertical uniforme (`height: 100%; min-height: 124px; display: flex; flex-direction: column; justify-content: space-between;`) en la clase `.nm-kpi`.
- **Estado de Causa Raíz:** **CONFIRMADA**
- **Corrección Implementada:** Se definió formalmente `.nm-kpi` con flex vertical, `min-height: 124px !important` y `justify-content: space-between !important`, extendiendo `height: 100%` a las columnas que alojan `.nm-kpi`.
- **Reprueba Ejecutada:** `TEST-46` reejecutada; las 4 tarjetas KPI superiores en Tab 3 lucen rigurosamente con idéntica altura visual y sus pies alineados.
- **Evidencia:** `docs/qa/evidence/area_10/DEF-05_before.png` y `docs/qa/evidence/area_10/DEF-05_after.png`.
- **Criterio de Cierre Cumplido:** Altura idéntica y alineación de línea de base entre las 4 tarjetas de gobernanza.
- **Estado:** **CERRADO**

---

### DEF-06
- **TEST-ID Origen:** `TEST-13`, `TEST-30`, `TEST-42`
- **Área:** Medición y Partición Documental / Trazabilidad
- **Tipo:** Trazabilidad / Integración
- **Clasificación:** SOPORTE / UX / ARQUITECTURA
- **Fuente del Criterio:** ADR (ADR-012) / HIPÓTESIS DE QA (HIP-H)
- **Severidad:** **P1 · ALTO**
- **Descripción:** En el banner de KPIs superior, el número de fragmentos indexados del lote (ej. 80) se rotulaba como "Fragmentos del Corpus", generando ambigüedad con los 3.020 fragmentos del corpus en base de datos y los 1.205 fragmentos totales de un documento extenso.
- **Causa Raíz:** Inconsistencia semántica en los rótulos HTML de `ui/app.py` donde se utilizó la etiqueta "Fragmentos del Corpus" en lugar de "Fragmentos del Lote Activo (ADR-012)".
- **Estado de Causa Raíz:** **CONFIRMADA**
- **Corrección Implementada:** Se modificó el título del KPI a `"Fragmentos del Lote Activo (ADR-012)"`, se añadió tooltip explicativo de ventana deslizante según límites de latencia/costos, y se aclaró en el pie `Fuente: {doc_ref_corta} (lote acotado)`.
- **Reprueba Ejecutada:**
  - `TEST-13`, `TEST-30` y `TEST-42` reejecutadas (PASS).
  - Regresión automatizada: `tests/test_session_lifecycle_regression.py::test_ui_kpi_banner_labels_active_batch_adr012` (PASS).
- **Evidencia:** `docs/qa/evidence/area_03/DEF-06_before.png` y `docs/qa/evidence/area_03/DEF-06_after.png`.
- **Criterio de Cierre Cumplido:** Distinción semántica total entre fragmentos del lote procesado (ADR-012) y el corpus global de la base de datos (3.020).
- **Estado:** **CERRADO**

---

## 3. REGISTRO DE MEJORAS DE UX ACEPTADAS

### IMP-01 (antigua HIP-C)
- **TEST-ID Origen:** `TEST-31`
- **Área:** Experiencia de Estudio (Flashcards)
- **Tipo:** UX / Accesibilidad
- **Clasificación:** SOPORTE / UX / ARQUITECTURA
- **Fuente del Criterio:** HIPÓTESIS DE QA (HIP-C) / CONTROL DE CAMBIOS
- **Severidad:** **P3 · FORMA**
- **Estado:** **ACEPTADO COMO MEJORA**
- **Dictamen:** La incorporación del botón explícito "Voltear Tarjeta" / "Ver Frente" (`btn_flip_{i}`) como control accesible complementario al hover/checkbox CSS nativo mejora la descubribilidad en dispositivos móviles y touch, no rompe la accesibilidad por teclado y no introduce regresión alguna. Se conserva e incorpora formalmente a la especificación y catálogo de interacción.
- **Reprueba:** `TEST-31` (PASS).
