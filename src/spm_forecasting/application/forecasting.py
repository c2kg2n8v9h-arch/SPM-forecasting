"""Forecasting application use case."""

from dataclasses import dataclass

from ..domain.models import ForecastPoint, ForecastRequest, Observation
from ..domain.services import linear_forecast


@dataclass
class ForecastingService:
    """Application boundary for creating forecasts."""

    def forecast(self, values: list[float], periods: int) -> list[ForecastPoint]:
        if any(not isinstance(value, (int, float)) for value in values):
            raise TypeError("values must contain only numbers")
        observations = tuple(
            Observation(period=index, value=value)
            for index, value in enumerate(values)
        )
        return linear_forecast(ForecastRequest(observations=observations, periods=periods))
