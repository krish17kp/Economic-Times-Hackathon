"""
Indexes PDF documents into ChromaDB vector store.
Location: backend/app/rag/indexer.py

Run manually: python -m app.rag.indexer
"""

import os
from pathlib import Path
import chromadb
from chromadb.config import Settings


DOCUMENTS_DIR = Path(__file__).parent / "documents"
CHROMA_DIR = Path(__file__).parent.parent.parent.parent / "chroma_data"


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """Split text into overlapping chunks."""
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i : i + chunk_size])
        if chunk.strip():
            chunks.append(chunk)
    return chunks


def index_documents():
    """Read all PDFs, chunk them, and store in ChromaDB."""
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))

    # Delete existing collection if re-indexing
    try:
        client.delete_collection("agroai_docs")
    except Exception:
        pass

    collection = client.create_collection(
        name="agroai_docs",
        metadata={"hnsw:space": "cosine"},
    )

    doc_id = 0

    for pdf_file in DOCUMENTS_DIR.glob("*.pdf"):
        print(f"Indexing: {pdf_file.name}")

        try:
            from pypdf import PdfReader
            reader = PdfReader(str(pdf_file))
            full_text = ""
            for page_num, page in enumerate(reader.pages):
                text = page.extract_text()
                if text:
                    full_text += f"\n[Page {page_num + 1}] " + text
        except Exception as e:
            print(f"  Error reading {pdf_file.name}: {e}")
            continue

        chunks = chunk_text(full_text)
        print(f"  → {len(chunks)} chunks")

        for i, chunk in enumerate(chunks):
            collection.add(
                documents=[chunk],
                metadatas=[{"source": pdf_file.name, "chunk_index": i}],
                ids=[f"doc_{doc_id}"],
            )
            doc_id += 1

    print(f"\nTotal chunks indexed: {doc_id}")


if __name__ == "__main__":
    index_documents()
