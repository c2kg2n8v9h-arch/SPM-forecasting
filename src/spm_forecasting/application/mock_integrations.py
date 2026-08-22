"""Mock integration workflow for routing, procurement, and notifications."""

from dataclasses import dataclass

from ..domain.operations import MockPurchaseOrder
from ..infrastructure.mock_services import MockEmailService, MockNetworkService, MockSystemGateway


@dataclass
class MockIntegrationWorkflow:
    """Coordinate simulated external interactions without leaving the process."""

    system: MockSystemGateway
    network: MockNetworkService
    email: MockEmailService

    def route_part(self, part_number: str, hangar: str, tail_number: str) -> None:
        payload = {"part_number": part_number, "hangar": hangar, "tail_number": tail_number}
        self.system.record("mock-mro", "create-routing-request", payload)
        self.network.request("POST", "/mock/routing-requests", payload)

    def queue_purchase_order(self, order: MockPurchaseOrder) -> None:
        payload = {"part_number": order.part_number, "quantity": order.quantity}
        self.system.record("mock-erp", "create-purchase-order-draft", payload)
        self.email.queue(
            order.approval_recipient,
            f"Mock approval required: PO for {order.part_number}",
            f"MOCK ONLY: approve {order.quantity} unit of {order.part_number}.",
        )