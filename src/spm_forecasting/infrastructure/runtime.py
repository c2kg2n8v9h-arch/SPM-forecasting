"""Fail-closed integration selection.

Live adapters are intentionally not included. A deployment must provide and review
implementations of the integration ports before live mode can be enabled.
"""

import os
from dataclasses import dataclass

from .mock_services import MockEmailService, MockNetworkService, MockSystemGateway


class LiveModeNotConfiguredError(RuntimeError):
    """Raised when live integration is requested without approved adapters."""


@dataclass(frozen=True)
class IntegrationBundle:
    system: object
    network: object
    email: object
    mode: str


def build_integrations(mode: str | None = None) -> IntegrationBundle:
    """Build the configured integration bundle without contacting any service."""
    selected_mode = (mode or os.getenv("SPM_MODE", "mock")).strip().lower()
    if selected_mode == "mock":
        return IntegrationBundle(
            MockSystemGateway(), MockNetworkService(), MockEmailService(), "mock"
        )
    if selected_mode == "live":
        raise LiveModeNotConfiguredError(
            "live mode is disabled: provide reviewed adapters for the integration ports"
        )
    raise ValueError("SPM_MODE must be either 'mock' or 'live'")
