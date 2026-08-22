"""Domain models for mock MRO operations planning."""

from dataclasses import dataclass
from enum import StrEnum


class Readiness(StrEnum):
    READY = "green"
    AT_RISK = "yellow"
    BLOCKED = "red"


@dataclass(frozen=True)
class PartRecord:
    part_number: str
    serial_number: str
    hangar: str
    airworthiness_verified: bool


@dataclass(frozen=True)
class AircraftVisit:
    tail_number: str
    hangar: str
    required_parts: tuple[str, ...]
    mel_expires_in_hours: int | None


@dataclass(frozen=True)
class GroundConstraints:
    severe_weather: bool
    support_vehicle_available: bool


@dataclass(frozen=True)
class StagingReport:
    tail_number: str
    hangar: str
    readiness: Readiness
    missing_parts: tuple[str, ...]
    unverified_parts: tuple[str, ...]
    mel_expires_in_hours: int | None
    constraint_alerts: tuple[str, ...]


@dataclass(frozen=True)
class MockPurchaseOrder:
    """A simulated approval request; no email or procurement system is called."""

    part_number: str
    quantity: int
    approval_recipient: str
    delivery_status: str = "mock_pending_approval"