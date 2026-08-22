import csv
import tempfile
import unittest
from pathlib import Path

from spm_forecasting.cli import main


class CliIntegrationTests(unittest.TestCase):
    def test_cli_writes_forecast_csv(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            input_path = folder / "input.csv"
            output_path = folder / "output.csv"
            input_path.write_text("value\n10\n12\n14\n", encoding="utf-8")

            import sys
            original_argv = sys.argv
            sys.argv = ["spm-forecast", "--input", str(input_path), "--output", str(output_path)]
            try:
                main()
            finally:
                sys.argv = original_argv

            with output_path.open(newline="", encoding="utf-8") as output_file:
                rows = list(csv.reader(output_file))
            self.assertEqual(rows[0], ["period", "forecast"])
            self.assertEqual(rows[1][1], "16.0000")