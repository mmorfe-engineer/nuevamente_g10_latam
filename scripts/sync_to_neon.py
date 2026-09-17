#!/usr/bin/env python3
"""
Sincronizador Oficial de Base de Datos Local a Neon Serverless PostgreSQL — Proyecto NuevaMente.
Permite reflejar el esquema relacional, los documentos del corpus, los fragmentos y el glosario
hacia la base de datos PostgreSQL 18.6 en Neon a través de la API HTTPS oficial (Puerto 443),
superando restricciones de cortafuegos en puertos directos (5432).
"""
import os
import sys
import json
import urllib.parse
from pathlib import Path
import requests

PROJECT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_DIR))

from config.settings import settings
from src.storage.database import SessionLocal
from src.storage.models import CorpusDocumentoModel, CorpusChunkModel, GlosarioCiberseguridadModel


def get_neon_config():
    neon_url = os.environ.get("NEON_DATABASE_URL")
    if not neon_url:
        # Intentar leer desde settings o .env
        from dotenv import dotenv_values
        env_vals = dotenv_values(PROJECT_DIR / ".env")
        neon_url = env_vals.get("NEON_DATABASE_URL")
    
    if not neon_url:
        raise ValueError("NEON_DATABASE_URL no encontrada en el archivo .env")

    clean_url = neon_url.replace('&channel_binding=require', '').replace('channel_binding=require&', '').replace('channel_binding=require', '').replace('-pooler', '')
    u = urllib.parse.urlparse(clean_url)
    api_url = f"https://{u.hostname}/sql"
    headers = {
        "Neon-Connection-String": clean_url,
        "Content-Type": "application/json"
    }
    return api_url, headers


def execute_neon_query(api_url, headers, sql, params=None):
    payload = {"query": sql}
    if params:
        payload["params"] = params
    resp = requests.post(api_url, headers=headers, json=payload, timeout=30)
    if resp.status_code != 200:
        raise RuntimeError(f"Error Neon HTTP ({resp.status_code}): {resp.text}")
    return resp.json()


def create_neon_schema(api_url, headers):
    print("🛠️  Creando esquema relacional en Neon PostgreSQL...")
    
    ddl_statements = [
        # Glosario
        """
        CREATE TABLE IF NOT EXISTS glosario_ciberseguridad (
            id SERIAL PRIMARY KEY,
            termino_en VARCHAR(150) UNIQUE NOT NULL,
            termino_es VARCHAR(150) NOT NULL,
            definicion_didactica TEXT NOT NULL,
            categoria VARCHAR(50) DEFAULT 'General' NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
        );
        """,
        # Documentos Corpus
        """
        CREATE TABLE IF NOT EXISTS corpus_documentos (
            doc_id VARCHAR(50) PRIMARY KEY,
            titulo VARCHAR(255) NOT NULL,
            archivo_origen VARCHAR(255) NOT NULL,
            idioma VARCHAR(10) DEFAULT 'en' NOT NULL,
            version_normativa VARCHAR(50),
            peso_bytes INTEGER DEFAULT 0 NOT NULL,
            sha256_hash VARCHAR(64) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
        );
        """,
        # Chunks Corpus
        """
        CREATE TABLE IF NOT EXISTS corpus_chunks (
            chunk_id VARCHAR(50) PRIMARY KEY,
            doc_id VARCHAR(50) NOT NULL REFERENCES corpus_documentos(doc_id) ON DELETE CASCADE,
            pagina_numero INTEGER DEFAULT 1 NOT NULL,
            capitulo_seccion VARCHAR(255),
            contenido_original TEXT NOT NULL,
            sintesis_espanol TEXT NOT NULL,
            terminos_clave_en JSONB DEFAULT '[]'::jsonb NOT NULL,
            terminos_clave_es JSONB DEFAULT '[]'::jsonb NOT NULL,
            aplicabilidad_roles JSONB DEFAULT '[]'::jsonb NOT NULL,
            modifica_a_chunk_id VARCHAR(50),
            version_prioridad FLOAT DEFAULT 1.0 NOT NULL,
            embedding_id VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
        );
        """
    ]

    for stmt in ddl_statements:
        execute_neon_query(api_url, headers, stmt.strip())
    print("   ✅ Esquema creado/verificado exitosamente en Neon.")


def sync():
    api_url, headers = get_neon_config()
    print("=================================================================")
    print("   🌐 SINCRONIZACIÓN A NEON SERVERLESS POSTGRESQL (HTTPS)        ")
    print("=================================================================")
    print(f"Endpoint Neon: {api_url}\n")

    create_neon_schema(api_url, headers)

    session = SessionLocal()
    try:
        # 1. Sincronizar Glosario
        glossary_items = session.query(GlosarioCiberseguridadModel).all()
        print(f"\n📖 Sincronizando {len(glossary_items)} términos del glosario...")
        for g in glossary_items:
            sql = """
            INSERT INTO glosario_ciberseguridad (termino_en, termino_es, definicion_didactica, categoria)
            VALUES ($1, $2, $3, $4)
            ON CONFLICT (termino_en) DO UPDATE 
            SET termino_es = EXCLUDED.termino_es,
                definicion_didactica = EXCLUDED.definicion_didactica,
                categoria = EXCLUDED.categoria;
            """
            execute_neon_query(api_url, headers, sql, [g.termino_en, g.termino_es, g.definicion_didactica, g.categoria])
        print("   ✅ Glosario sincronizado.")

        # 2. Sincronizar Documentos
        docs = session.query(CorpusDocumentoModel).all()
        print(f"\n📄 Sincronizando {len(docs)} documentos del corpus...")
        for d in docs:
            sql = """
            INSERT INTO corpus_documentos (doc_id, titulo, archivo_origen, idioma, version_normativa, peso_bytes, sha256_hash)
            VALUES ($1, $2, $3, $4, $5, $6, $7)
            ON CONFLICT (doc_id) DO UPDATE 
            SET titulo = EXCLUDED.titulo,
                archivo_origen = EXCLUDED.archivo_origen,
                idioma = EXCLUDED.idioma,
                version_normativa = EXCLUDED.version_normativa,
                peso_bytes = EXCLUDED.peso_bytes,
                sha256_hash = EXCLUDED.sha256_hash;
            """
            execute_neon_query(api_url, headers, sql, [d.doc_id, d.titulo, d.archivo_origen, d.idioma, d.version_normativa, d.peso_bytes, d.sha256_hash])
        print("   ✅ Documentos sincronizados.")

        # 3. Sincronizar Chunks
        chunks = session.query(CorpusChunkModel).all()
        print(f"\n🧩 Sincronizando {len(chunks)} fragmentos enriquecidos...")
        synced = 0
        for c in chunks:
            sql = """
            INSERT INTO corpus_chunks (
                chunk_id, doc_id, pagina_numero, capitulo_seccion, contenido_original,
                sintesis_espanol, terminos_clave_en, terminos_clave_es, aplicabilidad_roles,
                modifica_a_chunk_id, version_prioridad, embedding_id
            )
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
            ON CONFLICT (chunk_id) DO UPDATE
            SET sintesis_espanol = EXCLUDED.sintesis_espanol,
                terminos_clave_en = EXCLUDED.terminos_clave_en,
                terminos_clave_es = EXCLUDED.terminos_clave_es,
                aplicabilidad_roles = EXCLUDED.aplicabilidad_roles;
            """
            execute_neon_query(api_url, headers, sql, [
                c.chunk_id,
                c.doc_id,
                c.pagina_numero,
                c.capitulo_seccion,
                c.contenido_original,
                c.sintesis_espanol,
                json.dumps(c.termino_clave_en if hasattr(c, 'termino_clave_en') else (c.terminos_clave_en or [])),
                json.dumps(c.terminos_clave_es or []),
                json.dumps(c.aplicabilidad_roles or []),
                c.modifica_a_chunk_id,
                float(c.version_prioridad),
                c.embedding_id
            ])
            synced += 1
            if synced % 100 == 0 or synced == len(chunks):
                print(f"   ... {synced}/{len(chunks)} fragmentos transferidos a Neon")

        # 4. Verificar en Neon
        res_docs = execute_neon_query(api_url, headers, "SELECT COUNT(*) as total FROM corpus_documentos;")
        res_chunks = execute_neon_query(api_url, headers, "SELECT COUNT(*) as total FROM corpus_chunks;")
        res_gloss = execute_neon_query(api_url, headers, "SELECT COUNT(*) as total FROM glosario_ciberseguridad;")

        print("\n=================================================================")
        print("🎉 SINCRONIZACIÓN EXITOSA CON NEON SERVERLESS POSTGRESQL 18")
        print("=================================================================")
        print(f"📄 Documentos en Neon: {res_docs['rows'][0]['total']}")
        print(f"🧩 Fragmentos en Neon: {res_chunks['rows'][0]['total']}")
        print(f"📖 Términos en Neon: {res_gloss['rows'][0]['total']}")
        print("=================================================================\n")

    finally:
        session.close()


if __name__ == "__main__":
    sync()
