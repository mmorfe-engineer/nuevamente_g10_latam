# 🛡️ Corpus Canónico de Ciberseguridad Bancaria y Gobernanza Cloud
## Proyecto NuevaMente — Hackathon No Country / Oracle Next Education (ONE G10)

Este directorio contiene el corpus oficial de documentos primarios utilizado para alimentar la base de conocimiento RAG (Retrieval-Augmented Generation) y los flujos pedagógicos multi-agente de **NuevaMente**.

---

## 📊 Métricas Globales del Corpus
- **Total de Documentos Oficiales:** 7 documentos canónicos (formato PDF).
- **Volumen Total de Páginas:** 1,132 páginas de estándares técnicos oficiales.
- **Caracteres Extraídos por el Pipeline:** 2,440,022 caracteres.
- **Fragmentos Semánticos (Chunks):** 3,017 chunks procesados con trazabilidad por página.
- **Gobernanza:** 100% de neutralidad territorial e internacional (cero ataduras a leyes locales de un solo país).

---

## 📂 Mapeo de Documentos a los Casos de Uso del Piloto

| # | Archivo Normalizado | Emisor Oficial | Año / Versión | Páginas | Chunks | Caso de Uso en NuevaMente |
| :-: | :--- | :---: | :---: | :-: | :-: | :--- |
| **01** | `01_nist_sp_800_161r1_riesgo_proveedores_ti.pdf` | **NIST** (EE.UU. / Global) | 2022 (Rev. 1) | 325 págs | 1,068 | **Caso 1:** Integración de Proveedores TI y Evaluación de Riesgos de Seguridad en Contrataciones de Software (*Vendor Risk*). |
| **02** | `02_cisa_nsa_guia_phishing_antifraude.pdf` | **CISA / NSA / FBI** | 2023 | 14 págs | 37 | **Caso 2:** Onboarding y Concientización de Ciberseguridad para Personal de Agencias y Taquillas (Anti-phishing e Ingeniería Social). |
| **03** | `03_cis_oracle_cloud_infrastructure_v3_1_1.pdf` | **CIS / Oracle** | Julio 2026 (v3.1.1) | 222 págs | 376 | **Caso 3:** Despliegue de Infraestructura Segura en Oracle Cloud (VCN, Subnets, Security Lists e IAM). |
| **04** | `04_cisa_fbi_guia_stop_ransomware_bcp.pdf` | **CISA / MS-ISAC / FBI** | Octubre 2023 | 31 págs | 88 | **Caso 4:** Gobernanza de Datos, Plan de Continuidad de Negocio (BCP) y Protocolo de Respuesta ante Ransomware. |
| **05** | `05_pci_dss_v4_0_la_seguridad_bancaria.pdf` | **PCI SSC** (Oficial en Español) | Marzo 2022 (v4.0) | 399 págs | 1,187 | **Caso 5:** Auditoría de Control de Accesos, Privilegios Mínimos (RBAC) y Trazabilidad de Logs Bancarios. |
| **06** | `06_pci_dss_v4_0_a_v4_0_1_resumen_cambios.pdf` | **PCI SSC** | Agosto 2024 (v4.0.1) | 11 págs | 30 | **Diferencial Delta:** Auditoría de cambios regulatorios y entrenamiento diferencial (Changelog pedagógico). |
| **07** | `07_cis_oracle_saas_cloud_applications_v1_0_0.pdf` | **CIS / Oracle** | Noviembre 2025 (v1.0.0) | 130 págs | 231 | **Diferencial Enterprise:** Gobernanza y seguridad en aplicaciones SaaS y ERPs bancarios en la nube de Oracle. |

---

## 🛠️ Pipeline de Ingestión y Verificación
Para procesar o verificar la extracción de texto y fragmentación semántica de estos documentos:

```bash
# Ejecutar verificación de extracción y chunking con el entorno virtual
venv/bin/python -c "
from src.ingestion.loaders import DocumentLoader
from src.ingestion.chunker import DocumentChunker

chunker = DocumentChunker()
text = DocumentLoader.extract_from_file('data/fuentes_ciberseguridad/03_cis_oracle_cloud_infrastructure_v3_1_1.pdf')
chunks = chunker.split_text(text)
print(f'Procesados {len(chunks)} chunks de OCI Benchmark')
"
```
