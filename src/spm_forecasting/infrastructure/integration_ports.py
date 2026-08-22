"""Stable contracts for replacing mock integrations with approved live adapters."""

from typing import Any, Protocol


class SystemGateway(Protocol):
    """Port for an approved ERP/MRO system adapter."""

    def record(self, system: str, action: str, payload: dict[str, Any]) -> Any:
        ...


class NetworkService(Protocol):
    """Port for an approved network adapter."""

    def request(self, method: str, path: str, payload: dict[str, Any]) -> Any:
        ...


class EmailService(Protocol):
    """Port for an approved notification adapter."""

    def queue(self, recipient: str, subject: str, body: str) -> Any:
        ...