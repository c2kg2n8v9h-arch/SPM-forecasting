"""Offline demo entry point for the MRO planning workflow."""

import argparse

from ..application.mock_integrations import MockIntegrationWorkflow
from ..application.mock_operations import MockOperationsService
from ..infrastructure.mock_data import load_demo_data
from ..infrastructure.mock_services import MockEmailService, MockNetworkService, MockSystemGateway


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the offline SPM MRO operations demo.")
    parser.parse_args()
    visits, inventory, constraints = load_demo_data()
    service = MockOperationsService()
    integrations = MockIntegrationWorkflow(
        system=MockSystemGateway(),
        network=MockNetworkService(),
        email=MockEmailService(),
    )
    required_parts = tuple(part for visit in visits for part in visit.required_parts)

    print("MOCK MODE: no network, email, ERP, MRO, or live environment access")
    for visit in visits:
        report = service.staging_report(visit, inventory, constraints)
        print(f"{report.readiness.value.upper()} {report.tail_number} at {report.hangar}")
        if report.missing_parts:
            print(f"  missing compliant parts: {', '.join(report.missing_parts)}")
            for part_number in report.missing_parts:
                integrations.route_part(part_number, visit.hangar, visit.tail_number)
        if report.unverified_parts:
            print(f"  quarantined documentation: {', '.join(report.unverified_parts)}")
        if report.mel_expires_in_hours is not None:
            print(f"  MEL deadline: {report.mel_expires_in_hours} hours")

    for order in service.purchase_order_recommendations(required_parts, inventory):
        integrations.queue_purchase_order(order)
        print(f"MOCK PO {order.part_number}: {order.quantity} unit -> {order.delivery_status}")
        print(f"  approval artifact recipient: {order.approval_recipient}")

    print(f"MOCK system events recorded: {len(integrations.system.events)}")
    print(f"MOCK network requests recorded: {len(integrations.network.requests)}")
    print(f"MOCK emails queued, not sent: {len(integrations.email.outbox)}")


if __name__ == "__main__":
    main()