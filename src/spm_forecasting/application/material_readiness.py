"""Use cases that turn synthetic material data into explainable recommendations."""

from ..domain.material_readiness import (
    MaterialRisk,
    MaterialRiskLevel,
    MechanicReadinessCard,
    OrderAlternative,
    OrderRecommendation,
    ScenarioData,
)
from ..domain.operations import AircraftVisit
from .mock_operations import MockOperationsService


class MaterialReadinessService:
    """Evaluates deterministic fixtures only; it never orders, routes, or emails."""

    def material_risks(self, data: ScenarioData, hangar: str) -> tuple[MaterialRisk, ...]:
        risks = []
        for visit in data.visits:
            if visit.hangar != hangar:
                continue
            for part_number in visit.required_parts:
                risks.append(self._risk_for_part(data, visit, part_number))
        return tuple(risks)

    def mechanic_readiness(
        self, data: ScenarioData, hangar: str
    ) -> tuple[MechanicReadinessCard, ...]:
        operations = MockOperationsService()
        cards = []
        for visit in data.visits:
            if visit.hangar != hangar:
                continue
            report = operations.staging_report(visit, data.inventory, data.constraints)
            blockers = list(report.missing_parts)
            blockers.extend(f"unverified documentation: {part}" for part in report.unverified_parts)
            blockers.extend(report.constraint_alerts)
            safe_to_proceed = not blockers
            cards.append(
                MechanicReadinessCard(
                    tail_number=visit.tail_number,
                    hangar=visit.hangar,
                    readiness=report.readiness.value,
                    required_parts=visit.required_parts,
                    safe_to_proceed=safe_to_proceed,
                    blockers=tuple(blockers),
                    next_step=(
                        "Review the work pack and begin only under approved procedures."
                        if safe_to_proceed
                        else "Do not proceed. Escalate the listed blocker to the planner."
                    ),
                )
            )
        return tuple(cards)

    def order_recommendation(
        self, data: ScenarioData, hangar: str, part_number: str, quantity: int
    ) -> OrderRecommendation:
        risks = self.material_risks(data, hangar)
        risk = next((item for item in risks if item.part_number == part_number), None)
        if risk is None:
            raise ValueError("part is not required by a mock visit in this hangar")
        return OrderRecommendation(
            part_number=part_number,
            hangar=hangar,
            quantity=quantity,
            status="mock_pending_approval",
            transmitted=False,
            risk=risk,
            alternatives=(
                OrderAlternative(
                    "transfer from another approved location", "planner and compliance review"
                ),
                OrderAlternative("repair an existing unit", "technical and repair-capacity review"),
                OrderAlternative(
                    "source used serviceable material", "airworthiness and procurement review"
                ),
            ),
        )

    def _risk_for_part(
        self, data: ScenarioData, visit: AircraftVisit, part_number: str
    ) -> MaterialRisk:
        # Scope material evidence to the visit hangar; do not leak another station's stock level.
        records = tuple(
            part
            for part in data.inventory
            if part.part_number == part_number and part.hangar == visit.hangar
        )
        compliant_stock = sum(1 for part in records if part.airworthiness_verified)
        score = 0
        reasons = []
        if compliant_stock == 0:
            score += 50
            reasons.append("no compliant mock stock is available")
        if records and any(not part.airworthiness_verified for part in records):
            score += 30
            reasons.append("available stock has unverified airworthiness documentation")
        if visit.mel_expires_in_hours is not None and visit.mel_expires_in_hours <= 24:
            score += 25
            reasons.append(f"MEL deadline is within {visit.mel_expires_in_hours} hours")
        if data.supplier_delay:
            score += 20
            reasons.append("mock supplier lead-time disruption is active")
        if data.constraints.severe_weather:
            score += 10
            reasons.append("severe weather may delay material movement")
        if not reasons:
            reasons.append(
                "compliant mock stock is available and no active scenario blocker exists"
            )

        level = MaterialRiskLevel.LOW
        if score >= 75:
            level = MaterialRiskLevel.CRITICAL
        elif score >= 50:
            level = MaterialRiskLevel.HIGH
        elif score >= 20:
            level = MaterialRiskLevel.MEDIUM
        return MaterialRisk(
            part_number=part_number,
            hangar=visit.hangar,
            tail_number=visit.tail_number,
            risk_level=level,
            score=score,
            confidence="mock scenario: deterministic, not a production forecast",
            reasons=tuple(reasons),
            lead_time_days=14 if data.supplier_delay else 3,
            available_compliant_stock=compliant_stock,
        )
