from typing import Literal, Optional
from pydantic import BaseModel


class Chunk(BaseModel):
    chunk_id: str
    parent_id: Optional[str] = None
    text: str
    token_count: int
    book_title: str
    author: str
    category: str
    chapter: Optional[str] = None
    chunk_level: Literal["parent", "child"]
    score: Optional[float] = None


class QueryAnalysis(BaseModel):
    intent: Literal["how_to", "conceptual", "comparison", "specific_fact"]
    detected_category: Optional[str] = None
    expanded_queries: list[str]
    is_followup: bool = False


class FaithfulnessResult(BaseModel):
    faithful: bool
    unsupported_claims: list[str] = []
