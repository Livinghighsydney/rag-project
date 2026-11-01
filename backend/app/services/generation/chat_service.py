from app.graph.rag_graph import get_graph
from app.services.memory.session_service import get_history, add_message
from app.services.generation.query_service import analyze_query
from app.services.retrieval.search_service import search
from app.services.retrieval.rerank_service import rerank
from app.services.retrieval.context_service import build_context
from app.services.generation.llm_service import stream_answer


def handle_message(session_id: str, user_message: str, content_type: str = "coaching") -> str:
    history = get_history(session_id)

    initial_state = {
        "session_id": session_id,
        "user_query": user_message,
        "content_type": content_type,
        "history": history.messages,
        "history_summary": history.summary,
        "query_analysis": None,
        "retrieved_chunks": [],
        "reranked_chunks": [],
        "assembled_context": "",
        "generated_answer": "",
        "faithfulness_result": None,
        "retry_count": 0,
        "final_answer": "",
    }

    graph = get_graph()
    result = graph.invoke(initial_state)
    answer = result.get("final_answer", "")

    add_message(session_id, "user", user_message)
    add_message(session_id, "assistant", answer)

    return answer


def handle_message_stream(session_id: str, user_message: str, content_type: str = "coaching"):
    history = get_history(session_id)

    analysis = analyze_query(user_message, history.summary)
    queries = analysis.expanded_queries or [user_message]
    category = analysis.detected_category

    seen_ids: set = set()
    all_chunks: list = []
    for q in queries:
        for match in search(q, category=category):
            if match.id not in seen_ids:
                seen_ids.add(match.id)
                all_chunks.append(match)

    reranked = rerank(user_message, all_chunks)
    context = build_context(reranked)

    full_answer: list[str] = []
    try:
        for chunk in stream_answer(context, user_message, history.messages, content_type):
            full_answer.append(chunk)
            yield chunk
    finally:
        answer_text = "".join(full_answer)
        if answer_text:
            add_message(session_id, "user", user_message)
            add_message(session_id, "assistant", answer_text)
