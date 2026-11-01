"""
CLI: ingest the full corpus into Pinecone.

Usage:
  python scripts/ingest.py --corpus-path ../corpus-20261101T082003Z-1-001/corpus
  python scripts/ingest.py --corpus-path ... --dry-run
  python scripts/ingest.py --corpus-path ... --book "100M Leads"
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv
load_dotenv()

from app.helpers.hashing import detect_duplicates
from app.services.ingestion.ingest_service import ingest_file


def discover_files(corpus_path: str) -> list[str]:
    root = Path(corpus_path)
    files: list[str] = []
    for ext in ("*.pdf", "*.md"):
        files.extend(str(p) for p in root.rglob(ext))
    return files


def deduplicate(files: list[str]) -> list[str]:
    duplicates = detect_duplicates(files)
    skip = {paths[i] for paths in duplicates.values() for i in range(1, len(paths))}
    kept = [f for f in files if f not in skip]
    if skip:
        print(f"  Skipping {len(skip)} duplicate files")
    return kept


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus-path", required=True, help="Path to corpus folder")
    parser.add_argument("--dry-run", action="store_true", help="Parse and chunk but skip Pinecone upsert")
    parser.add_argument("--book", default=None, help="Filter by book name (partial match)")
    args = parser.parse_args()

    files = discover_files(args.corpus_path)
    files = deduplicate(files)

    if args.book:
        files = [f for f in files if args.book.lower() in f.lower()]

    print(f"Processing {len(files)} files  (dry_run={args.dry_run})\n")

    for file_path in files:
        name = Path(file_path).name
        print(f"  {name[:60]:<60}", end=" ", flush=True)
        result = ingest_file(file_path, dry_run=args.dry_run)
        print(result)


if __name__ == "__main__":
    main()
