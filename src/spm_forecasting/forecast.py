"""Simple forecasting models with no third-party runtime dependencies."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ForecastPoint:
    """A single predicted value and its zero-based forecast period."""

    period: int
    value: float


def linear_forecast(values: list[float], periods: int) -> list[ForecastPoint]:
    """Forecast future values using ordinary least-squares linear regression."""
    if len(values) < 2:
        raise ValueError("at least two historical values are required")
    if periods < 1:
        raise ValueError("periods must be at least 1")
    if any(not isinstance(value, (int, float)) for value in values):
        raise TypeError("values must contain only numbers")

    x_values = range(len(values))
    x_mean = (len(values) - 1) / 2
    y_mean = sum(values) / len(values)
    denominator = sum((x - x_mean) ** 2 for x in x_values)
    slope = sum((x - x_mean) * (y - y_mean) for x, y in zip(x_values, values)) / denominator
    intercept = y_mean - slope * x_mean

    return [
        ForecastPoint(period=index, value=intercept + slope * index)
        for index in range(len(values), len(values) + periods)
    ]