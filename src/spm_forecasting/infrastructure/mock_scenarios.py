"""Deterministic, synthetic scenarios for learning material-readiness workflows."""

from ..domain.material_readiness import MockScenario, ScenarioData
from ..domain.operations import AircraftVisit, GroundConstraints
from .mock_data import load_demo_data


def load_scenario(scenario: MockScenario) -> ScenarioData:
    """Return a predictable scenario so reviewers can reproduce every result."""

    visits, inventory, constraints = load_demo_data()
    if scenario == MockScenario.AOG_SHORTAGE:
        visits = (AircraftVisit("N100SP", "LHR-H1", ("PUMP-100",), 4),) + visits[1:]
        inventory = tuple(part for part in inventory if part.part_number != "PUMP-100")
    elif scenario == MockScenario.MEL_URGENCY:
        visits = (AircraftVisit("N100SP", "LHR-H1", ("PUMP-100",), 4),) + visits[1:]
    elif scenario == MockScenario.SEVERE_WEATHER:
        constraints = GroundConstraints(severe_weather=True, support_vehicle_available=True)
    elif scenario == MockScenario.SUPPLIER_DELAY:
        return ScenarioData(scenario, visits, inventory, constraints, supplier_delay=True)
    elif scenario == MockScenario.UNVERIFIED_DOCUMENTATION:
        # The baseline fixture already contains an unverified VALVE-200 record.
        pass
    return ScenarioData(scenario, visits, inventory, constraints)
