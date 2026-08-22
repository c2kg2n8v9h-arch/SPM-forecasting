import unittest

from spm_forecasting import linear_forecast


class LinearForecastTests(unittest.TestCase):
    def test_continues_linear_trend(self):
        result = linear_forecast([10, 12, 14, 16], periods=2)

        self.assertEqual([point.period for point in result], [4, 5])
        self.assertEqual([point.value for point in result], [18.0, 20.0])

    def test_rejects_insufficient_history(self):
        with self.assertRaises(ValueError):
            linear_forecast([10], periods=1)

    def test_rejects_invalid_period_count(self):
        with self.assertRaises(ValueError):
            linear_forecast([10, 12], periods=0)