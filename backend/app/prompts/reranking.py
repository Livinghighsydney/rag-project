RERANK_PROMPT = """\
Score each passage for how well it answers the query. Return a JSON array with "index" and "score" (0.0-1.0).

Query: {query}

Passages:
{passages}

Return only JSON: [{{"index": 0, "score": 0.9}}, {{"index": 1, "score": 0.4}}]"""
