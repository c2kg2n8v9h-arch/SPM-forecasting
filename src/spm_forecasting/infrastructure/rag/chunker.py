"""Deterministic text chunking for local ingestion."""


def chunk_text(text: str, size: int = 160, overlap: int = 30) -> list[str]:
    """Split text into word windows while preserving a small context overlap."""
    if size < 1 or overlap < 0 or overlap >= size:
        raise ValueError("overlap must be non-negative and smaller than size")
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = min(start + size, len(words))
        chunks.append(" ".join(words[start:end]))
        if end == len(words):
            break
        start = end - overlap
    return chunks
