"""Local mock-only API for planner and procurement learning workflows.

This module has no cloud, live-system, email, or external-network client.
"""

import argparse
from collections.abc import Callable
from dataclasses import asdict
from typing import Literal
from uuid import UUID, uuid4

from fastapi import Depends, FastAPI, Header, HTTPException, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from ..application.material_readiness import MaterialReadinessService
from ..application.mock_operations import MockOperationsService
from ..domain.access import MOCK_IDENTITIES, MockIdentity, Role
from ..domain.material_readiness import MockDecision, MockScenario
from ..domain.operations import StagingReport
from ..infrastructure.mock_audit import MockAuditLog, MockDecisionLog
from ..infrastructure.mock_data import load_demo_data
from ..infrastructure.mock_scenarios import load_scenario


class PurchaseDraftRequest(BaseModel):
    part_number: str = Field(min_length=1, max_length=64, pattern=r"^[A-Za-z0-9-]+$")
    quantity: int = Field(ge=1, le=100)
    hangar: str = Field(default="JFK-H2", min_length=1, max_length=32)
    scenario: MockScenario = MockScenario.NORMAL


class DecisionRequest(BaseModel):
    hangar: str = Field(min_length=1, max_length=32)
    decision: Literal["accepted", "rejected", "modified"]
    reason: str = Field(min_length=3, max_length=300)


def _report_payload(report: StagingReport) -> dict[str, object]:
    return {
        "tail_number": report.tail_number,
        "hangar": report.hangar,
        "readiness": report.readiness.value,
        "missing_parts": report.missing_parts,
        "unverified_parts": report.unverified_parts,
        "mel_expires_in_hours": report.mel_expires_in_hours,
        "constraint_alerts": report.constraint_alerts,
    }


def create_app(audit_log: MockAuditLog | None = None) -> FastAPI:
    """Build an isolated mock application instance for local use and testing."""

    app = FastAPI(title="SPM Forecasting Mock API", version="0.1.0", redoc_url=None)
    app.state.audit_log = audit_log or MockAuditLog()
    app.state.decision_log = MockDecisionLog()

    @app.middleware("http")
    async def correlation_id(request: Request, call_next: Callable) -> JSONResponse:
        supplied_id = request.headers.get("X-Correlation-ID")
        try:
            request.state.correlation_id = str(UUID(supplied_id)) if supplied_id else str(uuid4())
        except ValueError:
            request.state.correlation_id = str(uuid4())
        response = await call_next(request)
        response.headers["X-Correlation-ID"] = request.state.correlation_id
        response.headers["Cache-Control"] = "no-store"
        return response

    def identity_from_header(
        request: Request, x_mock_user: str | None = Header(default=None)
    ) -> MockIdentity:
        if not x_mock_user or x_mock_user not in MOCK_IDENTITIES:
            app.state.audit_log.record(
                "anonymous", "authenticate_mock_identity", "denied", request.state.correlation_id
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="mock identity required"
            )
        return MOCK_IDENTITIES[x_mock_user]

    def require_one_of(
        identity: MockIdentity,
        roles: set[Role],
        hangar: str,
        request: Request,
        action: str,
    ) -> None:
        """Every data view is checked against the fixed mock role and hangar scope."""

        permitted = identity.role in roles and hangar in identity.allowed_hangars
        app.state.audit_log.record(
            identity.subject,
            action,
            "allowed" if permitted else "denied",
            request.state.correlation_id,
        )
        if not permitted:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="action is not permitted"
            )

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "mode": "mock-only"}

    @app.get("/v1/mock/staging-reports")
    def staging_reports(
        request: Request,
        identity: MockIdentity = Depends(identity_from_header),  # noqa: B008
    ) -> dict[str, object]:
        if identity.role not in {Role.MAINTENANCE_PLANNER, Role.AUDITOR}:
            app.state.audit_log.record(
                identity.subject, "read_staging_reports", "denied", request.state.correlation_id
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="action is not permitted"
            )
        visits, inventory, constraints = load_demo_data()
        service = MockOperationsService()
        reports = [
            _report_payload(service.staging_report(visit, inventory, constraints))
            for visit in visits
            if visit.hangar in identity.allowed_hangars
        ]
        app.state.audit_log.record(
            identity.subject, "read_staging_reports", "allowed", request.state.correlation_id
        )
        return {"mode": "mock-only", "reports": reports}

    @app.get("/v1/mock/scenarios")
    def scenarios(
        request: Request,
        identity: MockIdentity = Depends(identity_from_header),  # noqa: B008
    ) -> dict[str, object]:
        """List the fixed scenarios available for safe, repeatable learning."""

        app.state.audit_log.record(
            identity.subject, "list_mock_scenarios", "allowed", request.state.correlation_id
        )
        return {"mode": "mock-only", "scenarios": [scenario.value for scenario in MockScenario]}

    @app.get("/v1/mock/material-risks")
    def material_risks(
        hangar: str,
        request: Request,
        scenario: MockScenario = MockScenario.NORMAL,
        identity: MockIdentity = Depends(identity_from_header),  # noqa: B008
    ) -> dict[str, object]:
        # The API exposes only the requested mock station, never a global inventory view.
        require_one_of(
            identity,
            {Role.MAINTENANCE_PLANNER, Role.PROCUREMENT, Role.AUDITOR},
            hangar,
            request,
            "read_material_risks",
        )
        risks = MaterialReadinessService().material_risks(load_scenario(scenario), hangar)
        return {
            "mode": "mock-only",
            "scenario": scenario.value,
            "risks": [asdict(risk) for risk in risks],
        }

    @app.get("/v1/mock/mechanic-readiness")
    def mechanic_readiness(
        hangar: str,
        request: Request,
        scenario: MockScenario = MockScenario.NORMAL,
        identity: MockIdentity = Depends(identity_from_header),  # noqa: B008
    ) -> dict[str, object]:
        require_one_of(
            identity,
            {Role.HANGAR_MECHANIC, Role.MAINTENANCE_PLANNER, Role.AUDITOR},
            hangar,
            request,
            "read_mechanic_readiness",
        )
        cards = MaterialReadinessService().mechanic_readiness(load_scenario(scenario), hangar)
        return {
            "mode": "mock-only",
            "scenario": scenario.value,
            "cards": [asdict(card) for card in cards],
        }

    @app.post("/v1/mock/purchase-order-drafts", status_code=status.HTTP_201_CREATED)
    def purchase_order_draft(
        body: PurchaseDraftRequest,
        request: Request,
        identity: MockIdentity = Depends(identity_from_header),  # noqa: B008
    ) -> dict[str, object]:
        require_one_of(
            identity,
            {Role.PROCUREMENT},
            body.hangar,
            request,
            "create_purchase_order_draft",
        )
        try:
            recommendation = MaterialReadinessService().order_recommendation(
                load_scenario(body.scenario), body.hangar, body.part_number, body.quantity
            )
        except ValueError as error:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(error)
            ) from error
        return {
            "mode": "mock-only",
            "scenario": body.scenario.value,
            # Keep these summary fields stable for simple clients; the full explanation is below.
            "part_number": recommendation.part_number,
            "quantity": recommendation.quantity,
            "status": recommendation.status,
            "transmitted": recommendation.transmitted,
            "recommendation": asdict(recommendation),
            "message": "Draft only. No procurement system or email service was contacted.",
        }

    @app.post("/v1/mock/decisions", status_code=status.HTTP_201_CREATED)
    def record_decision(
        body: DecisionRequest,
        request: Request,
        identity: MockIdentity = Depends(identity_from_header),  # noqa: B008
    ) -> dict[str, object]:
        """Capture simulated overrides so scenario usefulness can be measured later."""

        require_one_of(
            identity,
            {Role.MAINTENANCE_PLANNER, Role.PROCUREMENT},
            body.hangar,
            request,
            "record_recommendation_decision",
        )
        decision = app.state.decision_log.record(
            MockDecision(
                actor=identity.subject,
                role=identity.role.value,
                hangar=body.hangar,
                decision=body.decision,
                reason=body.reason,
                correlation_id=request.state.correlation_id,
            )
        )
        return {"mode": "mock-only", "decision": asdict(decision), "stored_locally": True}

    @app.get("/v1/mock/decisions")
    def decisions(
        request: Request,
        identity: MockIdentity = Depends(identity_from_header),  # noqa: B008
    ) -> dict[str, object]:
        if identity.role != Role.AUDITOR:
            app.state.audit_log.record(
                identity.subject, "read_mock_decisions", "denied", request.state.correlation_id
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="action is not permitted"
            )
        app.state.audit_log.record(
            identity.subject, "read_mock_decisions", "allowed", request.state.correlation_id
        )
        return {
            "mode": "mock-only",
            "decisions": [asdict(item) for item in app.state.decision_log.decisions],
        }

    @app.get("/v1/mock/audit-events")
    def audit_events(
        request: Request,
        identity: MockIdentity = Depends(identity_from_header),  # noqa: B008
    ) -> dict[str, object]:
        if identity.role != Role.AUDITOR:
            app.state.audit_log.record(
                identity.subject, "read_audit_events", "denied", request.state.correlation_id
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="action is not permitted"
            )
        app.state.audit_log.record(
            identity.subject, "read_audit_events", "allowed", request.state.correlation_id
        )
        return {
            "mode": "mock-only",
            "events": [event.__dict__ for event in app.state.audit_log.events],
        }

    return app


app = create_app()


def main() -> None:
    """Run only on the local loopback interface."""

    parser = argparse.ArgumentParser(description="Run the local mock-only SPM API.")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=args.port)
