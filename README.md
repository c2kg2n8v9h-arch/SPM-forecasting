# SPM Forecasting

Mock-first Python toolkit for SPM process data and MRO operations. It provides forecasting, compliance-aware hangar staging, MEL deadline visibility, operational constraint alerts, and simulated procurement recommendations.

## Quick start

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .
python -m unittest discover
spm-forecast --input data/sample.csv --periods 3
spm-demo
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

## Local UI

The responsive operations dashboard is in `web/`. It uses bundled mock data only and makes no browser requests to APIs, fonts, analytics, email, or live systems.

```powershell
python -m http.server 8080 --directory web
```

Open `http://localhost:8080` to view the dashboard. Search, status filtering, navigation, refresh, and export controls are local demonstrations.

## Mock-only safety boundary

`spm-demo` uses only deterministic fixtures in `infrastructure/mock_data.py`. The project intentionally has no HTTP clients, cloud SDKs, ERP/MRO connectors, email sender, credentials, telemetry exporter, or live-environment configuration. A purchase-order recommendation is printed as a `mock_pending_approval` artifact only; it is never emailed or submitted.

The mock workflow treats a part as available only when its serialized record has verified airworthiness documentation. It also reports MEL urgency, missing stock, documentation quarantine, weather, and support-vehicle constraints.

Mock integration components:

- `MockSystemGateway` records simulated ERP/MRO events in memory.
- `MockNetworkService` records local request-shaped objects and rejects external URLs.
- `MockEmailService` stores approval messages in an in-memory outbox and has no send method.
- `MockIntegrationWorkflow` coordinates those adapters for routing and procurement scenarios.

## Development

Run the checks with:

```powershell
python -m unittest discover -s tests -v
```

## UI end-to-end tests

Install the local browser test dependency and run the complete desktop/mobile mock UI matrix:

```powershell
npm install
npx playwright install chromium
npm run test:e2e
```

The Playwright configuration starts the static dashboard on `127.0.0.1` and tests only bundled mock data. It does not call external APIs, email, ERP/MRO systems, analytics, or live environments.

CI runs the same suite in Chromium desktop and mobile projects. Test reports and browser artifacts are intentionally excluded from Git.
