# REGISTRO MAESTRO DE DEFECTOS Y MEJORAS · NUEVAMENTE
**Campaña de Verificación QA · Repositorio Shadow (`mmorfe-engineer/nuevamente_g10_latam`)**  
**Fecha de Apertura:** 22 de Septiembre de 2026  
**Última Actualización:** 22 de Septiembre de 2026 · 21:30 UTC-4 (Adenda de Validación Pública)  
**Responsable:** Lead QA Architect & PM  

---

## 1. RESUMEN DE ESTADO DE DEFECTOS Y MEJORAS

| DEF-ID | TEST-ID Origen | Área | Severidad | Hipótesis | Causa Raíz | Reprueba | Estado |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **DEF-01** | `TEST-06` | Ingesta Documental | **P1 · ALTO** | HIP-A | Extracción síncrona en script header sin spinner contextual | `TEST-06` (PASS) | **CERRADO** |
| **DEF-02** | `TEST-56`, `TEST-58` | Ciclo de Vida / Sesión | **P0 · CRÍTICO** | HIP-D | Limpieza incompleta de `st.session_state` y bleeding de tarjetas/inputs | `TEST-56`, `TEST-58`, Regresión Pytest (PASS) | **CERRADO** |
| **DEF-03** | `TEST-02` | Arranque / Cabecera | **P2 · MEDIO** | HIP-E | Deployment en `b61fcd3` con padding 16px; recorte bajo fixed header | `TEST-02` (PASS Local / Desplegado en `41bce04`) | **REABIERTO (EN VERIFICACIÓN PÚBLICA)** |
| **DEF-04** | `TEST-44` | Auditoría de Calidad | **P2 · MEDIO** | HIP-F | Regla CSS global `max-width: 70ch` asimétrica en tarjetas `.nm-glass` | `TEST-44` (PASS) | **CERRADO** |
| **DEF-05** | `TEST-46` | Trazabilidad PMO | **P2 · MEDIO** | HIP-G | Deployment en `b61fcd3` sin height uniforme; asimetría por variación de texto | `TEST-46` (PASS Local / Desplegado en `41bce04`) | **REABIERTO (EN VERIFICACIÓN PÚBLICA)** |
| **DEF-06** | `TEST-13`, `TEST-30`, `TEST-42` | Medición / Trazabilidad | **P1 · ALTO** | HIP-H | Rotulado confuso: fragmentos de lote acotado llamados "del Corpus" | `TEST-13`, `TEST-30`, `TEST-42` (PASS) | **CERRADO** |
| **DEF-07** | `TEST-68` | Trazabilidad PMO | **P2 · MEDIO** | HIP-I | Indicador de tests en UI (52/52 vs 55/55) desincronizado por falta de push | `TEST-68` (PASS Local / Desplegado en `41bce04`) | **ABIERTO (EN VERIFICACIÓN PÚBLICA)** |
| **IMP-01** | `TEST-31` | Experiencia de Estudio | **P3 · FORMA** | HIP-C | Incorporación de botón explícito de volteo híbrido en Flashcards | `TEST-31` (PASS) | **ACEPTADO COMO MEJORA** |

---

## 2. FICHAS TÉCNICAS DE DEFECTOS

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
- **Fuente del Criterio:** HIPÓTESIS DE QA (HIP-E) / AUDITORÍA DE COORDINACIÓN EN INSTANCIA PÚBLICA
- **Severidad:** **P2 · MEDIO**
- **Descripción:** En la vista pública desplegada en Streamlit Community Cloud, el título "NuevaMente" continuaba apareciendo recortado verticalmente en su borde superior bajo la barra de navegación del host.
- **Causa Raíz:** La aplicación pública ejecutaba el commit `b61fcd3` (padding 16px). Adicionalmente, la barra `header[data-testid="stHeader"]` (46px) interactuaba con el contenedor sin margen suficiente.
- **Estado de Causa Raíz:** **CONFIRMADA Y AISLADA (Causa A + D)**
- **Corrección Implementada:**
  1. En `ui/assets/styles.css` se amplió la regla `.block-container` a `padding-top: clamp(4rem, 6vh, 5.5rem) !important;`.
  2. Se fijó `header[data-testid="stHeader"] { background-color: transparent !important; pointer-events: none !important; }` para asegurar paso de luz y cero oclusión visual.
  3. Se publicó el commit `41bce04` a `origin/main` en GitHub.
- **Reprueba Instrumental:** En Chromium CDP, la posición del encabezado se estabilizó en `+245.8px` en reposo, garantizando despeje completo.
- **Evidencia:** `docs/qa/evidence/area_01/DEF-03_before.png`, `docs/qa/evidence/final_regression/header_after_clearance_fix.png`.
- **Criterio de Cierre Formal:** Wordmark institucional visible en su totalidad en la URL pública autenticada.
- **Estado:** **REABIERTO (CORREGIDO EN CÓDIGO `41bce04` / DESPLEGADO / EN VERIFICACIÓN PÚBLICA)**

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
- **Tipo:** Visual / Consistencia Geométrica
- **Clasificación:** SOPORTE / UX / ARQUITECTURA
- **Fuente del Criterio:** HIPÓTESIS DE QA (HIP-G) / AUDITORÍA DE COORDINACIÓN EN INSTANCIA PÚBLICA
- **Severidad:** **P2 · MEDIO**
- **Descripción:** En la instancia pública, las 4 tarjetas KPI de Tab 3 no presentaban la misma altura visual. La segunda tarjeta ("Tests Automatizados") crecía más que las adyacentes por tener 2 líneas de descripción inferior.
- **Causa Raíz:** La aplicación pública ejecutaba el commit `b61fcd3` donde `.nm-kpi` no tenía altura mínima fija ni control de contenedor flex sobre los contenedores intermedios de Streamlit.
- **Estado de Causa Raíz:** **CONFIRMADA Y AISLADA (Causa A + G)**
- **Corrección Implementada:**
  1. Se forzó `.nm-kpi { height: 136px !important; min-height: 136px !important; display: flex !important; flex-direction: column !important; justify-content: space-between !important; box-sizing: border-box !important; }`.
  2. Se configuró flex stretch sobre los wrappers intermedios `[data-testid="column"] > div:has(.nm-kpi)`, `stElementContainer` y `stMarkdownContainer`.
  3. Se publicó el commit `41bce04` a `origin/main` en GitHub.
- **Reprueba Instrumental:** Medición con Chromium CDP en Tab 3 confirmó que las 4 tarjetas miden exactamente `136.00px` (`top: 499px`), con bordes superior e inferior alineados en un único plano continuo.
- **Evidencia:** `docs/qa/evidence/area_10/DEF-05_before.png`, `docs/qa/evidence/final_regression/tab3_kpis_uniform_height_verified.png`, `docs/qa/evidence/final_regression/tab3_kpis_cards_centered.png`.
- **Criterio de Cierre Formal:** Altura idéntica comprobada en pantalla en la URL pública autenticada.
- **Estado:** **REABIERTO (CORREGIDO EN CÓDIGO `41bce04` / DESPLEGADO / EN VERIFICACIÓN PÚBLICA)**

---

### DEF-06
- **TEST-ID Origen:** `TEST-13`, `TEST-30`, `TEST-42`
- **Área:** Medición y Trazabilidad Semántica
- **Tipo:** Trazabilidad / Honestidad Métrica
- **Clasificación:** SOPORTE / UX / ARQUITECTURA
- **Fuente del Criterio:** HIPÓTESIS DE QA (HIP-H) / PRINCIPIOS DE GOBERNANZA
- **Severidad:** **P1 · ALTO**
- **Descripción:** En la cabecera y en los KPIs, la métrica de fragmentos procesados se titulaba "Fragmentos Indexados del Corpus", dando a entender que los fragmentos del lote acotado por ADR-012 correspondían a la totalidad de la base de datos documental.
- **Causa Raíz:** Rótulo ambiguo en `ui/app.py` que no diferenciaba el lote acotado en memoria activa del corpus acumulado en SQLite.
- **Estado de Causa Raíz:** **CONFIRMADA**
- **Corrección Implementada:** Se renombró la tarjeta y el metadato formal a `Fragmentos del Lote Activo (ADR-012)`, y se documentó explícitamente en el pie que representa la ventana técnica procesada.
- **Reprueba Ejecutada:** `TEST-13`, `TEST-30`, `TEST-42` reejecutadas (PASS). Se constató la diferenciación nítida entre lote activo (80), tamaño estimado del documento (1207) y corpus global (3020).
- **Evidencia:** `docs/qa/evidence/area_03/DEF-06_before.png` y `docs/qa/evidence/area_03/DEF-06_after.png`.
- **Criterio de Cierre Cumplido:** Distinción inequívoca entre métricas de lote y métricas de corpus; cero rotulación confusa o inflada.
- **Estado:** **CERRADO**

---

### DEF-07
- **TEST-ID Origen:** `TEST-68`
- **Área:** Trazabilidad PMO y Gobernanza
- **Tipo:** Trazabilidad / Sincronización de Deployment
- **Clasificación:** SOPORTE / UX / ARQUITECTURA
- **Fuente del Criterio:** AUDITORÍA DE COORDINACIÓN EN INSTANCIA PÚBLICA (HALLAZGO 3)
- **Severidad:** **P2 · MEDIO**
- **Descripción:** La instancia pública desplegada mostraba `52/52, 52 tests pasando (18.43s)`, mientras la regresión formal del repositorio Shadow había elevado la suite automatizada a 55 pruebas pasando en 21.02s.
- **Causa Raíz:** Desincronización de deployment (Opción A). El componente de interfaz en `ui/app.py` lee dinámicamente el archivo `data/test_execution_report.json`. En el commit desplegado (`b61fcd3`), dicho archivo reflejaba la suite histórica de 52 pruebas del 19 de septiembre. Al no haberse publicado los commits locales a `origin/main`, el host no disponía del reporte de 55 pruebas.
- **Estado de Causa Raíz:** **CONFIRMADA (Causa A: Deployment ejecutando commit anterior)**
- **Corrección Implementada:**
  1. Se verificó que `ui/app.py` mantiene enlace dinámico hacia `data/test_execution_report.json` sin valores hardcodeados.
  2. Se incorporó `TEST-68` al plan de pruebas para auditar la correspondencia entre la suite en disco y el renderizado en interfaz.
  3. Se sincronizó el repositorio remoto de producción mediante `git push origin main` con el commit `41bce04` conteniendo el reporte de 55 pruebas.
- **Reprueba Instrumental:** Verificación local demostró que la tarjeta renderiza de forma reactiva `55/55` y `55 tests pasando (21.02s)`.
- **Evidencia:** `data/test_execution_report.json`, `docs/qa/evidence/final_regression/tab3_kpis_cards_centered.png`.
- **Criterio de Cierre Formal:** Renderizado de la medición reactiva actualizada a 55/55 visible en la instancia pública autenticada.
- **Estado:** **ABIERTO (CORREGIDO EN CÓDIGO `41bce04` / DESPLEGADO / EN VERIFICACIÓN PÚBLICA)**

---

### IMP-01 (Propuesta de Mejora Integrada)
- **TEST-ID Origen:** `TEST-31`
- **Área:** Experiencia de Estudio
- **Tipo:** Accesibilidad / Ergonomía
- **Severidad:** **P3 · FORMA**
- **Descripción:** La animación de flip 3D en flashcards requería clic directamente sobre el marco de la tarjeta, lo que en dispositivos móviles o con lectores de pantalla reducía la accesibilidad.
- **Mejora Implementada:** Se incorporó un botón alternativo accesible `Voltear Tarjeta` ubicado inmediatamente debajo de cada flashcard, permitiendo activar la rotación mediante teclado o interfaz táctil sin interferir con la tarjeta principal.
- **Estado:** **ACEPTADO COMO MEJORA**
