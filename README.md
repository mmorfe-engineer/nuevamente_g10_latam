# 🎓 NuevaMente — Sistema Inteligente de Adaptación y Generación de Contenido Educativo

[![Hackathon ONE G10](https://img.shields.io/badge/Hackathon-ONE%20G10%20%7C%20Alura%20%26%20Oracle-F80000?style=for-the-badge&logo=oracle)](https://www.oracle.com/lad/education/oracle-next-education/)
[![Costo Infraestructura](https://img.shields.io/badge/Costo%20Infraestructura-$0.00-blue?style=for-the-badge&logo=oracle)](https://www.oracle.com/cloud/free/)
[![Tests Passing](https://img.shields.io/badge/Pytest-52%2F52%20Passing%20(100%25)-brightgreen?style=for-the-badge&logo=pytest)](https://docs.pytest.org/)
[![Multi-Agent](https://img.shields.io/badge/Agents-LangGraph%20Multi--Agent-6366F1?style=for-the-badge)](https://langchain-ai.github.io/langgraph/)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![UI Streamlit](https://img.shields.io/badge/UI-Design%20System%20Dark%20Enterprise-FF4B4B?style=for-the-badge&logo=streamlit)](https://nuevamente.streamlit.app)
[![Storage](https://img.shields.io/badge/Storage-Universal%20S3%20%7C%20OCI%20Native-orange?style=for-the-badge)](https://aws.amazon.com/s3/)
[![Spaced Repetition](https://img.shields.io/badge/Algorithm-SuperMemo%20SM--2-purple?style=for-the-badge)](https://en.wikipedia.org/wiki/SuperMemo#SM-2_algorithm)

> 🚀 **PROTOTIPO DE REFERENCIA TÉCNICAMENTE CERRADO** (con dependencias externas declaradas)  
> Para la guía de adopción técnica por parte del equipo de desarrollo, consulta el [📦 Paquete de Transferencia Técnica para Squad 1](docs/PAQUETE_TRANSFERENCIA_PROYECTO_1.md) con la secuencia canónica de 12 commits, procedimiento de almacenamiento, bitácora de trampas resueltas y los 4 contratos JSON de referencia en [docs/contratos_referencia/](docs/contratos_referencia/).

---

## 📌 Visión General
**NuevaMente** es una plataforma SaaS EdTech de alto impacto desarrollada en el marco del **Hackathon ONE Grupo 10 (Oracle Next Education & Alura / No Country)**. Su misión es democratizar y acelerar el aprendizaje técnico ingiriendo documentaciones canónicas de alta densidad (manuales de arquitectura cloud, normativas de ingeniería, guías de ciberseguridad, especificaciones NIST, CIS y PCI-DSS) y transformándolas de manera automática en contenidos pedagógicos hiper-personalizados según el perfil cognitivo del estudiante, aplicando la **Taxonomía de Bloom**, la **Andragogía Laboral de Malcolm Knowles** y retención activa medible mediante el algoritmo **SuperMemo SM-2**.

La solución garantiza **fidelidad técnica rigurosa y mitigación de alucinaciones** a través de:
1. **Principio de Independencia del Corpus:** El dominio temático es dato de entrada, jamás arquitectura fija. Probado con éxito en Cloud OCI, Ciberseguridad y Manufactura Industrial (`tests/test_cross_corpus_domain.py`).
2. **Evaluación de Anclaje a la Fuente (`anclaje_fuente_score >= 0.85`):** Ponderación algorítmica de retención conceptual y similitud semántica.
3. **Regla de Nomenclatura Parentética Bilingüe:** `Término en Español [Término Canónico en Inglés]` para preservar correspondencia con la consola de Oracle Cloud.
4. **Adaptador Universal de Almacenamiento:** Conmutación sin fricción entre almacenamiento local, S3 compatible y OCI Object Storage.

---

## 🏗️ Arquitectura Integral del Sistema (C4 / Mermaid)

```mermaid
flowchart TB
    subgraph Ingestion ["1. Módulo de Ingestión & Deduplicación"]
        A["Documento Técnico: PDF / Markdown / TXT"] --> B["Extracción & Sanitización: PyPDF / Markdown / TXT"]
        B --> HASH["Cálculo Hash SHA-256 Deduplicación"]
        HASH --> C["Chunking Jerárquico Contextual: 1000 chars / 150 overlap"]
    end

    subgraph Storage ["2. Almacenamiento Conmutable (Universal Adapter)"]
        B -.->|Subida Documento Fuente| D[("Bucket: nuevamente-documentos-origen")]
        K[("Bucket: nuevamente-contenidos-educativos")]
    end

    subgraph RAG ["3. Pipeline RAG & Embeddings"]
        C --> E["Generación de Embeddings: all-MiniLM-L6-v2"]
        E --> F[("Vector Store: ChromaDB Persistente")]
        G["Parámetros del Estudiante & Consulta"] --> H["Retriever de Contexto Semántico"]
        F --> H
    end

    subgraph Orchestration ["4. Orquestación Pedagógica LLM & Grounding"]
        H --> I["Prompt Estructural Neutro: Taxonomía de Bloom & Perfil"]
        I --> J["Motor Multi-Proveedor: Google GenAI / Mistral / NVIDIA / OpenAI"]
        J --> L["Parser Tipado: Pydantic v2 Structured Output"]
        L --> Q["Evaluador de Calidad & Grounding Score"]
    end

    subgraph DB ["5. Persistencia Relacional SaaS (SQLAlchemy 2.0)"]
        L --> DB_ENG[("SQLite WAL / OCI Autonomous DB")]
        DB_ENG --- U["users"]
        DB_ENG --- TD["technical_documents"]
        DB_ENG --- KB["rag_knowledge_bases"]
        DB_ENG --- LS["learning_sessions"]
        DB_ENG --- FC["flashcards con SM-2"]
        DB_ENG --- QZ["quizzes y preguntas"]
    end

    subgraph Presentation ["6. Experiencia 'Deep Dev / Cyber-Modern'"]
        L --> K
        L --> M["Streamlit App / React Frontend: Glassmorphism & Neón"]
        M --> M1["Flashcards con Giro 3D & Algoritmo SM-2"]
        M --> M2["Visor de Quizzes con Feedback Inmediato"]
        M --> M3["Guía Didáctica Paso a Paso / Resumen Ejecutivo"]
        M --> M4["Exportador Multiformato: Anki CSV, Markdown, JSON ONE G10"]
    end
```

---

## 🎯 Cuatro Parámetros de Control (Requisito O-08)

| Dimensión | Opciones Soportadas | Enfoque Pedagógico |
| :--- | :--- | :--- |
| **1. Perfil del Destinatario** | • **Principiante**<br>• **Desarrollador Junior**<br>• **Arquitecto / Líder Técnico**<br>• **Ejecutivo / Gestor** | Calibración de sobrecarga cognitiva, metáforas cotidianas vs sistémicas, y profundidad técnica vs impacto de negocio. |
| **2. Formato Didáctico** | • **Flashcards 3D de Memorización**<br>• **Tutorial Paso a Paso (Guía Práctica)**<br>• **Resumen Ejecutivo (TL;DR)**<br>• *Quiz Interactivo Reactivo (Modo Avanzado)*<br>• *Guion de Video Didáctico (Modo Avanzado)* | Estructuras instruccionales alineadas a la **Taxonomía de Bloom** (Recordar, Comprender, Aplicar, Evaluar). |
| **3. Sector / Nicho (10 Sectores Canónicos)** | 1. Ciberseguridad & Gobernanza<br>2. Fintech & Banca Digital<br>3. Salud & Tecnología Médica (MedTech)<br>4. E-commerce & Retail Tech<br>5. Cloud & Infraestructura de TI<br>6. Manufactura e Ingeniería Industrial<br>7. Telecomunicaciones & Redes<br>8. LegalTech & Cumplimiento Normativo<br>9. EdTech & Formación Corporativa<br>10. General / Interdisciplinario | Contextualización semántica de analogías y casos reales al ámbito laboral específico. |
| **4. Nivel de Detalle** | • **Didáctico (Introductorio / Formativo)**<br>• **Técnico Profundo (Implementación)**<br>• **Estratégico (Gobernanza / Negocio)** | Regulación de la densidad analítica y complejidad del contenido generado. |

---

## 📦 Estructura de Salida JSON Estructurada (Pliego ONE G10)

```json
{
  "status": "exito",
  "metadatos": {
    "perfil_aplicado": "Principiante",
    "formato_generado": "Flashcards",
    "tiempo_estimado_estudio_minutos": 15,
    "conceptos_clave": [
      "Virtual Cloud Network (VCN) [Red Virtual en la Nube (VCN)]",
      "Subredes públicas y privadas",
      "Internet Gateway y NAT Gateway",
      "Security Lists [Listas de Seguridad]"
    ],
    "prerrequisitos": [
      "Conocimiento básico de redes informáticas",
      "Entendimiento de conceptos como IP, subred y firewall",
      "Familiaridad con Cloud Computing"
    ]
  },
  "contenido_adaptado": {
    "titulo": "Virtual Cloud Network (VCN) en OCI: Conceptos Básicos para Principiantes",
    "introduccion_contextualizada": "Imagina que necesitas crear tu propia oficina en la nube...",
    "items": [
      {
        "frente": "¿Qué es una Virtual Cloud Network (VCN) [Red Virtual en la Nube (VCN)]?",
        "dorso": "La VCN es una red privada y personalizable configurada en Oracle Cloud Infrastructure (OCI)...",
        "pista_didactica": "Piensa en la VCN como tu 'oficina en la nube': tú decides quién entra y cómo se organizan los equipos."
      }
    ]
  },
  "evaluacion_calidad": {
    "anclaje_fuente_score": 0.88,
    "claridad_pedagogica": "Alta",
    "observaciones": "Contenido adaptado para perfil Principiante. Anclaje riguroso en fuentes técnicas originales."
  },
  "almacenamiento_oci": {
    "bucket": "nuevamente-contenidos-educativos",
    "objeto_id": "contenido-introduccion-a-la-ar-principiante-flashcards-069c21.json",
    "status_upload": "completado"
  }
}
```

---

## 🔄 Conmutación Universal de Almacenamiento

El sistema conmuta de backend físico con una sola variable en `.env`:

```bash
# Opción A: Modo Local (Sin credenciales de red, almacena en ./data/storage_local/)
STORAGE_PROVIDER=local

# Opción B: Modo S3 Compatible (MinIO, Cloudflare R2, AWS S3 o Emulador)
STORAGE_PROVIDER=s3_compatible
OCI_S3_ENDPOINT_URL=https://<tenant_id>.compat.objectstorage.<region>.oraclecloud.com
OCI_S3_ACCESS_KEY_ID=<tu_access_key>
OCI_S3_SECRET_ACCESS_KEY=<tu_secret_key>

# Opción C: Modo OCI Nativo (Conexión OCI SDK)
STORAGE_PROVIDER=oci_native
OCI_CONFIG_FILE=~/.oci/config
```

---

## 🧪 Matriz de Verificación de Criterios Canónicos (O-01 a O-14, D-01 a D-05, X-01)

### Requisitos Obligatorios del Pliego (14)

| Criterio | Requisito Canónico | Estado | Evidencia Técnica |
| :--- | :--- | :---: | :--- |
| **O-01** | Ingestión funcional PDF, Markdown o texto | 🟢 VERIFICADO | `src/ingestion/loaders.py` (`extract_from_pdf`, `extract_from_markdown`, `extract_from_txt`) · `tests/test_ingestion.py` |
| **O-02** | RAG con segmentación, embeddings y Vector Store | 🟢 VERIFICADO | `src/ingestion/chunker.py` (1000/150 configurable) · `src/rag/vector_store.py` (ChromaDB) · `tests/test_rag_pipeline.py` |
| **O-03** | Orquestación de agentes o cadenas de prompts con LLM | 🟡 ABIERTA (Dependencia Externa) | Cliente migrado a `google-genai` listo en `src/llm/engine.py`; ejecución viva con proveedor LLM en producción abierta como dependencia externa pendiente de provisión de credencial por Squad 1. |
| **O-04** | Verificación de fidelidad al documento / mitigación de alucinaciones | 🟢 VERIFICADO | `src/quality/evaluator.py` (`anclaje_fuente_score >= 0.85`) · `tests/test_quality.py` |
| **O-05** | Mismo contenido adaptado a al menos 2 perfiles y 2 formatos | 🟢 VERIFICADO | Doble ejecución empírica sobre `05_pci_dss_v4_0`: Principiante/Flashcards y Arquitecto/Tutorial · `docs/contratos_referencia/` |
| **O-06** | JSON estructurado con status, metadatos, contenido_adaptado, evaluacion_calidad y almacenamiento_oci | 🟢 VERIFICADO | `src/utils/schemas.py` (`RespuestaAdaptacion` Pydantic v2) · `tests/test_schemas.py` |
| **O-07** | Metadatos de aprendizaje: conceptos, prerrequisitos y tiempo | 🟢 VERIFICADO | `src/utils/schemas.py` (`MetadatosAprendizaje`) · `tests/test_schemas.py` |
| **O-08** | Perfil, formato, nicho y nivel de detalle | 🟢 VERIFICADO | `ui/app.py` (Selectores de 4 parámetros en Paso 2) · `tests/test_ui_smoke.py` |
| **O-09** | Interfaz interactiva o API REST operativa | 🟢 VERIFICADO | `ui/app.py` (Interfaz interactiva Streamlit en 3 pasos con Design System Radix Dark y persistencia relacional) |
| **O-10** | Tipado estricto y manejo de excepciones con mensajes amigables | 🟢 VERIFICADO | `src/llm/engine.py` (conmutación defensiva multi-proveedor con fallback sintético local) · Pydantic v2 · `tests/test_llm_engine.py` |
| **O-11** | OCI Object Storage activo para originales y JSON | 🟠 ABIERTA (Dependencia Externa) | `docs/EXCEPCION_ALMACENAMIENTO_OCI.md` · Adaptador S3 conmutable local verificado; integración activa con OCI Object Storage abierta como dependencia externa. |
| **O-12** | Mínimo 3 ejemplos de ejecución | 🟢 VERIFICADO | `docs/contratos_referencia/` (5 contratos JSON versionados y autovalidados: VCN Flashcards, VCN Tutorial, IAM Resumen, Manufactura y Gemini) |
| **O-13** | Repositorio Git estructurado con commits claros y colaborativos | 🟢 VERIFICADO | GitHub `mmorfe-engineer/nuevamente_g10_latam` con historial estructurado de ramas y commits colaborativos por componente |
| **O-14** | README con arquitectura, diagrama RAG y guía de instalación | 🟢 VERIFICADO | `README.md` (Diagrama Mermaid C4/RAG, insignias, arquitectura técnica y guía de instalación paso a paso) |

### Capacidades Diferenciales de Alto Impacto (5)

| Criterio | Requisito Canónico | Estado | Evidencia Técnica |
| :--- | :--- | :---: | :--- |
| **D-01** | Quizzes con evaluación y retroalimentación en tiempo real | 🟢 VERIFICADO | `src/schemas/adaptation.py` · `ui/app.py` (evaluación interactiva de quizzes con justificación y citas al documento fuente) |
| **D-02** | Sistema multi-agente con LangGraph | 🟢 VERIFICADO | `src/agents/multi_agent_graph.py` (Investigador RAG, Redactor Pedagógico, Crítico/Revisor con traza visual) · `tests/test_multi_agent_graph.py` |
| **D-03** | Exportación Markdown/PDF/CSV compatible con Anki | 🟢 VERIFICADO | `src/exporters/anki.py` (CSV Anki), `src/exporters/markdown.py` (Guías MD) · `tests/test_exporters.py` |
| **D-04** | Despliegue completo sobre OCI Compute Always Free | 🟠 ABIERTA (Dependencia Externa) | Scripts y procedimiento de despliegue preparados; despliegue activo en OCI Compute pendiente de verificación. |
| **D-05** | Soporte multimodal para diagramas técnicos | 🟡 ABIERTA (Dependencia Externa) | Arquitectura y contratos preparados; interpretación multimodal directa de diagramas técnicos abierta para desarrollo del Squad 1. |

### Validación Interna de Robustez Arquitectónica (X-01 Interno)

| Criterio | Requisito Canónico | Estado | Evidencia Técnica |
| :--- | :--- | :---: | :--- |
| **X-01** | Control interno de independencia de corpus | 🟢 VERIFICADO | `docs/INFORME_INDEPENDENCIA_CORPUS.md` · `tests/test_cross_corpus_domain.py` (Sector 6: Manufactura de Compresores Industriales) |

---

## 🚀 Guía de Inicio Rápido

```bash
# 1. Clonar el repositorio
git clone https://github.com/mmorfe-engineer/nuevamente_g10_latam.git
cd nuevamente_g10_latam

# 2. Entorno virtual e instalación de dependencias
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Configuración de entorno
cp .env.example .env
# Configura tus API keys según disponibilidad (STORAGE_PROVIDER=local por defecto)

# 4. Ejecutar la suite de pruebas
pytest tests/ -v

# 5. Levantar la aplicación de referencia
streamlit run ui/app.py
```

---

## 👥 Equipo del Proyecto (Hackathon ONE G10 · No Country)

- **Martin Morfe** — *Project Manager & Coordinador General*
- **Esteban Guillermo Morales Velazquez** — *Software & Solution Architect (@Lead-Architect)*
- **Juan David Villegas Anaya** — *Backend & AI Developer (@Backend-AI-Dev)*
- **Harol Benjamin Medina Zárate** — *Cloud & Data Developer (@Cloud-Data-Dev)*
- **Heiner Jair Godoy Zamora** — *Cloud & Data Developer (@Cloud-Data-Dev)*
- **Cristian Contreras** — *Frontend & UI Developer (@Frontend-UI-Dev)*
- **Diana Castaño** — *Frontend & UI Developer (@Frontend-UI-Dev)*
- **Ivan Hernandez** — *DevOps & QA Engineer (@QA-DevOps-Dev)*

---

## 📄 Licencia y Marco Académico
Desarrollado con fines de impacto social y democratización formativa en América Latina bajo el programa **Oracle Next Education (ONE Grupo 10)**, **Alura Latam** y **No Country**.
