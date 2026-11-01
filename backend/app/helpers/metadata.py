from app.data.book_catalog import AUTHOR_MAP, CATEGORY_MAP


def get_author(book_title: str) -> str:
    title_lower = book_title.lower()
    for keyword, author in AUTHOR_MAP.items():
        if keyword in title_lower:
            return author
    return "Unknown"


def get_book_category(book_title: str) -> str:
    title_lower = book_title.lower()
    for keyword, category in CATEGORY_MAP.items():
        if keyword in title_lower:
            return category
    return "general"


def build_chunk_metadata(
    book_title: str, author: str, category: str, chapter: str | None, level: str
) -> dict:
    return {
        "book_title": book_title,
        "author": author,
        "category": category,
        "chapter": chapter or "",
        "chunk_level": level,
    }
