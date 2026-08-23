"""Framework-independent models for retrieval-augmented answers."""

from dataclasses import dataclass


@dataclass(frozen=True)
class DocumentChunk:
    """A searchable fragment of a source document."""

    document_id: str
    chunk_id: str
    text: str
    source: str
    metadata: dict[str, str]


@dataclass(frozen=True)
class SearchResult:
    """A chunk ranked against a user question."""

    chunk: DocumentChunk
    score: float


@dataclass(frozen=True)
class RAGAnswer:
    """An answer and the source documents used to produce it."""

    question: str
    answer: str
    sources: tuple[str, ...]
