import pdfplumber
from app.helpers.text import clean_text


def parse_pdf(file_path: str) -> list[dict]:
    try:
        return _parse_with_pdfplumber(file_path)
    except Exception:
        return _parse_with_pymupdf(file_path)


def _parse_with_pdfplumber(file_path: str) -> list[dict]:
    blocks = []
    with pdfplumber.open(file_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            if text and text.strip():
                blocks.append({"page_num": page_num, "text": clean_text(text)})
    return blocks


def _parse_with_pymupdf(file_path: str) -> list[dict]:
    import fitz
    blocks = []
    doc = fitz.open(file_path)
    for page_num, page in enumerate(doc, start=1):
        text = page.get_text()
        if text and text.strip():
            blocks.append({"page_num": page_num, "text": clean_text(text)})
    doc.close()
    return blocks
