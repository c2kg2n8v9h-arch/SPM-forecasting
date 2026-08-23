"""Backward-compatible facade for the forecasting domain service."""

from .application.forecasting import ForecastingService
from .domain.models import ForecastPoint


def linear_forecast(values: list[float], periods: int) -> list[ForecastPoint]:
    """Forecast future values using the application service."""
    return ForecastingService().forecast(values, periods)
