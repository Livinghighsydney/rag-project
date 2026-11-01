import json
from app.helpers.prompt_builder import build_faithfulness_prompt
from app.services.generation.llm_service import generate_structured
from app.models.chunk import FaithfulnessResult


def check(answer: str, context: str) -> FaithfulnessResult:
    prompt = build_faithfulness_prompt(answer, context)
    raw = generate_structured(prompt)
    return _parse_result(raw)


def _parse_result(raw: str) -> FaithfulnessResult:
    try:
        start, end = raw.find("{"), raw.rfind("}") + 1
        data = json.loads(raw[start:end])
        return FaithfulnessResult(
            faithful=bool(data.get("faithful", True)),
            unsupported_claims=data.get("unsupported_claims", []),
        )
    except Exception:
        return FaithfulnessResult(faithful=True)
