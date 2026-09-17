# Sistema de Skills y Competencias

Tres marcos, una sola lógica: **NIST NICE** define *qué* debe saber cada rol, **Knowles** define *cómo* se enseña (problemas reales del puesto, no teoría) y **Kirkpatrick** define *cómo se demuestra*.

## Rutas de aprendizaje por rol

| Ruta | Rol | Token | Skills núcleo | Referencia NICE |
| --- | --- | --- | --- | --- |
| A | Taquilla y Operaciones | `track-ops` | Anti-phishing · Ingeniería social · Manejo de datos | Concienciación transversal (fuera de los Work Roles técnicos) |
| B | Desarrollador Junior | `track-dev` | Hardening de VCN en OCI · Reglas de firewall · APIs seguras | Desarrollo de Software Seguro [Secure Software Development] |
| C | Arquitecto & CISO | `track-arch` | Confianza Cero [Zero Trust] · Plan BCP · Ransomware | Arquitectura de Ciberseguridad [Cybersecurity Architecture] |
| D | Gestor de Proyectos & Auditor | `track-audit` | Riesgo de proveedores TI · Cumplimiento PCI DSS | Evaluación de Controles de Seguridad [Security Control Assessment] |

Verificar el ID exacto de cada Work Role en la versión vigente de los *NICE Framework Components* antes de publicarlo en la interfaz.

**Visual:** grilla de 4 TrackCard; al entrar a una ruta, su `--tone` tiñe rótulos, barra de avance y bordes activos de toda la vista. Estructura por ruta: Módulo → Lección → Flashcards + Quiz + Checklist.

## Insignias de dominio

| Nivel | Insignia | Color | Kirkpatrick | Evidencia |
| --- | --- | --- | --- | --- |
| 1 | Iniciado | `cyber` | Reacción | Ruta completada y valorada |
| 2 | Operador Seguro | `success` | Aprendizaje | Quiz ≥ 80 % y retención ≥ 85 % |
| 3 | Guardián Cloud | `quantum-soft` | Comportamiento | Checklist aplicado en el puesto, validado por supervisor |
| 4 | Arquitecto Certificado | `amber` | Resultados | Mejora medible del área (incidentes, hallazgos) |

Los niveles 3 y 4 no se ganan solo dentro de la app: requieren evidencia externa. Eso es lo que hace creíble la insignia ante un banco.

## Visualización SM-2

**Algoritmo (SuperMemo 2).** Tras cada repaso el usuario califica *q* ∈ {0…5}:
- Si *q* < 3: *n* = 0 e intervalo *I* = 1 día.
- Si *q* ≥ 3: *I*(1) = 1, *I*(2) = 6, *I*(n) = *I*(n−1) × *EF*.
- *EF′* = *EF* + (0.1 − (5 − q) × (0.08 + (5 − q) × 0.02)), con mínimo 1.3 e inicial 2.5.

**Fuerza de Retención (estimación de NuevaMente, no parte de SM-2).** SM-2 no produce un porcentaje; para mostrarlo se asume que el intervalo se agenda cuando la retención cae a ~90 %:

`R(t) = 0.9 ^ (t / I)` — *t* = días desde el último repaso.

| R | Estado | Tono del anillo |
| --- | --- | --- |
| ≥ 85 % | Estable | `quantum` |
| 70–84 % | Repasar hoy | `amber` |
| < 70 % | En riesgo | `danger` |

**Dónde se ve**
- *Flashcard (reverso):* anillo 48 px arriba a la derecha.
- *Barra SM-2:* bajo la tarjeta volteada; tras elegir *q*, la línea inferior anuncia "Próximo repaso óptimo · en N días".
- *Tablero:* anillo 72 px por módulo + lista "Para repasar hoy" ordenada por R ascendente.

## Esqueleto de pantalla de estudio

```
┌ Ruta B · Endurecimiento de la VCN ─────────────── [anillo 72%] ┐
│  Flashcard 3D (320×236)                                        │
│  Barra SM-2  0 1 2 3 4 5                                       │
│  Próximo repaso óptimo · en 6 días                             │
└──────────────────────────── [Ver fuente]  [Siguiente tarjeta] ┘
```
