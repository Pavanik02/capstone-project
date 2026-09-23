from __future__ import annotations

import os
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

ROOT = Path(__file__).resolve().parent
CHROMA_PATH = ROOT / "chroma_db"
COLLECTION_NAME = "zepto_policy"
MODEL_NAME = "all-MiniLM-L6-v2"


class LocalRAG:
    def __init__(self) -> None:
        self.embedder = SentenceTransformer(MODEL_NAME)
        self.client = chromadb.PersistentClient(path=str(CHROMA_PATH))
        self.collection = self.client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
        )

    def retrieve(self, query: str, k: int = 3) -> list[dict]:
        vector = self.embedder.encode([query], normalize_embeddings=True).tolist()
        result = self.collection.query(
            query_embeddings=vector,
            n_results=k,
            include=["documents", "metadatas", "distances"],
        )

        docs = result.get("documents", [[]])[0]
        metas = result.get("metadatas", [[]])[0]
        distances = result.get("distances", [[]])[0]
        return [
            {
                "id": metas[i].get("chunk_id", f"unknown_{i}"),
                "document": docs[i],
                "distance": distances[i],
            }
            for i in range(len(docs))
        ]


def mock_enabled() -> bool:
    return os.getenv("MOCK_LLM", "1") != "0"
