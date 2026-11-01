import os
from dotenv import load_dotenv
from fastembed import TextEmbedding
from app.db.pinecone_client import query_vectors

load_dotenv()

_model: TextEmbedding | None = None


def _get_model() -> TextEmbedding:
    global _model
    if _model is None:
        model_name = os.getenv("EMBEDDING_MODEL", "BAAI/bge-small-en-v1.5")
        _model = TextEmbedding(model_name=model_name)
    return _model


def search(query: str, category: str | None = None) -> list:
    top_k = int(os.getenv("RETRIEVAL_TOP_K", 20))
    vector = list(_get_model().embed([query]))[0].tolist()
    pinecone_filter = {"category": category} if category else None
    return query_vectors(vector, top_k=top_k, filter=pinecone_filter)
