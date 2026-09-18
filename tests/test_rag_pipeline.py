"""Pruebas de Vector Store y Recuperador RAG (ChromaDB)."""
from src.ingestion.chunker import doc_chunker
from src.rag.vector_store import VectorStoreManager
from src.rag.retriever import RAGRetriever

def test_vector_store_indexing_and_retrieval(tmp_path):
    # Crear vector store aislado en directorio temporal
    vs = VectorStoreManager(collection_name="test_rag_collection")
    vs.clear()

    texto = (
        "La válvula de recirculación de gas del compresor se debe calibrar a 120 PSI. "
        "El sensor de temperatura monitorea continuamente el cabezal de compresión. "
        "En caso de sobrecalentamiento mayor a 95 grados Celsius, el relé térmico desconecta el motor."
    )
    chunks = doc_chunker.split_text(texto, source_id="compresor_doc")
    assert len(chunks) >= 1

    vs.add_chunks(chunks)

    # Búsqueda semántica por concepto
    results = vs.search_similar("calibrar válvula de recirculación PSI", top_k=2)
    assert len(results) >= 1
    assert "válvula" in results[0]["content"]

    # Recuperación con el retriever
    retriever = RAGRetriever(vs=vs)
    contexto, chunks_ret, score = retriever.retrieve_context("temperatura cabezal motor")
    assert len(chunks_ret) >= 1
    assert score > 0.0
    assert "temperatura" in contexto

    # Limpieza final
    vs.clear()
