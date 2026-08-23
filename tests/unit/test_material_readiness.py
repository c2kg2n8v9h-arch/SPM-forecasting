import unittest

from spm_forecasting.application.material_readiness import MaterialReadinessService
from spm_forecasting.domain.material_readiness import MaterialRiskLevel, MockScenario
from spm_forecasting.infrastructure.mock_scenarios import load_scenario


class MaterialReadinessTests(unittest.TestCase):
    def setUp(self):
        self.service = MaterialReadinessService()

    def test_aog_shortage_is_critical_and_explained(self):
        risks = self.service.material_risks(load_scenario(MockScenario.AOG_SHORTAGE), "LHR-H1")

        self.assertEqual(risks[0].risk_level, MaterialRiskLevel.CRITICAL)
        self.assertIn("no compliant mock stock is available", risks[0].reasons)
        self.assertIn("MEL deadline is within 4 hours", risks[0].reasons)

    def test_supplier_delay_changes_lead_time_and_reason(self):
        risks = self.service.material_risks(load_scenario(MockScenario.SUPPLIER_DELAY), "LHR-H1")

        self.assertEqual(risks[0].lead_time_days, 14)
        self.assertIn("mock supplier lead-time disruption is active", risks[0].reasons)

    def test_weather_card_blocks_mechanic_start(self):
        cards = self.service.mechanic_readiness(
            load_scenario(MockScenario.SEVERE_WEATHER), "LHR-H1"
        )

        self.assertFalse(cards[0].safe_to_proceed)
        self.assertIn("severe weather may delay ramp or vehicle operations", cards[0].blockers)

    def test_order_recommendation_is_a_draft_with_alternatives(self):
        recommendation = self.service.order_recommendation(
            load_scenario(MockScenario.UNVERIFIED_DOCUMENTATION), "JFK-H2", "VALVE-200", 2
        )

        self.assertFalse(recommendation.transmitted)
        self.assertEqual(recommendation.status, "mock_pending_approval")
        self.assertEqual(len(recommendation.alternatives), 3)
