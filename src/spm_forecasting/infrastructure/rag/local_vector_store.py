"""Dependency-free, persisted lexical retrieval for local development."""

import json
import re
from pathlib import Path

from ...domain.rag import DocumentChunk, SearchResult

_WORD_PATTERN = re.compile(r"[a-z0-9]+")


def _terms(value: str) -> set[str]:
    return set(_WORD_PATTERN.findall(value.lower()))


class LocalLexicalStore:
    """JSON-backed lexical retrieval adapter for local development only."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self._chunks: list[DocumentChunk] = []
        if path.exists():
            self._chunks = [
                DocumentChunk(**item) for item in json.loads(path.read_text(encoding="utf-8"))
            ]

    def upsert(self, chunks: list[DocumentChunk]) -> None:
        by_id = {chunk.chunk_id: chunk for chunk in self._chunks}
        by_id.update({chunk.chunk_id: chunk for chunk in chunks})
        self._chunks = list(by_id.values())
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps([chunk.__dict__ for chunk in self._chunks], indent=2),
            encoding="utf-8",
        )

    def search(self, question: str, limit: int = 4) -> list[SearchResult]:
        question_terms = _terms(question)
        ranked = []
        for chunk in self._chunks:
            chunk_terms = _terms(chunk.text)
            score = len(question_terms & chunk_terms) / max(len(question_terms), 1)
            if score > 0:
                ranked.append(SearchResult(chunk=chunk, score=score))
        return sorted(ranked, key=lambda result: result.score, reverse=True)[:limit]


# Backward-compatible name; migrate callers to LocalLexicalStore.
LocalVectorStore = LocalLexicalStore
