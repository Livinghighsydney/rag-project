import os
from dotenv import load_dotenv
from fastembed import TextEmbedding
from app.models.chunk import Chunk

load_dotenv()

_model: TextEmbedding | None = None

MODEL_DIMENSIONS = {
    "BAAI/bge-small-en-v1.5": 384,
    "BAAI/bge-base-en-v1.5": 768,
    "BAAI/bge-large-en-v1.5": 1024,
}


def get_model() -> TextEmbedding:
    global _model
    if _model is None:
        model_name = os.getenv("EMBEDDING_MODEL", "BAAI/bge-base-en-v1.5")
        _model = TextEmbedding(model_name=model_name)
    return _model


def embed_chunks(chunks: list[Chunk]) -> list[dict]:
    parent_map = {c.chunk_id: c for c in chunks if c.chunk_level == "parent"}
    children = [c for c in chunks if c.chunk_level == "child"]

    texts = [c.text for c in children]
    embeddings = list(get_model().embed(texts))

    return [_to_vector(child, emb, parent_map) for child, emb in zip(children, embeddings)]


def _to_vector(chunk: Chunk, embedding, parent_map: dict) -> dict:
    parent = parent_map.get(chunk.parent_id or "")
    return {
        "id": chunk.chunk_id,
        "values": embedding.tolist(),
        "metadata": {
            "parent_id": chunk.parent_id or "",
            "text": chunk.text,
            "parent_text": parent.text if parent else chunk.text,
            "book_title": chunk.book_title,
            "author": chunk.author,
            "category": chunk.category,
            "chapter": chunk.chapter or "",
        },
    }
