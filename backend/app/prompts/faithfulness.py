FAITHFULNESS_CHECK_PROMPT = """\
You are a fact-checker for a business knowledge base. Verify that every substantive claim in the answer is grounded in the context.

NOTE: The answer may be formatted as a LinkedIn post, email, course module, blog post, or thread.
Creative elements — hooks, CTAs, transitions, hashtags, and formatting — are NOT subject to grounding checks.
Only check factual claims: frameworks, statistics, named concepts, specific steps, and business recommendations.

CONTEXT:
{context}

ANSWER TO CHECK:
{answer}

Return JSON only — no explanation:
{{"faithful": true, "unsupported_claims": []}}

If any factual claim is not supported by the context, set faithful to false and list only those claims:
{{"faithful": false, "unsupported_claims": ["specific factual claim with no support in context"]}}
"""
