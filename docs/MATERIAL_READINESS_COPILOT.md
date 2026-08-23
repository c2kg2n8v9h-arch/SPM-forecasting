# Material Readiness Copilot: Learning Guide

## What this feature teaches

The Material Readiness Copilot connects a synthetic maintenance visit to its
required material, documentation status, timing pressure, and operational
constraints. It helps a reviewer see *why* a mock recommendation exists before
recording a simulated decision.

It does not connect to a supplier, ERP, MRO system, inventory system, aircraft,
email service, AWS account, LLM, or real user identity provider.

## Scenario walkthroughs

| Scenario | User question | Expected learning outcome |
| --- | --- | --- |
| `normal` | Is the planned work materially ready? | Compliant stock with no active blocker produces low risk. |
| `aog_shortage` | What makes an urgent shortage critical? | No compliant stock plus a four-hour MEL deadline causes a critical, explained risk. |
| `unverified_documentation` | Why is physically present stock not usable? | Unverified airworthiness documentation blocks use and creates a risk. |
| `supplier_delay` | How does lead-time disruption change a decision? | The risk explanation and simulated lead time change without asserting a live supplier fact. |
| `mel_urgency` | How does time pressure affect prioritization? | The reason list names the MEL deadline; the user remains accountable for action. |
| `severe_weather` | Why should a mechanic pause despite available material? | The readiness card gives a visible stop/escalate instruction. |

## Safety rules represented in code

- Risk scores are deterministic teaching aids, never a production model or a
  release-to-service decision.
- Every score includes readable reasons, a confidence statement, and mock data
  inputs; it never presents simulated information as live truth.
- Purchase recommendations are draft-only and explicitly return
  `transmitted: false`.
- Alternatives—transfer, repair, and used serviceable material—always require
  relevant human, technical, procurement, and airworthiness review.
- The mechanic card says **Do not proceed** when a required part,
  documentation, or operating constraint is blocked.
- The API checks both mock role and mock hangar scope before disclosing data or
  accepting a simulated decision.
- Audit and decision events store metadata only, not request bodies or sensitive
  operational content.

## Reviewer map

| File | Responsibility |
| --- | --- |
| `domain/material_readiness.py` | Small immutable models and their safety meaning. |
| `infrastructure/mock_scenarios.py` | All deterministic scenario inputs; no live client exists here. |
| `application/material_readiness.py` | Explainable risk, mechanic-card, and draft-order rules. |
| `interfaces/mock_api.py` | Role/scope enforcement and local HTTP endpoints. |
| `tests/unit/test_material_readiness.py` | Business and safety rules. |
| `tests/unit/test_mock_api.py` | Authorization, validation, and end-to-end mock API behavior. |
