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
spm-rag ingest --input data/documents
spm-rag ask --question "Which parts require verified documentation?"
```

The input CSV must contain a `value` column and may include a `date` column. Example output is written to `forecast.csv` unless `--output` is provided.

## Architecture

- `domain/` contains immutable business models and forecasting rules.
- `application/` contains use cases and orchestration.
- `infrastructure/` contains file and external-system adapters.
- `infrastructure/integration_ports.py` defines stable contracts for approved live adapters.
- `infrastructure/runtime.py` selects providers and fails closed when live mode is unconfigured.
- `interfaces/` contains entry points for CLI and future HTTP adapters.
- `domain/rag.py` contains framework-independent RAG models.
- `application/rag/` contains document ingestion and question-answering use cases.
- `infrastructure/rag/` contains replaceable retrieval adapters. The default adapter is a local JSON-backed lexical index with no cloud or model dependency.
- `tests/unit/` and `tests/integration/` separate fast business tests from boundary tests.
- `TEST_CASES.md` lists the action and expected result for each automated scenario.
- `.github/workflows/ci.yml` runs linting and tests on every push and pull request.
- `Dockerfile` and `Makefile` provide repeatable local and deployment workflows.
- `data/sample.csv` contains a small example dataset.

## Local UI

The responsive operations dashboard is in `web/`. It uses bundled mock data only and makes no browser requests to APIs, fonts, analytics, email, or live systems.

```powershell
python -m http.server 8080 --directory web
```

Open `http://localhost:8080` to view the dashboard. Search, status filtering, navigation, refresh, and export controls are local demonstrations.

## Local mock API

The optional API simulates role-scoped planner and procurement workflows using
only local fixtures. It listens only on `127.0.0.1`; it has no cloud, live
identity, ERP/MRO, email, or external-network integration.

```powershell
python -m pip install -e ".[api,dev]"
spm-mock-api
```

The API intentionally uses fixed mock identities through the `X-Mock-User`
header: `planner-lhr`, `buyer-jfk`, and `auditor-demo`. This is a learning aid,
not real authentication. Requests without a known identity are denied, records
are scope-filtered, purchase orders remain non-transmitted drafts, and audit
events contain metadata only. Open `http://127.0.0.1:8000/docs` to explore the
local API contract.

## Material Readiness Copilot (mock-only)

The local API now simulates the decisions that connect material planning,
procurement, and hangar execution. Every result is deterministic synthetic data,
and every recommendation remains a human-reviewed draft.

| Workflow | Mock user | Endpoint | What it demonstrates |
| --- | --- | --- | --- |
| Scenario simulation | Any known mock user | `GET /v1/mock/scenarios` | Normal, AOG shortage, documentation, supplier delay, MEL urgency, and weather scenarios. |
| Material risk | Planner, buyer, or auditor | `GET /v1/mock/material-risks?hangar=LHR-H1&scenario=aog_shortage` | Risk level, score, reasons, lead time, and compliant-stock evidence. |
| Mechanic readiness | Mechanic, planner, or auditor | `GET /v1/mock/mechanic-readiness?hangar=LHR-H1&scenario=aog_shortage` | Clear blockers and a safe-to-proceed/do-not-proceed instruction. |
| Draft order | Buyer | `POST /v1/mock/purchase-order-drafts` | A non-transmitted recommendation with human-review alternatives. |
| Decision learning | Planner or buyer | `POST /v1/mock/decisions` | Simulated accept/reject/modify feedback; auditors can view stored mock decisions. |

Use `planner-lhr`, `buyer-jfk`, `mechanic-lhr`, or `auditor-demo` in the
`X-Mock-User` header. Each identity can see only its assigned mock hangar. The
API rejects unknown identities, unsupported roles, and out-of-scope hangars.

## Mock-only safety boundary

`spm-demo` uses only deterministic fixtures in `infrastructure/mock_data.py`. The project intentionally has no HTTP clients, cloud SDKs, ERP/MRO connectors, email sender, credentials, telemetry exporter, or live-environment configuration. A purchase-order recommendation is printed as a `mock_pending_approval` artifact only; it is never emailed or submitted.

The mock workflow treats a part as available only when its serialized record has verified airworthiness documentation. It also reports MEL urgency, missing stock, documentation quarantine, weather, and support-vehicle constraints.

## Local RAG workflow

The initial RAG implementation is local by default. It supports Markdown, text, and CSV files, splits them into overlapping chunks, stores the chunks in `data/rag_index/index.json`, and returns matching excerpts with source paths. It does not call an LLM or invent an answer when no indexed text matches.

```powershell
New-Item -ItemType Directory -Force data/documents
spm-rag ingest --input data/documents
spm-rag ask --question "Which parts require verified documentation?"
```

Install the optional OpenAI adapter and request a grounded generated answer:

```powershell
python -m pip install -e ".[rag]"
$env:OPENAI_API_KEY = "your-key"
spm-rag ask --llm --question "Which parts require verified documentation?"
```

The LLM receives only retrieved chunks and is instructed to cite their source paths. `spm-rag ask` remains offline unless `--llm` is explicitly provided.

The retrieval boundary is defined in `infrastructure/rag/ports.py`, so a future embedding provider, vector database, or LLM can replace the local adapter without changing forecasting or domain code. Keep operational document metadata such as revision, station, part number, and effective date available when adding a production adapter.

## Live-system readiness

The application is structurally ready for approved live integrations through typed system, network, and email ports. The runtime remains fail-closed: `SPM_MODE=mock` is the default, while `SPM_MODE=live` raises an error until reviewed adapters are supplied by the deployment team. No live connector, endpoint, credential, or transmission is included in this repository.

Use `.env.example` only as a configuration reference. Store real credentials in an approved secret manager, never in source control. Before enabling live mode, add contract tests, allowlisted endpoints, TLS verification, timeouts, retries, audit logging, RBAC, data minimization, and an approval/change-control review.

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

To watch the browser while the scripts run with a 250 ms action delay:

```powershell
npm run test:e2e:watch
```

For a custom delay, use `PW_HEADLESS=false PW_SLOW_MO=500 npx playwright test --headed` in Bash, or `$env:PW_HEADLESS="false"; $env:PW_SLOW_MO="500"; npx playwright test --headed` in PowerShell. CI remains headless unless explicitly overridden.

CI runs the same suite in Chromium desktop and mobile projects. Test reports and browser artifacts are intentionally excluded from Git.
