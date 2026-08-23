"""CLI entry points for local RAG ingestion and question answering."""

import argparse
from pathlib import Path

from ..application.rag.answering import QuestionAnsweringService
from ..application.rag.ingestion import DocumentIngestionService
from ..infrastructure.rag.local_vector_store import LocalLexicalStore
from ..infrastructure.rag.openai_llm import OpenAILanguageModel


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Index local documents and ask grounded questions."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    ingest = subparsers.add_parser("ingest")
    ingest.add_argument("--input", type=Path, required=True)
    ingest.add_argument("--index", type=Path, default=Path("data/rag_index/index.json"))

    ask = subparsers.add_parser("ask")
    ask.add_argument("--index", type=Path, default=Path("data/rag_index/index.json"))
    ask.add_argument("--question", required=True)
    ask.add_argument("--llm", action="store_true", help="use OpenAI for a grounded answer")
    ask.add_argument("--model", help="OpenAI model; defaults to SPM_LLM_MODEL or gpt-4o-mini")
    args = parser.parse_args()

    store = LocalLexicalStore(args.index)
    if args.command == "ingest":
        count = DocumentIngestionService(store).ingest(args.input)
        print(f"Indexed {count} document chunks in {args.index}")
    else:
        language_model = OpenAILanguageModel(args.model) if args.llm else None
        answer = QuestionAnsweringService(store, language_model).ask(args.question)
        print(answer.answer)
        if answer.sources:
            print("\nSources:")
            for source in answer.sources:
                print(f"- {source}")


if __name__ == "__main__":
    main()
