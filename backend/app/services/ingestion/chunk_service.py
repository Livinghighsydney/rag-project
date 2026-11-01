import os
import uuid
from dotenv import load_dotenv
from app.helpers.text import count_tokens, split_into_sentences
from app.models.chunk import Chunk

load_dotenv()

PARENT_SIZE = int(os.getenv("PARENT_CHUNK_SIZE", 1500))
CHILD_SIZE = int(os.getenv("CHILD_CHUNK_SIZE", 300))


def build_chunks(text_blocks: list[dict], book_metadata: dict) -> list[Chunk]:
    all_chunks: list[Chunk] = []
    for block in text_blocks:
        chapter = block.get("heading_path") or str(block.get("page_num", ""))
        parents = _make_parents(block["text"], book_metadata, chapter)
        for parent in parents:
            all_chunks.append(parent)
            all_chunks.extend(_make_children(parent, book_metadata))
    return all_chunks


def _make_parents(text: str, meta: dict, chapter: str) -> list[Chunk]:
    return _split_into_chunks(text, PARENT_SIZE, meta, chapter, "parent", None)


def _make_children(parent: Chunk, meta: dict) -> list[Chunk]:
    return _split_into_chunks(parent.text, CHILD_SIZE, meta, parent.chapter, "child", parent.chunk_id)


def _split_into_chunks(
    text: str, max_tokens: int, meta: dict, chapter: str | None, level: str, parent_id: str | None
) -> list[Chunk]:
    sentences = split_into_sentences(text)
    chunks: list[Chunk] = []
    bucket: list[str] = []
    bucket_tokens = 0

    for sentence in sentences:
        sentence_tokens = count_tokens(sentence)
        if bucket_tokens + sentence_tokens > max_tokens and bucket:
            chunks.append(_build_chunk(bucket, meta, chapter, level, parent_id))
            bucket, bucket_tokens = [sentence], sentence_tokens
        else:
            bucket.append(sentence)
            bucket_tokens += sentence_tokens

    if bucket:
        chunks.append(_build_chunk(bucket, meta, chapter, level, parent_id))
    return chunks


def _build_chunk(sentences: list[str], meta: dict, chapter: str | None, level: str, parent_id: str | None) -> Chunk:
    text = " ".join(sentences)
    return Chunk(
        chunk_id=str(uuid.uuid4()),
        parent_id=parent_id,
        text=text,
        token_count=count_tokens(text),
        book_title=meta["book_title"],
        author=meta["author"],
        category=meta["category"],
        chapter=chapter,
        chunk_level=level,
    )
