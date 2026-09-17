# 🚀 Manual de Despliegue Híbrido: Landing en GitHub Pages + App en Oracle Cloud (OCI Always Free)

**Proyecto:** NuevaMente — Hackathon Oracle Next Education (ONE G10)  
**Coordinador General & PM:** Martin Morfe  
**Arquitectura:** 
- **Landing Page & Portada:** `https://nuevamente.tech` (Alojada en **GitHub Pages** desde `/docs`).
- **Plataforma Educativa:** `https://app.nuevamente.tech` (Alojada en **OCI Compute Ampere A1 Flex** Always Free).
- **Costo Total:** **$0.00 USD de por vida**.

---

## 📋 FASE 1: Obtener el Dominio Gratis con GitHub Student Pack

1. Ingresa a [GitHub Student Developer Pack](https://education.github.com/pack).
2. Busca la oferta de **.TECH Domains** o **Namecheap (.me)**.
3. Solicita tu dominio gratuito por 1 año:
   - Opción sugerida 1: `nuevamente.tech` (Muy corporativo para EdTech y Ciberseguridad).
   - Opción sugerida 2: `nuevamente.me`.
4. Completa el registro sin costo alguno.

---

## ☁️ FASE 2: Crear la Instancia en Oracle Cloud (OCI Always Free)

### Paso 1: Crear la Máquina Virtual Ampere A1
1. Inicia sesión en tu consola de Oracle Cloud: [https://cloud.oracle.com](https://cloud.oracle.com).
2. En el menú de navegación (arriba a la izquierda), ve a:  
   **Compute** ➔ **Instances** (Instancias).
3. Haz clic en **Create Instance** (Crear instancia):
   - **Name:** `nuevamente-prod-vm`
   - **Placement:** Deja el dominio de disponibilidad predeterminado.
   - **Image and Shape:**
     - Haz clic en **Change Shape** (Cambiar unidad).
     - Selecciona **Ampere** (ARM Processor) ➔ `VM.Standard.A1.Flex`.
     - Configura: **4 OCPUs** y **24 GB de memoria RAM** (Es 100% Always Free).
     - Sistema operativo: **Ubuntu 22.04 LTS** (o *Oracle Linux 8/9*).
   - **Networking:** Deja la VCN y subred pública predeterminadas (asegúrate de que tenga asignada una **Public IPv4 Address**).
   - **Add SSH Keys:** 
     - Selecciona *Generate a key pair for me* y descarga la clave privada (`.key` / `.pem`), o pega tu clave pública personal (`id_rsa.pub`).
4. Haz clic en **Create** (Crear). En 1 o 2 minutos estará en estado **Running** (Verde). Anota la **IP Pública** de la máquina (ej: `129.153.xx.xx`).

---

### Paso 2: Abrir los Puertos en la Red de Oracle (VCN Security List)
> [!IMPORTANT]
> Por seguridad, OCI bloquea todo el tráfico entrante a menos que lo autorices en su lista de seguridad. Debes abrir los puertos web (80 y 443):

1. En la página de detalles de tu instancia, en la sección **Instance details**, haz clic en el enlace de tu **Virtual Cloud Network (VCN)**.
2. Haz clic en **Security Lists** (Listas de seguridad) ➔ **Default Security List for...**.
3. Haz clic en **Add Ingress Rules** (Agregar reglas de entrada):
   - **Source CIDR:** `0.0.0.0/0`
   - **IP Protocol:** `TCP`
   - **Destination Port Range:** `80,443`
   - **Description:** `Permitir tráfico web HTTP y HTTPS para NuevaMente`
4. Haz clic en **Add Ingress Rules**.

---

## 🛠️ FASE 3: Aprovisionamiento Automático en la Instancia OCI

1. Conéctate a tu máquina por SSH desde tu terminal:
   ```bash
   ssh -i /ruta/a/tu/clave.key ubuntu@<IP_PUBLICA_OCI>
   # Si usaste Oracle Linux, el usuario es opc@<IP_PUBLICA_OCI>
   ```

2. Clona el repositorio oficial:
   ```bash
   git clone https://github.com/mmorfe-engineer/nuevamente_g10_latam.git nuevamente
   cd nuevamente
   ```

3. Crea tu archivo `.env` en la máquina con tus credenciales seguras:
   ```bash
   cp .env.example .env
   nano .env
   ```
   *(Pega tus API keys de NVIDIA NIM, Mistral AI y la URL de Neon PostgreSQL)*.

4. Ejecuta el script automatizado de aprovisionamiento:
   ```bash
   bash deploy/oci_setup.sh
   ```
   *El script instalará automáticamente Python 3.11, Nginx, Certbot, compilará el entorno virtual, correrá los 34 tests para verificar integridad y dejará el servicio corriendo en segundo plano bajo systemd*.

---

## 🌐 FASE 4: Configurar los Registros DNS de tu Dominio

En el panel de control de tu registrador de dominio (Namecheap o .TECH), ve a la sección **Advanced DNS / Gestión de DNS** y agrega estas dos reglas:

| Tipo de Registro | Host / Nombre | Valor / Destino | Propósito |
| :--- | :---: | :--- | :--- |
| **CNAME** | `@` (o raíz) | `mmorfe-engineer.github.io` | Apunta la Landing Page a **GitHub Pages** |
| **A** | `app` | `<IP_PUBLICA_OCI>` | Apunta la aplicación a tu servidor **Oracle Cloud** |

*(La propagación de DNS tarda entre 5 y 15 minutos)*.

---

## 📄 FASE 5: Activar GitHub Pages para la Landing Page

1. Ve a tu repositorio en GitHub: [https://github.com/mmorfe-engineer/nuevamente_g10_latam](https://github.com/mmorfe-engineer/nuevamente_g10_latam).
2. Haz clic en **Settings** (Configuración) ➔ **Pages** (en el menú lateral).
3. En **Build and deployment**:
   - **Source:** `Deploy from a branch`
   - **Branch:** `main`
   - **Folder:** `/docs`
   - Haz clic en **Save** (Guardar).
4. En **Custom domain**, escribe: `nuevamente.tech` y haz clic en **Save**.
5. Marca la casilla **Enforce HTTPS**.
¡Listo! Tu Landing Page oficial con el Design System ya estará activa en `https://nuevamente.tech`.

---

## 🔒 FASE 6: Activar Certificado SSL HTTPS en Oracle Cloud

Una vez que el registro `app.nuevamente.tech` responda a tu IP de OCI, conéctate a la máquina y ejecuta un solo comando:

```bash
sudo certbot --nginx -d app.nuevamente.tech
```
- Te pedirá tu correo y aceptar los términos de Let's Encrypt.
- Certbot reconfigurará Nginx automáticamente para cifrado SSL A+ sin costo alguno.

¡Tu plataforma completa estará en producción en **`https://app.nuevamente.tech`**!
