"""Explainable, mock-only material-readiness models.

These models deliberately represent recommendations, not operational commands.
"""

from dataclasses import dataclass
from enum import StrEnum

from .operations import AircraftVisit, GroundConstraints, PartRecord


class MockScenario(StrEnum):
    NORMAL = "normal"
    AOG_SHORTAGE = "aog_shortage"
    UNVERIFIED_DOCUMENTATION = "unverified_documentation"
    SUPPLIER_DELAY = "supplier_delay"
    MEL_URGENCY = "mel_urgency"
    SEVERE_WEATHER = "severe_weather"


class MaterialRiskLevel(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass(frozen=True)
class ScenarioData:
    """Synthetic scenario inputs shared across application and adapter layers."""

    scenario: MockScenario
    visits: tuple[AircraftVisit, ...]
    inventory: tuple[PartRecord, ...]
    constraints: GroundConstraints
    supplier_delay: bool = False


@dataclass(frozen=True)
class MaterialRisk:
    """A traceable mock risk assessment for one part needed by one aircraft visit."""

    part_number: str
    hangar: str
    tail_number: str
    risk_level: MaterialRiskLevel
    score: int
    confidence: str
    reasons: tuple[str, ...]
    lead_time_days: int
    available_compliant_stock: int


@dataclass(frozen=True)
class OrderAlternative:
    """A human-reviewed option; none of these choices executes an action."""

    option: str
    review_required: str


@dataclass(frozen=True)
class OrderRecommendation:
    """A non-transmitted purchase recommendation with its decision evidence."""

    part_number: str
    hangar: str
    quantity: int
    status: str
    transmitted: bool
    risk: MaterialRisk
    alternatives: tuple[OrderAlternative, ...]


@dataclass(frozen=True)
class MechanicReadinessCard:
    """A concise, pre-task card that clearly calls out safe-stop conditions."""

    tail_number: str
    hangar: str
    readiness: str
    required_parts: tuple[str, ...]
    safe_to_proceed: bool
    blockers: tuple[str, ...]
    next_step: str


@dataclass(frozen=True)
class MockDecision:
    """A simulated user decision captured to evaluate recommendation usefulness."""

    actor: str
    role: str
    hangar: str
    decision: str
    reason: str
    correlation_id: str
