from app.db.api_clients import get_anthropic_client

MODEL = "claude-sonnet-4-6"

_TOKEN_LIMITS: dict[str, int] = {
    "coaching": 3000,
    "linkedin": 1200,
    "instagram": 1000,
    "twitter": 1200,
    "email": 2000,
    "training_lesson": 7000,
    "playbook": 6000,
    "framework": 2500,
}


def generate_answer(context: str, query: str, history: list[dict], content_type: str = "coaching") -> str:
    from app.helpers.prompt_builder import build_generation_prompt
    system = build_generation_prompt(content_type, context, query)
    messages = history + [{"role": "user", "content": query}]
    max_tokens = _TOKEN_LIMITS.get(content_type, 1500)

    response = get_anthropic_client().messages.create(
        model=MODEL,
        max_tokens=max_tokens,
        system=system,
        messages=messages,
    )
    return response.content[0].text


def stream_answer(context: str, query: str, history: list[dict], content_type: str = "coaching"):
    from app.helpers.prompt_builder import build_generation_prompt
    system = build_generation_prompt(content_type, context, query)
    messages = history + [{"role": "user", "content": query}]
    max_tokens = _TOKEN_LIMITS.get(content_type, 1500)

    with get_anthropic_client().messages.stream(
        model=MODEL,
        max_tokens=max_tokens,
        system=system,
        messages=messages,
    ) as stream:
        for text in stream.text_stream:
            yield text


def generate_structured(prompt: str) -> str:
    response = get_anthropic_client().messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text
