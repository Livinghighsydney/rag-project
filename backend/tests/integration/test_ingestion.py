"""
Integration tests for Module 2 — Ingestion.
Uses real files from the corpus. No Pinecone calls (dry_run=True).
"""
import pytest
from pathlib import Path

CORPUS_MD = Path("../corpus-20261101T082003Z-1-001/corpus")
CORPUS_PDF = CORPUS_MD / "Source materials for content"

SAMPLE_MD = CORPUS_MD / "100m-leads-by-alex-hormozi.md"
SAMPLE_PDF = CORPUS_PDF / "100M Leads by Alex Hormozi.pdf"


# ── PDF parser ──────────────────────────────────────────────────────────────

@pytest.mark.skipif(not SAMPLE_PDF.exists(), reason="PDF corpus not present")
def test_pdf_parser_returns_blocks():
    from app.services.ingestion.pdf_service import parse_pdf
    blocks = parse_pdf(str(SAMPLE_PDF))
    assert len(blocks) > 0
    assert all("text" in b and "page_num" in b for b in blocks)


@pytest.mark.skipif(not SAMPLE_PDF.exists(), reason="PDF corpus not present")
def test_pdf_blocks_mostly_have_substantial_text():
    from app.services.ingestion.pdf_service import parse_pdf
    blocks = parse_pdf(str(SAMPLE_PDF))
    substantial = [b for b in blocks if len(b["text"]) > 10]
    assert len(substantial) / len(blocks) > 0.8, "Less than 80% of blocks have substantial text"


# ── MD parser ───────────────────────────────────────────────────────────────

@pytest.mark.skipif(not SAMPLE_MD.exists(), reason="MD corpus not present")
def test_md_parser_returns_blocks():
    from app.services.ingestion.md_service import parse_md
    blocks = parse_md(str(SAMPLE_MD))
    assert len(blocks) > 0


@pytest.mark.skipif(not SAMPLE_MD.exists(), reason="MD corpus not present")
def test_md_parser_preserves_heading_path():
    from app.services.ingestion.md_service import parse_md
    blocks = parse_md(str(SAMPLE_MD))
    assert all("heading_path" in b for b in blocks)


# ── Chunk service ────────────────────────────────────────────────────────────

SAMPLE_META = {
    "book_title": "100M Leads",
    "author": "Alex Hormozi",
    "category": "lead_generation",
}

SAMPLE_BLOCKS = [
    {"heading_path": "Chapter 1", "text": "Every business needs leads. " * 200},
    {"heading_path": "Chapter 2", "text": "Lead generation starts with an offer. " * 200},
]


def test_chunk_service_produces_parent_and_child():
    from app.services.ingestion.chunk_service import build_chunks
    chunks = build_chunks(SAMPLE_BLOCKS, SAMPLE_META)
    levels = {c.chunk_level for c in chunks}
    assert "parent" in levels and "child" in levels


def test_child_chunk_links_to_parent():
    from app.services.ingestion.chunk_service import build_chunks
    chunks = build_chunks(SAMPLE_BLOCKS, SAMPLE_META)
    parent_ids = {c.chunk_id for c in chunks if c.chunk_level == "parent"}
    children = [c for c in chunks if c.chunk_level == "child"]
    assert all(c.parent_id in parent_ids for c in children)


def test_child_chunks_within_token_limit():
    from app.services.ingestion.chunk_service import build_chunks, CHILD_SIZE
    chunks = build_chunks(SAMPLE_BLOCKS, SAMPLE_META)
    children = [c for c in chunks if c.chunk_level == "child"]
    oversized = [c for c in children if c.token_count > CHILD_SIZE + 50]
    assert len(oversized) == 0, f"{len(oversized)} children exceeded token limit"


# ── Ingest service (dry run) ─────────────────────────────────────────────────

@pytest.mark.skipif(not SAMPLE_MD.exists(), reason="MD corpus not present")
def test_ingest_service_dry_run_md():
    from app.services.ingestion.ingest_service import ingest_file
    result = ingest_file(str(SAMPLE_MD), dry_run=True)
    assert result["status"] == "dry_run"
    assert result["children"] > 0


@pytest.mark.skipif(not SAMPLE_PDF.exists(), reason="PDF corpus not present")
def test_ingest_service_dry_run_pdf():
    from app.services.ingestion.ingest_service import ingest_file
    result = ingest_file(str(SAMPLE_PDF), dry_run=True)
    assert result["status"] == "dry_run"
    assert result["children"] > 0


def test_ingest_service_skips_unsupported_extension(tmp_path):
    from app.services.ingestion.ingest_service import ingest_file
    f = tmp_path / "file.docx"
    f.write_text("content")
    result = ingest_file(str(f), dry_run=True)
    assert result["status"] == "skipped"
