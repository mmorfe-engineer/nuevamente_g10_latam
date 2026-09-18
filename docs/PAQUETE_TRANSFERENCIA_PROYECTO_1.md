# 📦 PAQUETE DE TRANSFERENCIA TÉCNICA — PROYECTO NUEVAMENTE (v4)
### Prototipo de Referencia Asíncrono para Squad 1 · Hackathon ONE G10 (Oracle Next Education & Alura)

**Coordinador General & PM:** Martin Morfe  
**Repositorio Oficial:** [https://github.com/mmorfe-engineer/nuevamente_g10_latam](https://github.com/mmorfe-engineer/nuevamente_g10_latam)  
**Despliegue Continuo (CI/CD):** [https://nuevamente.streamlit.app](https://nuevamente.streamlit.app)  
**Estado:** Prototipo de Referencia Asíncrono Construido para Transferencia Técnica  

---

## 1. Índice de Documentos Entregables del Paquete de Transferencia

El paquete de transferencia está compuesto por los siguientes documentos técnicos especializados disponibles en este repositorio:

1. 📋 **Registro de Excepción de Almacenamiento (O-13):** [`docs/EXCEPCION_ALMACENAMIENTO_OCI.md`](EXCEPCION_ALMACENAMIENTO_OCI.md)  
   *Registro formal, procedimiento de conmutación paso a paso y salida de prueba automatizada archivada.*
2. 📊 **Decisión Técnica de Chunking (1000/150 vs 500/50):** [`docs/DECISION_TECNICA_CHUNKING.md`](DECISION_TECNICA_CHUNKING.md)  
   *Mediciones empíricas de fragmentación, efecto acantilado y datos que sustentan el estándar del proyecto.*
3. 🧪 **Informe de Independencia del Corpus (X-01):** [`docs/INFORME_INDEPENDENCIA_CORPUS.md`](INFORME_INDEPENDENCIA_CORPUS.md)  
   *Certificación del principio de agnosticismo de dominio con el manual de manufactura de compresores industriales.*
4. 🗺️ **Mapa Exhaustivo de Módulos Reutilizables:** [`docs/MAPA_MODULOS_REUTILIZABLES.md`](MAPA_MODULOS_REUTILIZABLES.md)  
   *Inventario módulo por módulo clasificando qué copiar directamente a FastAPI y qué tomar como referencia para React.*
5. 🗂️ **Directorio de Contratos JSON de Referencia:** [`docs/contratos_referencia/`](contratos_referencia/)  
   *Colección de 5 contratos versionados y autovalidados para pruebas de integración.*

---

## 2. Secuencia Canónica de los 12 Commits

El prototipo se construyó en una secuencia estricta de 12 pasos donde cada hito resuelve las dependencias del siguiente. La siguiente tabla documenta la secuencia exacta, su justificación arquitectónica y los riesgos técnicos que mitiga.

| # | Commit Hash | Mensaje Canónico | Componentes Clave | Racionalidad del Orden | Riesgo Mitigado |
| :-: | :--- | :--- | :--- | :--- | :--- |
| **01** | `723909b` | `chore: estructura, .env.example y dependencias` | `.env.example`, `requirements.txt`, `pyproject.toml`, estructura `src/` | Establecer los cimientos del entorno y dependencias fijas antes de escribir lógica. | Incompatibilidad de paquetes, versiones conflictivas de Pydantic/LangChain y falta de variables requeridas. |
| **02** | `0ee9c15` | `feat(schemas): contrato literal del pliego` | `src/schemas/adaptation.py`, `src/utils/schemas.py`, `tests/test_schemas.py` | Definir el contrato de datos antes del procesamiento para asegurar interoperabilidad entre backend y frontend. | Desalineación con el pliego oficial de Oracle ONE, payloads inconsistentes entre subsistemas y campos obligatorios omitidos (`prerrequisitos`). |
| **03** | `210ed99` | `feat(storage): adaptador conmutable con fallback local` | `src/storage/oci_storage.py`, `tests/test_oci_storage.py` | La capa de almacenamiento debe existir antes de la ingesta para persistir documentos fuente y resultados. | Bloqueo del desarrollo por falta de credenciales cloud, fallos de red en CI/CD y acoplamiento rígido a un solo proveedor. |
| **04** | `d69d68d` | `feat(ingestion): loaders multiformato y limpieza` | `src/ingestion/loaders.py`, `tests/test_ingestion.py` | Normalizar y limpiar textos heterogéneos (PDF, Markdown, TXT) antes de particionarlos. | Caracteres corruptos de extracción PDF, inyecciones de saltos de línea destructivos y errores de codificación UTF-8. |
| **05** | `a18cb40` | `feat(ingestion): segmentación con solapamiento` | `src/ingestion/chunker.py`, `tests/test_ingestion.py` | Garantizar retención semántica en los límites de cada fragmento antes de vectorizar. | Pérdida de contexto entre bordes de chunks ("cliff effect") que degrada las búsquedas del RAG. |
| **06** | `7814c66` | `feat(rag): vector store y recuperador` | `src/rag/vector_store.py`, `tests/test_rag_pipeline.py` | Configurar la base vectorial persistente (ChromaDB) antes de la orquestación del LLM. | Consultas LLM sin grounding documental, latencias excesivas y duplicación de embeddings en memoria. |
| **07** | `5c1126a` | `feat(llm): cliente con salida JSON forzada y parser defensivo` | `src/llm/engine.py`, `tests/test_llm_engine.py` | Robustecer el cliente LLM con fallback multi-proveedor (Gemini, Mistral, NVIDIA NIM, OpenAI) y parsing tolerante a fallos. | Ruptura de la aplicación por respuestas no-JSON, errores 429 de cuota o caídas de un proveedor específico. |
| **08** | `e4c28d8` | `feat(llm): prompts por perfil y formato, en lenguaje estructural` | `src/llm/prompts.py`, `tests/test_domain_contracts.py` | Diseñar directivas cognitivas estructuradas (Bloom/Knowles) independientes de cualquier dominio temático. | Contaminación de prompts con jerga de un solo nicho (ej. solo ciberseguridad), imposibilitando el uso en medicina, educación o manufactura. |
| **09** | `2fe63ab` | `feat(quality): anclaje a la fuente y metadatos de aprendizaje` | `src/quality/evaluator.py`, `tests/test_quality.py` | Integrar cálculo algorítmico de fidelidad técnica (`anclaje_fuente_score >= 0.85`) antes de exponer la interfaz gráfica. | Alucinaciones indetectadas del LLM y entrega de contenidos pedagógicamente deficientes sin métricas objetivas. |
| **10** | `e483f0d` | `feat(ui): cuatro parámetros y caso oficial precargado` | `ui/app.py`, `src/utils/exporters.py` | Construir la interfaz de usuario sobre el motor probado, con carga en 1-click del caso Oracle VCN y selector de 10 sectores. | Curva de aprendizaje empinada para evaluadores, formularios vacíos confusos y fallos de usabilidad durante la demo. |
| **11** | `fb5820f` | `test(domain): corpus cruzado con documento de otro sector` | `data/samples/04_manufactura_compresores_industriales.md`, `tests/test_cross_corpus_domain.py`, `docs/contratos_referencia/` | Someter el pipeline completo a un documento de un sector no relacionado (Sector 6: Manufactura) para certificar agnosticismo. | Falsa sensación de agnosticismo; fallas ocultas cuando el cliente carga documentos fuera del área de prueba inicial. |
| **12** | `2ac5366` | `docs: README, procedimiento, matriz y bitácora` | `README.md`, `docs/PAQUETE_TRANSFERENCIA_PROYECTO_1.md` | Consolidar toda la evidencia, lecciones aprendidas y contratos para el equipo que construirá la versión definitiva. | Pérdida de conocimiento adquirido, reimplementación de soluciones a errores ya resueltos y retrasos de coordinación. |

---

## 3. Matriz de Trazabilidad de Cumplimiento (Criterios O-01 a O-14 + X-01)

| Código | Requisito del Pliego | Estado | Evidencia de Verificación en el Repositorio |
| :--- | :--- | :---: | :--- |
| **O-01** | Ingesta de documentos técnicos en PDF, Markdown y Texto Plano | 🟢 **VERIFICADO** | [`src/ingestion/loaders.py`](../src/ingestion/loaders.py) (`extract_from_pdf`, `extract_from_markdown`, `extract_from_txt`). Verificado en [`tests/test_ingestion.py`](../tests/test_ingestion.py). |
| **O-02** | Limpieza y normalización de texto conservando terminología técnica | 🟢 **VERIFICADO** | [`src/ingestion/loaders.py`](../src/ingestion/loaders.py) (función `clean_text` preservando mayúsculas y siglas). Verificado en [`tests/test_ingestion.py`](../tests/test_ingestion.py). |
| **O-03** | Segmentación en fragmentos con solapamiento configurable | 🟢 **VERIFICADO** | [`src/ingestion/chunker.py`](../src/ingestion/chunker.py) (`HierarchicalChunker` 1000/150). Justificado en [`docs/DECISION_TECNICA_CHUNKING.md`](DECISION_TECNICA_CHUNKING.md). |
| **O-04** | Almacenamiento y recuperación vectorial semántica | 🟢 **VERIFICADO** | [`src/rag/vector_store.py`](../src/rag/vector_store.py) (ChromaDB + `all-MiniLM-L6-v2`). Verificado en [`tests/test_rag_pipeline.py`](../tests/test_rag_pipeline.py). |
| **O-05** | Adaptación pedagógica según los cuatro perfiles del pliego | 🟢 **VERIFICADO** | Contratos de referencia enlazados:<br>• Principiante: [`docs/contratos_referencia/ejemplo_01_vcn_principiante_flashcards.json`](contratos_referencia/ejemplo_01_vcn_principiante_flashcards.json)<br>• Arquitecto: [`docs/contratos_referencia/ejemplo_02_vcn_arquitecto_tutorial.json`](contratos_referencia/ejemplo_02_vcn_arquitecto_tutorial.json)<br>• Ejecutivo: [`docs/contratos_referencia/ejemplo_03_seguridad_ejecutivo_resumen.json`](contratos_referencia/ejemplo_03_seguridad_ejecutivo_resumen.json)<br>• Junior: [`docs/contratos_referencia/ejemplo_gemini_google_genai.json`](contratos_referencia/ejemplo_gemini_google_genai.json) y [`tests/test_domain_contracts.py`](../tests/test_domain_contracts.py). |
| **O-06** | Generación en los tres formatos mínimos (Flashcards, Tutorial, Resumen) | 🟢 **VERIFICADO** | [`src/schemas/adaptation.py`](../src/schemas/adaptation.py) (`FormatoSalida`: Flashcards, Tutorial, Resumen, Quiz, Video Script). Verificado en [`tests/test_schemas.py`](../tests/test_schemas.py). |
| **O-07** | Metadatos de aprendizaje con tiempo estimado, conceptos y prerrequisitos | 🟢 **VERIFICADO** | [`src/schemas/adaptation.py`](../src/schemas/adaptation.py) (`MetadatosAprendizaje` con `tiempo_estimado_estudio_minutos`, `conceptos_clave`, `prerrequisitos`). |
| **O-08** | Control de alucinaciones con anclaje a la fuente comprobable | 🟢 **VERIFICADO** | [`src/quality/evaluator.py`](../src/quality/evaluator.py) (`QualityEvaluator.build_quality_evaluation` y `anclaje_fuente_score >= 0.85`). Verificado en [`tests/test_quality.py`](../tests/test_quality.py). |
| **O-09** | Salida forzada en formato JSON estructurado y tipado | 🟢 **VERIFICADO** | [`src/llm/engine.py`](../src/llm/engine.py) (validación estricta Pydantic con `RespuestaAdaptacion`). Verificado en [`tests/test_llm_engine.py`](../tests/test_llm_engine.py). |
| **O-10** | Manejo de excepciones defensivo ante caídas de la API del LLM | 🟢 **VERIFICADO** | [`src/llm/engine.py`](../src/llm/engine.py) (Cadena multi-proveedor: Google GenAI ➔ Mistral ➔ NVIDIA NIM ➔ OpenAI ➔ Motor Sintético). |
| **O-11** | Interfaz de usuario con los cuatro parámetros de control requeridos | 🟢 **VERIFICADO** | [`ui/app.py`](../ui/app.py) (Selector de Perfil, Formato, 10 Sectores Canónicos y Nivel de Detalle). |
| **O-12** | Caso de evaluación precargado seleccionable en un solo clic | 🟢 **VERIFICADO** | [`ui/app.py`](../ui/app.py) (Botón de carga del caso Oracle VCN pág. 4 del pliego y los 3 escenarios de la pág. 6). |
| **O-13** | Almacenamiento de contenidos generados en OCI Object Storage | 🟠 **EXCEPCIÓN** | Documentada y certificada en [`docs/EXCEPCION_ALMACENAMIENTO_OCI.md`](EXCEPCION_ALMACENAMIENTO_OCI.md). Adaptador conmutable con prueba y salida archivada en [`tests/test_oci_storage.py`](../tests/test_oci_storage.py). |
| **O-14** | Suite de pruebas automatizadas que valide el flujo completo | 🟢 **VERIFICADO** | Suite automatizada en [`tests/`](../tests/) ejecutada con Pytest. |
| **X-01** | Independencia del corpus demostrada con sector no relacionado | 🟢 **VERIFICADO** | [`data/samples/04_manufactura_compresores_industriales.md`](../data/samples/04_manufactura_compresores_industriales.md) y reporte formal en [`docs/INFORME_INDEPENDENCIA_CORPUS.md`](INFORME_INDEPENDENCIA_CORPUS.md). |

---

## 4. Contratos de Referencia Versionados en `docs/contratos_referencia/`

1. **`ejemplo_01_vcn_principiante_flashcards.json`:** VCN Oracle para Principiante en formato Flashcards con pistas didácticas y prerrequisitos.
2. **`ejemplo_02_vcn_arquitecto_tutorial.json`:** VCN Oracle para Arquitecto en formato Guía Práctica paso a paso.
3. **`ejemplo_03_seguridad_ejecutivo_resumen.json`:** Gobernanza Cloud e Identidad IAM para Ejecutivo en formato Resumen Ejecutivo.
4. **`ejemplo_sector6_manufactura.json`:** Prueba de corpus cruzado sobre compresores rotativos industriales (Sector 6: Manufactura).
5. **`ejemplo_gemini_google_genai.json`:** Generación estructurada ejercitando el SDK oficial `google-genai` para el perfil Desarrollador Junior en formato Quiz.

---

## 5. Bitácora de Trampas Encontradas y Solucionadas

1. **Colisión Léxica de Dominio:** La presencia de `"red"` en un manual industrial de tuberías neumáticas activó erróneamente el generador de subredes VCN en la heurística de fallback. Se resolvió restringiendo la detección a `"red virtual"` y generando pasos dinámicos directamente de las oraciones del texto recibido.
2. **Contaminación de Dominio en Prompts:** Plantillas base que citaban "roles NIST NICE" o "ciberseguridad" forzaban analogías de malware en textos de agricultura o manufactura. Se eliminó todo sesgo temático en `src/llm/prompts.py`, adoptando lenguaje puramente estructural y andragógico (Bloom / Knowles).
3. **Omisión de Prerrequisitos en Metadatos:** El modelo de respuesta omitía el campo `prerrequisitos: List[str]` exigido por el pliego O-07. Se incorporó formalmente en `src/schemas/adaptation.py` y se conectó al prompt del LLM.
4. **Calibración de Anclaje a la Fuente:** Para textos cortos, la métrica penalizaba la expansión explicativa pedagógica. Se recalibró `src/quality/evaluator.py` midiendo la cobertura de conceptos de la fuente combinada con la distancia semántica en espacio latente.

---
*Fin del Paquete de Transferencia Técnica.*
