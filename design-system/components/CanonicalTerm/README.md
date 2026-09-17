# CanonicalTerm
Etiqueta de Nomenclatura Canónica Bilingüe: el concepto en español seguido de su nombre exacto en inglés, tal como aparece en la consola OCI o en la norma.

**Marcado:** `<span class="nm-term">Lista de Seguridad<span class="nm-term__en">Security List</span></span>` — los corchetes los dibuja el CSS; no los escribas en el texto.

**Reglas**
- Español en `ink` peso 600; inglés en `font-mono`, borde y texto `cyber`, radio `radius-sm`.
- El inglés se copia literal de la fuente (mayúsculas incluidas): `Security List`, no `security list`.
- Solo en la primera aparición por tarjeta/sección; repetirlo en cada línea satura.
- Nunca traducir nombres propios de producto: "OCI Vault", no "Bóveda OCI [OCI Vault]".
- Lector de pantalla: el consumidor añade `lang="en"` al span interno.
