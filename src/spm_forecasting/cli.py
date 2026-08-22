"""Command-line interface for generating forecasts from CSV files."""

import argparse
from pathlib import Path

from .application.forecasting import ForecastingService
from .infrastructure.csv_repository import read_values, write_forecast


def main() -> None:
    parser = argparse.ArgumentParser(description="Forecast future SPM process values.")
    parser.add_argument("--input", type=Path, required=True, help="historical CSV file")
    parser.add_argument("--output", type=Path, default=Path("forecast.csv"))
    parser.add_argument("--periods", type=int, default=3, help="number of future periods")
    args = parser.parse_args()

    forecast = ForecastingService().forecast(read_values(args.input), args.periods)
    write_forecast(args.output, forecast)
    print(f"Wrote {len(forecast)} forecast rows to {args.output}")


if __name__ == "__main__":
    main()