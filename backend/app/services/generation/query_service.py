import json
from app.helpers.prompt_builder import build_query_expansion_prompt
from app.services.generation.llm_service import generate_structured
from app.models.chunk import QueryAnalysis


def analyze_query(query: str, history_summary: str = "") -> QueryAnalysis:
    prompt = build_query_expansion_prompt(query, history_summary)
    raw = generate_structured(prompt)
    expanded = _parse_expansions(raw, query)

    return QueryAnalysis(
        intent=_detect_intent(query),
        detected_category=None,
        expanded_queries=expanded,
        is_followup=bool(history_summary),
    )


def _parse_expansions(raw: str, original: str) -> list[str]:
    try:
        start, end = raw.find("["), raw.rfind("]") + 1
        queries = json.loads(raw[start:end])
        return [original] + [q for q in queries if isinstance(q, str)][:4]
    except Exception:
        return [original]


def _detect_intent(query: str) -> str:
    q = query.lower()
    if any(w in q for w in ("how", "what should", "steps", "way to")):
        return "how_to"
    if any(w in q for w in ("compare", "difference", "vs", "versus", "better")):
        return "comparison"
    if any(w in q for w in ("what is", "define", "explain", "mean")):
        return "conceptual"
    return "specific_fact"
