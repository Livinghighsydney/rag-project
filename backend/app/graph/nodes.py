from app.graph.state import RAGState
from app.services.generation.query_service import analyze_query
from app.services.retrieval.search_service import search
from app.services.retrieval.rerank_service import rerank
from app.services.retrieval.context_service import build_context
from app.services.generation.llm_service import generate_answer
from app.services.generation.faithfulness_service import check


def node_analyze_query(state: RAGState) -> dict:
    analysis = analyze_query(state["user_query"], state.get("history_summary", ""))
    return {"query_analysis": analysis}


def node_retrieve(state: RAGState) -> dict:
    analysis = state["query_analysis"]
    queries = analysis.expanded_queries or [state["user_query"]]
    category = analysis.detected_category

    seen_ids = set()
    all_chunks = []
    for q in queries:
        for match in search(q, category=category):
            if match.id not in seen_ids:
                seen_ids.add(match.id)
                all_chunks.append(match)

    return {"retrieved_chunks": all_chunks}


def node_rerank(state: RAGState) -> dict:
    reranked = rerank(state["user_query"], state["retrieved_chunks"])
    return {"reranked_chunks": reranked}


def node_assemble_context(state: RAGState) -> dict:
    context = build_context(state["reranked_chunks"])
    return {"assembled_context": context}


def node_generate_answer(state: RAGState) -> dict:
    answer = generate_answer(
        state["assembled_context"],
        state["user_query"],
        state["history"],
        state.get("content_type", "coaching"),
    )
    return {"generated_answer": answer}


def node_check_faithfulness(state: RAGState) -> dict:
    result = check(state["generated_answer"], state["assembled_context"])
    return {"faithfulness_result": result}


def node_refine_and_retry(state: RAGState) -> dict:
    return {
        "retry_count": state.get("retry_count", 0) + 1,
        "retrieved_chunks": [],
        "reranked_chunks": [],
        "assembled_context": "",
        "generated_answer": "",
        "faithfulness_result": None,
    }


def node_finalize(state: RAGState) -> dict:
    answer = state.get("generated_answer", "")
    result = state.get("faithfulness_result")

    if not answer or (result and not result.faithful and state.get("retry_count", 0) >= 2):
        answer = (
            "I couldn't find a well-grounded answer for that question in the available material. "
            "Try rephrasing or asking about a different aspect."
        )
    return {"final_answer": answer}
