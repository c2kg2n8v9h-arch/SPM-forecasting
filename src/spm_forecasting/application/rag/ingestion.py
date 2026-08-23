"""Document ingestion use case."""

from pathlib import Path

from ...domain.rag import DocumentChunk
from ...infrastructure.rag.chunker import chunk_text
from ...infrastructure.rag.ports import VectorStore


class DocumentIngestionService:
    """Read supported local documents and store searchable chunks."""

    supported_suffixes = {".md", ".txt", ".csv"}

    def __init__(self, store: VectorStore, chunk_size: int = 160) -> None:
        self.store = store
        self.chunk_size = chunk_size

    def ingest(self, input_path: Path) -> int:
        paths = [input_path] if input_path.is_file() else sorted(input_path.rglob("*"))
        chunks = []
        for path in paths:
            if path.suffix.lower() not in self.supported_suffixes:
                continue
            text = path.read_text(encoding="utf-8")
            for index, content in enumerate(chunk_text(text, self.chunk_size)):
                chunks.append(
                    DocumentChunk(
                        document_id=str(path),
                        chunk_id=f"{path}:{index}",
                        text=content,
                        source=str(path),
                        metadata={"suffix": path.suffix.lower()},
                    )
                )
        self.store.upsert(chunks)
        return len(chunks)
