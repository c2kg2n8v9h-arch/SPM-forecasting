# SPM Forecasting

Small Python forecasting toolkit for SPM process data. It provides a dependency-light linear trend model and a command-line interface that reads historical values from CSV and writes forecasts to CSV.

## Quick start

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .
python -m unittest discover
spm-forecast --input data/sample.csv --periods 3
```

The input CSV must contain a `value` column and may include a `date` column. Example output is written to `forecast.csv` unless `--output` is provided.

## Architecture

- `domain/` contains immutable business models and forecasting rules.
- `application/` contains use cases and orchestration.
- `infrastructure/` contains file and external-system adapters.
- `interfaces/` contains entry points for CLI and future HTTP adapters.
- `tests/unit/` and `tests/integration/` separate fast business tests from boundary tests.
- `.github/workflows/ci.yml` runs linting and tests on every push and pull request.
- `Dockerfile` and `Makefile` provide repeatable local and deployment workflows.
- `data/sample.csv` contains a small example dataset.

## Development

Run the checks with:

```powershell
python -m unittest discover -s tests -v
```
