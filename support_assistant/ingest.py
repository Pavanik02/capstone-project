from __future__ import annotations

from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

ROOT = Path(__file__).resolve().parent
DOCS = ROOT / "docs"
CHROMA_PATH = ROOT / "chroma_db"
COLLECTION_NAME = "zepto_policy"
MODEL_NAME = "all-MiniLM-L6-v2"


def main() -> None:
    files = sorted(DOCS.glob("doc_*.txt"))
    if len(files) != 8:
        raise RuntimeError(f"Expected exactly 8 corpus documents, found {len(files)}")

    model = SentenceTransformer(MODEL_NAME)
    client = chromadb.PersistentClient(path=str(CHROMA_PATH))
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    documents = [path.read_text(encoding="utf-8") for path in files]
    ids = [f"{path.stem}_chunk_01" for path in files]
    metadatas = [
        {"source": path.name, "chunk_id": chunk_id}
        for path, chunk_id in zip(files, ids)
    ]
    embeddings = model.encode(
        documents,
        normalize_embeddings=True,
        show_progress_bar=True,
    ).tolist()

    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
        embeddings=embeddings,
    )

    print(f"Indexed {collection.count()} chunks into {COLLECTION_NAME!r}")
    print("Persistence path:", CHROMA_PATH)


if __name__ == "__main__":
    main()
