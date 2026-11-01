QUERY_EXPANSION_PROMPT = """\
You are a search query optimizer for a business knowledge base.

Original query: {query}
Conversation context: {history_summary}

Generate 4 alternative phrasings that would surface different but relevant results.
Cover: synonyms, different angles, more specific versions, broader versions.

Return a JSON array of strings only. No explanation. Example:
["rephrasing 1", "rephrasing 2", "rephrasing 3", "rephrasing 4"]
"""
