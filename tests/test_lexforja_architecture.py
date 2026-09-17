"""
Pruebas Unitarias para la Arquitectura LexForja (Ingesta Asimétrica y Base de Datos Enriquecida).
Verifica:
1. Modelos Relacionales: CorpusDocumentoModel, CorpusChunkModel y GlosarioCiberseguridadModel.
2. Regla de Precedencia Determinista: Resolución de colisiones y enmiendas normativas.
3. Validador Parentético de Nomenclatura Canónica: Término en Español [Término Canónico en Inglés].
4. Búsqueda y Enriquecimiento de Glosario.
"""
import pytest
from datetime import datetime
from src.storage.database import SessionLocal, init_db
from src.storage.models import CorpusDocumentoModel, CorpusChunkModel, GlosarioCiberseguridadModel
from src.storage.repository import CorpusRepository, GlosarioRepository
from src.storage.seed_glossary import seed_glosario_database
from src.utils.validators import LexForjaValidator, lexforja_validator


@pytest.fixture(scope="module")
def db_session():
    init_db()
    session = SessionLocal()
    seed_glosario_database(session)
    yield session
    session.close()


def test_glosario_seed_and_search(db_session):
    """Verifica que el glosario semilla contiene los términos canónicos y permite búsquedas cruzadas."""
    terms = GlosarioRepository.get_all(db_session)
    assert len(terms) >= 12

    # Búsqueda por término en inglés
    vcn = GlosarioRepository.get_by_term_en(db_session, "Virtual Cloud Network (VCN)")
    assert vcn is not None
    assert vcn.categoria == "Redes"
    assert "Red Virtual" in vcn.termino_es

    # Búsqueda parcial por término en español
    results = GlosarioRepository.search(db_session, "Mínimo Privilegio")
    assert len(results) >= 1
    assert "Least Privilege" in results[0].termino_en


def test_corpus_document_and_chunks_persistence(db_session):
    """Verifica el registro de un documento y sus fragmentos enriquecidos con síntesis en español."""
    doc_id = "doc-test-pci-dss"
    
    # Limpiar si existía
    existing = db_session.query(CorpusDocumentoModel).filter_by(doc_id=doc_id).first()
    if existing:
        db_session.delete(existing)
        db_session.commit()

    doc_data = {
        "doc_id": doc_id,
        "titulo": "PCI-DSS v4.0 Estándar Oficial",
        "archivo_origen": "05_pci_dss_v4_0_la_seguridad_bancaria.pdf",
        "idioma": "es",
        "version_normativa": "4.0",
        "peso_bytes": 3500000,
        "sha256_hash": "a1b2c3d4e5f67890abcdef1234567890abcdef1234567890abcdef1234567890"
    }
    doc = CorpusRepository.create_document(db_session, doc_data)
    assert doc.doc_id == doc_id
    assert doc.version_normativa == "4.0"

    # Chunks enriquecidos
    chunks_data = [
        {
            "chunk_id": "chunk-pci-01",
            "doc_id": doc_id,
            "pagina_numero": 45,
            "capitulo_seccion": "Requisito 7: Restringir acceso al CDE",
            "contenido_original": "Restrict access to system components and cardholder data by business need to know.",
            "sintesis_espanol": "Restricción de accesos al entorno de datos de tarjetahabientes bajo necesidad estricta de conocer.",
            "terminos_clave_en": ["Cardholder Data Environment (CDE)", "Need to Know"],
            "terminos_clave_es": ["Entorno de Datos de Tarjetahabientes", "Necesidad de Conocer"],
            "aplicabilidad_roles": ["desarrollador", "auditor", "sysadmin"],
            "version_prioridad": 1.0
        }
    ]
    chunks = CorpusRepository.create_chunks(db_session, chunks_data)
    assert len(chunks) == 1
    assert chunks[0].chunk_id == "chunk-pci-01"
    assert "CDE" in chunks[0].terminos_clave_en[0]


def test_lexforja_deterministic_precedence_rule(db_session):
    """
    Verifica la Regla de Precedencia Determinista:
    Si un chunk de la enmienda (v4.0.1) modifica a uno anterior (v4.0),
    el de la enmienda adquiere prioridad forzada y el modificado es desplazado.
    """
    doc_id = "doc-test-precedence"
    existing = db_session.query(CorpusDocumentoModel).filter_by(doc_id=doc_id).first()
    if existing:
        db_session.delete(existing)
        db_session.commit()

    doc = CorpusRepository.create_document(db_session, {
        "doc_id": doc_id,
        "titulo": "Normativa Base y Enmienda",
        "archivo_origen": "test_precedence.pdf",
        "idioma": "en",
        "version_normativa": "4.0",
        "peso_bytes": 1000,
        "sha256_hash": "hash_precedence_test"
    })

    # Chunk base v4.0 y chunk enmienda v4.0.1
    chunks_data = [
        {
            "chunk_id": "chunk-v40-req8",
            "doc_id": doc_id,
            "pagina_numero": 100,
            "capitulo_seccion": "Requisito 8.2: Longitud de Contraseñas",
            "contenido_original": "Passwords must be at least 12 characters.",
            "sintesis_espanol": "Las contraseñas deben tener al menos 12 caracteres.",
            "version_prioridad": 1.0
        },
        {
            "chunk_id": "chunk-v401-amendment",
            "doc_id": doc_id,
            "pagina_numero": 5,
            "capitulo_seccion": "Enmienda 4.0.1: Requisito 8.2",
            "contenido_original": "Passwords must be at least 14 characters for service accounts.",
            "sintesis_espanol": "Las contraseñas deben tener al menos 14 caracteres para cuentas de servicio.",
            "modifica_a_chunk_id": "chunk-v40-req8",  # Puntero explícito de modificación
            "version_prioridad": 2.0  # Prioridad mayor de enmienda
        }
    ]
    CorpusRepository.create_chunks(db_session, chunks_data)

    ordered_chunks = CorpusRepository.get_chunks_with_precedence(db_session, doc_id=doc_id)
    assert len(ordered_chunks) == 2
    # El primer chunk debe ser la enmienda vigente v4.0.1
    assert ordered_chunks[0].chunk_id == "chunk-v401-amendment"
    assert ordered_chunks[0].modifica_a_chunk_id == "chunk-v40-req8"
    # El segundo debe ser el chunk original modificado
    assert ordered_chunks[1].chunk_id == "chunk-v40-req8"


def test_parenthetical_nomenclature_validator():
    """Verifica que el validador regex detecte correctamente la regla Término en Español [Término Canónico en Inglés]."""
    valid_text = (
        "Para proteger la base de datos, configure las Listas de Seguridad de Entrada con Estado "
        "[Stateful Ingress Security Lists] en la Red Virtual en la Nube [Virtual Cloud Network (VCN)] "
        "aplicando el Principio de Mínimo Privilegio [Principle of Least Privilege]."
    )
    result = lexforja_validator.validate_text_nomenclature(valid_text)
    assert result["is_valid"] is True
    assert result["parenthetical_count"] == 3
    assert result["compliance_score"] == 1.0

    pairs = result["extracted_pairs"]
    assert any("Stateful Ingress" in p["termino_en"] for p in pairs)
    assert any("Least Privilege" in p["termino_en"] for p in pairs)


def test_parenthetical_nomenclature_enforcement():
    """Verifica que el validador pueda enriquecer texto plano inyectando los términos en inglés faltantes."""
    raw_text = (
        "El desarrollador debe crear una Red Virtual en la Nube y asignar el Principio de Mínimo Privilegio."
    )
    glossary = [
        {"termino_es": "Red Virtual en la Nube", "termino_en": "Virtual Cloud Network (VCN)"},
        {"termino_es": "Principio de Mínimo Privilegio", "termino_en": "Principle of Least Privilege"}
    ]

    enforced = lexforja_validator.enforce_parenthetical_terms(raw_text, glossary)
    assert "[Virtual Cloud Network (VCN)]" in enforced
    assert "[Principle of Least Privilege]" in enforced

    # Verificar que al pasar por el validador ahora es 100% válido
    val_result = lexforja_validator.validate_text_nomenclature(enforced)
    assert val_result["is_valid"] is True
    assert val_result["parenthetical_count"] == 2
