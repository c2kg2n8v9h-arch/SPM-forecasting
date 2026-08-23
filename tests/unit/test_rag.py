import tempfile
import unittest
from pathlib import Path

from spm_forecasting.application.rag.answering import QuestionAnsweringService
from spm_forecasting.application.rag.ingestion import DocumentIngestionService
from spm_forecasting.infrastructure.rag.local_lexical_store import LocalLexicalStore


class RAGTests(unittest.TestCase):
    def test_ingest_and_ask_returns_grounded_source(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            document = folder / "procedure.md"
            document.write_text(
                "PUMP-100 requires verified airworthiness documentation.", encoding="utf-8"
            )
            store = LocalLexicalStore(folder / "index.json")

            self.assertEqual(DocumentIngestionService(store).ingest(document), 1)
            answer = QuestionAnsweringService(
                LocalLexicalStore(folder / "index.json")
            ).ask("PUMP-100 documentation")

            self.assertIn("PUMP-100", answer.answer)
            self.assertEqual(answer.sources, (str(document),))

    def test_unknown_question_is_not_invented(self):
        with tempfile.TemporaryDirectory() as directory:
            store = LocalLexicalStore(Path(directory) / "index.json")
            answer = QuestionAnsweringService(store).ask("unknown item")

            self.assertEqual(answer.sources, ())
            self.assertIn("could not find", answer.answer)
