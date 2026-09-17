"""
Semilla y Catálogo Canónico del Glosario de Ciberseguridad Cloud — Estándar LexForja.
Alimenta la tabla 'glosario_ciberseguridad' en la base de datos relacional.
"""
from typing import List, Dict
from sqlalchemy.orm import Session
from src.storage.database import get_db
from src.storage.models import GlosarioCiberseguridadModel

GLOSARIO_SEMILLA: List[Dict[str, str]] = [
    {
        "termino_en": "Virtual Cloud Network (VCN)",
        "termino_es": "Red Virtual en la Nube (VCN)",
        "definicion_didactica": "Red definida por software personalizable y aislada dentro de Oracle Cloud Infrastructure.",
        "categoria": "Redes"
    },
    {
        "termino_en": "Stateful Ingress Security Lists",
        "termino_es": "Listas de Seguridad de Entrada con Estado",
        "definicion_didactica": "Reglas de firewall que rastrean conexiones entrantes y permiten el tráfico de respuesta automáticamente.",
        "categoria": "Redes"
    },
    {
        "termino_en": "Network Security Groups (NSGs)",
        "termino_es": "Grupos de Seguridad de Red (NSGs)",
        "definicion_didactica": "Reglas de seguridad granulares aplicadas directamente a interfaces de red (VNIC) individuales.",
        "categoria": "Redes"
    },
    {
        "termino_en": "Role-Based Access Control (RBAC)",
        "termino_es": "Control de Acceso Basado en Roles (RBAC)",
        "definicion_didactica": "Mecanismo de autorización que asigna permisos a usuarios según su rol funcional en la organización.",
        "categoria": "IAM"
    },
    {
        "termino_en": "Principle of Least Privilege",
        "termino_es": "Principio de Mínimo Privilegio",
        "definicion_didactica": "Norma de seguridad que otorga a usuarios o sistemas únicamente los permisos mínimos requeridos para su tarea.",
        "categoria": "IAM"
    },
    {
        "termino_en": "Multi-Factor Authentication (MFA)",
        "termino_es": "Autenticación Multifactor (MFA)",
        "definicion_didactica": "Requisito de seguridad que exige dos o más evidencias independientes antes de conceder acceso.",
        "categoria": "IAM"
    },
    {
        "termino_en": "Supply Chain Risk Management (SCRM)",
        "termino_es": "Gestión de Riesgos en la Cadena de Suministro (SCRM)",
        "definicion_didactica": "Proceso sistemático de identificación y mitigación de amenazas asociadas a proveedores de hardware y software.",
        "categoria": "Gobernanza"
    },
    {
        "termino_en": "Software Bill of Materials (SBOM)",
        "termino_es": "Inventario de Componentes de Software (SBOM)",
        "definicion_didactica": "Registro formal que desglosa todas las dependencias y bibliotecas de código abierto usadas en una aplicación.",
        "categoria": "Gobernanza"
    },
    {
        "termino_en": "Business Continuity Plan (BCP)",
        "termino_es": "Plan de Continuidad de Negocio (BCP)",
        "definicion_didactica": "Conjunto de procedimientos preventivos y de respuesta para asegurar la operatividad crítica ante desastres.",
        "categoria": "Resiliencia"
    },
    {
        "termino_en": "Disaster Recovery Plan (DRP)",
        "termino_es": "Plan de Recuperación ante Desastres (DRP)",
        "definicion_didactica": "Estrategia técnica para restaurar sistemas informáticos y datos tras una catástrofe o ciberataque.",
        "categoria": "Resiliencia"
    },
    {
        "termino_en": "Cardholder Data Environment (CDE)",
        "termino_es": "Entorno de Datos de Tarjetahabientes (CDE)",
        "definicion_didactica": "Zona protegida de red donde se procesan, transmiten o almacenan datos de tarjetas de pago según PCI-DSS.",
        "categoria": "Bancario"
    },
    {
        "termino_en": "Ransomware Containment Protocol",
        "termino_es": "Protocolo de Contención de Ransomware",
        "definicion_didactica": "Secuencia inmediata de aislamiento de endpoints y corte de tráfico de red para frenar el cifrado malicioso.",
        "categoria": "Resiliencia"
    }
]


def seed_glosario_database(db: Session) -> int:
    """Inserta o actualiza los términos semilla en la base de datos."""
    inserted = 0
    for item in GLOSARIO_SEMILLA:
        existing = db.query(GlosarioCiberseguridadModel).filter_by(termino_en=item["termino_en"]).first()
        if not existing:
            nuevo = GlosarioCiberseguridadModel(
                termino_en=item["termino_en"],
                termino_es=item["termino_es"],
                definicion_didactica=item["definicion_didactica"],
                categoria=item["categoria"]
            )
            db.add(nuevo)
            inserted += 1
    db.commit()
    return inserted
