from pathlib import Path
from dotenv import load_dotenv
from app.helpers.metadata import get_book_category, get_author, build_chunk_metadata
from app.services.ingestion.pdf_service import parse_pdf
from app.services.ingestion.md_service import parse_md
from app.services.ingestion.chunk_service import build_chunks
from app.services.ingestion.embed_service import embed_chunks
from app.db.pinecone_client import upsert_vectors

load_dotenv()

SUPPORTED_EXTENSIONS = {".pdf", ".md"}


def ingest_file(file_path: str, dry_run: bool = False) -> dict:
    path = Path(file_path)

    if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        return {"status": "skipped", "reason": f"unsupported type: {path.suffix}"}

    blocks = _parse(path)
    if not blocks:
        return {"status": "skipped", "reason": "no text extracted"}

    book_title = _title_from_path(path)
    metadata = build_chunk_metadata(
        book_title=book_title,
        author=get_author(book_title),
        category=get_book_category(book_title),
        chapter=None,
        level="parent",
    )

    chunks = build_chunks(blocks, metadata)
    children = [c for c in chunks if c.chunk_level == "child"]

    if dry_run:
        return {"status": "dry_run", "parents": len(chunks) - len(children), "children": len(children)}

    vectors = embed_chunks(chunks)
    upsert_vectors(vectors)
    return {"status": "ok", "children_upserted": len(vectors)}


def _parse(path: Path) -> list[dict]:
    if path.suffix.lower() == ".pdf":
        return parse_pdf(str(path))
    return parse_md(str(path))


def _title_from_path(path: Path) -> str:
    name = path.stem.replace("-", " ").replace("_", " ")
    return " ".join(word.capitalize() for word in name.split())
