"""Immutable domain models used across application boundaries."""

import math
from dataclasses import dataclass


MAX_OBSERVATIONS = 1_000_000
MAX_FORECAST_PERIODS = 100_000


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
        if len(self.observations) > MAX_OBSERVATIONS:
            raise ValueError(f"at most {MAX_OBSERVATIONS} historical values are supported")
        if self.periods < 1:
            raise ValueError("periods must be at least 1")
        if self.periods > MAX_FORECAST_PERIODS:
            raise ValueError(f"periods must not exceed {MAX_FORECAST_PERIODS}")
        if any(not math.isfinite(observation.value) for observation in self.observations):
            raise ValueError("historical values must be finite numbers")