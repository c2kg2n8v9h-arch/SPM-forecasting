"""Use cases for the offline, deterministic MRO operations demo."""

from dataclasses import dataclass

from ..domain.operations import (
    AircraftVisit,
    GroundConstraints,
    MockPurchaseOrder,
    PartRecord,
    Readiness,
    StagingReport,
)


@dataclass(frozen=True)
class MockOperationsService:
    """Evaluate staging readiness using only data passed by the caller."""

    approval_recipient: str = "yuvaraaj.d@gmail.com"

    def staging_report(
        self,
        visit: AircraftVisit,
        inventory: tuple[PartRecord, ...],
        constraints: GroundConstraints,
    ) -> StagingReport:
        staged = [part for part in inventory if part.hangar == visit.hangar]
        available = {part.part_number for part in staged if part.airworthiness_verified}
        physically_present = {part.part_number for part in staged}
        missing = tuple(sorted(set(visit.required_parts) - available))
        unverified = tuple(sorted(set(visit.required_parts) & physically_present - available))
        alerts = []
        if constraints.severe_weather:
            alerts.append("severe weather may delay ramp or vehicle operations")
        if not constraints.support_vehicle_available:
            alerts.append("no support vehicle available for the planned turnaround")
        if missing:
            readiness = Readiness.BLOCKED
        elif alerts:
            readiness = Readiness.AT_RISK
        else:
            readiness = Readiness.READY
        return StagingReport(
            tail_number=visit.tail_number,
            hangar=visit.hangar,
            readiness=readiness,
            missing_parts=missing,
            unverified_parts=unverified,
            mel_expires_in_hours=visit.mel_expires_in_hours,
            constraint_alerts=tuple(alerts),
        )

    def purchase_order_recommendations(
        self,
        required_parts: tuple[str, ...],
        inventory: tuple[PartRecord, ...],
    ) -> tuple[MockPurchaseOrder, ...]:
        """Create approval artifacts when no compliant stock exists globally."""
        verified_stock = {part.part_number for part in inventory if part.airworthiness_verified}
        return tuple(
            MockPurchaseOrder(part_number=part_number, quantity=1, approval_recipient=self.approval_recipient)
            for part_number in sorted(set(required_parts) - verified_stock)
        )