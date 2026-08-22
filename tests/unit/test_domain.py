import unittest

from spm_forecasting.application.forecasting import ForecastingService
from spm_forecasting.domain.models import ForecastRequest, Observation


class DomainTests(unittest.TestCase):
    def test_service_continues_linear_trend(self):
        result = ForecastingService().forecast([10, 12, 14, 16], periods=2)

        self.assertEqual([point.value for point in result], [18.0, 20.0])

    def test_request_rejects_insufficient_history(self):
        with self.assertRaises(ValueError):
            ForecastRequest((Observation(0, 10),), periods=1)