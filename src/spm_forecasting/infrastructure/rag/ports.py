"""Ports that allow local RAG adapters to be replaced by real providers."""

from typing import Protocol

from ...domain.rag import DocumentChunk, SearchResult


class VectorStore(Protocol):
    def upsert(self, chunks: list[DocumentChunk]) -> None:
        ...

    def search(self, question: str, limit: int = 4) -> list[SearchResult]:
        ...


class LanguageModel(Protocol):
    def answer(self, question: str, context: list[DocumentChunk]) -> str:
        ...
