import json
import os
from dotenv import load_dotenv
from app.helpers.prompt_builder import build_rerank_prompt
from app.services.generation.llm_service import generate_structured

load_dotenv()


def rerank(query: str, matches: list) -> list:
    if not matches:
        return []

    top_k = int(os.getenv("RERANKER_TOP_K", 6))
    passages = _format_passages(matches)
    prompt = build_rerank_prompt(query, passages)
    raw = generate_structured(prompt)

    scores = _parse_scores(raw)
    ranked = sorted(scores, key=lambda x: x["score"], reverse=True)
    top_indices = [r["index"] for r in ranked[:top_k] if r["score"] > 0.3]
    return [matches[i] for i in top_indices if i < len(matches)]


def _format_passages(matches: list) -> str:
    return "\n\n".join(
        f"[{i}] {m.metadata.get('text', '')[:400]}" for i, m in enumerate(matches)
    )


def _parse_scores(text: str) -> list[dict]:
    try:
        start, end = text.find("["), text.rfind("]") + 1
        return json.loads(text[start:end])
    except Exception:
        return [{"index": i, "score": 0.5} for i in range(20)]
