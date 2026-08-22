import unittest

from spm_forecasting.infrastructure.runtime import LiveModeNotConfiguredError, build_integrations


class RuntimeIntegrationTests(unittest.TestCase):
    def test_default_runtime_is_mock(self):
        integrations = build_integrations()

        self.assertEqual(integrations.mode, "mock")

    def test_live_mode_fails_closed_without_adapters(self):
        with self.assertRaises(LiveModeNotConfiguredError):
            build_integrations("live")

    def test_unknown_mode_is_rejected(self):
        with self.assertRaises(ValueError):
            build_integrations("staging")