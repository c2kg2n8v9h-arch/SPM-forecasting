"""Local mock-only API for planner and procurement learning workflows.

This module has no cloud, live-system, email, or external-network client.
"""

import argparse
from collections.abc import Callable
from uuid import UUID, uuid4

from fastapi import Depends, FastAPI, Header, HTTPException, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from ..application.mock_operations import MockOperationsService
from ..domain.access import MOCK_IDENTITIES, MockIdentity, Role
from ..domain.operations import StagingReport
from ..infrastructure.mock_audit import MockAuditLog
from ..infrastructure.mock_data import load_demo_data


class PurchaseDraftRequest(BaseModel):
    part_number: str = Field(min_length=1, max_length=64, pattern=r"^[A-Za-z0-9-]+$")
    quantity: int = Field(ge=1, le=100)


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

    def require(
        identity: MockIdentity, role: Role, hangar: str, request: Request, action: str
    ) -> None:
        permitted = identity.role == role and hangar in identity.allowed_hangars
        outcome = "allowed" if permitted else "denied"
        app.state.audit_log.record(identity.subject, action, outcome, request.state.correlation_id)
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

    @app.post("/v1/mock/purchase-order-drafts", status_code=status.HTTP_201_CREATED)
    def purchase_order_draft(
        body: PurchaseDraftRequest,
        request: Request,
        identity: MockIdentity = Depends(identity_from_header),  # noqa: B008
    ) -> dict[str, object]:
        require(identity, Role.PROCUREMENT, "JFK-H2", request, "create_purchase_order_draft")
        return {
            "mode": "mock-only",
            "part_number": body.part_number,
            "quantity": body.quantity,
            "status": "mock_pending_approval",
            "transmitted": False,
            "message": "Draft only. No procurement system or email service was contacted.",
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
