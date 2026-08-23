"""Authorization primitives for the local mock API."""

from dataclasses import dataclass
from enum import StrEnum


class Role(StrEnum):
    MAINTENANCE_PLANNER = "maintenance_planner"
    PROCUREMENT = "procurement"
    AUDITOR = "auditor"


@dataclass(frozen=True)
class MockIdentity:
    """A fixed, non-production identity used only by local learning flows."""

    subject: str
    role: Role
    allowed_hangars: frozenset[str]


MOCK_IDENTITIES: dict[str, MockIdentity] = {
    "planner-lhr": MockIdentity(
        subject="planner-lhr", role=Role.MAINTENANCE_PLANNER, allowed_hangars=frozenset({"LHR-H1"})
    ),
    "buyer-jfk": MockIdentity(
        subject="buyer-jfk", role=Role.PROCUREMENT, allowed_hangars=frozenset({"JFK-H2"})
    ),
    "auditor-demo": MockIdentity(
        subject="auditor-demo", role=Role.AUDITOR, allowed_hangars=frozenset({"LHR-H1", "JFK-H2"})
    ),
}
