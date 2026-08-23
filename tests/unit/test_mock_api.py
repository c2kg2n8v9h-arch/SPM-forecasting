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
