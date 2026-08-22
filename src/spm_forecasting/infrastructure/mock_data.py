"""Deterministic fixtures. This module intentionally has no network or cloud clients."""

from ..domain.operations import AircraftVisit, GroundConstraints, PartRecord


def load_demo_data() -> tuple[tuple[AircraftVisit, ...], tuple[PartRecord, ...], GroundConstraints]:
    visits = (
        AircraftVisit("N100SP", "LHR-H1", ("PUMP-100",), mel_expires_in_hours=36),
        AircraftVisit("N200SP", "JFK-H2", ("VALVE-200",), mel_expires_in_hours=None),
    )
    inventory = (
        PartRecord("PUMP-100", "SN-001", "LHR-H1", airworthiness_verified=True),
        PartRecord("VALVE-200", "SN-002", "JFK-H2", airworthiness_verified=False),
    )
    constraints = GroundConstraints(severe_weather=False, support_vehicle_available=True)
    return visits, inventory, constraints