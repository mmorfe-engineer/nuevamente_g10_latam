#!/usr/bin/env python3
"""
Script Oficial de Ingesta y Carga del Corpus de Ciberseguridad en SQL — Proyecto NuevaMente.
Procesa los 7 documentos oficiales del corpus (1,132 páginas),
extrae fragmentos contextuales, genera síntesis técnica en español (Estándar LexForja),
asigna roles NIST NICE y persiste todo en la base de datos relacional y ChromaDB.
"""
import os
import sys
import time
from pathlib import Path

# Asegurar path del proyecto
PROJECT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_DIR))

from config.settings import settings
from src.storage.database import init_db, SessionLocal
from src.storage.models import CorpusDocumentoModel, CorpusChunkModel, GlosarioCiberseguridadModel
from src.storage.seed_glossary import seed_glosario_database
from src.ingestion.lexforja_pipeline import LexForjaPipeline

# Catálogo oficial de los 7 documentos
CORPUS_CATALOG = [
    {
        "file": "01_nist_sp_800_161r1_riesgo_proveedores_ti.pdf",
        "doc_id": "NIST-SP-800-161R1",
        "titulo": "NIST SP 800-161r1: Cybersecurity Supply Chain Risk Management (C-SCRM)",
        "version_normativa": "Revision 1",
        "idioma": "en"
    },
    {
        "file": "02_cisa_nsa_guia_phishing_antifraude.pdf",
        "doc_id": "CISA-NSA-PHISHING",
        "titulo": "CISA/NSA: Guía de Mitigación de Phishing y Autenticación FIDO2",
        "version_normativa": "2023.1",
        "idioma": "en"
    },
    {
        "file": "03_cis_oracle_cloud_infrastructure_v3_1_1.pdf",
        "doc_id": "CIS-OCI-V3.1.1",
        "titulo": "CIS Oracle Cloud Infrastructure Foundations Benchmark v3.1.1",
        "version_normativa": "v3.1.1",
        "idioma": "en"
    },
    {
        "file": "04_cisa_fbi_guia_stop_ransomware_bcp.pdf",
        "doc_id": "CISA-FBI-RANSOMWARE",
        "titulo": "CISA/FBI: StopRansomware Guide & Plan de Continuidad de Negocio (BCP)",
        "version_normativa": "2023.2",
        "idioma": "en"
    },
    {
        "file": "05_pci_dss_v4_0_la_seguridad_bancaria.pdf",
        "doc_id": "PCI-DSS-V4.0",
        "titulo": "PCI-DSS v4.0: Estándar de Seguridad de Datos para la Industria de Tarjetas de Pago",
        "version_normativa": "v4.0",
        "idioma": "es"
    },
    {
        "file": "06_pci_dss_v4_0_a_v4_0_1_resumen_cambios.pdf",
        "doc_id": "PCI-DSS-V4.0.1-CHANGES",
        "titulo": "PCI-DSS v4.0 a v4.0.1: Resumen de Cambios y Nuevos Requisitos de Tokenización",
        "version_normativa": "v4.0.1",
        "idioma": "es"
    },
    {
        "file": "07_cis_oracle_saas_cloud_applications_v1_0_0.pdf",
        "doc_id": "CIS-ORACLE-SAAS",
        "titulo": "CIS Oracle SaaS Cloud Applications Foundations Benchmark v1.0.0",
        "version_normativa": "v1.0.0",
        "idioma": "en"
    }
]


def main():
    print("=================================================================")
    print("      🚀 INGESTA DEL CORPUS REAL DE CIBERSEGURIDAD EN SQL       ")
    print("=================================================================")
    print(f"Base de Datos configurada: {settings.DATABASE_URL.split('@')[-1]}")
    print(f"Proveedor LLM activo: {settings.DEFAULT_LLM_PROVIDER} ({settings.DEFAULT_LLM_MODEL})")
    print("")

    start_time = time.time()

    # 1. Inicializar Tablas en la Base de Datos
    print("1️⃣  Inicializando tablas en la base de datos relacional...")
    init_db()

    session = SessionLocal()
    try:
        # 2. Sembrar Glosario Canónico Bilingüe
        print("2️⃣  Sembrando glosario canónico de ciberseguridad...")
        seed_glosario_database(session)
        total_glosario = session.query(GlosarioCiberseguridadModel).count()
        print(f"   ✅ Glosario sembrado con {total_glosario} términos oficiales.")

        # 3. Procesar cada documento del catálogo
        print("\n3️⃣  Procesando e ingiriendo los 7 documentos PDF...")
        pipeline = LexForjaPipeline(db_session=session)
        fuentes_dir = PROJECT_DIR / "data" / "fuentes_ciberseguridad"

        for idx, doc_meta in enumerate(CORPUS_CATALOG, 1):
            file_path = fuentes_dir / doc_meta["file"]
            print(f"\n--- [{idx}/7] {doc_meta['titulo']} ---")
            print(f"   Archivo: {doc_meta['file']}")
            
            if not file_path.exists():
                print(f"   ⚠️ Archivo no encontrado en {file_path}, saltando.")
                continue

            doc_start = time.time()
            res = pipeline.ingest_document(
                file_path=str(file_path),
                doc_id=doc_meta["doc_id"],
                titulo=doc_meta["titulo"],
                version_normativa=doc_meta["version_normativa"],
                idioma=doc_meta["idioma"]
            )
            doc_elapsed = time.time() - doc_start
            chunks_cnt = res.get('total_chunks_procesados', 0)
            sha_str = res.get('sha256', '')[:12]
            print(f"   ✅ Ingesta completada en {doc_elapsed:.2f}s:")
            print(f"      - ID Documento: {res.get('doc_id')}")
            print(f"      - Chunks indexados en SQL y VectorStore: {chunks_cnt}")
            print(f"      - SHA-256: {sha_str}... | Estado: {res.get('status', 'OK')}")

        # 4. Resumen final de la base de datos relacional
        total_docs = session.query(CorpusDocumentoModel).count()
        total_chunks = session.query(CorpusChunkModel).count()
        elapsed_total = time.time() - start_time

        print("\n=================================================================")
        print("🎉 INGESTA REAL EN BASE DE DATOS SQL COMPLETADA EXITOSAMENTE")
        print("=================================================================")
        print(f"⏱️  Tiempo total de procesamiento: {elapsed_total:.2f} segundos")
        print(f"📄 Documentos en 'corpus_documentos': {total_docs}")
        print(f"🧩 Fragmentos enriquecidos en 'corpus_chunks': {total_chunks}")
        print(f"📖 Términos bilingües en 'glosario_ciberseguridad': {total_glosario}")
        print("=================================================================\n")

    finally:
        session.close()


if __name__ == "__main__":
    main()
