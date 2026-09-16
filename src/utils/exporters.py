"""
Módulo de Exportación Multiformato para NuevaMente (Diferencial Pedagógico).
Permite exportar contenidos a:
- Anki Deck CSV (tarjetas de memorización con tags)
- Markdown Didáctico formateado
"""
import csv
import io
from typing import List, Dict, Any
from src.utils.schemas import RespuestaAdaptacion


def export_to_anki_csv(items: List[Dict[str, Any]], deck_tag: str = "nuevamente_oci") -> str:
    """
    Genera un archivo CSV compatible con la importación estándar de Anki.
    Columnas: Frente, Dorso, Pista Didáctica, Tags
    """
    output = io.StringIO()
    writer = csv.writer(output, delimiter=";", quoting=csv.QUOTE_MINIMAL)
    
    # Cabecera estándar de Anki
    writer.writerow(["# Front", "Back", "Hint", "Tags"])
    
    for item in items:
        frente = item.get("frente", "").replace("\n", "<br>")
        dorso = item.get("dorso", "").replace("\n", "<br>")
        pista = item.get("pista_didactica", "").replace("\n", "<br>")
        tags = f"{deck_tag} edtech hackathon_one_g10"
        writer.writerow([frente, dorso, pista, tags])
        
    return output.getvalue()


def export_to_markdown_guide(resp: RespuestaAdaptacion) -> str:
    """
    Genera una Guía de Estudio estructurada en formato Markdown lista para impresión o visualización.
    """
    lines = [
        f"# {resp.contenido_adaptado.titulo}",
        f"**Perfil de Aprendizaje:** {resp.metadatos.perfil_aplicado}  ",
        f"**Formato Pedagógico:** {resp.metadatos.formato_generado}  ",
        f"**Tiempo Estimado de Estudio:** {resp.metadatos.tiempo_estimado_estudio_minutos} minutos  ",
        f"**Puntuación de Anclaje RAG (Grounding):** {int(resp.evaluacion_calidad.anclaje_fuente_score * 100)}%  ",
        f"**Almacenamiento OCI Always Free:** `{resp.almacenamiento_oci.bucket}/{resp.almacenamiento_oci.objeto_id}`  ",
        "",
        "---",
        "",
        "## 💡 Introducción Contextualizada",
        resp.contenido_adaptado.introduccion_contextualizada,
        "",
        "## 🏷️ Conceptos Clave",
        ", ".join([f"`{c}`" for c in resp.metadatos.conceptos_clave]),
        "",
        "---",
        "",
        "## 📖 Contenido Desarrollado",
        ""
    ]

    for idx, itm in enumerate(resp.contenido_adaptado.items):
        if "frente" in itm:
            lines.append(f"### Tarjeta #{idx+1}: {itm.get('frente')}")
            lines.append(f"**Explicación:** {itm.get('dorso')}")
            if itm.get("pista_didactica"):
                lines.append(f"> 🧭 **Pista Didáctica:** *{itm.get('pista_didactica')}*")
            lines.append("")
        elif "pregunta" in itm:
            lines.append(f"### Pregunta #{idx+1}: {itm.get('pregunta')}")
            for opt in itm.get("opciones", []):
                lines.append(f"- {opt}")
            lines.append(f"\n**Respuesta Correcta:** `{itm.get('respuesta_correcta')}`")
            lines.append(f"**Fundamentación Técnica:** {itm.get('justificacion_didactica')}")
            lines.append("")
        elif "titulo_paso" in itm:
            lines.append(f"### Paso {itm.get('paso', idx+1)}: {itm.get('titulo_paso')}")
            lines.append(itm.get("descripcion", ""))
            if itm.get("comando_o_codigo"):
                lines.append("```bash")
                lines.append(itm.get("comando_o_codigo"))
                lines.append("```")
            if itm.get("verificacion"):
                lines.append(f"🔍 *Verificación:* `{itm.get('verificacion')}`")
            lines.append("")
        else:
            lines.append(f"```json\n{itm}\n```\n")

    lines.extend([
        "---",
        "",
        "*Generado automáticamente por NuevaMente — Sistema de Adaptación Educativa Inteligente (Hackathon ONE G10 / Oracle Next Education)*"
    ])

    return "\n".join(lines)
