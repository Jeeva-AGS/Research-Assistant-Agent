import chromadb
from chromadb.config import Settings
from utils.logging import get_logger

logger = get_logger("VectorStore")


class VectorStore:
    def __init__(self, collection_name: str = "papers"):
        self.client = chromadb.Client(
            Settings(persist_directory=".chroma", anonymized_telemetry=False)
        )

        self.collection = self.client.get_or_create_collection(
            name=collection_name
        )

    def add(self, ids: list[str], embeddings: list, documents: list, metadatas: list):
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
        )

    def query(self, query_embedding, top_k: int = 5):
        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
        )
