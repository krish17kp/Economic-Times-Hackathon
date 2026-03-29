"""
Retrieves relevant chunks from ChromaDB.
Location: backend/app/rag/retriever.py
"""

from pathlib import Path

CHROMA_DIR = Path(__file__).parent.parent.parent.parent / "chroma_data"
_collection = None


def _get_collection():
    global _collection
    if _collection is None:
        try:
            import chromadb  # type: ignore
        except ImportError:
            return None
            
        client = chromadb.PersistentClient(path=str(CHROMA_DIR))
        _collection = client.get_collection("agroai_docs")
    return _collection


def retrieve_context(query: str, category: str, top_k: int = 3) -> tuple[list[str], list[dict]]:
    """
    Returns (chunks, sources) relevant to the query.
    """
    try:
        collection = _get_collection()
        if not collection:
            return [], []

        results = collection.query(
            query_texts=[query],
            n_results=top_k,
        )
    except Exception:
        return [], []

    chunks = results["documents"][0] if results["documents"] else []
    metadatas = results["metadatas"][0] if results["metadatas"] else []

    sources = [
        {"document": m.get("source", "Unknown"), "page": m.get("chunk_index")}
        for m in metadatas
    ]

    return chunks, sources
