import time
from src.storage.database import get_db_session
from src.utils.schemas import (
    SolicitudAdaptacion,
    PerfilDestinatario,
    FormatoSalida,
    NichoSector,
    NivelDetalle
)
from src.services.adaptation_service import adaptation_service

def benchmark_965k_document():
    print("=== INICIANDO BENCHMARK DE DOCUMENTO DE 965,086 CARACTERES ===")
    
    # 1. Construir documento con exactamente 965,086 caracteres
    bloque = (
        "La arquitectura de red definida por software en Oracle Cloud Infrastructure (OCI) "
        "se fundamenta en la Virtual Cloud Network (VCN). Cada VCN reside en una región específica "
        "y cubre un bloque CIDR IPv4 contiguo de hasta /16. Las subredes dividen este espacio en "
        "dominios de disponibilidad o a nivel regional. Las tablas de enrutamiento dirigen el tráfico "
        "hacia Internet Gateways (para tráfico público), NAT Gateways (salida sin IP pública), "
        "Service Gateways (acceso privado a servicios OCI como Object Storage) y Dynamic Routing Gateways (DRG). "
        "La seguridad perimetral y granular se orquesta mediante Security Lists a nivel de subred "
        "y Network Security Groups (NSG) asociados directamente a las VNIC de las instancias de cómputo. "
    )
    repeticiones = 965086 // len(bloque)
    resto = 965086 % len(bloque)
    doc_965k = (bloque * repeticiones) + bloque[:resto]
    assert len(doc_965k) == 965086, f"Tamaño generado: {len(doc_965k)}"
    print(f"Documento generado: {len(doc_965k):,} caracteres.")

    req = SolicitudAdaptacion(
        documento_titulo="Especificación Integral de Redes Cloud OCI (965k)",
        documento_contenido=doc_965k,
        perfil_destinatario=PerfilDestinatario.PRINCIPIANTE,
        formato_salida=FormatoSalida.FLASHCARDS,
        nicho_sector=NichoSector.CLOUD_INFRAESTRUCTURA,
        nivel_detalle=NivelDetalle.DIDACTICO
    )

    progreso_fases = []
    fase2_fragmentos = []

    def callback_monitor(phase: int, phase_name: str, current: int, total: int, detail: str):
        progreso_fases.append((phase, phase_name, current, total, detail))
        if phase == 2 and current is not None and total is not None:
            pct = int((current / total) * 100) if total > 0 else 0
            fase2_fragmentos.append((current, total, pct))
            print(f"  [FASE 2] Indexación vectorial: Fragmento {current} de {total} ({pct}%)")

    t0 = time.time()
    with get_db_session() as db:
        resp, trace = adaptation_service.process_adaptation(
            req,
            db=db,
            progress_callback=callback_monitor,
            max_chunks=80,
            chunk_offset=0
        )
    duracion_total = time.time() - t0

    print("\n=== RESULTADOS DE RENDIMIENTO Y TRAZABILIDAD ===")
    print(f"⏱️ Tiempo total de procesamiento: {duracion_total:.2f} segundos (Criterio de aceptación: < 90.0s)")
    print(f"📄 Porción declarada: {trace.get('porcion_procesada')}")
    print(f"🧩 Chunks indexados: {trace.get('chunks_indexados')} de {trace.get('total_chunks_doc')} totales")
    print(f"📊 Cobertura del lote: {trace.get('cobertura_pct')}% ({trace.get('chars_procesados'):,} caracteres)")
    print(f"🎯 Tarjetas generadas: {len(resp.contenido_adaptado.items)}")
    print(f"🛡️ Puntaje de anclaje: {resp.evaluacion_calidad.anclaje_fuente_score:.2f}")

    assert duracion_total < 90.0, f"Fallo de rendimiento: tardó {duracion_total}s (debe ser < 90s)"
    assert trace["chunks_indexados"] == 80, "Debe indexar exactamente el lote representativo de 80 fragmentos"
    assert trace["total_chunks_doc"] > 1000, f"Total de chunks esperado > 1000, obtenido {trace['total_chunks_doc']}"
    assert len(fase2_fragmentos) >= 5, "Debe haber reportado progreso dinámico en fase 2"

    print("\n✅ BENCHMARK SUPERADO EXITOSAMENTE: Criterio estricto de < 90s y reporte dinámico de fragmentos verificado.")

if __name__ == "__main__":
    benchmark_965k_document()
