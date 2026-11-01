from typing import TypedDict, Optional
from app.models.chunk import QueryAnalysis, FaithfulnessResult


class RAGState(TypedDict):
    session_id: str
    user_query: str
    content_type: str
    history: list[dict]
    history_summary: str
    query_analysis: Optional[QueryAnalysis]
    retrieved_chunks: list
    reranked_chunks: list
    assembled_context: str
    generated_answer: str
    faithfulness_result: Optional[FaithfulnessResult]
    retry_count: int
    final_answer: str
