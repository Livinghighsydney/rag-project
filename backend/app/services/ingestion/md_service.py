import re
from app.helpers.text import clean_text


def parse_md(file_path: str) -> list[dict]:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    return _split_by_headings(content)


def _split_by_headings(content: str) -> list[dict]:
    lines = content.split("\n")
    blocks = []
    current_heading = "Introduction"
    current_lines: list[str] = []

    for line in lines:
        if re.match(r"^#{1,3}\s+", line):
            _flush(blocks, current_heading, current_lines)
            current_heading = re.sub(r"^#+\s+", "", line).strip()
            current_lines = []
        else:
            current_lines.append(line)

    _flush(blocks, current_heading, current_lines)
    return blocks


def _flush(blocks: list, heading: str, lines: list[str]) -> None:
    text = clean_text("\n".join(lines))
    if text:
        blocks.append({"heading_path": heading, "text": text})
