# TrackCard
Tarjeta de una de las cuatro Rutas de Aprendizaje por rol, con sus skills y el avance del usuario.

- Clases: `nm-track nm-track--ops | --dev | --arch | --audit`. Cada modificador fija `--tone` desde `track-ops`, `track-dev`, `track-arch`, `track-audit`.
- El color de ruta solo toca el rótulo, la barra y el borde en hover; el cuerpo queda en `bg-800` para que las cuatro convivan sin ruido.
- Máximo 3 chips de skill visibles; el resto va al detalle de la ruta.
- El porcentaje se escribe siempre junto a la barra.
