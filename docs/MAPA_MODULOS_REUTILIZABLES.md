# 🗺️ MAPA DE REUTILIZACIÓN DE MÓDULOS TÉCNICOS
### Guía de Transferencia para Squad 1 (Stack: React + FastAPI)

**Proyecto:** NuevaMente (NewMind)  
**Hackathon:** ONE G10 (Oracle Next Education & Alura)  
**Coordinador General & PM:** Martin Morfe  

---

## 1. Visión General de la Transferencia

Para evitar que Squad 1 comience desde cero o cometa errores en la estructuración de tipos, chunking o prompts, el prototipo de referencia provee una base de código probada y desacoplada. 

La arquitectura de Squad 1 separará el sistema en dos capas:
- **Backend:** FastAPI (Python 3.11+)
- **Frontend:** React (Vite, TypeScript, Tailwind CSS, Shadcn UI)

A continuación se detalla el inventario módulo por módulo clasificado entre **Copiables Directamente** y **Solo Referencia Arquitectónica**.

---

## 2. Inventario Módulo por Módulo

| Módulo / Archivo en Prototipo | Clasificación | Destino en Squad 1 (FastAPI + React) | Descripción y Utilidad Directa |
| :--- | :---: | :--- | :--- |
| [`src/schemas/adaptation.py`](src/schemas/adaptation.py) | 🟢 **COPIABLE DIRECTO** | `backend/app/schemas/adaptation.py` | Modelos Pydantic v2 estandarizados (`SolicitudAdaptacion`, `RespuestaAdaptacion`, `MetadatosAprendizaje`, enums de 10 sectores). Sirve directamente para validación de endpoints y OpenAPI (Swagger). |
| [`src/ingestion/loaders.py`](src/ingestion/loaders.py) | 🟢 **COPIABLE DIRECTO** | `backend/app/services/ingestion/loaders.py` | Extractores multiformato para PDF (`pypdf`), Markdown y texto plano con sanitización `clean_text` que preserva mayúsculas técnicas y siglas. |
| [`src/ingestion/chunker.py`](src/ingestion/chunker.py) | 🟢 **COPIABLE DIRECTO** | `backend/app/services/ingestion/chunker.py` | Algoritmo jerárquico calibrado a 1000 caracteres de tamaño y 150 de solapamiento para evitar fragmentar directivas indivisibles. |
| [`src/rag/vector_store.py`](src/rag/vector_store.py) | 🟢 **COPIABLE DIRECTO** | `backend/app/services/rag/vector_store.py` | Gestor de base vectorial persistente con ChromaDB y modelo `sentence-transformers/all-MiniLM-L6-v2`. |
| [`src/llm/prompts.py`](src/llm/prompts.py) | 🟢 **COPIABLE DIRECTO** | `backend/app/services/llm/prompts.py` | Prompts estructurales neutros basados en Taxonomía de Bloom y Andragogía de Knowles. 100% libres de contaminación de dominio. |
| [`src/llm/engine.py`](src/llm/engine.py) | 🟢 **COPIABLE DIRECTO** | `backend/app/services/llm/engine.py` | Orquestador multi-proveedor con `google-genai` primario, fallback defensivo a Mistral/NVIDIA/OpenAI y parser JSON tolerante a fallos. |
| [`src/quality/evaluator.py`](src/quality/evaluator.py) | 🟢 **COPIABLE DIRECTO** | `backend/app/services/quality/evaluator.py` | Algoritmo de cálculo de fidelidad documental (`anclaje_fuente_score >= 0.85`) combinando retención léxica y similitud en espacio latente. |
| [`src/storage/oci_storage.py`](src/storage/oci_storage.py) | 🟢 **COPIABLE DIRECTO** | `backend/app/services/storage/oci_storage.py` | Adaptador universal conmutable entre almacenamiento local, S3 compatible y OCI Object Storage Always Free. |
| [`src/algorithms/spaced_repetition.py`](src/algorithms/spaced_repetition.py) | 🟢 **COPIABLE DIRECTO** | `backend/app/services/algorithms/spaced_repetition.py` | Algoritmo matemático SuperMemo SM-2 para cálculo de intervalos y factores de facilidad en repasos activos de flashcards. |
| [`src/utils/exporters.py`](src/utils/exporters.py) | 🟢 **COPIABLE DIRECTO** | `backend/app/services/exporters/` | Generadores de mazos Anki CSV y guías didácticas formateadas en Markdown descargables desde endpoints de la API. |
| [`src/api/routes.py`](src/api/routes.py) | 🟡 **SOLO REFERENCIA** | `backend/app/api/v1/endpoints/` | Guía de cómo exponer los endpoints `/adapt`, `/upload` y `/health`. Debe refactorizarse para inyección de dependencias `Depends(get_db)` y CORS middleware. |
| [`ui/app.py`](ui/app.py) | 🟡 **SOLO REFERENCIA** | `frontend/src/components/` | Guía visual y de interacción funcional. Squad 1 no utilizará Streamlit, sino React. Este archivo define la UX de: formulario de 4 parámetros, tarjeta de flashcard con animación de giro 3D, visor de quiz con feedback visual y tabla de trazabilidad. |

---

## 3. Instrucciones de Integración para el Líder Técnico de Squad 1

1. **Copiar la carpeta `src/schemas/` íntegra:** Asegura que el backend y cualquier cliente TypeScript compartan la misma estructura de datos literal del pliego.
2. **Copiar los servicios RAG y Quality:** Permite que el equipo tenga resuelto el pipeline RAG desde el Día 1 sin tener que investigar qué tamaño de chunking o modelo de embeddings utilizar.
3. **Conectar el adaptador OCI:** Usar el modo `local` durante las primeras dos semanas de desarrollo y conmutar a `s3_compatible` con OCI en el Sprint 3 según el procedimiento de [`docs/EXCEPCION_ALMACENAMIENTO_OCI.md`](docs/EXCEPCION_ALMACENAMIENTO_OCI.md).

---
*Fin del Mapa de Módulos Reutilizables.*
