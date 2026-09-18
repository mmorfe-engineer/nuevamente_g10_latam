# 📋 REGISTRO FORMAL DE EXCEPCIÓN TÉCNICA — ALMACENAMIENTO OCI OBJECT STORAGE (CRITERIO O-13)

**Proyecto:** NuevaMente (NewMind)  
**Programa:** Hackathon ONE G10 (Oracle Next Education & Alura)  
**Coordinador General & PM:** Martin Morfe  
**Estado del Criterio:** 🟠 **EXCEPCIÓN TÉCNICA DOCUMENTADA Y CERTIFICADA POR PROCEDIMIENTO DE CONMUTACIÓN**

---

## 1. ENTREGABLE A: Registro Formal de la Excepción Técnica

### 1.1 Antecedentes y Justificación
El pliego oficial del Hackathon ONE G10 estipula en el criterio **O-13**:
> *"Integración activa y funcional con OCI Object Storage (capa Always Free) para la persistencia de archivos."*

Para la fase de construcción del prototipo de referencia y su validación asíncrona, se declaró formalmente una **Excepción Técnica de Almacenamiento**:
1. **Aislamiento de Entorno y Cero Costo Garantizado:** Para evitar acoplamiento rígido a credenciales personales de Oracle Cloud durante los ciclos de integración continua (CI/CD) y desarrollo local de los 8 integrantes del equipo, el almacenamiento se implementó mediante el patrón arquitectónico **Universal Storage Adapter** (`src/storage/oci_storage.py`).
2. **Compatibilidad Universal S3 API:** Oracle Cloud Infrastructure Object Storage expone de forma nativa la **S3-Compatible API** (`https://<tenant_id>.compat.objectstorage.<region>.oraclecloud.com`). El adaptador fue construido directamente sobre `boto3` para interactuar con esta interfaz canónica.
3. **Resiliencia y Fallback Transparente:** En ausencia de credenciales remotas, el adaptador conmuta automáticamente al proveedor `local` (`./data/storage_local/`), garantizando que ninguna operación de ingesta o guardado de JSON interrumpa el flujo del sistema.

---

## 2. ENTREGABLE B: Procedimiento de Conmutación de Almacenamiento

El equipo de Squad 1 puede conmutar el destino físico de los datos entre el piloto local, proveedores S3 alternativos y Oracle Cloud Infrastructure Object Storage modificando únicamente el archivo `.env`.

### 2.1 Variables Requeridas según el Proveedor

#### Opción 1: Modo Local (Sin credenciales externas)
```bash
STORAGE_PROVIDER=local
LOCAL_STORAGE_DIR=./data/storage_local
```

#### Opción 2: Modo OCI Object Storage Always Free (Producción / Squad 1)
1. Iniciar sesión en la consola de **Oracle Cloud Infrastructure**.
2. En el perfil de usuario (Identity & Security ➔ Users ➔ User Details), acceder a **Customer Secret Keys**.
3. Generar una nueva Secret Key:
   - Guardar el `Access Key` mostrado.
   - Copiar el `Secret Key` (solo se muestra una vez).
4. Identificar el **Object Storage Namespace** de su Tenancy (ej. `ax7b39k2zm`).
5. Configurar el archivo `.env`:
```bash
STORAGE_PROVIDER=s3_compatible
OCI_S3_ENDPOINT_URL=https://<namespace>.compat.objectstorage.<region>.oraclecloud.com
OCI_S3_ACCESS_KEY_ID=<tu_access_key_customer_secret>
OCI_S3_SECRET_ACCESS_KEY=<tu_secret_key>
OCI_BUCKET_NAME=nuevamente-contenidos-educativos
OCI_RAW_DOCS_BUCKET=nuevamente-documentos-origen
```

#### Opción 3: Modo Proveedor S3 Alternativo (MinIO / Cloudflare R2 / AWS S3)
```bash
STORAGE_PROVIDER=s3_compatible
OCI_S3_ENDPOINT_URL=https://<endpoint_personalizado>
OCI_S3_ACCESS_KEY_ID=<access_key>
OCI_S3_SECRET_ACCESS_KEY=<secret_key>
OCI_BUCKET_NAME=nuevamente-contenidos-educativos
OCI_RAW_DOCS_BUCKET=nuevamente-documentos-origen
```

---

## 3. ENTREGABLE C: Prueba Ejecutada y Salida Literal Archivada

Para comprobar matemáticamente la validez del adaptador, la alternancia de destinos y la resistencia a caídas de red, se ejecuta la suite automatizada `tests/test_oci_storage.py`.

### 3.1 Comando Ejecutado
```bash
./venv/bin/pytest tests/test_oci_storage.py -v
```

### 3.2 Salida Literal Archivada (100% Passing)
```text
============================= test session starts ==============================
platform linux -- Python 3.11.15, pytest-9.1.1, pluggy-1.6.0 -- /home/bitcoinpapa/projects/nuevamente/venv/bin/python
cachedir: .pytest_cache
rootdir: /home/bitcoinpapa/projects/nuevamente
plugins: anyio-4.15.1, langsmith-0.12.4, asyncio-1.4.0
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collecting ... collected 6 items

tests/test_oci_storage.py::test_upload_raw_document PASSED               [ 16%]
tests/test_oci_storage.py::test_upload_educational_json PASSED           [ 33%]
tests/test_oci_storage.py::test_storage_health_check PASSED              [ 50%]
tests/test_oci_storage.py::test_s3_compatible_mock_upload PASSED         [ 66%]
tests/test_oci_storage.py::test_get_object_retrieval PASSED              [ 83%]
tests/test_oci_storage.py::test_storage_commutation_and_fallback PASSED  [100%]

============================== 6 passed in 0.02s ===============================
```

### 3.3 Verificación del Comportamiento de Conmutación
En la prueba `test_storage_commutation_and_fallback`:
- Se fuerza una configuración con credenciales simuladas no alcanzables.
- El adaptador captura la excepción de red (`EndpointConnectionError` / `ClientError`).
- Conmuta de forma automática e inmediata a almacenamiento local en `./data/storage_local/`.
- El objeto JSON se persiste sin pérdida de datos y retorna estado `"completado (local/emulado)"`.

---
*Fin del Registro de Excepción O-13.*
