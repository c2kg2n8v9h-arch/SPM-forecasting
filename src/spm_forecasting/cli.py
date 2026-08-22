"""Command-line interface for generating forecasts from CSV files."""

import argparse
import csv
from pathlib import Path

from .forecast import linear_forecast


def _read_values(path: Path) -> list[float]:
    with path.open(newline="", encoding="utf-8") as input_file:
        rows = csv.DictReader(input_file)
        if not rows.fieldnames or "value" not in rows.fieldnames:
            raise ValueError("input CSV must contain a 'value' column")
        try:
            return [float(row["value"]) for row in rows]
        except (TypeError, ValueError) as error:
            raise ValueError("every value entry must be numeric") from error


def _write_forecast(path: Path, forecast) -> None:
    with path.open("w", newline="", encoding="utf-8") as output_file:
        writer = csv.writer(output_file)
        writer.writerow(["period", "forecast"])
        writer.writerows((point.period, f"{point.value:.4f}") for point in forecast)


def main() -> None:
    parser = argparse.ArgumentParser(description="Forecast future SPM process values.")
    parser.add_argument("--input", type=Path, required=True, help="historical CSV file")
    parser.add_argument("--output", type=Path, default=Path("forecast.csv"))
    parser.add_argument("--periods", type=int, default=3, help="number of future periods")
    args = parser.parse_args()

    forecast = linear_forecast(_read_values(args.input), args.periods)
    _write_forecast(args.output, forecast)
    print(f"Wrote {len(forecast)} forecast rows to {args.output}")


if __name__ == "__main__":
    main()