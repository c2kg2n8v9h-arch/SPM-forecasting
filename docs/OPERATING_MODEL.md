# Product Operating Model and Safety Boundary

## Purpose

SPM Forecasting helps maintenance planners and inventory/procurement teams make
traceable, evidence-based planning decisions. It does not autonomously change an
ERP, MRO, inventory system, purchase order, routing plan, maintenance record, or
compliance record.

Privacy is a product requirement equal to safety, security, and usability. A
feature must not be released merely because it is useful; it must also collect,
use, retain, and expose operational or personal data only when there is a clear,
documented, authorized need.

## Primary users

### Maintenance planner

**Job:** plan maintenance activity while keeping aircraft availability, material
readiness, MEL urgency, and documentation constraints visible.

**Product outcome:** a planner can understand what needs attention, why it is
prioritized, how confident the forecast is, and which source data supports the
recommendation.

### Inventory and procurement team

**Job:** identify material risk early and prepare the correct replenishment or
transfer action without creating non-compliant stock movement or procurement.

**Product outcome:** a buyer can review an explainable recommendation with the
part, quantity, demand horizon, lead time, documentation status, and source data
before taking action in an approved system.

## User-problem discovery standard

The following are hypotheses, not verified customer facts. Before prioritizing a
feature, validate the relevant hypothesis with at least five representative users
across the two roles, using interviews, workflow observation, or anonymized
product/support data.

| Hypothesis | Validation signal | Do not build until |
| --- | --- | --- |
| Planners spend too long reconciling demand, MEL urgency, and material readiness. | Time-to-plan, rework rate, and interview evidence. | The workflow and highest-friction decision are identified. |
| Buyers discover shortages too late to meet operational demand. | Expedite rate, stock-out rate, lead-time variance, and interview evidence. | The trusted source of inventory and lead-time data is identified. |
| Users do not trust opaque recommendations. | Review/override reasons and explanation-comprehension testing. | A recommendation can show its inputs, assumptions, confidence, and source references. |

## Safety and approval boundary

SPM may calculate, rank, explain, and prepare a **draft** recommendation. A
human remains accountable for every operational or external-system change.

| Capability | Permitted system behavior | Required human approval |
| --- | --- | --- |
| Forecast demand | Generate a versioned forecast with confidence and input-data references. | Approval is required before it is used as an operational commitment. |
| Flag material risk | Display an alert and its evidence. | A planner/buyer decides the response. |
| Suggest purchase order | Create a non-transmitted draft recommendation only. | Authorized procurement user approves outside or through an approved workflow. |
| Suggest inventory transfer/routing | Create a non-transmitted draft recommendation only. | Authorized planner approves after compliance and operational review. |
| Update ERP/MRO/inventory/compliance data | Not permitted by this service. | Requires a separately reviewed integration and explicit approval workflow. |
| Generate RAG answer | Return cited, retrieved information; abstain when unsupported. | User verifies the cited source before operational use. |

## Non-negotiable product controls

- Default-deny integrations: live connectors are disabled unless explicitly
  configured, reviewed, and tested.
- Role-based access: a user may only view stations, programs, and data assigned
  to their role; privileged actions require least privilege.
- Evidence first: every recommendation records input data version, rules/model
  version, timestamp, confidence, source references, and reviewer decision.
- No silent automation: no background purchase order, message, stock movement,
  routing, or record update is allowed.
- Fail safely: missing, stale, contradictory, or non-compliant data produces a
  visible warning and blocks action recommendations where appropriate.
- Privacy and security by design: use a secret manager, encrypt data in transit
  and at rest, minimize retained data, and never expose credentials or sensitive
  operational data in logs or LLM prompts.

## Privacy requirements

- **Minimize data:** collect only the fields necessary for the defined planning
  outcome. Do not ingest employee, customer, aircraft, supplier, or operational
  data "just in case".
- **Classify data:** maintain a data inventory that identifies each field's
  owner, sensitivity, purpose, source, legal basis/approval, storage location,
  retention period, and authorized roles.
- **Separate and restrict access:** enforce role and station/program scope in
  the backend. Production data must be separated from development/test data;
  use synthetic or de-identified data outside production.
- **Retain and delete intentionally:** define retention schedules, support
  approved deletion requests, and securely delete expired data and RAG indexes.
- **Protect exports and audit trails:** redact sensitive values in logs and
  analytics, prevent uncontrolled bulk export, and audit access to sensitive
  records without placing the records themselves in audit events.
- **Constrain AI use:** send the minimum necessary, authorized context to an
  LLM; never send secrets; apply document access controls before retrieval;
  record provider, purpose, and data classification for each AI request; and
  require an approved data-processing arrangement before using an external AI
  provider with production data.
- **Assess changes early:** perform a privacy impact assessment and legal/
  compliance review before introducing a new sensitive-data source, sharing
  data with a third party, or expanding an AI capability.

## Feature definition of done

Every future feature must include:

1. The user, job-to-be-done, validated pain point, and measurable outcome.
2. A threat model covering data access, abuse cases, integration failures, and
   unsafe or misleading recommendations.
3. A privacy review covering data minimization, classification, retention,
   access scope, third-party sharing, and deletion.
4. Authorization rules and audit events.
5. Usability acceptance criteria, including empty, stale, and error states.
6. Automated tests for both happy paths and failure/safety paths.
7. Observability: structured logs, metrics, alert criteria, and an operational
   owner.
8. A rollback or feature-flag plan for production changes.

## Measures of success

- Planner time from demand signal to reviewed plan.
- Material-risk detection lead time and stock-out/expedite rate.
- Recommendation acceptance, override, and abstention rates with reasons.
- Forecast accuracy by part, station, and planning horizon.
- Data freshness and recommendation traceability coverage.
- Security events, authorization denials, and failed integration attempts.
