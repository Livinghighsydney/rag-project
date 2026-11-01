import os
from langgraph.graph import StateGraph, END
from app.graph.state import RAGState
from app.graph.nodes import (
    node_analyze_query,
    node_retrieve,
    node_rerank,
    node_assemble_context,
    node_generate_answer,
    node_check_faithfulness,
    node_refine_and_retry,
    node_finalize,
)

_graph = None


def _faithfulness_router(state: RAGState) -> str:
    result = state.get("faithfulness_result")
    max_retries = int(os.getenv("MAX_FAITHFULNESS_RETRIES", 2))

    if result and result.faithful:
        return "finalize"
    if state.get("retry_count", 0) >= max_retries:
        return "finalize"
    return "refine_and_retry"


def get_graph():
    global _graph
    if _graph is not None:
        return _graph

    g = StateGraph(RAGState)

    g.add_node("analyze_query", node_analyze_query)
    g.add_node("retrieve", node_retrieve)
    g.add_node("rerank", node_rerank)
    g.add_node("assemble_context", node_assemble_context)
    g.add_node("generate_answer", node_generate_answer)
    g.add_node("check_faithfulness", node_check_faithfulness)
    g.add_node("refine_and_retry", node_refine_and_retry)
    g.add_node("finalize", node_finalize)

    g.set_entry_point("analyze_query")
    g.add_edge("analyze_query", "retrieve")
    g.add_edge("retrieve", "rerank")
    g.add_edge("rerank", "assemble_context")
    g.add_edge("assemble_context", "generate_answer")
    g.add_edge("generate_answer", "check_faithfulness")

    g.add_conditional_edges(
        "check_faithfulness",
        _faithfulness_router,
        {"finalize": "finalize", "refine_and_retry": "refine_and_retry"},
    )

    g.add_edge("refine_and_retry", "retrieve")
    g.add_edge("finalize", END)

    _graph = g.compile()
    return _graph
