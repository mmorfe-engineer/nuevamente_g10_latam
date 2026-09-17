"""
Cliente Universal de Almacenamiento de Objetos para NuevaMente.
Diseñado bajo el patrón de arquitectura desacoplada y multicloud:
1. S3-Compatible Genérico (boto3):
   - Compatible nativamente con Oracle Cloud Infrastructure (OCI) Object Storage S3 API.
   - Compatible con Supabase Storage S3, Cloudflare R2, MinIO y AWS S3.
2. OCI SDK Nativo:
   - Fallback automático o modo directo si existen credenciales en ~/.oci/config.
3. Modo Emulado Local:
   - Persistencia local en disco (data/oci_local_storage) para ejecución offline, testing y CI/CD sin costo.
"""
import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List
from config.settings import settings
from src.utils.schemas import AlmacenamientoOCI

logger = logging.getLogger(__name__)

class OCIStorageClient:
    """Cliente universal de almacenamiento de objetos (S3-Compatible, OCI Native y Emulado)."""

    def __init__(self):
        self.s3_client = None
        self.oci_client = None
        self.mode = "emulated"
        self.namespace = settings.OCI_OBJECT_STORAGE_NAMESPACE or "nuevamente-namespace"
        self.bucket_docs = settings.STORAGE_BUCKET_DOCS or settings.OCI_BUCKET_DOCS
        self.bucket_outputs = settings.STORAGE_BUCKET_OUTPUTS or settings.OCI_BUCKET_OUTPUTS
        self._init_backend()

    @property
    def is_emulated(self) -> bool:
        """Indica si el almacenamiento está operando en réplica local emulada."""
        return self.mode == "emulated"

    def _init_backend(self):
        """Inicializa el proveedor de almacenamiento según disponibilidad de credenciales."""
        # Intento 1: Proveedor S3-Compatible genérico (boto3)
        # OCI Object Storage S3 API, Supabase Storage S3, Cloudflare R2 o AWS S3
        access_key = settings.STORAGE_ACCESS_KEY_ID or os.getenv("AWS_ACCESS_KEY_ID")
        secret_key = settings.STORAGE_SECRET_ACCESS_KEY or os.getenv("AWS_SECRET_ACCESS_KEY")
        endpoint_url = settings.STORAGE_ENDPOINT_URL or os.getenv("S3_ENDPOINT_URL")

        if access_key and secret_key:
            try:
                import boto3
                from botocore.config import Config

                boto_config = Config(
                    signature_version='s3v4',
                    retries={'max_attempts': 3, 'mode': 'standard'}
                )
                self.s3_client = boto3.client(
                    's3',
                    endpoint_url=endpoint_url,
                    aws_access_key_id=access_key,
                    aws_secret_access_key=secret_key,
                    region_name=settings.STORAGE_REGION,
                    config=boto_config
                )
                self.mode = "s3_compatible"
                logger.info(
                    f"Almacenamiento inicializado en modo S3-Compatible vía boto3. "
                    f"Endpoint: {endpoint_url or 'AWS S3 Default'} | Región: {settings.STORAGE_REGION}"
                )
                return
            except Exception as e:
                logger.warning(f"No se pudo inicializar cliente S3 con boto3: {e}. Intentando proveedor nativo...")

        # Intento 2: Proveedor OCI SDK Nativo (si existe ~/.oci/config o variables OCI_*)
        if settings.STORAGE_PROVIDER == "oci_native" or settings.OCI_USER_OCID:
            try:
                import oci

                config_path = os.path.expanduser(settings.OCI_CONFIG_FILE)
                if os.path.exists(config_path):
                    config = oci.config.from_file(config_path, settings.OCI_CONFIG_PROFILE)
                    self.oci_client = oci.object_storage.ObjectStorageClient(config)
                    if not settings.OCI_OBJECT_STORAGE_NAMESPACE:
                        self.namespace = self.oci_client.get_namespace().data
                    self.mode = "oci_native"
                    logger.info(f"Almacenamiento inicializado con OCI SDK nativo. Namespace: {self.namespace}")
                    return

                if settings.OCI_USER_OCID and settings.OCI_TENANCY_OCID and settings.OCI_KEY_FILE:
                    key_path = os.path.expanduser(settings.OCI_KEY_FILE)
                    if os.path.exists(key_path):
                        config = {
                            "user": settings.OCI_USER_OCID,
                            "fingerprint": settings.OCI_FINGERPRINT,
                            "tenancy": settings.OCI_TENANCY_OCID,
                            "region": settings.OCI_REGION,
                            "key_file": key_path
                        }
                        oci.config.validate_config(config)
                        self.oci_client = oci.object_storage.ObjectStorageClient(config)
                        if not settings.OCI_OBJECT_STORAGE_NAMESPACE:
                            self.namespace = self.oci_client.get_namespace().data
                        self.mode = "oci_native"
                        logger.info(f"Almacenamiento inicializado con OCI SDK nativo vía variables de entorno.")
                        return
            except Exception as e:
                logger.warning(f"No se pudo inicializar cliente nativo OCI: {e}. Activando modo emulado.")

        # Intento 3: Modo Emulado Local (Fallback transparente y testing)
        self.mode = "emulated"
        settings.LOCAL_STORAGE_DIR.mkdir(parents=True, exist_ok=True)
        (settings.LOCAL_STORAGE_DIR / self.bucket_docs).mkdir(parents=True, exist_ok=True)
        (settings.LOCAL_STORAGE_DIR / self.bucket_outputs).mkdir(parents=True, exist_ok=True)
        logger.info(f"Almacenamiento operando en modo local emulado en: {settings.LOCAL_STORAGE_DIR}")

    def upload_raw_document(self, filename: str, content: bytes, content_type: str = "application/octet-stream") -> Dict[str, Any]:
        """Sube un documento original al bucket de documentos."""
        bucket_name = self.bucket_docs

        # 1. Modo S3-Compatible (OCI S3 API / Supabase / Cloudflare R2 / AWS)
        if self.mode == "s3_compatible" and self.s3_client:
            try:
                response = self.s3_client.put_object(
                    Bucket=bucket_name,
                    Key=filename,
                    Body=content,
                    ContentType=content_type
                )
                etag = response.get("ETag", "").strip('"')
                return {
                    "status": "completado",
                    "provider": "s3_compatible",
                    "bucket": bucket_name,
                    "object_id": filename,
                    "etag": etag
                }
            except Exception as e:
                logger.error(f"Error subiendo a S3: {e}. Guardando réplica en almacenamiento local.")

        # 2. Modo OCI Nativo
        if self.mode == "oci_native" and self.oci_client:
            try:
                response = self.oci_client.put_object(
                    namespace_name=self.namespace,
                    bucket_name=bucket_name,
                    object_name=filename,
                    put_object_body=content,
                    content_type=content_type
                )
                return {
                    "status": "completado",
                    "provider": "oci_native",
                    "bucket": bucket_name,
                    "object_id": filename,
                    "etag": response.headers.get("etag")
                }
            except Exception as e:
                logger.error(f"Error subiendo a OCI: {e}. Guardando réplica en almacenamiento local.")

        # 3. Modo Local Emulado (Fallback)
        dest_path = settings.LOCAL_STORAGE_DIR / bucket_name / filename
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        with open(dest_path, "wb") as f:
            f.write(content)

        return {
            "status": "emulado_local",
            "provider": "emulated",
            "bucket": bucket_name,
            "object_id": filename,
            "local_path": str(dest_path)
        }

    def upload_educational_json(self, object_id: str, data: Dict[str, Any]) -> AlmacenamientoOCI:
        """Sube contenido educativo estructurado en formato JSON al bucket de resultados."""
        bucket_name = self.bucket_outputs
        json_bytes = json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8")

        # 1. Modo S3-Compatible
        if self.mode == "s3_compatible" and self.s3_client:
            try:
                self.s3_client.put_object(
                    Bucket=bucket_name,
                    Key=object_id,
                    Body=json_bytes,
                    ContentType="application/json"
                )
                return AlmacenamientoOCI(
                    bucket=bucket_name,
                    objeto_id=object_id,
                    status_upload="completado (s3_compatible)"
                )
            except Exception as e:
                logger.error(f"Error subiendo JSON a S3: {e}. Guardando réplica local.")

        # 2. Modo OCI Nativo
        if self.mode == "oci_native" and self.oci_client:
            try:
                self.oci_client.put_object(
                    namespace_name=self.namespace,
                    bucket_name=bucket_name,
                    object_name=object_id,
                    put_object_body=json_bytes,
                    content_type="application/json"
                )
                return AlmacenamientoOCI(
                    bucket=bucket_name,
                    objeto_id=object_id,
                    status_upload="completado (oci_native)"
                )
            except Exception as e:
                logger.error(f"Error subiendo JSON a OCI: {e}. Guardando réplica local.")

        # 3. Modo Local Emulado (Fallback)
        dest_path = settings.LOCAL_STORAGE_DIR / bucket_name / object_id
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        with open(dest_path, "wb") as f:
            f.write(json_bytes)

        return AlmacenamientoOCI(
            bucket=bucket_name,
            objeto_id=object_id,
            status_upload="completado (local/emulado)"
        )

    def get_object(self, bucket_name: str, object_id: str) -> Optional[bytes]:
        """Descarga un objeto del almacenamiento o de la réplica local."""
        if self.mode == "s3_compatible" and self.s3_client:
            try:
                response = self.s3_client.get_object(Bucket=bucket_name, Key=object_id)
                return response["Body"].read()
            except Exception as e:
                logger.warning(f"Error descargando objeto de S3: {e}. Buscando en réplica local.")

        if self.mode == "oci_native" and self.oci_client:
            try:
                response = self.oci_client.get_object(self.namespace, bucket_name, object_id)
                return response.data.content
            except Exception as e:
                logger.warning(f"Error descargando de OCI nativo: {e}. Buscando en réplica local.")

        local_file = settings.LOCAL_STORAGE_DIR / bucket_name / object_id
        if local_file.exists():
            with open(local_file, "rb") as f:
                return f.read()

        return None

    def health_check(self) -> Dict[str, Any]:
        """Verifica el estado del subsistema de almacenamiento."""
        return {
            "mode": self.mode,
            "is_emulated": self.is_emulated,
            "bucket_docs": self.bucket_docs,
            "bucket_outputs": self.bucket_outputs,
            "endpoint": settings.STORAGE_ENDPOINT_URL if self.mode == "s3_compatible" else "local"
        }

# Instancia singleton para consumo transversal
oci_storage = OCIStorageClient()
universal_storage = oci_storage
s3_storage = oci_storage
UniversalStorageClient = OCIStorageClient
S3StorageClient = OCIStorageClient

