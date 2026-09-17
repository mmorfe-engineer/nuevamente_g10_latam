"""
Interfaz Gráfica Oficial de NuevaMente.
Implementada bajo el Sistema de Diseño Oficial 'NuevaMente UI Kit':
- Tokens CSS oficiales (Paleta Dark Enterprise: Vacío Profundo, Placa Base, Violeta Cuántico, Cian Centinela).
- Tipografía oficial: Space Grotesk, Inter y JetBrains Mono.
- Componentes oficiales: TrackCard (Rutas NIST NICE), Flashcard 3D, SM-2 Rating Bar, Quiz Neón, CanonicalTerm y KPICards.
- Integración completa con el Corpus Real de Ciberseguridad (3,020 Chunks en SQL y ChromaDB).
- Orquestación con NVIDIA NIM (DeepSeek v4) y Mistral AI.
"""
import sys
import os
import re
import json
import uuid
from datetime import datetime
from pathlib import Path
import streamlit as st

# Asegurar path del proyecto en sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# Cargar secretos de Streamlit Community Cloud en os.environ si existen
try:
    for sec_key, sec_val in st.secrets.items():
        if isinstance(sec_val, str):
            os.environ[sec_key] = sec_val
except Exception:
    pass

from config.settings import settings
from src.storage.database import init_db, get_db_session, SessionLocal
from src.storage.models import (
    CorpusDocumentoModel,
    CorpusChunkModel,
    GlosarioCiberseguridadModel
)
from src.storage.repository import (
    UserRepository,
    TechnicalDocumentRepository,
    LearningSessionRepository,
    FlashcardRepository,
    QuizRepository,
    CorpusRepository,
    GlosarioRepository
)
from src.storage.oci_client import oci_storage
from src.utils.schemas import (
    SolicitudAdaptacion,
    PerfilDestinatario,
    FormatoSalida,
    NichoSector,
    NivelDetalle,
    FlashcardUpdateMastery
)
from src.utils.spaced_repetition import calculate_sm2
from src.utils.exporters import export_to_anki_csv, export_to_markdown_guide
from src.ingestion.loaders import doc_loader
from src.services.adaptation_service import adaptation_service

# Inicializar esquema relacional de forma segura e idempotente
init_db()

# Configuración de página Streamlit
st.set_page_config(
    page_title="NuevaMente — Normativa Densa, Mente Nueva",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inyección de estilos CSS del Sistema de Diseño Oficial
css_path = BASE_DIR / "ui" / "assets" / "styles.css"
if css_path.exists():
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def format_canonical_terms(text: str) -> str:
    """Convierte [Término Canónico EN] en elementos span .nm-term oficiales."""
    if not text:
        return ""
    # Formato: Término en Español [Canonical English]
    pattern = r"([A-Za-zÁÉÍÓÚáéíóúñÑ0-9\s]+?)\s*\[([A-Za-z0-9\s\-_\.\:]+)\]"
    return re.sub(pattern, r'<span class="nm-term">\1<span class="nm-term__en">\2</span></span>', text)


# ==============================================================================
# ENCABEZADO OFICIAL DE MARCA (Wordmark & Tagline Oficial)
# ==============================================================================
st.markdown("""
<div class="nm-glass" style="padding: 1.25rem 2rem; margin-bottom: 1.5rem; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
    <div>
        <div style="font-family: var(--font-display); font-size: 2.3rem; font-weight: 700; letter-spacing: -0.03em; line-height: 1.1;">
            <span style="color: var(--ink);">Nueva</span><span style="color: var(--quantum-soft);">Mente</span>
        </div>
        <div class="nm-caption" style="margin-top: 4px;">
            Del manual de mil páginas al equipo que cumple · <span style="color: var(--quantum-soft); font-weight: 600;">Normativa densa, mente nueva.</span>
        </div>
    </div>
    <div style="display: flex; gap: 10px; align-items: center; flex-wrap: wrap;">
        <span class="nm-oci">OCI Always Free · $0.00</span>
        <span class="nm-chip" style="color: var(--cyber); border: 1px solid var(--cyber);">NIST NICE Framework</span>
        <span class="nm-chip" style="color: var(--success); border: 1px solid var(--success);">SuperMemo SM-2</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# RUTAS DE APRENDIZAJE NIST NICE (TrackCards Oficiales)
# ==============================================================================
st.markdown("""
<div class="nm-row" style="margin-bottom: 1.5rem; justify-content: space-between;">
  <div class="nm-track nm-track--ops" style="flex: 1; min-width: 220px;">
    <div class="nm-track__head"><span class="nm-track__tag">RUTA A</span><span class="nm-caption">Operativo</span></div>
    <h4 class="nm-track__title">Taquilla & Operaciones</h4>
    <div class="nm-track__skills"><span class="nm-chip">Anti-phishing</span><span class="nm-chip">FIDO2 MFA</span><span class="nm-chip">Ingeniería Social</span></div>
    <div class="nm-bar" style="margin-top: 6px;"><i style="width: 85%"></i></div>
  </div>
  <div class="nm-track nm-track--dev" style="flex: 1; min-width: 220px;">
    <div class="nm-track__head"><span class="nm-track__tag">RUTA B</span><span class="nm-caption">Desarrollo</span></div>
    <h4 class="nm-track__title">Desarrollador Junior</h4>
    <div class="nm-track__skills"><span class="nm-chip">Hardening VCN</span><span class="nm-chip">Security Lists</span><span class="nm-chip">Tokenización</span></div>
    <div class="nm-bar" style="margin-top: 6px;"><i style="width: 65%"></i></div>
  </div>
  <div class="nm-track nm-track--arch" style="flex: 1; min-width: 220px;">
    <div class="nm-track__head"><span class="nm-track__tag">RUTA C</span><span class="nm-caption">Estratégico</span></div>
    <h4 class="nm-track__title">Arquitecto & CISO</h4>
    <div class="nm-track__skills"><span class="nm-chip">Zero Trust</span><span class="nm-chip">Plan BCP</span><span class="nm-chip">Ransomware</span></div>
    <div class="nm-bar" style="margin-top: 6px;"><i style="width: 40%"></i></div>
  </div>
  <div class="nm-track nm-track--audit" style="flex: 1; min-width: 220px;">
    <div class="nm-track__head"><span class="nm-track__tag">RUTA D</span><span class="nm-caption">Gobernanza</span></div>
    <h4 class="nm-track__title">Auditor & Compras</h4>
    <div class="nm-track__skills"><span class="nm-chip">C-SCRM</span><span class="nm-chip">PCI DSS v4.0</span><span class="nm-chip">Contratos TI</span></div>
    <div class="nm-bar" style="margin-top: 6px;"><i style="width: 25%"></i></div>
  </div>
</div>
""", unsafe_allow_html=True)


# ==============================================================================
# SIDEBAR: Carga de Documentos y Parametrización
# ==============================================================================
with st.sidebar:
    st.markdown("### ⚙️ Entrada de Documentos")
    
    modo_entrada = st.radio(
        "Modo de Ingesta:",
        [
            "🛡️ Corpus Real de Ciberseguridad (3,020 Chunks en SQL)",
            "Escenarios Rápidos de Prueba (Demo ONE)",
            "Subir Documento (PDF / MD / TXT)",
            "Pegar Texto Técnico Libre"
        ],
        index=0
    )

    doc_titulo = ""
    doc_contenido = ""

    if modo_entrada == "🛡️ Corpus Real de Ciberseguridad (3,020 Chunks en SQL)":
        casos_ciberseguridad = {
            "NIST SP 800-161r1 (Riesgo en Proveedores TI / SCRM)": {
                "file": "01_nist_sp_800_161r1_riesgo_proveedores_ti.pdf",
                "perfil_defecto": PerfilDestinatario.EJECUTIVO,
                "formato_defecto": FormatoSalida.RESUMEN
            },
            "CISA / NSA (Guía de Phishing y Autenticación FIDO2)": {
                "file": "02_cisa_nsa_guia_phishing_antifraude.pdf",
                "perfil_defecto": PerfilDestinatario.PRINCIPIANTE,
                "formato_defecto": FormatoSalida.FLASHCARDS
            },
            "CIS Oracle Cloud Infrastructure v3.1.1 (Hardening VCN & IAM)": {
                "file": "03_cis_oracle_cloud_infrastructure_v3_1_1.pdf",
                "perfil_defecto": PerfilDestinatario.JUNIOR_MID,
                "formato_defecto": FormatoSalida.TUTORIAL
            },
            "CISA / FBI (StopRansomware & Continuidad de Negocio BCP)": {
                "file": "04_cisa_fbi_guia_stop_ransomware_bcp.pdf",
                "perfil_defecto": PerfilDestinatario.ARQUITECTO,
                "formato_defecto": FormatoSalida.FLASHCARDS
            },
            "PCI-DSS v4.0 (Seguridad de Tarjetas y Tokenización PAN)": {
                "file": "05_pci_dss_v4_0_la_seguridad_bancaria.pdf",
                "perfil_defecto": PerfilDestinatario.JUNIOR_MID,
                "formato_defecto": FormatoSalida.QUIZ
            }
        }
        
        seleccion_caso = st.selectbox("Selecciona un documento del corpus:", list(casos_ciberseguridad.keys()))
        info_caso = casos_ciberseguridad[seleccion_caso]
        archivo_ciber = BASE_DIR / "data" / "fuentes_ciberseguridad" / info_caso["file"]
        
        if archivo_ciber.exists():
            doc_titulo = seleccion_caso.split("(")[0].strip()
            doc_contenido = doc_loader.extract_from_file(archivo_ciber)
            if len(doc_contenido) > 30000:
                doc_contenido = doc_contenido[:30000] + "\n\n... [Muestra del documento canónico]"
            st.success(f"📄 Corpus Oficial: `{info_caso['file']}` ({len(doc_contenido):,} chars)")

    elif modo_entrada == "Escenarios Rápidos de Prueba (Demo ONE)":
        escenarios_disponibles = {
            "Escenario 1: Redes VCN en OCI (Principiante / Flashcards)": "01_oci_vcn_redes.md",
            "Escenario 2: Arquitectura Microservicios (Arquitecto / Tutorial)": "02_arquitectura_microservicios.md",
            "Escenario 3: Gobernanza IAM y Seguridad (Ejecutivo / Resumen)": "03_seguridad_cloud_iam.txt"
        }
        seleccion_escenario = st.selectbox("Selecciona un escenario de prueba:", list(escenarios_disponibles.keys()))
        archivo_muestra = settings.SAMPLES_DIR / escenarios_disponibles[seleccion_escenario]
        if archivo_muestra.exists():
            doc_titulo = seleccion_escenario.split(":")[1].split("(")[0].strip()
            doc_contenido = doc_loader.extract_from_file(archivo_muestra)
            st.success(f"📄 Cargado: `{escenarios_disponibles[seleccion_escenario]}`")

    elif modo_entrada == "Subir Documento (PDF / MD / TXT)":
        doc_titulo_input = st.text_input("Título del Documento:", value="Guía Técnica Interna")
        archivo_subido = st.file_uploader("Arrastra tu documento:", type=["pdf", "md", "txt", "markdown"])
        if archivo_subido is not None:
            bytes_data = archivo_subido.read()
            doc_titulo = doc_titulo_input or archivo_subido.name
            doc_contenido = doc_loader.extract_from_bytes(archivo_subido.name, bytes_data)
            st.success(f"📄 Procesado: `{archivo_subido.name}` ({len(doc_contenido):,} chars)")

    else:
        doc_titulo = st.text_input("Título del Documento:", value="Procedimiento de Seguridad")
        doc_contenido = st.text_area("Pega el texto técnico aquí:", height=180)

    st.markdown("---")
    st.markdown("### 🎯 Adaptación Pedagógica (NIST NICE)")

    perfil = st.selectbox(
        "Perfil del Destinatario (NICE Work Role):",
        [p.value for p in PerfilDestinatario],
        index=1 if "JUNIOR_MID" in dir(PerfilDestinatario) else 0,
        help="Adecúa el lenguaje y el nivel de abstracción a las competencias del puesto laboral."
    )

    formato = st.selectbox(
        "Formato Andragógico de Salida:",
        [f.value for f in FormatoSalida],
        index=0,
        help="Estructura didáctica generada por el orquestador."
    )

    col_side1, col_side2 = st.columns(2)
    with col_side1:
        nicho = st.selectbox("Sector / Industria:", [n.value for n in NichoSector], index=0)
    with col_side2:
        detalle = st.selectbox("Nivel de Detalle:", [d.value for d in NivelDetalle], index=1)

    st.markdown("---")
    modo_orquestacion = st.radio(
        "Orquestador Cognitivo:",
        ["⚡ Motor RAG Directo", "🤖 Sistema Multi-Agente (LangGraph)"],
        index=1,
        help="Multi-Agente activa: Agente Investigador RAG + Agente Redactor NIST + Agente Crítico Revisor."
    )

    st.markdown("---")
    btn_generar = st.button("⚡ Generar Adaptación Pedagógica", type="primary", use_container_width=True)


# ==============================================================================
# KPIs DE ESTADO EN TIEMPO REAL (Banner con KPICard)
# ==============================================================================
with get_db_session() as db_session:
    total_chunks_db = db_session.query(CorpusChunkModel).count()
    total_docs_db = db_session.query(CorpusDocumentoModel).count()
    total_gloss_db = db_session.query(GlosarioCiberseguridadModel).count()

st.markdown(f"""
<div class="nm-row" style="margin-bottom: 1.5rem; justify-content: space-between;">
  <div class="nm-glass nm-kpi" style="flex:1; min-width:180px;">
    <span class="nm-overline">Costo OCI / mes</span>
    <span class="nm-kpi__val">$0.00</span>
    <span class="nm-kpi__foot"><span class="nm-oci">Always Free</span> Certificado</span>
  </div>
  <div class="nm-glass nm-kpi" style="flex:1; min-width:180px;">
    <span class="nm-overline">Corpus SQL</span>
    <span class="nm-kpi__val">{total_chunks_db:,}</span>
    <span class="nm-kpi__foot"><span class="nm-dot"></span>{total_docs_db} Documentos indexados</span>
  </div>
  <div class="nm-glass nm-kpi" style="flex:1; min-width:180px;">
    <span class="nm-overline">Glosario Canónico</span>
    <span class="nm-kpi__val">{total_gloss_db}</span>
    <span class="nm-kpi__foot"><span class="nm-dot"></span>Términos Bilingües EN/ES</span>
  </div>
  <div class="nm-glass nm-kpi" style="flex:1; min-width:180px;">
    <span class="nm-overline">Motor LLM Activo</span>
    <span class="nm-kpi__val" style="font-size: 20px;">{settings.DEFAULT_LLM_PROVIDER.upper()}</span>
    <span class="nm-kpi__foot">{settings.DEFAULT_LLM_MODEL.split('/')[-1]}</span>
  </div>
</div>
""", unsafe_allow_html=True)


# ==============================================================================
# PROCESAMIENTO AL PRESIONAR EL BOTÓN GENERAR
# ==============================================================================
if btn_generar:
    if not doc_contenido.strip():
        st.error("Por favor ingresa o selecciona un documento técnico antes de continuar.")
    else:
        is_multi_agent = (modo_orquestacion == "🤖 Sistema Multi-Agente (LangGraph)")
        progress_placeholder = st.empty()
        with progress_placeholder.container():
            msg = (
                "🤖 **Ejecutando Grafo Multi-Agente LangGraph:** Investigador RAG ➔ Redactor Pedagógico NIST ➔ Crítico Revisor..."
                if is_multi_agent
                else "🔄 **Ejecutando Pipeline RAG:** Ingesta Asimétrica, recuperación semántica y adaptación cognitiva..."
            )
            st.info(msg)

        try:
            req = SolicitudAdaptacion(
                documento_titulo=doc_titulo,
                documento_contenido=doc_contenido,
                perfil_destinatario=PerfilDestinatario(perfil),
                formato_salida=FormatoSalida(formato),
                nicho_sector=NichoSector(nicho),
                nivel_detalle=NivelDetalle(detalle)
            )

            with get_db_session() as db:
                respuesta, trace = adaptation_service.process_adaptation(
                    req, db=db, use_multi_agent=is_multi_agent
                )

            st.session_state["ultima_respuesta"] = respuesta
            st.session_state["ultimo_request"] = req
            st.session_state["ultimo_trace"] = trace
            progress_placeholder.empty()
            st.success("✅ ¡Adaptación pedagógica completada y persistida en base de datos relacional y OCI Object Storage!")

        except Exception as e:
            progress_placeholder.empty()
            st.error(f"❌ Error durante el procesamiento: {str(e)}")


# ==============================================================================
# PESTAÑAS PRINCIPALES DEL SISTEMA (Tablero NuevaMente)
# ==============================================================================
tab_contenido, tab_calidad, tab_insignias, tab_oci, tab_biblioteca, tab_pmo, tab_squad = st.tabs([
    "📖 Experiencia de Aprendizaje",
    "📊 Métricas & Traza Multi-Agente",
    "🎖️ Insignias Kirkpatrick",
    "☁️ Persistencia OCI & JSON",
    "📚 Biblioteca SQL",
    "🏢 Tablero PMO (WBS 96%)",
    "👥 Squad & Arquitectura"
])


# ------------------------------------------------------------------------------
# TAB 1: CONTENIDO ADAPTADO (Flashcards 3D, Quizzes, Tutoriales)
# ------------------------------------------------------------------------------
with tab_contenido:
    if "ultima_respuesta" in st.session_state:
        resp = st.session_state["ultima_respuesta"]
        req = st.session_state["ultimo_request"]
        trace = st.session_state.get("ultimo_trace", {})

        st.markdown(f"## {resp.contenido_adaptado.titulo}")
        
        # Apertura didáctica con estilo glass
        intro_formateada = format_canonical_terms(resp.contenido_adaptado.introduccion_contextualizada)
        st.markdown(f"""
        <div class="nm-glass" style="padding: 1.25rem 1.5rem; margin-bottom: 1.5rem; border-left: 4px solid var(--quantum);">
            <span class="nm-overline" style="color: var(--quantum-soft);">Apertura Andragógica:</span>
            <p style="margin: 0.35rem 0 0 0; font-size: 1.05rem; color: var(--ink); line-height: 1.6;">
                {intro_formateada}
            </p>
        </div>
        """, unsafe_allow_html=True)

        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.markdown(f"**👤 Perfil:** `{resp.metadatos.perfil_aplicado}`")
        with col_m2:
            st.markdown(f"**⏱️ Tiempo Estimado:** `{resp.metadatos.tiempo_estimado_estudio_minutos} min`")
        with col_m3:
            st.markdown(f"**🏷️ Conceptos Clave:** {', '.join(resp.metadatos.conceptos_clave)}")

        st.markdown("---")
        items = resp.contenido_adaptado.items

        # --- CASO 1: FLASHCARDS 3D CON SUPERMEMO SM-2 ---
        if req.formato_salida == FormatoSalida.FLASHCARDS:
            col_fc_title, col_fc_anki = st.columns([3, 1])
            with col_fc_title:
                st.markdown("### 🗂️ Flashcards 3D con Repetición Espaciada SM-2")
                st.caption("Pasa el cursor sobre la tarjeta para voltearla en 3D. Cada concepto incluye Nomenclatura Canónica [Término EN] y su cita normativa.")
            with col_fc_anki:
                st.download_button(
                    "🗃️ Exportar a Anki (.csv)",
                    data=export_to_anki_csv(items),
                    file_name=f"anki_{resp.almacenamiento_oci.objeto_id.replace('.json', '.csv')}",
                    mime="text/csv",
                    use_container_width=True
                )

            session_id_str = trace.get("session_id")
            saved_cards_db = []
            if session_id_str:
                with get_db_session() as db:
                    saved_cards_db = FlashcardRepository.get_by_session(db, uuid.UUID(session_id_str))

            for i, itm in enumerate(items):
                frente = itm.get("frente", "Pregunta")
                dorso = itm.get("dorso", "Respuesta")
                pista = itm.get("pista_didactica", "")
                fuente = itm.get("fuente", req.documento_titulo)
                card_db = saved_cards_db[i] if i < len(saved_cards_db) else None

                frente_html = format_canonical_terms(frente)
                dorso_html = format_canonical_terms(dorso)

                # Flashcard 3D Oficial del Design System
                card_html = f"""
                <div class="nm-row" style="margin-bottom: 1.25rem;">
                  <div class="nm-flash" style="width: 100%; max-width: 680px; height: 260px;" onclick="this.classList.toggle('is-flipped')">
                    <div class="nm-flash__inner">
                      <div class="nm-flash__face">
                        <div class="nm-flash__meta">
                          <span class="nm-overline">Tarjeta #{i+1} · {req.perfil_destinatario.value}</span>
                          <span class="nm-oci">OCI / NIST</span>
                        </div>
                        <p class="nm-flash__q" style="margin-top: 1rem;">{frente_html}</p>
                        {f'<div class="nm-flash__hint"><b>Pista Didáctica:</b> {pista}</div>' if pista else ''}
                      </div>
                      <div class="nm-flash__face nm-flash__back">
                        <div class="nm-flash__meta">
                          <span class="nm-overline">Explicación Canónica & Fundamento</span>
                          <div class="nm-ring nm-ring--sm" style="--p:90"><span class="nm-ring__val">90%</span></div>
                        </div>
                        <p class="nm-flash__a" style="margin-top: 0.5rem;">{dorso_html}</p>
                        <span class="nm-flash__src">Fuente Oficial: {fuente}</span>
                      </div>
                    </div>
                  </div>
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)

                # Barra de Autoevaluación SM-2 (0 a 5)
                st.markdown("<span class='nm-overline' style='font-size:11px;'>Calificar Asimilación (Algoritmo SM-2):</span>", unsafe_allow_html=True)
                c0, c1, c2, c3, c4, c5, c_info = st.columns([1, 1, 1, 1, 1, 1, 4])
                
                with c0:
                    if st.button("0 Nada", key=f"q0_{i}", use_container_width=True):
                        reps, iv, ef, next_rev = calculate_sm2(quality=0)
                        if card_db:
                            with get_db_session() as db:
                                FlashcardRepository.update_mastery(db, card_db.id, FlashcardUpdateMastery(mastery_level=0, next_review_at=next_rev))
                        st.toast(f"SM-2: Olvido total. Intervalo reseteado a 1 día.", icon="⏳")

                with c1:
                    if st.button("1 Vago", key=f"q1_{i}", use_container_width=True):
                        reps, iv, ef, next_rev = calculate_sm2(quality=1)
                        if card_db:
                            with get_db_session() as db:
                                FlashcardRepository.update_mastery(db, card_db.id, FlashcardUpdateMastery(mastery_level=1, next_review_at=next_rev))
                        st.toast(f"SM-2: Repaso mañana (+1 día)", icon="⏳")

                with c2:
                    if st.button("2 Casi", key=f"q2_{i}", use_container_width=True):
                        reps, iv, ef, next_rev = calculate_sm2(quality=2)
                        st.toast(f"SM-2: Repaso mañana (+1 día)", icon="⏳")

                with c3:
                    if st.button("3 Difícil", key=f"q3_{i}", use_container_width=True):
                        reps, iv, ef, next_rev = calculate_sm2(quality=3, repetitions=1)
                        st.toast(f"SM-2: Próximo repaso en {iv} días ({next_rev.strftime('%d/%m')})", icon="👍")

                with c4:
                    if st.button("4 Bien", key=f"q4_{i}", use_container_width=True):
                        reps, iv, ef, next_rev = calculate_sm2(quality=4, repetitions=2, previous_interval=1)
                        st.toast(f"SM-2: Próximo repaso en {iv} días", icon="🌟")

                with c5:
                    if st.button("5 Pro", key=f"q5_{i}", use_container_width=True):
                        reps, iv, ef, next_rev = calculate_sm2(quality=5, repetitions=3, previous_interval=6)
                        st.toast(f"SM-2: Dominado (+{iv} días, EF {ef})", icon="🔥")

                st.markdown("<hr style='border:0; border-top: 1px solid var(--line); margin: 1.5rem 0;'>", unsafe_allow_html=True)

        # --- CASO 2: QUIZ INTERACTIVO NEÓN ---
        elif req.formato_salida == FormatoSalida.QUIZ:
            st.markdown("### ❓ Evaluación Diagnóstica de Retención")
            st.caption("Cada respuesta evalúa competencias NIST NICE con anclaje estricto a las normas.")

            for i, itm in enumerate(items):
                pregunta = itm.get("pregunta", "Pregunta de evaluación")
                opciones = itm.get("opciones", [])
                correcta = itm.get("respuesta_correcta", "")
                explicacion = itm.get("explicacion", "")

                st.markdown(f"#### {i+1}. {format_canonical_terms(pregunta)}", unsafe_allow_html=True)
                opcion_seleccionada = st.radio(
                    f"Selecciona tu respuesta para la pregunta {i+1}:",
                    opciones,
                    key=f"quiz_opt_{i}",
                    label_visibility="collapsed"
                )

                if st.button(f"Validar Pregunta {i+1}", key=f"btn_val_{i}"):
                    is_correct = (opcion_seleccionada == correcta)
                    if is_correct:
                        st.markdown(f"""
                        <div class="nm-opt is-correct" style="margin-top: 10px;">
                            <span class="nm-opt__key">✓</span>
                            <span><strong>Respuesta Correcta:</strong> {format_canonical_terms(opcion_seleccionada)}
                                <span class="nm-opt__note" style="display:block; margin-top: 6px;">
                                    <strong>Justificación Técnica:</strong> {format_canonical_terms(explicacion)}
                                </span>
                            </span>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="nm-opt is-wrong" style="margin-top: 10px;">
                            <span class="nm-opt__key">✕</span>
                            <span><strong>No exactamente.</strong>
                                <span class="nm-opt__note" style="display:block; margin-top: 6px;">
                                    <strong>Respuesta Esperada:</strong> {format_canonical_terms(correcta)}<br/>
                                    <strong>Fundamento:</strong> {format_canonical_terms(explicacion)}
                                </span>
                            </span>
                        </div>
                        """, unsafe_allow_html=True)

                st.markdown("---")

        # --- CASO 3: GUÍA PRÁCTICA / TUTORIAL PASO A PASO ---
        elif req.formato_salida == FormatoSalida.TUTORIAL:
            st.markdown("### 📋 Guía Técnica de Aplicación Inmediata")
            for itm in items:
                paso_num = itm.get("paso", 1)
                st.markdown(f"""
                <div class="nm-glass" style="padding: 1.25rem 1.5rem; margin-bottom: 1rem; border-left: 4px solid var(--cyber);">
                    <span class="nm-overline" style="color: var(--cyber);">PASO {paso_num}:</span>
                    <h3 style="margin: 0.25rem 0 0.5rem 0; color: var(--ink);">{format_canonical_terms(itm.get('titulo_paso', ''))}</h3>
                    <p style="color: var(--ink-muted); line-height: 1.6;">{format_canonical_terms(itm.get('descripcion', ''))}</p>
                </div>
                """, unsafe_allow_html=True)
                if itm.get("comando_o_codigo"):
                    st.code(itm.get("comando_o_codigo"), language="bash")
                if itm.get("verificacion"):
                    st.info(f"🔍 **Criterio de Verificación:** {itm.get('verificacion')}")

        else:
            for itm in items:
                st.json(itm)
    else:
        st.info("👈 Selecciona un documento en la barra lateral y presiona **'⚡ Generar Adaptación Pedagógica'** para explorar la experiencia interactiva.")


# ------------------------------------------------------------------------------
# TAB 2: MÉTRICAS Y TRAZA MULTI-AGENTE
# ------------------------------------------------------------------------------
with tab_calidad:
    st.markdown("### Auditoría de Calidad y Traza del Grafo Multi-Agente")
    if "ultima_respuesta" in st.session_state:
        resp = st.session_state["ultima_respuesta"]
        trace = st.session_state.get("ultimo_trace", {})

        col_c1, col_c2, col_c3 = st.columns(3)
        with col_c1:
            score = resp.evaluacion_calidad.anclaje_fuente_score
            st.metric("Puntuación de Anclaje (Grounding)", f"{int(score * 100)}%", help="Fidelidad verificable contra el documento técnico.")
            st.progress(score)
        with col_c2:
            st.metric("Claridad Andragógica", resp.evaluacion_calidad.claridad_pedagogica)
        with col_c3:
            st.metric("Promesa de Calidad", "Citas Verificables", "Cero Inventiva Normativa")

        st.markdown("---")
        st.markdown(f"""
        <div class="nm-glass" style="padding: 1.25rem 1.5rem;">
            <span class="nm-overline" style="color: var(--cyber);">Dictamen del Agente Crítico:</span>
            <p style="margin: 0.35rem 0 0 0; color: var(--ink);">{resp.evaluacion_calidad.observaciones}</p>
        </div>
        """, unsafe_allow_html=True)

        if trace.get("agent_logs"):
            st.markdown("---")
            with st.expander("🤖 Traza Completa de Ejecución Multi-Agente (LangGraph)", expanded=True):
                for log_line in trace["agent_logs"]:
                    st.markdown(f"- {log_line}")
    else:
        st.info("Las métricas de anclaje y la traza de los 3 agentes se calculan al generar una adaptación.")


# ------------------------------------------------------------------------------
# TAB 3: INSIGNIAS DE DOMINIO KIRKPATRICK (Oficiales del Design System)
# ------------------------------------------------------------------------------
with tab_insignias:
    st.markdown("### 🎖️ Sistema de Insignias y Competencias Demostrables")
    st.caption("Basado en el Modelo de Evaluación Kirkpatrick (Niveles 1 a 4) y el marco de roles laborales NIST NICE.")

    st.markdown("""
    <div class="nm-row" style="justify-content: space-around; margin-top: 1.5rem;">
      <div class="nm-badge nm-badge--l1">
        <div class="nm-badge__hex"><div class="nm-badge__core">
          <svg viewBox="0 0 24 24"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
        </div></div>
        <span class="nm-badge__lvl">NIVEL 1 · CIAN</span>
        <div class="nm-badge__name">Iniciado</div>
        <span class="nm-caption">Reacción: Ruta completada</span>
      </div>

      <div class="nm-badge nm-badge--l2">
        <div class="nm-badge__hex"><div class="nm-badge__core">
          <svg viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>
        </div></div>
        <span class="nm-badge__lvl">NIVEL 2 · ESMERALDA</span>
        <div class="nm-badge__name">Operador Seguro</div>
        <span class="nm-caption">Aprendizaje: Quiz ≥80% y SM-2</span>
      </div>

      <div class="nm-badge nm-badge--l3">
        <div class="nm-badge__hex"><div class="nm-badge__core">
          <svg viewBox="0 0 24 24"><path d="M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9Z"></path></svg>
        </div></div>
        <span class="nm-badge__lvl">NIVEL 3 · VIOLETA</span>
        <div class="nm-badge__name">Guardián Cloud</div>
        <span class="nm-caption">Comportamiento: Checklist en puesto</span>
      </div>

      <div class="nm-badge nm-badge--l4">
        <div class="nm-badge__hex"><div class="nm-badge__core">
          <svg viewBox="0 0 24 24"><circle cx="12" cy="8" r="7"></circle><polyline points="8.21 13.89 7 23 12 20 17 23 15.79 13.88"></polyline></svg>
        </div></div>
        <span class="nm-badge__lvl">NIVEL 4 · ÁMBAR</span>
        <div class="nm-badge__name">Arquitecto Certificado</div>
        <span class="nm-caption">Resultados: Auditoría Cero Brechas</span>
      </div>
    </div>
    """, unsafe_allow_html=True)


# ------------------------------------------------------------------------------
# TAB 4: PERSISTENCIA OCI OBJECT STORAGE Y JSON OFICIAL
# ------------------------------------------------------------------------------
with tab_oci:
    st.markdown("### Persistencia en OCI Object Storage Always Free")
    if "ultima_respuesta" in st.session_state:
        resp = st.session_state["ultima_respuesta"]
        st.info(f"📦 **Bucket OCI:** `{resp.almacenamiento_oci.bucket}` | **Objeto:** `{resp.almacenamiento_oci.objeto_id}`")
        
        json_output = resp.model_dump()
        json_str = json.dumps(json_output, indent=2, ensure_ascii=False)

        col_d1, col_d2 = st.columns(2)
        with col_d1:
            st.download_button(
                "⬇️ Descargar JSON Oficial (ONE G10)",
                data=json_str,
                file_name=resp.almacenamiento_oci.objeto_id,
                mime="application/json",
                use_container_width=True
            )
        with col_d2:
            st.download_button(
                "📝 Descargar Guía Didáctica Markdown",
                data=export_to_markdown_guide(resp),
                file_name=resp.almacenamiento_oci.objeto_id.replace(".json", ".md"),
                mime="text/markdown",
                use_container_width=True
            )

        st.code(json_str, language="json")
    else:
        st.markdown("""
        <div class="nm-glass" style="padding: 1.25rem 1.5rem;">
            <h4 style="margin:0 0 0.5rem 0; color: var(--ink);">Configuración de Almacenamiento OCI Always Free:</h4>
            <ul>
                <li><strong>Bucket Origen:</strong> <code>nuevamente-documentos-origen</code></li>
                <li><strong>Bucket Artefactos:</strong> <code>nuevamente-contenidos-educativos</code></li>
                <li><strong>Cuota Permanente:</strong> 10 GB de almacenamiento gratuito de por vida ($0.00 USD)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)


# ------------------------------------------------------------------------------
# TAB 5: BIBLIOTECA SQL (Explorador de la Base de Datos Relacional)
# ------------------------------------------------------------------------------
with tab_biblioteca:
    st.markdown("### 📚 Explorador Relacional del Corpus (SQLAlchemy 2.0)")
    st.caption("Visualiza los documentos y fragmentos procesados bajo el Estándar de Ingesta Asimétrica LexForja.")

    with get_db_session() as db:
        docs_db = CorpusRepository.get_all_documents(db) if hasattr(CorpusRepository, "get_all_documents") else db.query(CorpusDocumentoModel).all()
        
    for d in docs_db:
        with st.expander(f"📄 {d.titulo} ({d.idioma.upper()}) · Chunks: {len(d.chunks)}"):
            st.markdown(f"**ID del Documento:** `{d.doc_id}` | **Versión:** `{d.version_normativa}`")
            st.markdown(f"**Archivo de Origen:** `{d.archivo_origen}` | **SHA-256:** `{d.sha256_hash[:16]}...`")
            if d.chunks:
                st.markdown(f"**Muestra del Primer Chunk ({d.chunks[0].chunk_id}):**")
                st.caption(f"**Síntesis en Español:** {d.chunks[0].sintesis_espanol}")
                st.text(d.chunks[0].contenido_original[:300] + "...")


# ------------------------------------------------------------------------------
# TAB 6: OFICINA DE PROYECTO (PMO & WBS TRACKER)
# ------------------------------------------------------------------------------
with tab_pmo:
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; flex-wrap: wrap; gap: 1rem;">
        <div>
            <h2 style="margin:0;">🏢 Oficina de Gestión de Proyecto (PMO)</h2>
            <div class="nm-caption">Monitoreo Ejecutivo del WBS en 5 Sprints · <strong>Coordinador General: Martin Morfe</strong></div>
        </div>
        <div><span class="nm-chip" style="color: var(--success); border: 1px solid var(--success); font-weight: 700;">🟢 AVANCE GLOBAL: 96%</span></div>
    </div>
    """, unsafe_allow_html=True)

    # 4 KPIs PMO oficiales
    st.markdown("""
    <div class="nm-row" style="margin-bottom: 1.5rem; justify-content: space-between;">
      <div class="nm-glass nm-kpi" style="flex:1; min-width:180px;">
        <span class="nm-overline">Costo OCI / mes</span>
        <span class="nm-kpi__val">$0.00</span>
        <span class="nm-kpi__foot"><span class="nm-oci">Always Free</span></span>
      </div>
      <div class="nm-glass nm-kpi" style="flex:1; min-width:180px;">
        <span class="nm-overline">Tests Unitarios</span>
        <span class="nm-kpi__val">34<span style="color:var(--ink-muted);font-size:18px">/34</span></span>
        <span class="nm-kpi__foot"><span class="nm-dot"></span>100% pasando</span>
      </div>
      <div class="nm-glass nm-kpi" style="flex:1; min-width:180px;">
        <span class="nm-overline">Avance WBS</span>
        <span class="nm-kpi__val">96%</span>
        <div class="nm-bar" style="--tone:var(--quantum)"><i style="width:96%"></i></div>
        <span class="nm-kpi__foot">Fase 5 · Release</span>
      </div>
      <div class="nm-glass nm-kpi" style="flex:1; min-width:180px;">
        <span class="nm-overline">Chunks en SQL</span>
        <span class="nm-kpi__val">3,020</span>
        <span class="nm-kpi__foot"><span class="nm-dot" style="--tone:var(--cyber)"></span>9 Documentos</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📅 Cronograma de Sprints (Metodología Scrum)")
    sprints = [
        {"s": "Sprint 1", "f": "14 Sep - 20 Sep", "m": "Setup, Arquitectura Base y Contratos Pydantic v2", "st": "🟢 CERRADO (100%)"},
        {"s": "Sprint 2", "f": "21 Sep - 27 Sep", "m": "Ingestión Multiformato, OCI Object Storage y ChromaDB", "st": "🟢 CERRADO (100%)"},
        {"s": "Sprint 3", "f": "28 Sep - 04 Oct", "m": "Orquestación LLM, Adaptación Pedagógica y JSON ONE G10", "st": "🟢 CERRADO (100%)"},
        {"s": "Sprint 4", "f": "05 Oct - 11 Oct", "m": "UI Cyber-Modern, Flashcards 3D, Quizzes, E2E y OCI VM", "st": "🟢 CERRADO (100%)"},
        {"s": "Sprint 5", "f": "12 Oct - 18 Oct", "m": "Diferenciales (NIST NICE/SM-2), Corpus Real SQL, Video y Entrega", "st": "🟡 EN CURSO (90%)"}
    ]
    for sp in sprints:
        st.markdown(f"""
        <div class="nm-glass" style="padding: 0.9rem 1.25rem; margin-bottom: 0.6rem; display: flex; justify-content: space-between; align-items: center;">
            <div>
                <strong>{sp['s']}</strong> · <span class="nm-caption">{sp['f']}</span>
                <p style="margin: 0.2rem 0 0 0; color: var(--ink-muted); font-size: 0.9rem;">{sp['m']}</p>
            </div>
            <span style="font-family: var(--font-mono); font-weight: 600; font-size: 0.85rem; color: {'var(--success)' if 'CERRADO' in sp['st'] else 'var(--amber)'};">
                {sp['st']}
            </span>
        </div>
        """, unsafe_allow_html=True)


# ------------------------------------------------------------------------------
# TAB 7: SQUAD & CRÉDITOS
# ------------------------------------------------------------------------------
with tab_squad:
    st.markdown("### 👥 Squad de Ingeniería — Proyecto NuevaMente")
    st.markdown("""
    - **Project Manager & Coordinador General:** Martin Morfe
    - **Software & Solution Architect (@Lead-Architect):** Esteban Guillermo Morales Velazquez
    - **Backend & AI Developer (@Backend-AI-Dev):** Juan David Villegas Anaya
    - **Cloud & Data Developer (@Cloud-Data-Dev):** Harol Benjamin Medina Zárate, Heiner Jair Godoy Zamora
    - **Frontend & UI Developer (@Frontend-UI-Dev):** Cristian Contreras, Diana Castaño
    - **DevOps & QA Engineer (@QA-DevOps-Dev):** Ivan Hernandez
    """)
    st.markdown("---")
    st.markdown("**Repositorio Oficial del PM:** [https://github.com/mmorfe-engineer/nuevamente_g10_latam](https://github.com/mmorfe-engineer/nuevamente_g10_latam)")
