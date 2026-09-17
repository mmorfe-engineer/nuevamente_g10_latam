"""Pruebas de persistencia del Cliente Universal de Almacenamiento (S3-Compatible y OCI)."""
from unittest.mock import MagicMock
from src.storage.oci_client import oci_storage, OCIStorageClient

def test_upload_raw_document():
    content = b"Contenido de prueba para almacenamiento universal"
    res = oci_storage.upload_raw_document("test_doc.txt", content)
    assert res["status"] in ["completado", "emulado_local"]
    assert res["object_id"] == "test_doc.txt"

def test_upload_educational_json():
    data = {"prueba": "valor", "estado": "ok"}
    res = oci_storage.upload_educational_json("resultado_test.json", data)
    assert res.objeto_id == "resultado_test.json"
    assert "completado" in res.status_upload

def test_storage_health_check():
    health = oci_storage.health_check()
    assert "mode" in health
    assert "bucket_docs" in health
    assert "bucket_outputs" in health
    assert health["bucket_docs"] == "nuevamente-documentos-origen"

def test_s3_compatible_mock_upload():
    """Valida que en modo S3-Compatible se utilice la API de boto3 put_object."""
    client = OCIStorageClient()
    mock_s3 = MagicMock()
    mock_s3.put_object.return_value = {"ETag": '"abc123etag"'}
    
    client.s3_client = mock_s3
    client.mode = "s3_compatible"

    # Test raw document upload via S3 API
    res_raw = client.upload_raw_document("s3_test.pdf", b"%PDF-test", "application/pdf")
    assert res_raw["status"] == "completado"
    assert res_raw["provider"] == "s3_compatible"
    assert res_raw["etag"] == "abc123etag"
    mock_s3.put_object.assert_called_once()

    # Test educational JSON upload via S3 API
    res_json = client.upload_educational_json("s3_output.json", {"key": "value"})
    assert res_json.objeto_id == "s3_output.json"
    assert "s3_compatible" in res_json.status_upload

def test_get_object_retrieval():
    """Valida la descarga de objetos desde el almacenamiento local o S3."""
    content = b"Prueba de recuperacion binaria"
    oci_storage.upload_raw_document("retrieval_test.bin", content)
    retrieved = oci_storage.get_object(oci_storage.bucket_docs, "retrieval_test.bin")
    assert retrieved == content

