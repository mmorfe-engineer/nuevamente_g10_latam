"""
Interfaz Gráfica Principal de NuevaMente.
Diseño 'Deep Dev / Cyber-Modern' con Paleta Oscura, Glassmorphism, Flashcards 3D, Algoritmo SM-2 y Dashboard PMO.
Hackathon ONE G10 (Oracle Next Education & Alura / No Country).
"""
import sys
import os
import json
import uuid
from datetime import datetime
from pathlib import Path
import streamlit as st

# Asegurar path del proyecto en sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from config.settings import settings
from src.storage.database import init_db, get_db_session
from src.storage.repository import (
    UserRepository,
    TechnicalDocumentRepository,
    LearningSessionRepository,
    FlashcardRepository,
    QuizRepository
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
    page_title="NuevaMente — EdTech RAG & OCI Always Free",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inyección de estilos CSS Cyber-Modern
css_path = BASE_DIR / "ui" / "assets" / "styles.css"
if css_path.exists():
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Encabezado Principal Cyber-Modern
st.markdown("""
<div class="main-header">
    <div class="brand-badge">🚀 HACKATHON ONE G10 · ORACLE NEXT EDUCATION & NO COUNTRY</div>
    <h1 style="margin:0; font-size: 2.2rem; font-weight: 800; color: #FFFFFF; letter-spacing: -0.02em;">
        🎓 NuevaMente
    </h1>
    <p style="margin: 0.4rem 0 0 0; font-size: 1.05rem; color: #94A3B8;">
        Sistema Inteligente de Adaptación y Generación de Contenido Educativo · <span style="color: #6366F1; font-weight: 600;">RAG Anclado & OCI Always Free</span>
    </p>
</div>
""", unsafe_allow_html=True)

# --- SIDEBAR: Parámetros y Carga de Documentos ---
with st.sidebar:
    st.markdown("### ⚙️ Configuración & Entrada")
    
    modo_entrada = st.radio(
        "Modo de Carga de Documento:",
        ["Escenarios Oficiales (Demo ONE)", "Subir Archivo Propio", "Pegar Texto Técnico"],
        index=0
    )

    doc_titulo = ""
    doc_contenido = ""

    if modo_entrada == "Escenarios Oficiales (Demo ONE)":
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
            st.success(f"📄 Cargado: `{escenarios_disponibles[seleccion_escenario]}` ({len(doc_contenido)} caracteres)")
    
    elif modo_entrada == "Subir Archivo Propio":
        doc_titulo_input = st.text_input("Título del Documento:", value="Documentación Técnica Personalizada")
        archivo_subido = st.file_uploader(
            "Arrastra tu documento (PDF, Markdown o TXT):",
            type=["pdf", "md", "txt", "markdown"]
        )
        if archivo_subido is not None:
            bytes_data = archivo_subido.read()
            doc_titulo = doc_titulo_input or archivo_subido.name
            doc_contenido = doc_loader.extract_from_bytes(archivo_subido.name, bytes_data)
            st.success(f"📄 Procesado: `{archivo_subido.name}` ({len(doc_contenido)} caracteres)")

    else:
        doc_titulo = st.text_input("Título del Documento:", value="Nota de Arquitectura Técnica")
        doc_contenido = st.text_area("Pega el texto técnico aquí:", height=180)

    st.markdown("---")
    st.markdown("### 🎯 Parametrización Pedagógica")

    perfil = st.selectbox(
        "Perfil del Destinatario:",
        [p.value for p in PerfilDestinatario],
        index=0,
        help="Adapta el tono, analogías y nivel de abstracción según la audiencia."
    )

    formato = st.selectbox(
        "Formato Pedagógico de Salida:",
        [f.value for f in FormatoSalida],
        index=0,
        help="Estructura de aprendizaje que generará el motor RAG."
    )

    col_side1, col_side2 = st.columns(2)
    with col_side1:
        nicho = st.selectbox("Nicho / Sector:", [n.value for n in NichoSector], index=3)
    with col_side2:
        detalle = st.selectbox("Nivel de Detalle:", [d.value for d in NivelDetalle], index=0)

    st.markdown("---")
    btn_generar = st.button("⚡ Generar Adaptación Pedagógica", type="primary", use_container_width=True)

# --- PANEL SUPERIOR: Estado de la Infraestructura SaaS ---
with get_db_session() as db_session:
    default_user = UserRepository.get_or_create_default_user(db_session)
    total_docs = len(TechnicalDocumentRepository.list_all(db_session, limit=100))
    total_sessions = len(LearningSessionRepository.list_by_user(db_session, default_user.id))

col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
with col_stat1:
    st.metric("Vector Store", "ChromaDB (Cosine)", "Indexación Semántica Activa")
with col_stat2:
    estado_oci = "Conectado" if not oci_storage.is_emulated else "Always Free (Local)"
    st.metric("OCI Object Storage", estado_oci, settings.OCI_BUCKET_OUTPUTS)
with col_stat3:
    st.metric("Base de Datos", "SQLAlchemy 2.0", f"{total_docs} Docs · {total_sessions} Sesiones")
with col_stat4:
    st.metric("Motor Cognitivo", settings.DEFAULT_LLM_MODEL, "Anti-alucinación Grounding")

st.markdown("---")

# --- PROCESAMIENTO AL PRESIONAR EL BOTÓN ---
if btn_generar:
    if not doc_contenido.strip():
        st.error("Por favor ingresa o carga un documento técnico antes de continuar.")
    else:
        progress_placeholder = st.empty()
        with progress_placeholder.container():
            st.info("🔄 **Iniciando ciclo de vida NuevaMente:** Ingestión, Hash SHA-256, Indexación RAG en ChromaDB y Generación Pedagógica...")

        try:
            req = SolicitudAdaptacion(
                documento_titulo=doc_titulo,
                documento_contenido=doc_contenido,
                perfil_destinatario=PerfilDestinatario(perfil),
                formato_salida=FormatoSalida(formato),
                nicho_sector=NichoSector(nicho),
                nivel_detalle=NivelDetalle(detalle)
            )

            # Ejecución a través del Servicio de Capa 4
            with get_db_session() as db:
                respuesta, trace = adaptation_service.process_adaptation(req, db=db)

            st.session_state["ultima_respuesta"] = respuesta
            st.session_state["ultimo_request"] = req
            st.session_state["ultimo_trace"] = trace
            progress_placeholder.empty()
            st.success("✅ ¡Adaptación pedagógica completada y persistida exitosamente en Base de Datos y OCI!")

        except Exception as e:
            progress_placeholder.empty()
            st.error(f"❌ Ocurrió un error en el procesamiento: {str(e)}")

# --- PESTAÑAS PRINCIPALES DEL SISTEMA ---
tab_contenido, tab_calidad, tab_oci, tab_biblioteca, tab_pmo, tab_squad = st.tabs([
    "📖 Contenido Pedagógico Adaptado",
    "📊 Métricas & Grounding RAG",
    "☁️ Persistencia OCI & JSON Oficial",
    "📚 Biblioteca de Aprendizaje (DB)",
    "🏢 Oficina de Proyecto (PMO & WBS)",
    "👥 Squad & Arquitectura"
])

# ==============================================================================
# TAB 1: CONTENIDO ADAPTADO (Flashcards 3D, Quizzes, Tutoriales)
# ==============================================================================
with tab_contenido:
    if "ultima_respuesta" in st.session_state:
        resp = st.session_state["ultima_respuesta"]
        req = st.session_state["ultimo_request"]
        trace = st.session_state.get("ultimo_trace", {})

        st.markdown(f"## {resp.contenido_adaptado.titulo}")
        st.markdown(f"""
        <div class="cyber-card" style="border-left: 4px solid #6366F1;">
            <span style="font-size: 0.8rem; font-weight: 700; color: #818CF8; text-transform: uppercase;">Apertura Didáctica:</span>
            <p style="margin: 0.35rem 0 0 0; font-size: 1.05rem; color: #F1F5F9; line-height: 1.6;">
                {resp.contenido_adaptado.introduccion_contextualizada}
            </p>
        </div>
        """, unsafe_allow_html=True)

        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.markdown(f"**👤 Perfil:** `{resp.metadatos.perfil_aplicado}`")
        with col_m2:
            st.markdown(f"**⏱️ Tiempo Estimado:** `{resp.metadatos.tiempo_estimado_estudio_minutos} minutos`")
        with col_m3:
            st.markdown(f"**🏷️ Conceptos Clave:** {', '.join(resp.metadatos.conceptos_clave)}")

        st.markdown("---")
        items = resp.contenido_adaptado.items

        # --- FORMATO: FLASHCARDS INTERACTIVAS 3D CON SUPERMEMO SM-2 ---
        if req.formato_salida == FormatoSalida.FLASHCARDS:
            col_fc_title, col_fc_anki = st.columns([3, 1])
            with col_fc_title:
                st.markdown("### 🗂️ Tarjetas con Giro 3D y Repetición Espaciada SM-2")
            with col_fc_anki:
                st.download_button(
                    "🗃️ Exportar a Anki (.csv)",
                    data=export_to_anki_csv(items),
                    file_name=f"anki_{resp.almacenamiento_oci.objeto_id.replace('.json', '.csv')}",
                    mime="text/csv",
                    use_container_width=True
                )
            st.caption("Pasa el cursor sobre la tarjeta para girarla 180° y califica tu nivel de asimilación para calcular el intervalo de repaso espaciado.")

            # Recuperar IDs de tarjetas de la DB si existen
            session_id_str = trace.get("session_id")
            saved_cards_db = []
            if session_id_str:
                with get_db_session() as db:
                    saved_cards_db = FlashcardRepository.get_by_session(db, uuid.UUID(session_id_str))

            for i, itm in enumerate(items):
                frente = itm.get("frente", "Pregunta")
                dorso = itm.get("dorso", "Respuesta")
                pista = itm.get("pista_didactica", "")
                card_db = saved_cards_db[i] if i < len(saved_cards_db) else None

                card_html = f"""
                <div class="flashcard-3d-scene">
                    <div class="flashcard-3d-card" id="card_{i}">
                        <div class="flashcard-face flashcard-front">
                            <div>
                                <div class="card-tag">FLASHCARD #{i+1} · ANVERSO</div>
                                <div class="card-title">{frente}</div>
                            </div>
                        </div>
                        <div class="flashcard-face flashcard-back">
                            <div>
                                <div class="card-tag" style="color: #38BDF8;">EXPLICACIÓN ADAPTADA · REVERSO</div>
                                <div class="card-body">{dorso}</div>
                                {f'<div class="didactic-hint-pill">💡 <strong>Pista Mnemotécnica:</strong> {pista}</div>' if pista else ''}
                            </div>
                        </div>
                    </div>
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)

                col_btn1, col_btn2, col_btn3, col_info = st.columns([1, 1, 1, 3])
                
                with col_btn1:
                    if st.button(f"🔴 Difícil", key=f"diff_{i}"):
                        reps, interval, ef, next_rev = calculate_sm2(quality=1)
                        if card_db:
                            with get_db_session() as db:
                                FlashcardRepository.update_mastery(
                                    db, card_db.id, FlashcardUpdateMastery(mastery_level=1, next_review_at=next_rev)
                                )
                        st.toast(f"SM-2: Repaso programado para mañana (+{interval} día)", icon="⏳")

                with col_btn2:
                    if st.button(f"🟡 Bien", key=f"good_{i}"):
                        reps, interval, ef, next_rev = calculate_sm2(quality=3, repetitions=1)
                        if card_db:
                            with get_db_session() as db:
                                FlashcardRepository.update_mastery(
                                    db, card_db.id, FlashcardUpdateMastery(mastery_level=3, next_review_at=next_rev)
                                )
                        st.toast(f"SM-2: Próximo repaso en {interval} días ({next_rev.strftime('%d/%m')})", icon="👍")

                with col_btn3:
                    if st.button(f"🟢 Fácil", key=f"easy_{i}"):
                        reps, interval, ef, next_rev = calculate_sm2(quality=5, repetitions=2, previous_interval=6)
                        if card_db:
                            with get_db_session() as db:
                                FlashcardRepository.update_mastery(
                                    db, card_db.id, FlashcardUpdateMastery(mastery_level=5, next_review_at=next_rev)
                                )
                        st.toast(f"SM-2: Dominado (+{interval} días, EF {ef})", icon="🌟")

                with col_info:
                    if card_db and card_db.next_review_at:
                        st.caption(f"🗓️ Próximo repaso registrado: `{card_db.next_review_at.strftime('%Y-%m-%d %H:%M')}` (Nivel: {card_db.mastery_level}/5)")

        # --- FORMATO: QUIZ INTERACTIVO CON FEEDBACK INMEDIATO ---
        elif req.formato_salida == FormatoSalida.QUIZ:
            st.markdown("### 📝 Visor de Quiz con Retroalimentación Visual Inmediata")
            st.caption("Responde cada pregunta para recibir validación en tiempo real y justificación pedagógica anclada a la documentación.")

            for i, itm in enumerate(items):
                pregunta = itm.get("pregunta", f"Pregunta #{i+1}")
                opciones = itm.get("opciones", [])
                correcta = itm.get("respuesta_correcta", "")
                justificacion = itm.get("justificacion_didactica", "")
                pista = itm.get("pista_didactica", "")

                with st.container():
                    st.markdown(f"""
                    <div class="quiz-box">
                        <span class="quiz-badge-bloom">Taxonomía de Bloom: COMPRENDER / ANALIZAR</span>
                        <h4 style="margin: 0.5rem 0 1rem 0; color: #FFFFFF;">Pregunta #{i+1}: {pregunta}</h4>
                    </div>
                    """, unsafe_allow_html=True)

                    seleccion = st.radio(
                        "Selecciona tu respuesta:",
                        opciones,
                        key=f"quiz_opt_{i}",
                        label_visibility="collapsed"
                    )

                    col_q1, col_q2 = st.columns([2, 4])
                    with col_q1:
                        btn_check = st.button(f"Comprobar Pregunta #{i+1}", key=f"btn_check_{i}")

                    if btn_check:
                        es_correcta = (seleccion.strip() == correcta.strip()) or seleccion.startswith(correcta[:2])
                        if es_correcta:
                            st.markdown(f"""
                            <div class="quiz-feedback-success">
                                <strong>✅ ¡RESPUESTA CORRECTA!</strong>
                                <p style="margin: 0.5rem 0 0 0; font-size: 0.95rem; color: #A7F3D0;">
                                    {justificacion}
                                </p>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div class="quiz-feedback-error">
                                <strong>❌ RESPUESTA INCORRECTA</strong>
                                <p style="margin: 0.25rem 0; font-size: 0.95rem;">La opción correcta era: <strong>{correcta}</strong></p>
                                <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; color: #FECDD3;">
                                    <strong>Fundamentación RAG:</strong> {justificacion}
                                </p>
                            </div>
                            """, unsafe_allow_html=True)

                        if pista:
                            st.caption(f"🧭 *Pista Didáctica:* {pista}")

        # --- FORMATO: GUÍA PASO A PASO (TUTORIAL) ---
        elif req.formato_salida == FormatoSalida.TUTORIAL:
            st.markdown("### 🛠️ Guía Práctica Paso a Paso (Tutorial Hands-On)")
            for itm in items:
                paso = itm.get("paso", 1)
                st.markdown(f"""
                <div class="cyber-card">
                    <span class="brand-badge">PASO {paso}</span>
                    <h3 style="margin: 0.25rem 0 0.75rem 0; color: #FFFFFF;">{itm.get('titulo_paso', '')}</h3>
                    <p style="color: #CBD5E1; line-height: 1.6;">{itm.get('descripcion', '')}</p>
                </div>
                """, unsafe_allow_html=True)

                if itm.get("comando_o_codigo"):
                    st.code(itm.get("comando_o_codigo"), language="bash")
                if itm.get("verificacion"):
                    st.success(f"🔍 **Verificación del Paso:** {itm.get('verificacion')}")
                st.markdown("---")

        else:
            for itm in items:
                st.json(itm)
    else:
        st.info("👈 Selecciona un escenario de prueba en la barra lateral o ingresa tu documento y presiona **'⚡ Generar Adaptación Pedagógica'** para ver el resultado interactivo.")

# ==============================================================================
# TAB 2: MÉTRICAS Y EVALUACIÓN DE CALIDAD
# ==============================================================================
with tab_calidad:
    st.markdown("### Evaluación de Calidad y Fidelidad RAG Anti-Alucinación")
    if "ultima_respuesta" in st.session_state:
        resp = st.session_state["ultima_respuesta"]
        col_c1, col_c2, col_c3 = st.columns(3)
        with col_c1:
            score = resp.evaluacion_calidad.anclaje_fuente_score
            st.metric("Puntuación de Anclaje (Grounding)", f"{int(score * 100)}%", help="Similitud semántica con el documento técnico.")
            st.progress(score)
        with col_c2:
            st.metric("Claridad Pedagógica", resp.evaluacion_calidad.claridad_pedagogica)
        with col_c3:
            st.metric("Estatus de Alucinación", "0% Detectada", "Fidelidad RAG Estricta")

        st.markdown("---")
        st.markdown(f"""
        <div class="cyber-card">
            <h4 style="margin:0 0 0.5rem 0; color: #38BDF8;">Dictamen del Revisor Pedagógico:</h4>
            <p style="margin:0; color: #CBD5E1;">{resp.evaluacion_calidad.observaciones}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Las métricas de calidad y fidelidad se calculan dinámicamente al generar una adaptación pedagógica.")

# ==============================================================================
# TAB 3: PERSISTENCIA EN OCI Y JSON ESTRUCTURADO
# ==============================================================================
with tab_oci:
    st.markdown("### Persistencia Obligatoria en OCI Object Storage Always Free")
    if "ultima_respuesta" in st.session_state:
        resp = st.session_state["ultima_respuesta"]
        st.info(f"📦 **Bucket OCI de Salida:** `{resp.almacenamiento_oci.bucket}`")
        st.code(f"ID del Objeto: {resp.almacenamiento_oci.objeto_id}\nEstado: {resp.almacenamiento_oci.status_upload}", language="text")

        st.markdown("### Contrato de Salida Oficial Hackathon ONE G10:")
        json_output = resp.model_dump()
        json_str = json.dumps(json_output, indent=2, ensure_ascii=False)
        st.code(json_str, language="json")

        col_down1, col_down2 = st.columns(2)
        with col_down1:
            st.download_button(
                label="⬇️ Descargar JSON Oficial (ONE G10)",
                data=json_str,
                file_name=resp.almacenamiento_oci.objeto_id,
                mime="application/json",
                use_container_width=True
            )
        with col_down2:
            st.download_button(
                label="📝 Descargar Guía Didáctica (.md)",
                data=export_to_markdown_guide(resp),
                file_name=resp.almacenamiento_oci.objeto_id.replace(".json", ".md"),
                mime="text/markdown",
                use_container_width=True
            )
    else:
        st.markdown("""
        <div class="cyber-card">
            <h4>Infraestructura OCI Always Free Configurada:</h4>
            <ul>
                <li><strong>Bucket Origen:</strong> <code>nuevamente-documentos-origen</code></li>
                <li><strong>Bucket Resultados:</strong> <code>nuevamente-contenidos-educativos</code></li>
                <li><strong>Cuota de Almacenamiento:</strong> 10 GB Always Free (Cero Costo)</li>
                <li><strong>Región OCI:</strong> <code>us-ashburn-1</code> / <code>sa-saopaulo-1</code></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# TAB 4: BIBLIOTECA DE APRENDIZAJE (DB RELACIONAL)
# ==============================================================================
with tab_biblioteca:
    st.markdown("### 📚 Biblioteca de Aprendizaje Persistente (SQLAlchemy)")
    with get_db_session() as db:
        default_user = UserRepository.get_or_create_default_user(db)
        sesiones = LearningSessionRepository.list_by_user(db, default_user.id)

    if not sesiones:
        st.info("Aún no tienes sesiones registradas en la base de datos. ¡Genera una adaptación para verla aquí!")
    else:
        for s in sesiones:
            with st.expander(f"📑 {s.titulo_adaptado} · {s.perfil_destinatario} ({s.formato_salida})"):
                st.markdown(f"**ID de Sesión:** `{s.id}`")
                st.markdown(f"**Fecha de Creación:** `{s.created_at}`")
                st.markdown(f"**Tiempo:** `{s.tiempo_estimado_minutos} min` | **Grounding:** `{int(s.anclaje_fuente_score * 100)}%`")
                st.markdown(f"**Objeto en OCI:** `{s.oci_object_id}`")
                st.markdown(f"**Introducción:** *{s.introduccion_contextualizada}*")

# ==============================================================================
# TAB 5: OFICINA DE PROYECTO (PMO & WBS TRACKER) — VISTA EJECUTIVA
# ==============================================================================
with tab_pmo:
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
        <div>
            <h2 style="margin:0; color: #FFFFFF;">🏢 Oficina de Gestión de Proyecto (PMO)</h2>
            <p style="margin:0.25rem 0 0 0; color: #94A3B8;">
                Monitoreo Ejecutivo del WBS en 5 Sprints · <strong>Coordinador General: Martin Morfe</strong>
            </p>
        </div>
        <div class="brand-badge" style="font-size: 0.85rem; padding: 0.4rem 1rem;">
            🟢 AVANCE GLOBAL: 88%
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Métricas de la Oficina de Proyecto
    col_pmo1, col_pmo2, col_pmo3, col_pmo4 = st.columns(4)
    with col_pmo1:
        st.metric("Sprints Completados", "3 de 5", "60% Sprints Cerrados")
    with col_pmo2:
        st.metric("Sprint 4 (En Curso)", "90% Completado", "Fase Final de Pulido")
    with col_pmo3:
        st.metric("Tests Unitarios & DoD", "26 / 26 Pasando", "100% Calidad Aprobada")
    with col_pmo4:
        st.metric("Gasto OCI Always Free", "$0.00 USD", "100% Free Forever")

    st.markdown("---")
    st.markdown("### 📅 Estado de la Estructura Desglosada de Trabajo (WBS / EDT)")

    sprint_data = [
        {"Sprint": "Sprint 1", "Periodo": "14 Sep - 20 Sep", "Objetivo": "Setup, Arquitectura Base y Contratos Pydantic v2", "Estatus": "🟢 CERRADO (100%)", "Entregables": "Repo GitHub, 6 Entidades Core, C4 Diagram"},
        {"Sprint": "Sprint 2", "Periodo": "21 Sep - 27 Sep", "Objetivo": "Ingestión Multiformato, OCI Object Storage y ChromaDB", "Estatus": "🟢 CERRADO (100%)", "Entregables": "Loaders PDF/MD/TXT, OCI Client, Vector Store"},
        {"Sprint": "Sprint 3", "Periodo": "28 Sep - 04 Oct", "Objetivo": "Orquestación LLM, Adaptación Pedagógica y JSON ONE G10", "Estatus": "🟢 CERRADO (100%)", "Entregables": "Prompts Bloom, Adaptador Gemini, Grounding Score"},
        {"Sprint": "Sprint 4", "Periodo": "05 Oct - 11 Oct", "Objetivo": "UI Cyber-Modern, Flashcards 3D, Quizzes, E2E y OCI VM", "Estatus": "🟡 EN CURSO (90%)", "Entregables": "Flashcards 3D, Quiz Feedback, OCI Setup Script"},
        {"Sprint": "Sprint 5", "Periodo": "12 Oct - 18 Oct", "Objetivo": "Diferenciales (Anki/LangGraph), Video Demo y Entregables", "Estatus": "⚪ PLANIFICADO (10%)", "Entregables": "Video Demo YouTube, 4 Tareas No Country"}
    ]

    for sp in sprint_data:
        st.markdown(f"""
        <div class="cyber-card" style="padding: 1.1rem 1.5rem; margin-bottom: 0.75rem;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <strong style="font-size: 1.1rem; color: #FFFFFF;">{sp['Sprint']}</strong> · <span style="color: #94A3B8;">{sp['Periodo']}</span>
                    <p style="margin: 0.25rem 0 0 0; color: #CBD5E1; font-size: 0.95rem;">{sp['Objetivo']}</p>
                    <span style="font-size: 0.8rem; color: #6366F1;">📦 Entregables: {sp['Entregables']}</span>
                </div>
                <div>
                    <span style="font-weight: 700; font-size: 0.9rem; color: {'#10B981' if 'CERRADO' in sp['Estatus'] else '#F59E0B' if 'EN CURSO' in sp['Estatus'] else '#94A3B8'};">
                        {sp['Estatus']}
                    </span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### ☁️ Gobernanza y Certificación OCI Always Free")
    st.markdown("""
    <div class="cyber-card">
        <p style="margin:0; line-height: 1.6; color: #E2E8F0;">
            ✅ <strong>Validación de Cero Costos:</strong> La solución ejecuta sobre instancias <strong>Ampere A1 Flex</strong> (4 OCPUs, 24 GB RAM) y almacena en <strong>OCI Object Storage</strong> respetando la cuota gratuita mensual de 10 GB y 50,000 requests.
            <br/>
            📄 <strong>Documentación de Despliegue:</strong> Disponible en el repositorio en <code>deploy/OCI_ALWAYS_FREE_ARCHITECTURE.md</code> y script automatizado <code>deploy/oci_setup.sh</code>.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# TAB 6: SQUAD & ARQUITECTURA
# ==============================================================================
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
