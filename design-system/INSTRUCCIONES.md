# NuevaMente — Sistema de Diseño (paquete para Antigravity)

## Estructura
- `README.md` — Manual de marca (ADN, voz, taglines, pitch, paleta, tipografía, efectos).
- `guidelines/10-sistema-de-skills.md` — Rutas NIST NICE, insignias Kirkpatrick, fórmula SM-2.
- `tokens.json` — Fuente de verdad de los tokens (colores Dark/Light, tipografía, espaciado, radios, sombras).
- `tokens.css` — Variables CSS listas para usar (`--quantum`, `--cyber`, `--radius-lg`…). Tema oscuro por defecto; tema claro con `<html data-theme="light">`.
- `components/bundle.css` — Todo el UI kit (clases `nm-*`). Importa las Google Fonts.
- `components/<Componente>/README.md` — Reglas de uso de cada componente.
- `components/<Componente>/preview.html` — Marcado de referencia de cada componente.
- `preview/index.html` — Galería local de todos los componentes con botón de tema.

## Uso rápido en tu frontend
```html
<link rel="stylesheet" href="tokens.css">
<link rel="stylesheet" href="components/bundle.css">
<body class="nm-stage"> … </body>
```

## Ver la galería
Las vistas previas usan iframes, así que ábrela con un servidor local (no con doble clic):
```bash
npx serve .      # o: python -m http.server
```
y entra a `http://localhost:3000/preview/` (o `:8000/preview/`).

## Prompt sugerido para el agente de Antigravity
> Lee `README.md`, `guidelines/10-sistema-de-skills.md` y el README de cada carpeta en `components/`. Construye el frontend de NuevaMente usando solo las variables de `tokens.css` y las clases de `components/bundle.css`; no inventes colores ni tamaños fuera de los tokens. Si usas React, convierte cada `preview.html` en un componente conservando las clases `nm-*`.
