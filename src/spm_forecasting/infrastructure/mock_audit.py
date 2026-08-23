"""In-memory, redacted audit events for local learning flows only."""

from dataclasses import dataclass, field
from datetime import UTC, datetime
from threading import Lock


@dataclass(frozen=True)
class MockAuditEvent:
    actor: str
    action: str
    outcome: str
    correlation_id: str
    created_at: str


@dataclass
class MockAuditLog:
    """Records metadata only; request bodies and sensitive records are never stored."""

    events: list[MockAuditEvent] = field(default_factory=list)
    _lock: Lock = field(default_factory=Lock, repr=False)

    def record(self, actor: str, action: str, outcome: str, correlation_id: str) -> MockAuditEvent:
        event = MockAuditEvent(
            actor=actor,
            action=action,
            outcome=outcome,
            correlation_id=correlation_id,
            created_at=datetime.now(UTC).isoformat(),
        )
        with self._lock:
            self.events.append(event)
        return event
