import unittest

from fastapi.testclient import TestClient

from spm_forecasting.interfaces.mock_api import create_app


class MockApiTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(create_app())

    def test_health_is_explicitly_mock_only(self):
        response = self.client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok", "mode": "mock-only"})
        self.assertEqual(response.headers["cache-control"], "no-store")

    def test_missing_identity_is_denied(self):
        response = self.client.get("/v1/mock/staging-reports")

        self.assertEqual(response.status_code, 401)

    def test_planner_sees_only_assigned_hangar(self):
        response = self.client.get(
            "/v1/mock/staging-reports", headers={"X-Mock-User": "planner-lhr"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual([report["hangar"] for report in response.json()["reports"]], ["LHR-H1"])

    def test_planner_cannot_create_procurement_draft(self):
        response = self.client.post(
            "/v1/mock/purchase-order-drafts",
            headers={"X-Mock-User": "planner-lhr"},
            json={"part_number": "PUMP-100", "quantity": 1},
        )

        self.assertEqual(response.status_code, 403)

    def test_buyer_creates_non_transmitted_draft(self):
        response = self.client.post(
            "/v1/mock/purchase-order-drafts",
            headers={"X-Mock-User": "buyer-jfk"},
            json={"part_number": "VALVE-200", "quantity": 2},
        )

        self.assertEqual(response.status_code, 201)
        self.assertFalse(response.json()["transmitted"])
        self.assertEqual(response.json()["status"], "mock_pending_approval")

    def test_payload_validation_rejects_invalid_part_number(self):
        response = self.client.post(
            "/v1/mock/purchase-order-drafts",
            headers={"X-Mock-User": "buyer-jfk"},
            json={"part_number": "not valid!", "quantity": 0},
        )

        self.assertEqual(response.status_code, 422)

    def test_planner_can_review_explainable_aog_risk_for_assigned_hangar(self):
        response = self.client.get(
            "/v1/mock/material-risks?hangar=LHR-H1&scenario=aog_shortage",
            headers={"X-Mock-User": "planner-lhr"},
        )

        self.assertEqual(response.status_code, 200)
        risk = response.json()["risks"][0]
        self.assertEqual(risk["risk_level"], "critical")
        self.assertIn("MEL deadline is within 4 hours", risk["reasons"])

    def test_procurement_user_cannot_view_another_hangar_material_risk(self):
        response = self.client.get(
            "/v1/mock/material-risks?hangar=LHR-H1",
            headers={"X-Mock-User": "buyer-jfk"},
        )

        self.assertEqual(response.status_code, 403)

    def test_mechanic_sees_safe_stop_instruction_for_shortage(self):
        response = self.client.get(
            "/v1/mock/mechanic-readiness?hangar=LHR-H1&scenario=aog_shortage",
            headers={"X-Mock-User": "mechanic-lhr"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()["cards"][0]["safe_to_proceed"])
        self.assertIn("Do not proceed", response.json()["cards"][0]["next_step"])

    def test_buyer_gets_explainable_draft_with_human_review_options(self):
        response = self.client.post(
            "/v1/mock/purchase-order-drafts",
            headers={"X-Mock-User": "buyer-jfk"},
            json={
                "part_number": "VALVE-200",
                "quantity": 2,
                "hangar": "JFK-H2",
                "scenario": "unverified_documentation",
            },
        )

        self.assertEqual(response.status_code, 201)
        recommendation = response.json()["recommendation"]
        self.assertFalse(recommendation["transmitted"])
        self.assertEqual(len(recommendation["alternatives"]), 3)

    def test_planner_decision_is_visible_to_auditor_only(self):
        decision = self.client.post(
            "/v1/mock/decisions",
            headers={"X-Mock-User": "planner-lhr"},
            json={"hangar": "LHR-H1", "decision": "modified", "reason": "check transfer first"},
        )
        audit_view = self.client.get("/v1/mock/decisions", headers={"X-Mock-User": "auditor-demo"})

        self.assertEqual(decision.status_code, 201)
        self.assertEqual(audit_view.status_code, 200)
        self.assertEqual(audit_view.json()["decisions"][0]["decision"], "modified")
