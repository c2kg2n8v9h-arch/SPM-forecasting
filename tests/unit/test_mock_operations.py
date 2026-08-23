import unittest

from spm_forecasting.application.mock_operations import MockOperationsService
from spm_forecasting.domain.operations import (
    AircraftVisit,
    GroundConstraints,
    PartRecord,
    Readiness,
)


class MockOperationsTests(unittest.TestCase):
    def setUp(self):
        self.service = MockOperationsService()
        self.constraints = GroundConstraints(False, True)

    def test_only_verified_parts_are_ready(self):
        visit = AircraftVisit("N1", "H1", ("P1",), None)
        inventory = (PartRecord("P1", "S1", "H1", False),)

        report = self.service.staging_report(visit, inventory, self.constraints)

        self.assertEqual(report.readiness, Readiness.BLOCKED)
        self.assertEqual(report.unverified_parts, ("P1",))

    def test_zero_compliant_stock_creates_mock_po(self):
        orders = self.service.purchase_order_recommendations(("P1",), ())

        self.assertEqual(orders[0].delivery_status, "mock_pending_approval")
        self.assertEqual(orders[0].approval_recipient, "mock-approver@example.invalid")
