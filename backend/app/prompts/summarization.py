SESSION_SUMMARY_PROMPT = """\
Summarize this business coaching conversation in 3-5 sentences.

Preserve: the user's business context, main topics discussed, key frameworks or decisions mentioned.
Write as a compact paragraph a future AI can use to understand prior context.

CONVERSATION:
{messages}

Summary:"""
