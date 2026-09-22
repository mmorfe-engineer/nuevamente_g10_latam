# PLAN DE MEJORA Y ACCIÓN CORRECTIVA QA · NUEVAMENTE
**Entorno de Ejecución:** Repositorio Shadow (`mmorfe-engineer/nuevamente_g10_latam`)  
**Fecha de Consolidación:** 22 de Septiembre de 2026  
**Responsable de Gobierno:** PM & Lead QA Architect  
**Estado General:** EN EJECUCIÓN CONTROLADA  

---

## 1. PRINCIPIOS Y CRITERIOS DE GOBIERNO

1. **Custodia y Aislamiento Estricto:** Trabajo confinado exclusivamente al repositorio Shadow (`mmorfe-engineer/nuevamente_g10_latam`). Verificado mediante `~/protect_squad_repo.sh` (`CUSTODY_OK_SHADOW`). Prohibición absoluta de mutación sobre `No-Country-simulation/G10-team1-newmind`.
2. **Priorización por Impacto de Arquitectura y Estado:** El orden de resolución responde estrictamente a la criticidad técnica y ciclo de vida:
   - 1. Estado y ciclo de vida (P0)
   - 2. Integridad de resultados y medición (P1)
   - 3. Feedback de procesamiento en tiempo real (P1)
   - 4. Consistencia y balance visual/UX (P2)
   - 5. Mejoras de interacción aceptadas (P3)
3. **Cambio Mínimo y Trazable:** Cada defecto cuenta con causa raíz aislada y confirmada, corrección de alcance mínimo quirúrgico, pruebas de reprueba asignadas y criterios de cierre unívocos.
4. **No Incorporación de Alcance Nuevo:** No se crean endpoints no previstos ni se altera la arquitectura multi-agente LangGraph o el pipeline de embeddings de ChromaDB. Se corrigen defectos reproducidos y se valida su no-regresión.

---

## 2. MATRIZ DE PRIORIZACIÓN DE DEFECTOS Y MEJORAS

| Orden | DEF-ID | TEST-ID Origen | Área | Severidad | Clasificación | Hipótesis | Estado |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | **DEF-02** | `TEST-56`, `TEST-58` | Ciclo de Vida y Sesión | **P0 · CRÍTICO** | Estado y Ciclo de Vida | HIP-D | **EN CORRECCIÓN** |
| **2** | **DEF-06** | `TEST-13`, `TEST-30`, `TEST-42` | Medición y Partición | **P1 · ALTO** | Integridad de Resultados | HIP-H | **EN CORRECCIÓN** |
| **3** | **DEF-01** | `TEST-06` | Ingesta Documental | **P1 · ALTO** | Feedback de Procesamiento | HIP-A | **EN CORRECCIÓN** |
| **4** | **DEF-03** | `TEST-02` | Arranque / Cabecera | **P2 · MEDIO** | Consistencia Visual | HIP-E | **EN CORRECCIÓN** |
| **5** | **DEF-04** | `TEST-44` | Auditoría de Calidad | **P2 · MEDIO** | Consistencia Visual | HIP-F | **EN CORRECCIÓN** |
| **6** | **DEF-05** | `TEST-46` | Trazabilidad PMO | **P2 · MEDIO** | Consistencia Visual | HIP-G | **EN CORRECCIÓN** |
| **7** | **IMP-01** | `TEST-31` | Experiencia de Estudio | **P3 · FORMA** | UX / Accesibilidad | HIP-C | **ACEPTADO COMO MEJORA** |

---

## 3. FICHAS TÉCNICAS DETALLADAS DE INTERVENCIÓN

### DEF-02: Retención Residual de Estados, Desincronización y Bleeding entre Documentos
- **DEF-ID:** `DEF-02`
- **TEST-ID Origen:** `TEST-56` (Persistencia de Sesión y F5), `TEST-58` (Reinicio y Ciclo "Adaptar Nuevo Documento")
- **Área:** Ciclo de Vida y Sesión
- **Tipo:** Estado / Limpieza Residual
- **Clasificación de Alcance:** SOPORTE / UX / ARQUITECTURA
- **Fuente del Criterio:** HIPÓTESIS DE QA (HIP-D) / CONTRATO DE ESTADO STREAMLIT
- **Descripción:** Al accionar "Adaptar Nuevo Documento" (`btn_sidebar_reset`, `btn_tab1_reset`, `btn_tab1_reset_bottom`), la rutina solo ejecuta `del st.session_state["ultima_respuesta"]` y restablece `current_chunk_offset = 0`. Se retienen intactas las claves dinámicas `card_flipped_{i}` y `card_graded_{i}`. Al cargar un Documento B o conmutar de subida de archivo a texto libre, las tarjetas del Documento A permanecen en memoria o las calificaciones SM-2 previas se aplican indebidamente a los nuevos contenidos generados.
- **Impacto Observable:** Desincronización crítica entre el documento activo indicado en el sidebar y las flashcards mostradas en pantalla; persistencia de calificaciones previas en tarjetas recién generadas; imposibilidad de garantizar que una ejecución pertenezca exclusivamente al documento en análisis.
- **Severidad:** **P0 · CRÍTICO** (Invalida la integridad del ciclo de vida y los datos de la sesión de estudio).
- **Causa Raíz:**
  1. Ausencia de un método centralizado de invalidación de estado de adaptación en `ui/app.py`.
  2. Acumulación sin purga de claves de interacción dinámicas (`card_flipped_*`, `card_graded_*`) en `st.session_state`.
  3. Falta de hook de invalidación cuando se detecta un nuevo archivo cargado (`ultimo_archivo_cargado != up_file.name`) o cambio en `input_modo`.
- **Estado de Causa Raíz:** **CONFIRMADA**
- **Corrección Propuesta:**
  1. Implementar función centralizada `reset_adaptation_session(clear_document: bool = False)` en `ui/app.py`.
  2. Purgar determinísticamente `ultima_respuesta`, `ultimo_request`, `ultimo_trace`, `current_chunk_offset` y todas las claves iterables que comiencen con `card_flipped_` y `card_graded_`.
  3. Invocar `reset_adaptation_session(clear_document=False)` en todos los botones de reset (`btn_sidebar_reset`, `btn_tab1_reset`, `btn_tab1_reset_bottom`).
  4. Invocar `reset_adaptation_session()` al detectar cambio de archivo cargado en el header del uploader.
- **Archivos/Componentes Afectados:** `ui/app.py`
- **Dependencias de la Corrección:** Ninguna (módulo autocontenido en la capa UI).
- **Riesgo de Regresión:** Bajo. Se asegura que la persistencia en base de datos (repositorios de flashcards y sesiones) no se altere; solo se purga el estado volátil del navegador.
- **TEST-ID de Reprueba:** `TEST-56`, `TEST-58`, `tests/test_session_lifecycle_regression.py` (automatizado).
- **Pruebas Relacionadas a Reejecutar:** `TEST-24` (Flashcards render), `TEST-30` (Calificación SM-2), `TEST-57` (Navegación entre pestañas).
- **Criterio Exacto de Cierre:** Al accionar el botón de reinicio o cambiar de documento, `st.session_state` queda desprovisto de claves `card_*` y `ultima_respuesta`; la vista de bienvenida se monta limpia; y un nuevo documento genera flashcards sin estados de volteo ni calificaciones heredadas.
- **Estado:** **EN CORRECCIÓN**

---

### DEF-06: Ambigüedad en Rotulado de Fragmentos (Lote Activo ADR-012 vs Corpus Completo)
- **DEF-ID:** `DEF-06`
- **TEST-ID Origen:** `TEST-13` (Partición y Chunking), `TEST-30` (Trazabilidad de Métricas), `TEST-42` (Conteo de Fragmentos)
- **Área:** Medición y Partición Documental / Trazabilidad
- **Tipo:** Trazabilidad / Integración / Semántica
- **Clasificación de Alcance:** SOPORTE / UX / ARQUITECTURA
- **Fuente del Criterio:** ADR-012 / HIPÓTESIS DE QA (HIP-H)
- **Descripción:** En la franja superior de KPIs de Tab 1, el número de fragmentos indexados en la corrida se rotula genéricamente como "Fragmentos del Corpus". Esto induce al usuario a creer que dicho número representa la totalidad de la base de datos (3.020 chunks) o la totalidad del documento (ej. 1.205 chunks en el PDF de Arquitectura), cuando en realidad representa el lote activo acotado por ADR-012 (máximo 80 fragmentos por ejecución).
- **Impacto Observable:** Confusión en la interpretación técnica del sistema; imposibilidad de constatar si el motor procesó el archivo completo o un subconjunto acotado; discrepancia aparente con los 3.020 fragmentos reportados en Tab 3.
- **Severidad:** **P1 · ALTO** (Compromete la trazabilidad y la veracidad de las métricas expuestas al usuario y evaluadores).
- **Causa Raíz:** Inconsistencia de diseño en la plantilla HTML de `ui/app.py` (líneas 250-254), donde se nombró "Fragmentos del Corpus" a la variable `chunks_idx` generada por la ventana deslizante de ADR-012.
- **Estado de Causa Raíz:** **CONFIRMADA**
- **Corrección Propuesta:**
  1. Modificar el rótulo en `ui/app.py` a: `"Fragmentos del Lote Activo (ADR-012)"`.
  2. Ajustar el texto descriptivo del pie para clarificar la proporción respecto a los chunks estimados del documento: `"{chunks_idx} procesados · Lote acotado de ventana (ADR-012)"`.
  3. Agregar tooltip explicativo formal: `"Fragmentos procesados en esta ejecución según límite de latencia y costos ADR-012 (máx. 80 chunks)."`.
- **Archivos/Componentes Afectados:** `ui/app.py`
- **Dependencias de la Corrección:** `ultimo_trace`, `documento_contenido`.
- **Riesgo de Regresión:** Nulo (ajuste semántico y visual en plantilla HTML).
- **TEST-ID de Reprueba:** `TEST-13`, `TEST-30`, `TEST-42`.
- **Pruebas Relacionadas a Reejecutar:** `TEST-46` (KPIs globales en Tab 3).
- **Criterio Exacto de Cierre:** El banner muestra inequívocamente "Fragmentos del Lote Activo (ADR-012)", diferenciando el lote procesado de los chunks totales del corpus (3.020) y del documento cargado.
- **Estado:** **EN CORRECCIÓN**

---

### DEF-01: Carga Asíncrona sin Feedback Contextual durante Extracción de PDFs Extensos
- **DEF-ID:** `DEF-01`
- **TEST-ID Origen:** `TEST-06` (Ingesta de Documento Técnico Extenso)
- **Área:** Ingesta Documental
- **Tipo:** UX / Rendimiento / Feedback
- **Clasificación de Alcance:** SOPORTE / UX / ARQUITECTURA
- **Fuente del Criterio:** HIPÓTESIS DE QA (HIP-A) / PRINCIPIOS DE FEEDBACK HEURÍSTICO
- **Descripción:** Durante la subida de documentos técnicos pesados (>20 páginas / >500 KB), el script de Streamlit bloquea la interfaz durante 3 a 8 segundos para la extracción de texto sin mostrar un spinner contextual en la zona de trabajo. La pantalla se atenúa (dimming) generando la impresión de bloqueo o falla del sistema.
- **Impacto Observable:** Incertidumbre en el usuario; riesgo de recarga forzada (F5) por percepción de congelamiento de la aplicación.
- **Severidad:** **P1 · ALTO** (Afecta severamente la percepción de fluidez y robustez en la primera interacción).
- **Causa Raíz:** Llamadas síncronas a `doc_loader.extract_from_file(tmp_file_path)` en `ui/app.py` sin envoltorio `st.spinner(...)` tanto en el bloque de sincronización inicial como en el uploader de Tab 1.
- **Estado de Causa Raíz:** **CONFIRMADA**
- **Corrección Propuesta:**
  1. Envolver la llamada `extract_from_file` en bloque `with st.spinner("Leyendo y preparando documento técnico..."):`.
  2. Implementar retroalimentación inmediata con mensaje descriptivo no porcentual (factual).
- **Archivos/Componentes Afectados:** `ui/app.py`
- **Dependencias de la Corrección:** `doc_loader` (extractor de pypdf/markdown).
- **Riesgo de Regresión:** Nulo.
- **TEST-ID de Reprueba:** `TEST-06`.
- **Pruebas Relacionadas a Reejecutar:** `TEST-04` (Carga de archivo oficial), `TEST-05` (Carga de PDF estándar).
- **Criterio Exacto de Cierre:** Al cargar un PDF pesado, la interfaz presenta de inmediato el spinner "Leyendo y preparando documento técnico..." hasta que la extracción finaliza y se montan las métricas previas.
- **Estado:** **EN CORRECCIÓN**

---

### DEF-03: Solapamiento y Recorte de Cabecera Institucional por Barra Fija de Streamlit
- **DEF-ID:** `DEF-03`
- **TEST-ID Origen:** `TEST-02` (Render Inicial y Encabezado de Marca)
- **Área:** Arranque e Inicialización
- **Tipo:** Visual / Consistencia
- **Clasificación de Alcance:** SOPORTE / UX / ARQUITECTURA
- **Fuente del Criterio:** HIPÓTESIS DE QA (HIP-E) / ENTORNO DESPLEGADO STREAMLIT CLOUD
- **Descripción:** En la vista desplegada pública de Streamlit, la barra de herramientas superior (`[data-testid="stHeader"]`) se fija con una altura de ~56px. Con el padding superior actual de `.block-container` (`padding-top: var(--space-16)` = 16px), la tarjeta institucional superior queda parcialmente solapada o con la parte superior del título "NuevaMente" visualmente recortada.
- **Impacto Observable:** Deterioro de la imagen corporativa del producto y sensación de desajuste responsivo en la pantalla principal.
- **Severidad:** **P2 · MEDIO** (Defecto visual de alta visibilidad en el primer pantallazo).
- **Causa Raíz:** En `ui/assets/styles.css` (línea 179), la regla para `.block-container` define `padding-top: var(--space-16) !important;`, insuficiente para compensar la barra fija de Streamlit Cloud.
- **Estado de Causa Raíz:** **CONFIRMADA**
- **Corrección Propuesta:**
  1. Actualizar `padding-top` en `.block-container` a `clamp(3rem, 5vh, 4.5rem) !important;` (48px - 64px) en `ui/assets/styles.css`.
  2. Asegurar que en viewport móvil y desktop la tarjeta de marca conserve un margen superior respirable de al menos 16px respecto a los controles del navegador y barra de estado.
- **Archivos/Componentes Afectados:** `ui/assets/styles.css`
- **Dependencias de la Corrección:** Ninguna.
- **Riesgo de Regresión:** Nulo.
- **TEST-ID de Reprueba:** `TEST-02`.
- **Pruebas Relacionadas a Reejecutar:** `TEST-01` (Carga limpia en frío), `TEST-64` (Responsividad mobile).
- **Criterio Exacto de Cierre:** El wordmark "NuevaMente" y su subtítulo son 100% visibles sin solapamiento ni recorte bajo la barra de Streamlit en cualquier resolución.
- **Estado:** **EN CORRECCIÓN**

---

### DEF-04: Confinamiento Tipográfico Asimétrico a 70ch en Tarjetas Anchas de Metodología
- **DEF-ID:** `DEF-04`
- **TEST-ID Origen:** `TEST-44` (Fundamento Metodológico del Puntaje de Anclaje)
- **Área:** Auditoría de Calidad
- **Tipo:** Visual / Tipografía
- **Clasificación de Alcance:** SOPORTE / UX / ARQUITECTURA
- **Fuente del Criterio:** HIPÓTESIS DE QA (HIP-F) / GUÍA DE ESTILOS SHADOW
- **Descripción:** En Tab 2, la tarjeta informativa de "Fundamento Metodológico del Puntaje de Anclaje" presenta su texto confinado a una columna estrecha a la izquierda, dejando más del 40% del ancho del contenedor en blanco en pantallas desktop de 1200px.
- **Impacto Observable:** Apariencia desbalanceada y truncada de la sección explicativa metodológica; desaprovechamiento del espacio útil de la tarjeta.
- **Severidad:** **P2 · MEDIO** (Afecta la legibilidad y la presentación prolija del documento técnico en Tab 2).
- **Causa Raíz:** Regla global en `ui/assets/styles.css` (línea 239): `p, .stMarkdown p { max-width: 70ch; }`, aplicada de manera uniforme sin excepción para bloques explicativos dentro de contenedores `.nm-glass`.
- **Estado de Causa Raíz:** **CONFIRMADA**
- **Corrección Propuesta:**
  1. Agregar en `ui/assets/styles.css` una regla de especificidad que permita a los párrafos dentro de tarjetas `.nm-glass` expandirse armónicamente: `.nm-glass p, .nm-glass .stMarkdown p { max-width: min(90ch, 100%); }`.
  2. Asegurar interlineado y jerarquía balanceada para lectura técnica fluida.
- **Archivos/Componentes Afectados:** `ui/assets/styles.css`
- **Dependencias de la Corrección:** Ninguna.
- **Riesgo de Regresión:** Nulo.
- **TEST-ID de Reprueba:** `TEST-44`.
- **Pruebas Relacionadas a Reejecutar:** `TEST-38` (Tab 2 Auditoría completa), `TEST-65` (Legibilidad responsive tablet/desktop).
- **Criterio Exacto de Cierre:** El texto de Fundamento Metodológico ocupa el ancho armónico de la tarjeta (hasta 90ch) eliminando el vacío asimétrico derecho en pantallas de 1200px.
- **Estado:** **EN CORRECCIÓN**

---

### DEF-05: Disparidad Geométrica y Falta de Flex Layout en Tarjetas KPI de Tab 3
- **DEF-ID:** `DEF-05`
- **TEST-ID Origen:** `TEST-46` (Dashboard PMO - Métricas de Infraestructura)
- **Área:** Trazabilidad PMO
- **Tipo:** Visual / Geometría de Componentes
- **Clasificación de Alcance:** SOPORTE / UX / ARQUITECTURA
- **Fuente del Criterio:** HIPÓTESIS DE QA (HIP-G) / GUÍA DE COMPONENTES SHADOW
- **Descripción:** En el tablero de Tab 3, las cuatro tarjetas KPI ("Cloud en esta Ejecución", "Tests Automatizados", "Almacenamiento", "Corpus en Base de Datos") presentan alturas verticales diferentes debido a variaciones en la longitud de las leyendas secundarias del pie (`.nm-kpi__foot`), luciendo desalineadas horizontalmente.
- **Impacto Observable:** Desalineación estética en la presentación de datos de gobierno ante la PMO.
- **Severidad:** **P2 · MEDIO** (Afecta la uniformidad visual del módulo de auditoría y métricas).
- **Causa Raíz:** Falta de una regla CSS formal para `.nm-kpi` que establezca `min-height`, `height: 100%`, y un layout `flex` vertical con `justify-content: space-between`.
- **Estado de Causa Raíz:** **CONFIRMADA**
- **Corrección Propuesta:**
  1. Definir formalmente la clase `.nm-kpi` en `ui/assets/styles.css`:
     ```css
     .nm-kpi {
       height: 100% !important;
       min-height: 124px !important;
       display: flex !important;
       flex-direction: column !important;
       justify-content: space-between !important;
     }
     [data-testid="column"] > div:has(.nm-kpi) {
       height: 100% !important;
     }
     ```
- **Archivos/Componentes Afectados:** `ui/assets/styles.css`
- **Dependencias de la Corrección:** Ninguna.
- **Riesgo de Regresión:** Nulo.
- **TEST-ID de Reprueba:** `TEST-46`.
- **Pruebas Relacionadas a Reejecutar:** `TEST-45` (Carga de Tab 3), `TEST-51` (Registro de artefactos).
- **Criterio Exacto de Cierre:** Las 4 tarjetas superiores de Tab 3 exhiben idéntica altura visual (124px) y sus pies (`.nm-kpi__foot`) quedan perfectamente alineados sobre una misma línea de base.
- **Estado:** **EN CORRECCIÓN**

---

### IMP-01: Incorporación del Botón Explícito de Volteo Híbrido en Flashcards
- **DEF-ID:** `IMP-01` (antigua `HIP-C`)
- **TEST-ID Origen:** `TEST-31` (Interacción y Volteo de Flashcards)
- **Área:** Experiencia de Estudio (Flashcards)
- **Tipo:** UX / Accesibilidad
- **Clasificación de Alcance:** SOPORTE / UX / ARQUITECTURA
- **Fuente del Criterio:** EVALUACIÓN TÉCNICA DE QA / CONTROL DE CAMBIOS
- **Descripción:** Se evaluó la conveniencia de conservar el botón secundario "Voltear Tarjeta" / "Ver Frente" (`btn_flip_{i}`) junto a la animación hover/checkbox CSS nativa.
- **Evaluación y Dictamen:**
  - **Descubribilidad:** Mejora ostensiblemente la comprensión de la tarjeta en dispositivos móviles y navegación táctil donde `:hover` no existe.
  - **Accesibilidad:** Permite operar el volteo mediante teclado (`Tab` + `Enter`), facilitando el acceso a usuarios que no interactúan con cursor.
  - **Riesgo / Regresión:** Ninguno. La tarjeta conserva ambas modalidades sincronizadas.
- **Dictamen de Gobierno:** **MEJORA UX ACEPTADA**. No se cataloga como defecto ni se retira. Queda incorporada formalmente a la especificación de producto.
- **Archivos/Componentes Afectados:** `ui/app.py` (componente flashcards conservado).
- **TEST-ID de Reprueba:** `TEST-31` (Resultado: **PASS**).
- **Estado:** **ACEPTADO COMO MEJORA**

---

## 4. EVALUACIÓN DE HIPÓTESIS PREVIAS (HIP-A a HIP-H)

| Hipótesis | Enfoque | Evaluación de Causa Raíz | Decisión / Acción en Plan |
| :---: | :--- | :--- | :--- |
| **HIP-A** | Ausencia de testigo de carga en ingesta pesada | **CONFIRMADA** (Llamada síncrona sin spinner) | Corregida vía `DEF-01` (`st.spinner`). |
| **HIP-B** | 4 fases de generación (¿reales o decorativas?) | **DESCARTADA COMO DEFECTO** (Eventos reales comprobados en callbacks de `adaptation_service`) | Mantenida intacta; las 4 etapas corresponden a invocaciones funcionales demostrables. |
| **HIP-C** | Botón de volteo en Flashcards (¿desviación o mejora?) | **ACEPTADA COMO MEJORA** | Mantenida e incorporada al catálogo vía `IMP-01`. |
| **HIP-D** | Persistencia residual / Bleeding entre documentos | **CONFIRMADA** (Invalidez incompleta de `st.session_state`) | Corregida vía `DEF-02` (`reset_adaptation_session`). |
| **HIP-E** | Encabezado "NuevaMente" cortado en prod | **CONFIRMADA** (Padding de 16px insuficiente para barra fija de 56px) | Corregida vía `DEF-03` (`clamp(3rem, 5vh, 4.5rem)`). |
| **HIP-F** | Fundamento metodológico asimétrico/estrecho | **CONFIRMADA** (Regla CSS global `max-width: 70ch`) | Corregida vía `DEF-04` (`max-width: min(90ch, 100%)`). |
| **HIP-G** | Tarjetas KPI de Tab 3 con alturas dispares | **CONFIRMADA** (Carencia de flex vertical y min-height) | Corregida vía `DEF-05` (Flex column + `min-height: 124px`). |
| **HIP-H** | Ambigüedad en rotulado de fragmentos (Lote vs Corpus) | **CONFIRMADA** (Rótulo confuso en `ui/app.py`) | Corregida vía `DEF-06` (Rotulado explícito ADR-012). |

---

## 5. ESTRATEGIA DE REPRUEBAS Y SUITE AUTOMATIZADA

1. **Repruebas Manuales y Visuales:**
   - `DEF-01`: Reejecución de `TEST-06` con archivo de 963k caracteres.
   - `DEF-03`: Reejecución de `TEST-02` en entorno desktop y emulación móvil.
   - `DEF-04`: Reejecución de `TEST-44` en resolución 1200px.
   - `DEF-05`: Reejecución de `TEST-46` en Tab 3.
   - `DEF-06`: Reejecución de `TEST-13`, `TEST-30` y `TEST-42`.
2. **Reprueba Automatizada de Regresión:**
   - Se crea `tests/test_session_lifecycle_regression.py` para validar programáticamente el aislamiento de sesiones, la función `reset_adaptation_session()` y la no persistencia de claves dinámicas entre adaptaciones.
   - Ejecución de la suite total: `venv/bin/pytest tests/`.
