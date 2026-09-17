#!/usr/bin/env bash
# ==============================================================================
# SCRIPT DE APROVISIONAMIENTO AUTOMATIZADO EN OCI COMPUTE ALWAYS FREE
# Plataforma: Ubuntu 22.04 LTS o Oracle Linux 8/9 (Ampere A1 Flex)
# Proyecto: NuevaMente (Hackathon ONE G10 / No Country)
# ==============================================================================
set -euo pipefail

CURRENT_USER=$(whoami)
CURRENT_DIR=$(pwd)

echo "=================================================================="
echo "🚀 INICIANDO APROVISIONAMIENTO COMPLETO EN OCI COMPUTE ALWAYS FREE"
echo "Usuario: ${CURRENT_USER} | Directorio: ${CURRENT_DIR}"
echo "=================================================================="

# 1. Actualización e Instalación de Dependencias del Sistema
echo "📦 1. Instalando paquetes del sistema (Python 3.11, Nginx, Certbot, Git)..."
if [ -f /etc/oracle-release ]; then
    sudo dnf update -y
    sudo dnf install -y python3.11 python3.11-devel python3.11-pip git gcc nginx certbot python3-certbot-nginx
elif [ -f /etc/debian_version ]; then
    sudo apt-get update -y
    sudo apt-get install -y python3.11 python3.11-venv python3.11-dev python3-pip git build-essential nginx certbot python3-certbot-nginx
fi

# 2. Configurar Firewall Local (OS)
echo "🛡️ 2. Habilitando puertos 80, 443 y 8501 en el firewall del sistema operativo..."
if command -v firewall-cmd &> /dev/null; then
    sudo firewall-cmd --zone=public --add-service=http --permanent || true
    sudo firewall-cmd --zone=public --add-service=https --permanent || true
    sudo firewall-cmd --zone=public --add-port=8501/tcp --permanent || true
    sudo firewall-cmd --reload || true
elif command -v ufw &> /dev/null; then
    sudo ufw allow 22/tcp || true
    sudo ufw allow 80/tcp || true
    sudo ufw allow 443/tcp || true
    sudo ufw allow 8501/tcp || true
    sudo ufw --force enable || true
fi

# OCI Iptables fix para instancias Oracle Linux / Ubuntu
echo "🔧 Ajustando reglas iptables de OCI..."
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 80 -j ACCEPT || true
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 443 -j ACCEPT || true
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 8501 -j ACCEPT || true

# 3. Entorno Virtual Python
echo "🐍 3. Creando y configurando entorno virtual Python 3.11..."
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

# 4. Directorios de Persistencia y Base de Datos
echo "📁 4. Creando directorios de persistencia local..."
mkdir -p data/chroma_db data/samples data/oci_local_storage/nuevamente-documentos-origen data/oci_local_storage/nuevamente-contenidos-educativos

# 5. Ejecutar Suite de Tests
echo "🧪 5. Verificando integridad de la plataforma (34 tests)..."
pytest tests/ -v

# 6. Configurar Servicio systemd
echo "⚙️ 6. Configurando servicio systemd 'nuevamente.service'..."
cat << SERVICE_EOF | sudo tee /etc/systemd/system/nuevamente.service
[Unit]
Description=NuevaMente EdTech RAG Platform - OCI Always Free
After=network.target

[Service]
Type=simple
User=${CURRENT_USER}
WorkingDirectory=${CURRENT_DIR}
ExecStart=${CURRENT_DIR}/venv/bin/streamlit run ui/app.py --server.port 8501 --server.address 127.0.0.1 --server.headless true
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
SERVICE_EOF

sudo systemctl daemon-reload
sudo systemctl enable nuevamente.service
sudo systemctl restart nuevamente.service

# 7. Configurar Nginx Reverse Proxy
echo "🌐 7. Configurando Nginx Reverse Proxy..."
cat << NGINX_EOF | sudo tee /etc/nginx/conf.d/nuevamente.conf
server {
    listen 80;
    server_name app.nuevamente.tech nuevamente.tech _;

    client_max_body_size 50M;

    location / {
        proxy_pass http://127.0.0.1:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_read_timeout 86400;
    }

    location /_stcore/stream {
        proxy_pass http://127.0.0.1:8501/_stcore/stream;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
        proxy_read_timeout 86400;
    }
}
NGINX_EOF

# En Debian/Ubuntu deshabilitar el default site si existe
if [ -f /etc/nginx/sites-enabled/default ]; then
    sudo rm -f /etc/nginx/sites-enabled/default || true
fi

sudo nginx -t
sudo systemctl enable nginx
sudo systemctl restart nginx

echo "=================================================================="
echo "✅ DESPLIEGUE EN OCI COMPUTE COMPLETADO EXITOSAMENTE"
echo "La plataforma está activa localmente en: http://127.0.0.1:8501"
echo "Nginx está respondiendo en el puerto 80."
echo ""
echo "PASO FINAL PARA ACTIVAR HTTPS (Let's Encrypt):"
echo "Una vez configurado el DNS de tu dominio, ejecuta:"
echo "  sudo certbot --nginx -d app.nuevamente.tech"
echo "=================================================================="
