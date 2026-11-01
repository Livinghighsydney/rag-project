# CLI: evaluate retrieval quality against a fixed test query set
#
# Prints for each query:
#   - Top 6 reranked chunks (book title + score + first 100 chars)
#   - Whether the right category was hit
#
# Use this to tune RETRIEVAL_TOP_K, RERANKER_TOP_K, chunk sizes
# before running the full system
