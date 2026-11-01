import os
from dotenv import load_dotenv
from app.helpers.text import truncate_to_token_limit

load_dotenv()

CONTEXT_TOKEN_BUDGET = 6000
SECTION_SEPARATOR = "\n\n---\n\n"


def build_context(reranked_matches: list) -> str:
    seen_parents: set[str] = set()
    sections: list[str] = []

    for match in reranked_matches:
        meta = match.metadata
        parent_id = meta.get("parent_id", "")

        if parent_id and parent_id in seen_parents:
            continue

        if parent_id:
            seen_parents.add(parent_id)

        text = meta.get("parent_text") or meta.get("text", "")
        book = meta.get("book_title", "")
        section = f"[{book}]\n{text}" if book else text
        sections.append(section)

    combined = SECTION_SEPARATOR.join(sections)
    return truncate_to_token_limit(combined, CONTEXT_TOKEN_BUDGET)
