# KPICard
Tarjeta de métrica del Tablero PMO sobre panel glass: rótulo, cifra en `font-mono` 32/36 y pie con contexto.

- Estructura: `nm-glass nm-kpi` → `nm-overline` + `nm-kpi__val` + `nm-kpi__foot`.
- KPIs base: Costo OCI ($0.00 con sello `nm-oci` "Always Free"), Tests pasando, % Avance WBS (con `nm-bar`), Riesgos abiertos.
- Punto de estado `nm-dot`: `success` por defecto; `--tone` en `amber` o `danger` según el caso, siempre acompañado de texto.
- Cifras de la vista previa: datos de ejemplo. El consumidor las conecta a CI (tests), OCI Cost Analysis (costo) y su WBS.
