"""Question answering use case."""

from ...domain.rag import RAGAnswer
from ...infrastructure.rag.ports import LanguageModel, VectorStore


class QuestionAnsweringService:
    """Return grounded excerpts until an LLM adapter is configured."""

    def __init__(self, store: VectorStore, language_model: LanguageModel | None = None) -> None:
        self.store = store
        self.language_model = language_model

    def ask(self, question: str, limit: int = 4) -> RAGAnswer:
        results = self.store.search(question, limit=limit)
        if not results:
            return RAGAnswer(
                question,
                "I could not find supporting information in the indexed documents.",
                (),
            )
        sources = tuple(dict.fromkeys(result.chunk.source for result in results))
        if self.language_model is not None:
            answer = self.language_model.answer(question, [result.chunk for result in results])
        else:
            answer = "\n\n".join(
                f"[{result.chunk.source}] {result.chunk.text}" for result in results
            )
        return RAGAnswer(question, answer, sources)
