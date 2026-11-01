# Manual retrieval quality tester — run before full integration
# Fires a set of test queries and prints retrieved chunks + scores
# Helps tune: chunk size, top-K, reranker threshold
#
# Test query set covers:
#   - Broad concept ("how do I scale my business")
#   - Author-specific ("what does Hormozi say about lead magnets")
#   - Cross-book comparison ("difference between Traction and Rockefeller Habits")
#   - Specific fact ("what is the Profit First allocation percentages")
