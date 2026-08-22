"""CSV adapter for importing observations and exporting forecasts."""

import csv
from pathlib import Path

from ..domain.models import ForecastPoint


def read_values(path: Path) -> list[float]:
    with path.open(newline="", encoding="utf-8") as input_file:
        rows = csv.DictReader(input_file)
        if not rows.fieldnames or "value" not in rows.fieldnames:
            raise ValueError("input CSV must contain a 'value' column")
        try:
            return [float(row["value"]) for row in rows]
        except (TypeError, ValueError) as error:
            raise ValueError("every value entry must be numeric") from error


def write_forecast(path: Path, forecast: list[ForecastPoint]) -> None:
    with path.open("w", newline="", encoding="utf-8") as output_file:
        writer = csv.writer(output_file)
        writer.writerow(["period", "forecast"])
        writer.writerows((point.period, f"{point.value:.4f}") for point in forecast)