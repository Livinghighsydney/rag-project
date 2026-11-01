from app.prompts.query_expansion import QUERY_EXPANSION_PROMPT
from app.prompts.faithfulness import FAITHFULNESS_CHECK_PROMPT
from app.prompts.summarization import SESSION_SUMMARY_PROMPT
from app.prompts.reranking import RERANK_PROMPT
from app.prompts.content_modes import PROMPT_MAP, _GROUNDING


def build_generation_prompt(content_type: str, context: str, query: str) -> str:
    template = PROMPT_MAP.get(content_type, PROMPT_MAP["coaching"])
    return template.format(context=context, query=query) + _GROUNDING


def build_query_expansion_prompt(query: str, history_summary: str) -> str:
    return QUERY_EXPANSION_PROMPT.format(query=query, history_summary=history_summary)


def build_faithfulness_prompt(answer: str, context: str) -> str:
    return FAITHFULNESS_CHECK_PROMPT.format(answer=answer, context=context)


def build_summary_prompt(messages_text: str) -> str:
    return SESSION_SUMMARY_PROMPT.format(messages=messages_text)


def build_rerank_prompt(query: str, passages: str) -> str:
    return RERANK_PROMPT.format(query=query, passages=passages)
