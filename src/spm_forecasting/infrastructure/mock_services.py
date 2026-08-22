"""Safe in-memory replacements for external systems, network, and email.

These adapters deliberately have no transport dependencies. They are suitable for
local demos and tests only; they cannot reach an ERP, MRO system, network, or SMTP.
"""

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass(frozen=True)
class MockSystemEvent:
    """A simulated write to an external system."""

    system: str
    action: str
    payload: dict[str, Any]
    created_at: str


@dataclass(frozen=True)
class MockNetworkRequest:
    """A simulated network request that is never transmitted."""

    method: str
    path: str
    payload: dict[str, Any]


@dataclass(frozen=True)
class MockEmail:
    """An email held in a local outbox, never sent."""

    recipient: str
    subject: str
    body: str


@dataclass
class MockSystemGateway:
    """In-memory ERP/MRO gateway for deterministic integration tests."""

    events: list[MockSystemEvent] = field(default_factory=list)

    def record(self, system: str, action: str, payload: dict[str, Any]) -> MockSystemEvent:
        event = MockSystemEvent(
            system=system,
            action=action,
            payload=dict(payload),
            created_at=datetime.now(UTC).isoformat(),
        )
        self.events.append(event)
        return event


@dataclass
class MockNetworkService:
    """Network-shaped adapter that records requests instead of sending them."""

    requests: list[MockNetworkRequest] = field(default_factory=list)

    def request(self, method: str, path: str, payload: dict[str, Any]) -> MockNetworkRequest:
        if not path.startswith("/"):
            raise ValueError("mock network paths must start with '/'")
        request = MockNetworkRequest(method=method.upper(), path=path, payload=dict(payload))
        self.requests.append(request)
        return request


@dataclass
class MockEmailService:
    """Email outbox that never connects to an SMTP provider."""

    outbox: list[MockEmail] = field(default_factory=list)

    def queue(self, recipient: str, subject: str, body: str) -> MockEmail:
        if not recipient or "@" not in recipient:
            raise ValueError("a valid mock recipient is required")
        message = MockEmail(recipient=recipient, subject=subject, body=body)
        self.outbox.append(message)
        return message