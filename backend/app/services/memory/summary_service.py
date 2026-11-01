from app.helpers.prompt_builder import build_summary_prompt
from app.services.generation.llm_service import generate_structured


def summarize_session(messages: list[dict]) -> str:
    text = "\n".join(f"{m['role'].upper()}: {m['content']}" for m in messages)
    prompt = build_summary_prompt(text)
    return generate_structured(prompt)
