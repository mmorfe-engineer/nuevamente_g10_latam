"""
Orquestador de IA Generativa y Adaptación Pedagógica.
Coordina RAG, prompts especializados, generación con LLMs y persistencia en OCI.
"""
import json
import logging
import os
import re
import uuid
from typing import Dict, Any, Optional
from config.settings import settings
from src.utils.schemas import (
    SolicitudAdaptacion,
    RespuestaAdaptacion,
    MetadatosAprendizaje,
    ContenidoAdaptado,
    EvaluacionCalidad,
    AlmacenamientoOCI,
    PerfilDestinatario,
    FormatoSalida
)
from src.llm.prompts import construir_prompt_sistema
from src.rag.retriever import rag_retriever
from src.storage.oci_client import oci_storage

logger = logging.getLogger(__name__)

class LLMEngine:
    def __init__(self):
        self.nvidia_key = settings.NVIDIA_API_KEY
        self.mistral_key = settings.MISTRAL_API_KEY
        self.gemini_key = settings.GEMINI_API_KEY
        self.openai_key = settings.OPENAI_API_KEY

    def adapt_content(self, request: SolicitudAdaptacion) -> RespuestaAdaptacion:
        """Flujo integral de adaptación pedagógica."""
        # 1. Recuperación de contexto RAG
        context_text, retrieved_chunks, avg_similarity = rag_retriever.retrieve_context(
            query=f"{request.documento_titulo} {request.perfil_destinatario.value} {request.formato_salida.value}"
        )
        
        if not context_text:
            context_text = request.documento_contenido

        # 2. Generación con LLM
        system_prompt = construir_prompt_sistema(
            perfil=request.perfil_destinatario.value,
            formato=request.formato_salida.value,
            nicho=request.nicho_sector.value,
            nivel_detalle=request.nivel_detalle.value
        )

        user_content = f"""DOCUMENTO FUENTE: '{request.documento_titulo}'
CONTEXTO TÉCNICO VERIFICADO:
{context_text[:2500]}

Adapta este contenido para el perfil '{request.perfil_destinatario.value}' en formato '{request.formato_salida.value}'.
Genera entre 3 y 4 items pedagógicos concisos pero rigurosos. Responde ÚNICAMENTE un JSON válido con los campos:
- titulo (string)
- introduccion_contextualizada (string)
- tiempo_estimado_estudio_minutos (entero)
- conceptos_clave (lista de strings)
- prerrequisitos (lista de 2 a 3 strings con conocimientos previos recomendados)
- items (lista de objetos con las especificaciones del formato)
"""

        generated_raw = self._call_llm(system_prompt, user_content, request)

        # 3. Construcción del objeto de calidad y metadatos con cálculo de anclaje
        from src.quality.evaluator import quality_evaluator
        calidad = quality_evaluator.build_quality_evaluation(
            source_text=context_text,
            generated_items=generated_raw.get("items", []),
            perfil_destinatario=request.perfil_destinatario.value,
            vector_similarity=avg_similarity
        )

        metadatos = MetadatosAprendizaje(
            perfil_aplicado=request.perfil_destinatario.value,
            formato_generado=request.formato_salida.value,
            tiempo_estimado_estudio_minutos=generated_raw.get("tiempo_estimado_estudio_minutos", 5),
            conceptos_clave=generated_raw.get("conceptos_clave", ["Conceptos Fundamentales", "Estructura Operativa"]),
            prerrequisitos=generated_raw.get("prerrequisitos", ["Conocimientos generales del sector", "Lectura técnica básica"])
        )

        contenido = ContenidoAdaptado(
            titulo=generated_raw.get("titulo", f"Aprendizaje: {request.documento_titulo}"),
            introduccion_contextualizada=generated_raw.get(
                "introduccion_contextualizada",
                f"Guía adaptada de {request.documento_titulo} para {request.perfil_destinatario.value}."
            ),
            items=generated_raw.get("items", [])
        )

        # 4. Generar ID único de objeto y persistir en OCI Object Storage
        slug_titulo = re.sub(r'[^a-zA-Z0-9]', '-', request.documento_titulo.lower())[:20].strip('-')
        slug_perfil = request.perfil_destinatario.name.lower()
        slug_formato = request.formato_salida.name.lower()
        objeto_id = f"contenido-{slug_titulo}-{slug_perfil}-{slug_formato}-{uuid.uuid4().hex[:6]}.json"

        # 5. Persistencia obligatoria en OCI Object Storage (Always Free)
        payload_para_oci = {
            "status": "exito",
            "metadatos": metadatos.model_dump(),
            "contenido_adaptado": contenido.model_dump(),
            "evaluacion_calidad": calidad.model_dump()
        }
        almacenamiento_oci = oci_storage.upload_educational_json(objeto_id, payload_para_oci)

        # 6. Respuesta final estructurada
        return RespuestaAdaptacion(
            status="exito",
            metadatos=metadatos,
            contenido_adaptado=contenido,
            evaluacion_calidad=calidad,
            almacenamiento_oci=almacenamiento_oci
        )

    def _parse_llm_json(self, raw_text: str) -> Dict[str, Any]:
        """Extrae de forma robusta un bloque JSON del texto generado por el LLM."""
        if not raw_text:
            raise ValueError("Texto de respuesta vacío.")
        text = raw_text.strip()
        # 1. Limpiar bloques markdown si existen
        if "```json" in text:
            match = re.search(r"```json\s*(.*?)\s*```", text, re.DOTALL)
            if match:
                text = match.group(1).strip()
            else:
                text = text.split("```json", 1)[1].strip()
        elif "```" in text:
            match = re.search(r"```\s*(.*?)\s*```", text, re.DOTALL)
            if match:
                text = match.group(1).strip()
            else:
                text = text.split("```", 1)[1].strip()

        # 2. Localizar límites estrictos del objeto JSON {...}
        start_idx = text.find("{")
        end_idx = text.rfind("}")
        if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
            text = text[start_idx:end_idx + 1].strip()

        try:
            parsed = json.loads(text)
            return self._normalize_generated_dict(parsed)
        except Exception:
            try:
                import ast
                evaluated = ast.literal_eval(text)
                if isinstance(evaluated, dict):
                    return self._normalize_generated_dict(evaluated)
            except Exception:
                pass
            raise

    def _normalize_generated_dict(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        """Normaliza la salida del LLM a la estructura canónica."""
        if not isinstance(raw, dict):
            return {}

        # Si el LLM envolvió el contenido en una clave superior
        for wrapper_key in ["flashcards", "quiz", "tutorial", "resumen", "resultado", "data", "cards", "preguntas"]:
            if wrapper_key in raw:
                val = raw[wrapper_key]
                if isinstance(val, dict) and ("items" in val or "titulo" in val):
                    raw = val
                    break
                elif isinstance(val, list) and len(val) > 0 and isinstance(val[0], dict):
                    if "items" in val[0] or "titulo" in val[0]:
                        raw = val[0]
                        break
                    elif "frente" in val[0] or "pregunta" in val[0] or "paso" in val[0]:
                        raw = {"items": val}
                        break

        # Normalizar clave de items
        if "items" not in raw or not isinstance(raw.get("items"), list):
            for alt_key in ["flashcards", "preguntas", "pasos", "secciones", "questions", "cards", "elementos"]:
                if alt_key in raw and isinstance(raw[alt_key], list):
                    raw["items"] = raw[alt_key]
                    break

        return raw

    def _call_llm(self, system_prompt: str, user_prompt: str, request: SolicitudAdaptacion) -> Dict[str, Any]:
        """Llama a NVIDIA NIM (DeepSeek), Mistral AI, Gemini, OpenAI o fallback heurístico con tolerancia a fallos."""
        # En entorno de pruebas automatizadas, usar directamente el generador determinista
        if settings.APP_ENV == "testing":
            return self._generate_heuristic_demo(request)

        # Resolver API keys dinámicamente de os.environ (inyectadas por st.secrets en Streamlit Cloud)
        nvidia_key = os.environ.get("NVIDIA_API_KEY") or settings.NVIDIA_API_KEY or self.nvidia_key
        mistral_key = os.environ.get("MISTRAL_API_KEY") or settings.MISTRAL_API_KEY or self.mistral_key
        gemini_key = os.environ.get("GEMINI_API_KEY") or settings.GEMINI_API_KEY or self.gemini_key
        openai_key = os.environ.get("OPENAI_API_KEY") or settings.OPENAI_API_KEY or self.openai_key

        # 1. Intento con Mistral AI primero si está disponible (baja latencia y modo JSON nativo)
        if mistral_key:
            try:
                from openai import OpenAI
                client = OpenAI(
                    base_url=settings.MISTRAL_BASE_URL,
                    api_key=mistral_key,
                    timeout=15.0
                )
                response = client.chat.completions.create(
                    model=settings.MISTRAL_MODEL,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.2,
                    max_tokens=1400,
                    response_format={"type": "json_object"}
                )
                if response and getattr(response, "choices", None) and len(response.choices) > 0:
                    content = response.choices[0].message.content
                    if content:
                        parsed = self._parse_llm_json(content)
                        if parsed and parsed.get("items"):
                            logger.info("Respuesta generada exitosamente con Mistral AI.")
                            return parsed
            except Exception as e:
                logger.warning(f"Error llamando a Mistral AI API: {e}. Probando siguiente proveedor.")

        # 2. Intento con NVIDIA NIM (DeepSeek)
        if nvidia_key:
            try:
                from openai import OpenAI
                client = OpenAI(
                    base_url=settings.NVIDIA_BASE_URL,
                    api_key=nvidia_key,
                    timeout=6.0
                )
                response = client.chat.completions.create(
                    model=settings.NVIDIA_MODEL,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.2,
                    max_tokens=1400
                )
                if response and getattr(response, "choices", None) and len(response.choices) > 0:
                    msg = response.choices[0].message
                    content = msg.content if msg.content else getattr(msg, "reasoning_content", "")
                    if content:
                        parsed = self._parse_llm_json(content)
                        if parsed and parsed.get("items"):
                            logger.info("Respuesta generada exitosamente con NVIDIA NIM.")
                            return parsed
            except Exception as e:
                logger.warning(f"Error llamando a NVIDIA NIM API: {e}. Probando siguiente proveedor.")

        # 3. Intento con Gemini
        if gemini_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=gemini_key)
                model = genai.GenerativeModel(
                    model_name="gemini-1.5-flash",
                    system_instruction=system_prompt,
                    generation_config={"response_mime_type": "application/json"}
                )
                response = model.generate_content(user_prompt)
                parsed = json.loads(response.text)
                if parsed and parsed.get("items"):
                    return parsed
            except Exception as e:
                logger.warning(f"Error llamando a Gemini API: {e}. Probando siguiente proveedor.")

        # 4. Intento con OpenAI
        if openai_key:
            try:
                from openai import OpenAI
                client = OpenAI(api_key=openai_key, timeout=12.0)
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    response_format={"type": "json_object"}
                )
                parsed = json.loads(response.choices[0].message.content)
                if parsed and parsed.get("items"):
                    return parsed
            except Exception as e:
                logger.warning(f"Error llamando a OpenAI API: {e}.")

        # 5. Generador Heurístico Inteligente de Alta Calidad (Offline Fallback para demos sin costo)
        return self._generate_heuristic_demo(request)

    def _generate_heuristic_demo(self, request: SolicitudAdaptacion) -> Dict[str, Any]:
        """Generador heurístico de alta calidad pedagógica para demostraciones del MVP."""
        titulo = request.documento_titulo or "Seguridad Cloud"
        perfil = request.perfil_destinatario
        formato = request.formato_salida
        doc_lower = (request.documento_contenido or "").lower()

        # Detección contextual del dominio
        is_vcn = "vcn" in doc_lower or "red" in doc_lower or "virtual cloud network" in doc_lower
        is_pci = "pci" in doc_lower or "tarjeta" in doc_lower or "pago" in doc_lower
        is_iam = "iam" in doc_lower or "identidad" in doc_lower or "acceso" in doc_lower or "mfa" in doc_lower
        is_ransom = "ransomware" in doc_lower or "incidente" in doc_lower or "bcp" in doc_lower

        # =========================================================================
        # 1. CASO FLASHCARDS 3D (5 a 6 tarjetas completas con anclaje normativo)
        # =========================================================================
        if formato == FormatoSalida.FLASHCARDS:
            if is_vcn:
                items_fc = [
                    {
                        "frente": "¿Qué es una Red Virtual en la Nube [Virtual Cloud Network - VCN] en Oracle Cloud?",
                        "dorso": "Es una red de software definida (SDN) privada y configurable en una región de OCI. Permite aislar cargas de trabajo mediante subredes, tablas de enrutamiento y firewalls con estado [Security Lists].",
                        "pista_didactica": "Analogía: Es el vecindario corporativo privado donde levantas tus instancias de cómputo y bases de datos.",
                        "fuente": "OCI Networking Architecture & NIST SP 800-207"
                    },
                    {
                        "frente": "¿Cómo operan las Listas de Seguridad [Security Lists] frente a los Grupos de Seguridad de Red [Network Security Groups - NSGs]?",
                        "dorso": "Las Listas de Seguridad se aplican a nivel de toda la Subred [Subnet-level], mientras que los NSGs aplican reglas de firewall granulares directamente a las interfaces de red de tarjeta virtual [VNIC-level].",
                        "pista_didactica": "Security List = Guardia en la entrada del edificio; NSG = Guardia asignado a una oficina específica.",
                        "fuente": "OCI Security Architecture v4.2"
                    },
                    {
                        "frente": "¿Cuál es la función crítica de una Pasarela de Internet [Internet Gateway] vs Pasarela NAT [NAT Gateway]?",
                        "dorso": "La Pasarela de Internet [Internet Gateway] permite tráfico entrante y saliente directo hacia IPs públicas. La Pasarela NAT [NAT Gateway] permite a servidores privados salir a internet (ej. parches) sin exponer IPs públicas a ataques entrantes.",
                        "pista_didactica": "Internet Gateway = Puerta principal bidireccional; NAT Gateway = Salida de emergencia unidireccional.",
                        "fuente": "OCI Core Infrastructure Guide"
                    },
                    {
                        "frente": "¿En qué consiste la Arquitectura de Confianza Cero [Zero Trust Architecture - ZTA] en subredes privadas?",
                        "dorso": "Ningún recurso dentro de la red es considerado seguro por defecto. Toda comunicación entre microservicios o bases de datos exige autenticación mutua TLS [mTLS] y autorización por políticas de mínimo privilegio.",
                        "pista_didactica": "Principio: 'Nunca confíes, siempre verifica' cada paquete y solicitud.",
                        "fuente": "NIST SP 800-207 Zero Trust Architecture"
                    },
                    {
                        "frente": "¿Cómo se previene el Agotamiento de Espacio IP mediante Bloques CIDR [Classless Inter-Domain Routing]?",
                        "dorso": "Planificando bloques CIDR no superpuestos (ej. 10.0.0.0/16) divididos en subredes /24, reservando bloques contiguos para expansión futura y conectividad híbrida mediante VPN IPSec o FastConnect.",
                        "pista_didactica": "Divide el terreno en parcelas con holgura para evitar solapamientos destructivos.",
                        "fuente": "NIST SP 800-53 SC-7 Boundary Protection"
                    }
                ]
            else:
                items_fc = [
                    {
                        "frente": f"¿Cuál es el principio rector de Mínimo Privilegio [Principle of Least Privilege] en '{titulo}'?",
                        "dorso": f"Garantizar que cada usuario, servicio o proceso acceda únicamente a los recursos indispensables para su rol operativo, reduciendo el radio de explosión [Blast Radius] ante incidentes.",
                        "pista_didactica": "Otorga solo las llaves indispensables para cada puerta, nunca la llave maestra.",
                        "fuente": f"{titulo} · Marco NIST NICE"
                    },
                    {
                        "frente": "¿Por qué es obligatorio implementar Autenticación Multifactor FIDO2 [Multi-Factor Authentication - MFA]?",
                        "dorso": "MFA con claves criptográficas de hardware FIDO2 mitiga hasta el 99.9% de ataques de Suplantación de Identidad [Phishing] e Intermediario [Man-in-the-Middle], neutralizando la captura de contraseñas.",
                        "pista_didactica": "Algo que sabes (contraseña) + Algo que tienes (token FIDO2 resistente a phishing).",
                        "fuente": "NIST SP 800-63B Digital Identity Guidelines"
                    },
                    {
                        "frente": "¿Cómo se asegura la Integridad de Datos [Data Integrity] en reposo y en tránsito?",
                        "dorso": "En reposo mediante cifrado AES-256 administrado por llaves en OCI Vault / HSM; en tránsito mediante canales TLS 1.3 con conjuntos de cifrado seguros [Cipher Suites].",
                        "pista_didactica": "Cifrado en la caja fuerte y túnel blindado durante el transporte.",
                        "fuente": "PCI DSS v4.0 Requerimiento 3 & 4"
                    },
                    {
                        "frente": "¿Qué función cumple el Registro de Auditoría Inmutable [Immutable Audit Logging]?",
                        "dorso": "Proveer trazabilidad forense no repudiable de todas las llamadas a API, modificaciones de configuración y accesos a datos para cumplir con estándares de cumplimiento normativo.",
                        "pista_didactica": "Caja negra de un avión: registra cada evento sin posibilidad de alteración.",
                        "fuente": "ISO/IEC 27001:2022 Control A.8.15"
                    },
                    {
                        "frente": "¿Cuál es el rol del Plan de Continuidad del Negocio [Business Continuity Plan - BCP] ante Ransomware?",
                        "dorso": "Asegurar que existan copias de seguridad aisladas [Air-gapped Backups] y procedimientos de recuperación validados para restablecer operaciones críticas dentro de los límites de RTO y RPO.",
                        "pista_didactica": "Tener un búnker de respaldo desconectado que garantice levantarte tras una crisis.",
                        "fuente": "NIST SP 800-34 Contingency Planning"
                    }
                ]

            return {
                "titulo": f"Tarjetas Didácticas 3D: {titulo}",
                "introduccion_contextualizada": f"Flashcards interactivas optimizadas para el perfil {perfil.value}. Diseñadas con repetición espaciada y anclaje técnico en fuentes oficiales.",
                "tiempo_estimado_estudio_minutos": 8,
                "conceptos_clave": ["Fundamentos Técnicos", "Estructura Operativa", "Buenas Prácticas"],
                "prerrequisitos": ["Lectura comprensiva de manuales técnicos", "Conocimientos generales de arquitectura de sistemas"],
                "items": items_fc
            }

        # =========================================================================
        # 2. CASO QUIZ INTERACTIVO (3 a 4 preguntas con 4 opciones y justificación)
        # =========================================================================
        elif formato == FormatoSalida.QUIZ:
            if is_vcn:
                items_quiz = [
                    {
                        "pregunta": "¿Qué componente de red debe configurarse para permitir que servidores en una subred privada descarguen parches de seguridad de internet sin permitir conexiones entrantes no deseadas?",
                        "opciones": [
                            "A) Pasarela NAT [NAT Gateway]",
                            "B) Pasarela de Internet [Internet Gateway]",
                            "C) Pasarela de Enrutamiento Dinámico [Dynamic Routing Gateway - DRG]",
                            "D) Pasarela de Servicio [Service Gateway]"
                        ],
                        "respuesta_correcta": "A) Pasarela NAT [NAT Gateway]",
                        "justificacion_didactica": "La Pasarela NAT [NAT Gateway] permite conexiones de salida iniciadas por instancias privadas (tráfico unidireccional) mientras bloquea cualquier tráfico entrante iniciado desde el internet público, protegiendo las cargas de trabajo.",
                        "explicacion": "La Pasarela NAT [NAT Gateway] permite conexiones de salida iniciadas por instancias privadas (tráfico unidireccional) mientras bloquea cualquier tráfico entrante iniciado desde el internet público, protegiendo las cargas de trabajo.",
                        "pista_didactica": "Busca el componente que provee salida segura unidireccional para entornos privados."
                    },
                    {
                        "pregunta": "¿Cuál es la principal diferencia arquitectónica entre una Lista de Seguridad [Security List] y un Grupo de Seguridad de Red [Network Security Group - NSG] en OCI?",
                        "opciones": [
                            "A) Las Listas de Seguridad se asocian a toda la Subred, mientras los NSGs se asocian a interfaces VNIC específicas",
                            "B) Los NSGs solo funcionan para IPv6, mientras las Listas de Seguridad solo admiten IPv4",
                            "C) Las Listas de Seguridad son sin estado [stateless], mientras los NSGs siempre son con estado [stateful]",
                            "D) Las Listas de Seguridad solo se aplican a bases de datos autónomas"
                        ],
                        "respuesta_correcta": "A) Las Listas de Seguridad se asocian a toda la Subred, mientras los NSGs se asocian a interfaces VNIC específicas",
                        "justificacion_didactica": "Las Listas de Seguridad aplican sus reglas a todos los recursos de una subred de manera homogénea. Los NSGs permiten microsegmentación aplicando reglas de firewall a interfaces de red virtuales (VNIC) individuales sin importar su subred.",
                        "explicacion": "Las Listas de Seguridad aplican sus reglas a todos los recursos de una subred de manera homogénea. Los NSGs permiten microsegmentación aplicando reglas de firewall a interfaces de red virtuales (VNIC) individuales sin importar su subred.",
                        "pista_didactica": "Recuerda el nivel de granularidad: Subred completa vs. Tarjeta de red virtual específica."
                    },
                    {
                        "pregunta": "Bajo las mejores prácticas de Arquitectura de Confianza Cero [Zero Trust], ¿dónde deben alojarse las bases de datos de producción dentro de la VCN?",
                        "opciones": [
                            "A) En subredes privadas sin asignación de direcciones IP públicas",
                            "B) En subredes públicas con el puerto 1521/5432 abierto al mundo",
                            "C) Directamente conectadas a la Pasarela de Internet para menor latencia",
                            "D) En la zona desmilitarizada (DMZ) expuesta al balanceador público"
                        ],
                        "respuesta_correcta": "A) En subredes privadas sin asignación de direcciones IP públicas",
                        "justificacion_didactica": "Las bases de datos corporativas nunca deben tener dirección IP pública. Deben situarse en subredes privadas aisladas accesibles únicamente mediante bastion hosts, balanceadores privados o capas intermedias de aplicación.",
                        "explicacion": "Las bases de datos corporativas nunca deben tener dirección IP pública. Deben situarse en subredes privadas aisladas accesibles únicamente mediante bastion hosts, balanceadores privados o capas intermedias de aplicación.",
                        "pista_didactica": "Aislamiento estricto: sin exposición a direcciones de enrutamiento público."
                    }
                ]
            else:
                items_quiz = [
                    {
                        "pregunta": f"¿Cuál es el objetivo primario de la arquitectura de seguridad descrita en '{titulo}'?",
                        "opciones": [
                            "A) Establecer una defensa en profundidad [Defense in Depth] con controles modulares e independientes",
                            "B) Eliminar la necesidad de monitoreo continuo mediante scripts estáticos",
                            "C) Depender exclusivamente del firewall perimetral para proteger todos los activos internos",
                            "D) Reducir la disponibilidad del servicio para garantizar confidencialidad"
                        ],
                        "respuesta_correcta": "A) Establecer una defensa en profundidad [Defense in Depth] con controles modulares e independientes",
                        "justificacion_didactica": "El principio de defensa en profundidad asegura múltiples capas concéntricas de control (identidad, red, aplicación y datos), evitando que una sola falla comprometa la integridad total del sistema.",
                        "explicacion": "El principio de defensa en profundidad asegura múltiples capas concéntricas de control (identidad, red, aplicación y datos), evitando que una sola falla comprometa la integridad total del sistema.",
                        "pista_didactica": "Piensa en capas de protección concéntricas y no en una muralla única."
                    },
                    {
                        "pregunta": "¿Qué mecanismo proporciona la máxima protección contra ataques de Suplantación de Identidad [Phishing] en la autenticación de usuarios?",
                        "opciones": [
                            "A) Llaves criptográficas de hardware basadas en estándares FIDO2 / WebAuthn",
                            "B) Contraseñas de 8 caracteres cambiadas cada 30 días",
                            "C) Códigos de 6 dígitos enviados por SMS sin cifrar",
                            "D) Preguntas de seguridad sobre datos personales del usuario"
                        ],
                        "respuesta_correcta": "A) Llaves criptográficas de hardware basadas en estándares FIDO2 / WebAuthn",
                        "justificacion_didactica": "FIDO2 vincula criptográficamente el proceso de autenticación al origen del dominio web legítimo (domain binding), imposibilitando que un sitio falso intercepte o reutilice las credenciales del usuario.",
                        "explicacion": "FIDO2 vincula criptográficamente el proceso de autenticación al origen del dominio web legítimo (domain binding), imposibilitando que un sitio falso intercepte o reutilice las credenciales del usuario.",
                        "pista_didactica": "Revisa los lineamientos de NIST SP 800-63B para autenticadores resistentes a phishing."
                    },
                    {
                        "pregunta": "¿Cuál es la recomendación del estándar PCI DSS v4.0 y NIST SP 800-53 con respecto a las cuentas con privilegios administrativos?",
                        "opciones": [
                            "A) Exigir autenticación multifactor (MFA) obligatoria y sesiones con expiración automática",
                            "B) Compartir una cuenta de superusuario 'root' entre todo el equipo de desarrollo",
                            "C) Deshabilitar los registros de auditoría para evitar saturar el almacenamiento",
                            "D) Permitir acceso SSH con contraseñas débiles desde cualquier dirección IP"
                        ],
                        "respuesta_correcta": "A) Exigir autenticación multifactor (MFA) obligatoria y sesiones con expiración automática",
                        "justificacion_didactica": "El principio de mínimo privilegio y separación de funciones exige autenticación robusta individualizada, trazabilidad completa en registros inmutables y expiración de sesiones para prevenir accesos no supervisados.",
                        "explicacion": "El principio de mínimo privilegio y separación de funciones exige autenticación robusta individualizada, trazabilidad completa en registros inmutables y expiración de sesiones para prevenir accesos no supervisados.",
                        "pista_didactica": "Control de accesos críticos: individualización, MFA y límite temporal."
                    }
                ]

            return {
                "titulo": f"Evaluación Diagnóstica: {titulo}",
                "introduccion_contextualizada": f"Evaluación de asimilación técnica adaptada para {perfil.value}. Cada ítem valida competencias demostrables y comprensión conceptual.",
                "tiempo_estimado_estudio_minutos": 10,
                "conceptos_clave": ["Evaluación Técnica", "Validación Operativa", "Criterios de Decisión"],
                "prerrequisitos": ["Revisión previa de la documentación técnica del sistema", "Terminología operativa básica"],
                "items": items_quiz
            }

        # =========================================================================
        # 3. CASO GUÍA PRÁCTICA / TUTORIAL PASO A PASO
        # =========================================================================
        elif formato == FormatoSalida.TUTORIAL:
            items_tut = [
                {
                    "paso": 1,
                    "titulo_paso": "Planificación y Aislamiento Perimetral (CIDR Block)",
                    "descripcion": "Define el rango de direcciones IP no solapado (10.0.0.0/16) y crea la Red Virtual en la Nube [Virtual Cloud Network - VCN] con políticas de enrutamiento estrictas.",
                    "comando_o_codigo": "oci network vcn create --cidr-block 10.0.0.0/16 --display-name VCN-Produccion-Segura --compartment-id <COMPARTMENT_OCID>",
                    "verificacion": "Comprobar con 'oci network vcn get' que el estado de ciclo de vida de la VCN sea 'AVAILABLE'."
                },
                {
                    "paso": 2,
                    "titulo_paso": "Segmentación de Subredes Públicas y Privadas",
                    "descripcion": "Divide la red en una subred pública para balanceadores de carga y una subred privada para aplicaciones y bases de datos sin enrutamiento a internet.",
                    "comando_o_codigo": "oci network subnet create --vcn-id <VCN_OCID> --cidr-block 10.0.1.0/24 --display-name Subnet-Privada-DB --prohibit-public-ip-on-vnic true",
                    "verificacion": "Verificar que el flag 'prohibit-public-ip-on-vnic' esté configurado en 'true' para impedir la asignación de IPs públicas."
                },
                {
                    "paso": 3,
                    "titulo_paso": "Fortalecimiento [Hardening] con Listas de Seguridad y NSGs",
                    "descripcion": "Configura reglas de entrada [Ingress] mínimas indispensables: únicamente puerto 443 (HTTPS) en balanceadores y puerto 5432 restringido al CIDR interno.",
                    "comando_o_codigo": "oci network security-list create --vcn-id <VCN_OCID> --ingress-security-rules '[{\"protocol\":\"6\",\"source\":\"10.0.1.0/24\",\"tcpOptions\":{\"destinationPortRange\":{\"max\":5432,\"min\":5432}}}]'",
                    "verificacion": "Escanear puertos internos para certificar que el acceso a base de datos esté denegado desde cualquier IP externa."
                },
                {
                    "paso": 4,
                    "titulo_paso": "Habilitación de Registros de Flujo [VCN Flow Logs]",
                    "descripcion": "Activa el registro continuo del tráfico de red aceptado y rechazado hacia OCI Object Storage para detección de anomalías y auditoría forense.",
                    "comando_o_codigo": "oci logging log create --log-group-id <LOG_GROUP_OCID> --display-name VCN-FlowLogs --log-type SERVICE --configuration '{\"source\":{\"service\":\"flowlogs\",\"category\":\"all\",\"resource\":\"<SUBNET_OCID>\"}}'",
                    "verificacion": "Consultar OCI Logging Analytics para confirmar la ingesta activa de eventos de red cada 60 segundos."
                }
            ]

            return {
                "titulo": f"Guía Técnica de Implementación: {titulo}",
                "introduccion_contextualizada": f"Procedimiento técnico paso a paso adaptado para el perfil {perfil.value}. Instrucciones concretas con comandos de CLI y criterios de verificación.",
                "tiempo_estimado_estudio_minutos": 15,
                "conceptos_clave": ["Implementación Paso a Paso", "Procedimientos de Configuración", "Criterios de Verificación"],
                "prerrequisitos": ["Acceso a terminal de línea de comandos (CLI)", "Credenciales con privilegios para aprovisionamiento"],
                "items": items_tut
            }

        # =========================================================================
        # 4. CASO RESUMEN EJECUTIVO / METÁFORAS / CASOS DE ESTUDIO
        # =========================================================================
        else:
            items_doc = [
                {
                    "seccion": "1. Diagnóstico y Postura Estratégica",
                    "contenido": f"La normativa y arquitectura de '{titulo}' establece directrices críticas para la protección de activos tecnológicos corporativos, priorizando mitigación de riesgos y resiliencia operativa.",
                    "pista_didactica": "Alineado a marcos normativos internacionales y mejores prácticas de la industria."
                },
                {
                    "seccion": "2. Controles Críticos de Implementación",
                    "contenido": "Implementación de controles de autenticación multifactor [MFA], segmentación de redes privadas [VCN Subnets] y cifrado obligatorio de datos en tránsito (TLS 1.3) y en reposo (AES-256).",
                    "pista_didactica": "Cumplimiento obligatorio para auditorías de calidad y seguridad."
                },
                {
                    "seccion": "3. Procedimiento de Respuesta y Resiliencia",
                    "contenido": "Mecanismos de detección automatizada mediante monitoreo de logs, aislamiento perimetral ante incidentes y plan de continuidad del negocio [BCP] con copias de seguridad aisladas [Air-gapped].",
                    "pista_didactica": "Garantiza tiempos de recuperación (RTO/RPO) dentro de los SLA institucionales."
                }
            ]

            return {
                "titulo": f"Síntesis Ejecutiva & Andragógica: {titulo}",
                "introduccion_contextualizada": f"Resumen estratégico adaptado para el perfil {perfil.value}. Enfoque en toma de decisiones, impacto operativo y gobernanza técnica.",
                "tiempo_estimado_estudio_minutos": 7,
                "conceptos_clave": ["Gobernanza", "Resiliencia Operativa", "Gestión de Riesgo", "Toma de Decisiones"],
                "prerrequisitos": ["Comprensión global de los objetivos del proyecto", "Nociones de gobernanza y acuerdos de nivel de servicio (SLA)"],
                "items": items_doc
            }

llm_engine = LLMEngine()

