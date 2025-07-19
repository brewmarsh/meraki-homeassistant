"""Tests for the Meraki data aggregator."""

from unittest.mock import MagicMock

from custom_components.meraki_ha.coordinators.data_aggregator import (
    DataAggregator,
)


async def test_data_aggregator() -> None:
    """Test the Meraki data aggregator."""
    ssid_status_calculator = MagicMock()
    data_aggregator = DataAggregator(ssid_status_calculator)
    processed_devices = [
        {"serial": "Q234-ABCD-5678", "tags": ["tag1", "tag2"]},
    ]
    ssid_data = [
        {"number": 0, "name": "Test SSID", "networkId": "N_123"},
    ]
    network_data = [
        {"id": "N_123", "name": "Test Network"},
    ]
    client_data = [
        {"id": "1", "description": "Client 1", "networkId": "N_123"},
    ]
    network_client_counts = {
        "N_123": 1,
    }
    aggregated_data = await data_aggregator.aggregate_data(
        processed_devices,
        ssid_data,
        network_data,
        client_data,
        network_client_counts,
    )
    assert aggregated_data["devices"][0]["tags"] == ["tag1", "tag2"]
