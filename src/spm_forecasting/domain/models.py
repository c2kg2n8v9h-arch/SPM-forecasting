"""Immutable domain models used across application boundaries."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Observation:
    """A historical process measurement."""

    period: int
    value: float


@dataclass(frozen=True)
class ForecastPoint:
    """A predicted process measurement."""

    period: int
    value: float


@dataclass(frozen=True)
class ForecastRequest:
    """Validated input for a forecast operation."""

    observations: tuple[Observation, ...]
    periods: int

    def __post_init__(self) -> None:
        if len(self.observations) < 2:
            raise ValueError("at least two historical values are required")
        if self.periods < 1:
            raise ValueError("periods must be at least 1")