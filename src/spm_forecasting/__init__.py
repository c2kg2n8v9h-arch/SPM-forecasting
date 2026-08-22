"""Forecasting tools for SPM process data."""

from .domain.models import ForecastPoint
from .forecast import linear_forecast

__all__ = ["ForecastPoint", "linear_forecast"]