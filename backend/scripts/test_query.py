"""
Quick end-to-end query test — no LangGraph yet.
Runs: embed query → search Pinecone → rerank → build context → Claude answer → faithfulness check

Usage:
  python scripts/test_query.py "How do I generate leads for my business?"
  python scripts/test_query.py --all     (runs the full test suite)
"""
import sys
import argparse
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv
load_dotenv()

from app.services.retrieval.search_service import search
from app.services.retrieval.rerank_service import rerank
from app.services.retrieval.context_service import build_context
from app.services.generation.llm_service import generate_answer
from app.services.generation.faithfulness_service import check as check_faithfulness

TEST_QUERIES = [
    "How do I generate leads for my business?",
    "What is the Profit First method?",
    "What is a lead magnet and how do I create one?",
    "How should I manage cash flow in my business?",
    "What does Hormozi say about making an irresistible offer?",
]

FALLBACK = "My knowledge base doesn't have enough on this topic."


def run_query(query: str) -> None:
    print(f"\n{'='*60}")
    print(f"QUERY: {query}")
    print('='*60)

    matches = search(query)
    print(f"  Retrieved: {len(matches)} chunks from Pinecone")

    reranked = rerank(query, matches)
    print(f"  Reranked:  {len(reranked)} chunks kept")
    if reranked:
        books = {m.metadata.get('book_title') for m in reranked}
        print(f"  Sources:   {', '.join(books)}")

    if not reranked:
        print(f"\nANSWER: {FALLBACK}")
        return

    context = build_context(reranked)
    answer = generate_answer(context, query, history=[])

    result = check_faithfulness(answer, context)
    faithful_tag = "FAITHFUL" if result.faithful else f"UNFAITHFUL: {result.unsupported_claims}"

    print(f"\nANSWER [{faithful_tag}]:")
    print(answer)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("query", nargs="?", help="Query to run")
    parser.add_argument("--all", action="store_true", help="Run all test queries")
    args = parser.parse_args()

    if args.all:
        for q in TEST_QUERIES:
            run_query(q)
    elif args.query:
        run_query(args.query)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
