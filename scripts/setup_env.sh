#!/bin/bash
# ==============================================================================
# NUEVAMENTE - Asistente de Configuración de Credenciales (.env)
# ==============================================================================

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

ENV_FILE="$PROJECT_DIR/.env"

echo "================================================================="
echo "       🎓 NUEVAMENTE - CONFIGURACIÓN DE APIS Y BASE DE DATOS    "
echo "================================================================="
echo ""
echo "Este script te guiará para configurar tus credenciales en el archivo .env"
echo "Tus claves se guardarán localmente y nunca se subirán a Git."
echo ""

# Si ya existe .env, cargar valores actuales
if [ -f "$ENV_FILE" ]; then
    echo "ℹ️  Archivo .env detectado. Mostrando configuración actual..."
    EXISTING_NVIDIA=$(grep "^NVIDIA_API_KEY=" "$ENV_FILE" | cut -d '=' -f2- || true)
    EXISTING_MISTRAL=$(grep "^MISTRAL_API_KEY=" "$ENV_FILE" | cut -d '=' -f2- || true)
    EXISTING_DB=$(grep "^DATABASE_URL=" "$ENV_FILE" | cut -d '=' -f2- || true)
else
    EXISTING_NVIDIA=""
    EXISTING_MISTRAL=""
    EXISTING_DB="sqlite:///data/nuevamente.db"
fi

# 1. NVIDIA API Key
echo ""
echo "--- [1/3] NVIDIA NIM API KEY (DeepSeek / Llama) ---"
if [ -n "$EXISTING_NVIDIA" ]; then
    MASKED_NVIDIA="${EXISTING_NVIDIA:0:6}...${EXISTING_NVIDIA: -4}"
    read -rp "API Key de NVIDIA actual ($MASKED_NVIDIA) [Presiona ENTER para mantener, o pega una nueva]: " INPUT_NVIDIA
    NVIDIA_KEY="${INPUT_NVIDIA:-$EXISTING_NVIDIA}"
else
    read -rp "Pega tu NVIDIA_API_KEY (ej. nvapi-...): " INPUT_NVIDIA
    NVIDIA_KEY="$INPUT_NVIDIA"
fi

# 2. Mistral API Key
echo ""
echo "--- [2/3] MISTRAL AI API KEY ---"
if [ -n "$EXISTING_MISTRAL" ]; then
    MASKED_MISTRAL="${EXISTING_MISTRAL:0:6}...${EXISTING_MISTRAL: -4}"
    read -rp "API Key de Mistral actual ($MASKED_MISTRAL) [Presiona ENTER para mantener, o pega una nueva]: " INPUT_MISTRAL
    MISTRAL_KEY="${INPUT_MISTRAL:-$EXISTING_MISTRAL}"
else
    read -rp "Pega tu MISTRAL_API_KEY: " INPUT_MISTRAL
    MISTRAL_KEY="$INPUT_MISTRAL"
fi

# 3. Base de Datos
echo ""
echo "--- [3/3] BASE DE DATOS (SQL) ---"
echo "Opciones recomendadas:"
echo "  1) SQLite local enriquecido (data/nuevamente.db) -> Cero configuración"
echo "  2) Neon Serverless Postgres -> Pega tu URL (postgresql://...)"
echo ""
if [ -n "$EXISTING_DB" ]; then
    read -rp "DATABASE_URL [$EXISTING_DB]: " INPUT_DB
    DB_URL="${INPUT_DB:-$EXISTING_DB}"
else
    read -rp "DATABASE_URL [sqlite:///data/nuevamente.db]: " INPUT_DB
    DB_URL="${INPUT_DB:-sqlite:///data/nuevamente.db}"
fi

# Generar archivo .env
cat <<EOF > "$ENV_FILE"
# ==============================================================================
# NUEVAMENTE - VARIABLES DE ENTORNO OFICIALES
# ==============================================================================

# Entorno
APP_ENV=development
LOG_LEVEL=INFO

# ------------------------------------------------------------------------------
# 1. Proveedores LLM
# ------------------------------------------------------------------------------
# NVIDIA NIM (DeepSeek R1 / V3 - Motor Principal)
NVIDIA_API_KEY=$NVIDIA_KEY
NVIDIA_BASE_URL=https://integrate.api.nvidia.com/v1
NVIDIA_MODEL=deepseek-ai/deepseek-r1

# Mistral AI (Motor de Respaldo / Especialista)
MISTRAL_API_KEY=$MISTRAL_KEY
MISTRAL_BASE_URL=https://api.mistral.ai/v1
MISTRAL_MODEL=mistral-small-latest

# Configuración del Motor por defecto
DEFAULT_LLM_PROVIDER=nvidia
DEFAULT_LLM_MODEL=deepseek-ai/deepseek-r1

# ------------------------------------------------------------------------------
# 2. Base de Datos Relacional (SQLAlchemy 2.0)
# ------------------------------------------------------------------------------
# SQLite local o Neon Serverless Postgres
DATABASE_URL=$DB_URL
DB_ECHO=false

# ------------------------------------------------------------------------------
# 3. Vector Store & RAG
# ------------------------------------------------------------------------------
CHROMA_PERSIST_DIR=./data/chroma_db
EMBEDDING_MODEL=all-MiniLM-L6-v2

# ------------------------------------------------------------------------------
# 4. Oracle Cloud Infrastructure (OCI Always Free)
# ------------------------------------------------------------------------------
OCI_USER_OCID=
OCI_FINGERPRINT=
OCI_TENANCY_OCID=
OCI_REGION=us-ashburn-1
OCI_KEY_FILE=~/.oci/oci_api_key.pem
OCI_OBJECT_STORAGE_NAMESPACE=
OCI_BUCKET_DOCS=nuevamente-documentos-origen
OCI_BUCKET_OUTPUTS=nuevamente-contenidos-educativos
EOF

chmod 600 "$ENV_FILE"

echo ""
echo "✅ Archivo .env generado exitosamente en: $ENV_FILE"
echo "🔒 Permisos asignados: 600 (solo lectura/escritura para tu usuario)."
echo ""
echo "Probando carga de configuración con Python..."
venv/bin/python -c "from config.settings import settings; print(f'Proveedor predeterminado: {settings.DEFAULT_LLM_PROVIDER} | Modelo: {settings.DEFAULT_LLM_MODEL} | BD: {settings.DATABASE_URL.split(\"@\")[-1]}')"
echo ""
echo "🎉 ¡Configuración lista para la ingesta SQL y el pipeline de agentes!"
