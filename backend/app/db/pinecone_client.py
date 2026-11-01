import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec

load_dotenv()

_index = None


def get_index():
    global _index
    if _index is not None:
        return _index

    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    index_name = os.getenv("PINECONE_INDEX_NAME", "rag-business-kb")
    dimension = int(os.getenv("PINECONE_DIMENSION", "1024"))

    existing = [i.name for i in pc.list_indexes()]
    if index_name not in existing:
        pc.create_index(
            name=index_name,
            dimension=dimension,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )

    _index = pc.Index(index_name)
    return _index


def upsert_vectors(vectors: list[dict]) -> None:
    index = get_index()
    for i in range(0, len(vectors), 100):
        index.upsert(vectors=vectors[i : i + 100])


def query_vectors(vector: list[float], top_k: int, filter: dict | None = None) -> list:
    index = get_index()
    response = index.query(vector=vector, top_k=top_k, include_metadata=True, filter=filter)
    return response.matches


def fetch_by_ids(ids: list[str]) -> list:
    index = get_index()
    response = index.fetch(ids=ids)
    return list(response.vectors.values())
