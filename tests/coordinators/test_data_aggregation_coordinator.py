"""Tests for the Meraki data aggregation coordinator."""

from unittest.mock import MagicMock

from custom_components.meraki_ha.coordinators.data_aggregation_coordinator import (
    DataAggregationCoordinator,
)


async def test_data_aggregation_coordinator() -> None:
    """Test the Meraki data aggregation coordinator."""
    main_coordinator = MagicMock()
    main_coordinator.data = {
        "devices": [
            {"serial": "Q234-ABCD-5678", "tags": ["tag1", "tag2"]},
            {"serial": "Q234-ABCD-5679", "tags": ["tag3", "tag4"]},
        ],
        "networks": [
            {"id": "N_123", "name": "Test Network"},
        ],
        "ssids": [
            {"number": 0, "name": "Test SSID", "networkId": "N_123"},
        ],
        "clients": [
            {"id": "1", "description": "Client 1", "networkId": "N_123"},
        ],
    }
    data_processor = MagicMock()
    data_aggregator = MagicMock()
    coordinator = DataAggregationCoordinator(
        main_coordinator, data_processor, data_aggregator
    )
    coordinator.data = await coordinator._async_update_data(
        main_coordinator.data["devices"],
        main_coordinator.data["ssids"],
        main_coordinator.data["networks"],
        main_coordinator.data["clients"],
        {},
    )
    assert "devices" in coordinator.data
    assert coordinator.data["devices"][0]["tags"] == ["tag1", "tag2"]
