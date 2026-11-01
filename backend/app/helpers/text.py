import re
import tiktoken

_encoder = tiktoken.get_encoding("cl100k_base")


def clean_text(raw: str) -> str:
    text = re.sub(r'^\s*\d+\s*$', '', raw, flags=re.MULTILINE)  # lone page numbers
    text = re.sub(r'[ \t]{2,}', ' ', text)                       # excess spaces
    text = re.sub(r'\n{3,}', '\n\n', text)                        # excess newlines
    return text.strip()


def count_tokens(text: str) -> int:
    return len(_encoder.encode(text))


def truncate_to_token_limit(text: str, max_tokens: int) -> str:
    tokens = _encoder.encode(text)
    if len(tokens) <= max_tokens:
        return text
    truncated = _encoder.decode(tokens[:max_tokens])
    last_period = truncated.rfind('.')
    return truncated[:last_period + 1] if last_period > 0 else truncated


def split_into_sentences(text: str) -> list[str]:
    parts = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s for s in parts if s.strip()]
