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

# 2. Configurar Firewall local del SO para permitir puertos 80, 443 y 8501
echo "🛡️ 2. Abriendo puertos 80, 443 y 8501 en el firewall local de la instancia..."
if command -v firewall-cmd &> /dev/null; then
    sudo firewall-cmd --zone=public --add-port=80/tcp --permanent || true
    sudo firewall-cmd --zone=public --add-port=443/tcp --permanent || true
    sudo firewall-cmd --zone=public --add-port=8501/tcp --permanent || true
    sudo firewall-cmd --reload || true
elif command -v ufw &> /dev/null; then
    sudo ufw allow 80/tcp || true
    sudo ufw allow 443/tcp || true
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

# 6. Configuración de Systemd y Nginx (Opcional para servicio 24/7)
echo "⚙️ 6. Configurando servicio systemd y proxy inverso Nginx..."
if [ -d /etc/systemd/system ]; then
    sudo cp deploy/systemd/nuevamente.service /etc/systemd/system/nuevamente.service || true
    sudo systemctl daemon-reload || true
    sudo systemctl enable nuevamente || true
fi

if [ -f /etc/oracle-release ]; then
    sudo dnf install -y nginx || true
    sudo cp deploy/nginx/nuevamente.conf /etc/nginx/conf.d/nuevamente.conf || true
    sudo systemctl enable --now nginx || true
elif [ -f /etc/debian_version ]; then
    sudo apt-get install -y nginx || true
    sudo cp deploy/nginx/nuevamente.conf /etc/nginx/sites-available/nuevamente.conf || true
    sudo ln -sf /etc/nginx/sites-available/nuevamente.conf /etc/nginx/sites-enabled/ || true
    sudo systemctl enable --now nginx || true
fi

echo "=================================================================="
echo "✅ INSTALACIÓN Y CONFIGURACIÓN COMPLETADA EN OCI COMPUTE"
echo "Estado de los servicios:"
echo "  - Servicio NuevaMente: sudo systemctl start nuevamente"
echo "  - Estado del servicio: sudo systemctl status nuevamente"
echo "  - Proxy Nginx (Puerto 80): sudo systemctl status nginx"
echo "=================================================================="
