"""Forecasting algorithms that do not depend on storage or transport."""

from .models import ForecastPoint, ForecastRequest


def linear_forecast(request: ForecastRequest) -> list[ForecastPoint]:
    """Project a linear trend using ordinary least-squares regression."""
    values = [observation.value for observation in request.observations]
    x_values = range(len(values))
    x_mean = (len(values) - 1) / 2
    y_mean = sum(values) / len(values)
    denominator = sum((x - x_mean) ** 2 for x in x_values)
    slope = sum(
        (x - x_mean) * (value - y_mean)
        for x, value in zip(x_values, values)
    ) / denominator
    intercept = y_mean - slope * x_mean

    start = len(values)
    return [
        ForecastPoint(period=index, value=intercept + slope * index)
        for index in range(start, start + request.periods)
    ]