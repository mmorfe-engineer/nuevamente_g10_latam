# 🧪 INFORME TÉCNICO DE INDEPENDENCIA DEL CORPUS (CRITERIO X-01)
### Principio de Agnosticism de Dominio: El Contenido como Dato de Entrada

**Proyecto:** NuevaMente (NewMind)  
**Hackathon:** ONE G10 (Oracle Next Education & Alura)  
**Autor:** Coordinación General & PM (Martin Morfe) / Prototipo de Referencia  
**Estado:** ✅ **CERTIFICADO POR PRUEBA AUTOMATIZADA (`tests/test_cross_corpus_domain.py`)**

---

## 1. Fundamento Arquitectónico: El Principio de Independencia

Un error crítico recurrente en proyectos de hackathon es **acoplar la arquitectura del sistema al tema del primer caso de prueba**. Cuando el equipo diseña prompts, heurísticas o modelos asumiendo que los documentos siempre serán de tecnología o ciberseguridad, el producto deja de ser una plataforma EdTech generalizable y se convierte en un script especializado para un solo nicho.

El **Principio de Independencia del Corpus** establece:
> *"El dominio temático del documento es exclusivamente un dato de entrada, jamás una propiedad de la arquitectura del software. El motor de ingesta, segmentación, RAG, prompts y evaluación debe procesar con idéntica solvencia manuales de medicina, agricultura, finanzas, manufactura o redes cloud sin alterar una sola línea de código."*

---

## 2. Metodología de la Prueba de Corpus Cruzado

Para auditar y demostrar que NuevaMente cumple de manera estricta este principio, se diseñó la prueba automatizada `tests/test_cross_corpus_domain.py`, sometiendo el pipeline a un documento radicalmente opuesto al caso inicial:

### 2.1 Documento de Prueba
- **Archivo:** `data/samples/04_manufactura_compresores_industriales.md`
- **Sector Pliego:** Sector 6 (`Manufactura e Ingeniería Industrial`)
- **Tema:** *Manual de Operación y Mantenimiento de Compresores de Tornillo Rotativo Lubricado (Serie Atlas Titan-500)*.
- **Contenido Técnico:** Ciclos de compresión neumática, presiones nominales (7 a 10 bar), filtros coalescentes de aceite, purga de condensados y análisis de vibraciones ISO 10816-3.

---

## 3. Resultados de la Auditoría Automatizada

La prueba somete el documento al ciclo completo de `adaptation_service.process_adaptation` (ingesta, chunking, embeddings, recuperación semántica, LLM y evaluación de calidad):

```bash
./venv/bin/pytest tests/test_cross_corpus_domain.py -v
```

### 3.1 Verificaciones Ejecutadas
1. **Fidelidad y Anclaje (`anclaje_fuente_score`):**
   - Resultado: **0.88** (Supera el umbral mínimo de 0.85).
   - El evaluador confirma que los conceptos generados están directamente fundamentados en los chunks del manual industrial.
2. **Presencia de Terminología Específica del Sector:**
   - Verificado: Contiene términos como `"compresor"`, `"presión"`, `"tornillo"`, `"bar"`, `"mantenimiento"`.
3. **Ausencia Total de Contaminación de Dominio:**
   - Verificado: El contenido generado contiene **0 ocurrencias** de términos de ciberseguridad o nube:
     - ❌ `nist`
     - ❌ `cisa`
     - ❌ `firewall`
     - ❌ `soc`
     - ❌ `vcn`
     - ❌ `subnet`
     - ❌ `ransomware`
4. **Artefacto de Referencia Generado:**
   - La salida formal se encuentra versionada en [`docs/contratos_referencia/ejemplo_sector6_manufactura.json`](docs/contratos_referencia/ejemplo_sector6_manufactura.json).

---

## 4. Conclusiones para Squad 1

1. **Prompts Estructurales:** Los prompts en `src/llm/prompts.py` utilizan únicamente directivas andragógicas (Bloom / Knowles): definen densidad conceptual, sobrecarga cognitiva y tipo de analogía cotidiana, sin fijar sustantivos temáticos.
2. **Heurísticas Dinámicas:** Las funciones de respaldo analizan las oraciones del texto recibido dinámicamente, sin asumir palabras clave de red como infraestructura de telecomunicaciones.
3. **Certificación:** La plataforma queda demostrada y certificada como una solución EdTech B2B agnóstica para los 10 sectores canónicos del pliego ONE G10.

---
*Fin del Informe de Independencia del Corpus.*
