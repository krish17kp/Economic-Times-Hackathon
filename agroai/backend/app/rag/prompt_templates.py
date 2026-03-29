"""
Prompt templates for the AI assistant.
Location: backend/app/rag/prompt_templates.py
"""

from typing import Optional


def build_prompt(question: str, chunks: list[str], category: str, context: Optional[dict] = None) -> str:
    """
    Builds the final prompt sent to the LLM.
    Includes retrieved context and constraints.
    """
    context_text = "\n---\n".join(chunks)

    extra = ""
    if context:
        if "waste_type" in context:
            extra = f"\nThe user is asking about: {context['waste_type']}"

    prompt = f"""Based ONLY on the following reference material, answer the user's question.
If the answer is not in the material, say "I don't have information about this."
Do NOT make up facts. Use simple language a farmer can understand.

REFERENCE MATERIAL:
{context_text}
{extra}

USER QUESTION ({category}):
{question}

ANSWER (keep under 200 words, use bullet points if helpful):"""

    return prompt
