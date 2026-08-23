"""OpenAI adapter for grounded question answering."""

import os

from openai import OpenAI

from ...domain.rag import DocumentChunk


class OpenAILanguageModel:
    """Generate an answer using only the chunks supplied by the application."""

    def __init__(self, model: str | None = None) -> None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY must be set when --llm is used")
        self.client = OpenAI(api_key=api_key)
        self.model = model or os.getenv("SPM_LLM_MODEL", "gpt-4o-mini")

    def answer(self, question: str, context: list[DocumentChunk]) -> str:
        source_text = "\n\n".join(f"Source: {chunk.source}\n{chunk.text}" for chunk in context)
        response = self.client.chat.completions.create(
            model=self.model,
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Answer only from the supplied sources. If the sources do not support "
                        "the answer, say so. Cite sources using their exact Source path."
                    ),
                },
                {"role": "user", "content": f"Sources:\n{source_text}\n\nQuestion: {question}"},
            ],
        )
        return response.choices[0].message.content or "The model returned an empty answer."