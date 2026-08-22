# Test Case Matrix

All tests use deterministic local mock data. No test connects to live APIs, ERP/MRO systems, SMTP, cloud services, or external environments.

## Python Tests

| ID | Area | Action | Expected result |
| --- | --- | --- | --- |
| PY-001 | Forecasting | Forecast `[10, 12, 14, 16]` for 2 periods | Returns periods 4 and 5 with values 18.0 and 20.0 |
| PY-002 | Forecasting validation | Forecast with one historical value | Raises `ValueError` requiring at least two values |
| PY-003 | Forecasting validation | Forecast with zero periods | Raises `ValueError` requiring at least one period |
| PY-004 | Domain validation | Create a request containing `NaN` | Raises `ValueError` and rejects non-finite history |
| PY-005 | Domain validation | Forecast with a string in the values list | Raises `TypeError` and rejects non-numeric input |
| PY-006 | Compliance staging | Stage a physically present part without verified documentation | Marks the visit `BLOCKED` and lists the part as unverified |
| PY-007 | Procurement | Request a required part with no compliant global stock | Creates a `mock_pending_approval` PO artifact for one unit |
| PY-008 | Routing integration | Route a missing part to a hangar | Records a mock MRO event and local request; sends nothing externally |
| PY-009 | Email integration | Queue a PO approval email | Stores one message in the in-memory outbox; does not send email |
| PY-010 | Network safety | Submit `https://example.com` to the mock network service | Raises `ValueError` and rejects external-style paths |
| PY-011 | CLI integration | Run the CLI with a CSV containing `10, 12, 14` | Writes a CSV with forecast header and first forecast value `16.0000` |

## Playwright UI Tests

| ID | Area | Action | Expected result |
| --- | --- | --- | --- |
| UI-001 | Overview | Open the dashboard | Title, greeting, KPI cards, fleet readiness, alerts, and arrival table are visible |
| UI-002 | Navigation | Select Overview, Staging board, Demand forecast, and Procurement | Breadcrumb updates to the exact selected view name |
| UI-003 | Status filter | Select Ready, At risk, or Blocked | Table shows respectively 2, 1, or 1 matching rows, all with the selected status |
| UI-004 | Filter reset | Select Blocked, then All statuses | Table returns to 4 rows |
| UI-005 | Search by aircraft | Search `N200SP` | Exactly one matching arrival is displayed |
| UI-006 | Search by station | Search `JFK-H2` | Exactly one matching arrival is displayed |
| UI-007 | Search by part | Search `VALVE-200` | Exactly one matching arrival is displayed |
| UI-008 | Empty search | Clear the search field | All 4 arrival rows are displayed |
| UI-009 | No-match search | Search `not-found` | Zero arrival rows are displayed |
| UI-010 | Search/filter combination | Search `N200SP` and select Blocked | One row remains |
| UI-011 | Search/filter combination | Search `JFK-H2` and select Ready | Zero rows remain |
| UI-012 | Search/filter combination | Search `VALVE-200` and select Ready | Zero rows remain |
| UI-013 | Search/filter combination | Search `FILTER-318` and select At risk | One row remains |
| UI-014 | Search/filter combination | Search `station` with All statuses | Zero rows remain |
| UI-015 | Refresh action | Click Refresh mock data | Local toast says mock data was refreshed; no non-local request is made |
| UI-016 | Export action | Click Export briefing | Local toast says the briefing was prepared; no upload occurs |
| UI-017 | Safety indicator | Open the dashboard | Mock mode and no-live-system indicators are visible |
| UI-018 | Responsive layout | Open the dashboard in mobile Chrome | Greeting, search, and status controls remain usable without horizontal page overflow |
| UI-019 | Monthly schedule | Open the dashboard and inspect the August schedule | All 12 mock flights are visible with route, departure, arrival, station, and operational status |
| UI-020 | Monthly schedule search | Search `N200SP` in the August schedule | Exactly 3 matching monthly flights remain visible |
| UI-021 | Parts inventory | Open the dashboard and inspect Parts inventory | Serialized part numbers, serials, stations, and Verified/Quarantined states are visible |
| UI-022 | Parts to order | Inspect the Parts to order panel | Parts with no compliant stock show a reason and urgency/demand due indicator |
| UI-023 | Station transfers | Inspect the Station transfers panel | Active part movements show source station, destination station, and ETA/status |
| UI-024 | Actual report | Open Actual vs forecast report | Actual numbers table shows seven dated rows with required, consumed, and variance values |
| UI-025 | Graphical report | Inspect the graphical representation | Actual and Forecast series render together with a visible legend |
| UI-026 | Staging board details | Select Staging board | Four aircraft visits show station, required part, documentation, MEL window, and next action |
| UI-027 | Demand forecast details | Select Demand forecast | Four parts show stock, 30-day demand, confidence, signal, and recommendation |
| UI-028 | Procurement details | Select Procurement | Three mock POs show quantity, priority, approval state, and next step |

## Execution

```powershell
python -m unittest discover -s tests -p "test_*.py"
npm run test:e2e
npm run test:e2e:watch
```

The Playwright suite runs the UI cases in both desktop Chromium and mobile Chrome, producing 46 executions from the matrix above.