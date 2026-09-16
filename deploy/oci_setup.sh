#!/usr/bin/env bash
# ==============================================================================
# SCRIPT DE APROVISIONAMIENTO Y DESPLIEGUE AUTOMATIZADO EN OCI ALWAYS FREE
# Plataforma: Oracle Linux 8/9 o Ubuntu 22.04 LTS (Shape VM.Standard.A1.Flex)
# Proyecto: NuevaMente (Hackathon ONE G10 / No Country)
# ==============================================================================
set -euo pipefail

echo "=================================================================="
echo "🚀 INICIANDO INSTALACIÓN DE NUEVAMENTE EN OCI COMPUTE ALWAYS FREE"
echo "=================================================================="

# 1. Actualización de paquetes del sistema
echo "📦 1. Actualizando paquetes del sistema..."
if [ -f /etc/oracle-release ]; then
    sudo dnf update -y
    sudo dnf install -y python3.11 python3.11-devel git gcc
elif [ -f /etc/debian_version ]; then
    sudo apt-get update -y
    sudo apt-get install -y python3.11 python3.11-venv python3-pip git build-essential
fi

# 2. Configurar Firewall local del SO para permitir puerto 8501
echo "🛡️ 2. Abriendo puerto 8501 en el firewall local de la instancia..."
if command -v firewall-cmd &> /dev/null; then
    sudo firewall-cmd --zone=public --add-port=8501/tcp --permanent || true
    sudo firewall-cmd --reload || true
elif command -v ufw &> /dev/null; then
    sudo ufw allow 8501/tcp || true
fi

# 3. Setup de entorno virtual
echo "🐍 3. Creando entorno virtual Python 3.11..."
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

# 4. Crear directorios de datos y réplicas locales
echo "📁 4. Inicializando directorios de persistencia..."
mkdir -p data/chroma_db data/samples data/oci_local_storage/nuevamente-documentos-origen data/oci_local_storage/nuevamente-contenidos-educativos

# 5. Ejecutar suite de pruebas de aceptación
echo "🧪 5. Ejecutando pruebas automatizadas de aseguramiento DoD..."
pytest tests/ -v

echo "=================================================================="
echo "✅ INSTALACIÓN COMPLETADA EXITOSAMENTE EN OCI COMPUTE"
echo "Para iniciar la aplicación:"
echo "  source venv/bin/activate && streamlit run ui/app.py --server.port 8501 --server.address 0.0.0.0"
echo "=================================================================="
