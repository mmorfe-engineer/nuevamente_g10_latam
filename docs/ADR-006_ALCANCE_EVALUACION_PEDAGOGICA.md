# 📋 REGISTRO DE DECISIÓN DE ARQUITECTURA (ADR-006)
## Delimitación del Alcance de Evaluación Pedagógica: Exclusión del Modelo Kirkpatrick en el Prototipo de Referencia y Transferencia a Squad 1

- **Estado:** Aprobado / Decisión Canónica
- **Fecha:** 18 de Septiembre de 2026
- **Autor / Emite:** Coordinación General & PM (Martin Morfe) / Arquitectura de Referencia
- **Destinatario:** Squad 1 (Equipo de Continuidad y Escalamiento) & Evaluadores Hackathon ONE G10
- **Criterios de Pliego Asociados:** O-01, O-02, O-05, O-06, O-08, O-14

---

### 1. Contexto y Antecedentes

Durante las fases iniciales de diseño conceptual e ideación del kit de interfaz (Figma / Design System), se incorporaron componentes visuales basados en los 4 Niveles del **Modelo de Evaluación de Kirkpatrick** (*Nivel 1: Reacción, Nivel 2: Aprendizaje, Nivel 3: Comportamiento, Nivel 4: Resultados*), proponiendo un sistema de insignias hexagonales (Iniciado, Operador, Guardián, Arquitecto).

Posteriormente, en revisiones de aseguramiento de calidad (QA) y auditoría técnica del prototipo de referencia, se detectó que estas insignias permanecían en la pestaña de métricas como elementos meramente cosméticos o estáticos, sin telemetría ni cálculo funcional subyacente.

---

### 2. Planteamiento del Problema

1. **Inviabilidad Operativa en Tiempo Real:** Los niveles 3 (Comportamiento en el puesto laboral) y 4 (Resultados de negocio y ROI organizacional) del Modelo Kirkpatrick requieren semanas o meses de seguimiento longitudinal en entornos empresariales de producción. Es metodológicamente imposible medirlos de forma honesta en una sesión interactiva de software de 90 segundos o en una prueba de hackathon.
2. **Riesgo de Pérdida de Credibilidad Técnica:** Mostrar una insignia que declare "Nivel 4: Resultados / Especialista" sin una fórmula matemática o evidencia de telemetría real degrada la credibilidad del sistema ante el jurado evaluador y el PMO. Una métrica declarativa no verificable es una vulnerabilidad de rúbrica.
3. **Riesgo de Deuda Técnica y Desvío de Alcance (Scope Creep) para Squad 1:** Si el prototipo de referencia entrega componentes de Kirkpatrick sin implementar, Squad 1 heredaría la falsa expectativa o la carga técnica de intentar medir impacto organizacional en un SaaS cuyo foco de pliego es la ingestión documental RAG y la adaptación andragógica en 3 semanas.
4. **Discrepancia con el Pliego Oficial de Requisitos:** Ninguno de los 14 criterios obligatorios (O-01 a O-14) exige el Modelo Kirkpatrick. El pliego exige explícitamente:
   - Ingestión de documentos técnicos arbitrarios (O-01).
   - Adaptación a perfiles destinatarios (O-02, O-05).
   - Formatos didácticos interactivos con retención activa (O-06).
   - Ausencia de alucinaciones y anclaje estricto a la fuente original (O-08, O-14).
   - Despliegue costo cero en OCI Always Free (O-11).

---

### 3. Decisión Adoptada

Se aprueba formalmente y de manera irrevocable la siguiente directiva técnica:

1. **Exclusión Total del Modelo Kirkpatrick:** Se declara el Modelo Kirkpatrick **Fuera de Alcance (Out-of-Scope)** para el prototipo de referencia, la interfaz web y el paquete de transferencia técnica a Squad 1.
2. **Retiro Inmediato de Elementos Cosméticos en UI:** Se retiran las 4 insignias estáticas de Kirkpatrick de `ui/app.py` (Pestaña 2: Auditoría y Métricas de Calidad).
3. **Sustitución por Fundamento Metodológico Canónico:** En su lugar, la interfaz expone la definición concisa y el fundamento del **Puntaje de Anclaje a la Fuente (O-08)**:
   > *"El Puntaje de Anclaje (O-08) mide la fidelidad técnica del contenido adaptado contrastando la retención de terminología y conceptos clave del documento fuente frente a una base mínima del 85%. No evalúa satisfacción subjetiva ni niveles de impacto organizacional, sino la estricta ausencia de alucinaciones técnicas sobre el material original."*
4. **Retención Activa Delegada al Algoritmo SuperMemo SM-2 (O-06):** La evidencia de asimilación y repaso espaciado se canaliza íntegramente a través del algoritmo matemático estándar **SuperMemo SM-2** implementado en `src/pedagogy/spaced_repetition.py` y reflejado interactivamente en las Flashcards (calificaciones 0 a 5, cálculo de intervalos y Factor de Facilidad).

---

### 4. Consecuencias y Beneficios

- **Protección del Alcance de Squad 1:** Squad 1 recibe una base de código limpia y focalizada al 100% en los 14 criterios del pliego, sin ambigüedades sobre requerimientos fantasma.
- **Rigor y Verificabilidad:** Todas las métricas presentadas en pantalla (anclaje, latencia, SM-2, trazabilidad multi-agente) se derivan de ejecuciones reales en vivo o se presentan honestamente como `-- · Aún sin medir` antes de procesar.
- **Robustez ante el Jurado:** Ante cualquier consulta sobre evaluación pedagógica durante la defensa técnica, el equipo responde con precisión apoyado en este registro: la evaluación en NuevaMente es formativa, algorítmica (SM-2) y de fidelidad documental (O-08), no de impacto conductual externo.

---
*Fin del Registro de Decisión de Arquitectura ADR-006.*
