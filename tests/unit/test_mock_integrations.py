import unittest

from spm_forecasting.application.mock_integrations import MockIntegrationWorkflow
from spm_forecasting.domain.operations import MockPurchaseOrder
from spm_forecasting.infrastructure.mock_services import (
    MockEmailService,
    MockNetworkService,
    MockSystemGateway,
)


class MockIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.system = MockSystemGateway()
        self.network = MockNetworkService()
        self.email = MockEmailService()
        self.workflow = MockIntegrationWorkflow(self.system, self.network, self.email)

    def test_routing_is_recorded_without_network_transmission(self):
        self.workflow.route_part("P1", "H1", "N1")

        self.assertEqual(self.network.requests[0].path, "/mock/routing-requests")
        self.assertEqual(self.system.events[0].system, "mock-mro")

    def test_purchase_order_email_is_queued_not_sent(self):
        self.workflow.queue_purchase_order(MockPurchaseOrder("P1", 1, "planner@example.test"))

        self.assertEqual(len(self.email.outbox), 1)
        self.assertIn("MOCK ONLY", self.email.outbox[0].body)

    def test_network_service_rejects_external_style_path(self):
        with self.assertRaises(ValueError):
            self.network.request("GET", "https://example.com", {})