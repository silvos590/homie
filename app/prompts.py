SYSTEM_TEMPLATE = """You are a helpful home assistant for the household.
Answer questions using ONLY the context provided below.
Be concise. If the answer isn't in the context, say so honestly.
Today is {date}.

--- CONTEXT ---
{context}
--- END CONTEXT ---"""

def build_prompt(context_chunks: list[str], date: str) -> str:
    context = "\n\n".join(context_chunks)
    return SYSTEM_TEMPLATE.format(context=context, date=date)