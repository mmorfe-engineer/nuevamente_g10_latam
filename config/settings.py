"""
Módulo de Configuración Centralizada para NuevaMente.
Maneja variables de entorno, parámetros de OCI Always Free, configuración de LLMs y Vector Store.
"""
from pathlib import Path
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # Entorno y Logging
    APP_ENV: str = Field(default="development", description="Entorno de ejecución")
    LOG_LEVEL: str = Field(default="INFO", description="Nivel de logging")

    # Proveedores de LLM
    GEMINI_API_KEY: Optional[str] = Field(default=None, description="API Key de Google Gemini")
    OPENAI_API_KEY: Optional[str] = Field(default=None, description="API Key de OpenAI")
    ANTHROPIC_API_KEY: Optional[str] = Field(default=None, description="API Key de Anthropic")
    
    # NVIDIA NIM (DeepSeek / Llama)
    NVIDIA_API_KEY: Optional[str] = Field(default=None, description="API Key de NVIDIA NIM")
    NVIDIA_BASE_URL: str = Field(default="https://integrate.api.nvidia.com/v1", description="Endpoint base de NVIDIA NIM")
    NVIDIA_MODEL: str = Field(default="deepseek-ai/deepseek-v4-flash-0731", description="Modelo predeterminado de NVIDIA NIM")

    # Mistral AI
    MISTRAL_API_KEY: Optional[str] = Field(default=None, description="API Key de Mistral AI")
    MISTRAL_BASE_URL: str = Field(default="https://api.mistral.ai/v1", description="Endpoint base de Mistral AI")
    MISTRAL_MODEL: str = Field(default="mistral-small-latest", description="Modelo predeterminado de Mistral AI")

    DEFAULT_LLM_PROVIDER: str = Field(default="nvidia", description="Proveedor predeterminado (nvidia, mistral, gemini, openai)")
    DEFAULT_LLM_MODEL: str = Field(default="deepseek-ai/deepseek-r1", description="Modelo LLM predeterminado")

    # Oracle Cloud Infrastructure (OCI Always Free)
    OCI_CONFIG_FILE: str = Field(default="~/.oci/config", description="Ruta al archivo config de OCI")
    OCI_CONFIG_PROFILE: str = Field(default="DEFAULT", description="Perfil del archivo config OCI")
    OCI_USER_OCID: Optional[str] = Field(default=None, description="OCID del usuario OCI")
    OCI_FINGERPRINT: Optional[str] = Field(default=None, description="Fingerprint de la clave API")
    OCI_TENANCY_OCID: Optional[str] = Field(default=None, description="OCID del tenancy OCI")
    OCI_REGION: str = Field(default="us-ashburn-1", description="Región de OCI")
    OCI_KEY_FILE: Optional[str] = Field(default=None, description="Ruta de la clave privada PEM")
    OCI_OBJECT_STORAGE_NAMESPACE: Optional[str] = Field(default=None, description="Namespace de Object Storage")
    OCI_BUCKET_DOCS: str = Field(default="nuevamente-documentos-origen", description="Bucket para documentos originales")
    OCI_BUCKET_OUTPUTS: str = Field(default="nuevamente-contenidos-educativos", description="Bucket para contenidos generados")

    # Almacenamiento de Objetos Universal S3-Compatible (Desacoplado: OCI S3 API / Supabase / Cloudflare R2 / MinIO)
    STORAGE_PROVIDER: str = Field(default="s3_compatible", description="Proveedor de almacenamiento (s3_compatible, oci_native, emulated)")
    STORAGE_ENDPOINT_URL: Optional[str] = Field(default=None, description="Endpoint personalizado S3 (ej: https://{ns}.compat.objectstorage.{region}.oraclecloud.com)")
    STORAGE_ACCESS_KEY_ID: Optional[str] = Field(default=None, description="Access Key ID de S3 / Customer Secret Key de OCI")
    STORAGE_SECRET_ACCESS_KEY: Optional[str] = Field(default=None, description="Secret Access Key de S3 / Customer Secret Key de OCI")
    STORAGE_REGION: str = Field(default="us-ashburn-1", description="Región del proveedor de almacenamiento")
    STORAGE_BUCKET_DOCS: str = Field(default="nuevamente-documentos-origen", description="Bucket de documentos de origen")
    STORAGE_BUCKET_OUTPUTS: str = Field(default="nuevamente-contenidos-educativos", description="Bucket de contenidos educativos generados")

    # Vector Store & RAG
    CHROMA_PERSIST_DIR: str = Field(default=str(BASE_DIR / "data" / "chroma_db"), description="Directorio de persistencia de ChromaDB")
    EMBEDDING_MODEL: str = Field(default="all-MiniLM-L6-v2", description="Modelo de embeddings")
    DEFAULT_CHUNK_SIZE: int = Field(default=1000, description="Tamaño del chunk en caracteres")
    DEFAULT_CHUNK_OVERLAP: int = Field(default=150, description="Solapamiento entre chunks")
    TOP_K_RETRIEVAL: int = Field(default=4, description="Número de chunks relevantes a recuperar")
    MAX_CHUNKS_PER_BATCH: int = Field(default=80, description="Máximo de fragmentos indexados por lote representativo de adaptación")

    # Rutas locales auxiliares
    DATA_DIR: Path = BASE_DIR / "data"
    SAMPLES_DIR: Path = BASE_DIR / "data" / "samples"
    LOCAL_STORAGE_DIR: Path = BASE_DIR / "data" / "oci_local_storage"

    # Base de Datos (Relacional - Dual SQLite / PostgreSQL)
    DATABASE_URL: str = Field(default=f"sqlite:///{BASE_DIR}/data/nuevamente.db", description="URL de conexión a la base de datos (SQLite o PostgreSQL)")
    DB_ECHO: bool = Field(default=False, description="Activar log de queries SQL en consola")

settings = Settings()
