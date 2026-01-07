"""Tests for the Meraki data coordinator."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from custom_components.meraki_ha.meraki_data_coordinator import MerakiDataCoordinator
from tests.const import MOCK_NETWORK


@pytest.fixture
def mock_api_client():
    """Fixture for a mocked MerakiAPIClient."""
    client = MagicMock()
    client.get_all_data = AsyncMock()
    return client


@pytest.fixture
def coordinator(hass, mock_api_client):
    """Fixture for a MerakiDataCoordinator instance."""
    entry = MagicMock()
    entry.options = {}
    return MerakiDataCoordinator(hass=hass, api_client=mock_api_client, entry=entry)


@pytest.mark.asyncio
async def test_update_data_handles_errors(coordinator, mock_api_client):
    """Test that _async_update_data handles disabled features."""
    # Arrange
    mock_api_client.get_all_data.return_value = {
        "networks": [MOCK_NETWORK],
        "devices": [],
        "appliance_traffic": {
            MOCK_NETWORK["id"]: {
                "error": "disabled",
                "reason": "Traffic analysis is not enabled",
            }
        },
        "vlans": {MOCK_NETWORK["id"]: []},
    }
    coordinator.add_network_status_message = MagicMock()
    coordinator.mark_traffic_check_done = MagicMock()
    coordinator.mark_vlan_check_done = MagicMock()

    # Act
    await coordinator._async_update_data()

    # Assert
    coordinator.add_network_status_message.assert_any_call(
        MOCK_NETWORK["id"], "Traffic Analysis is not enabled for this network."
    )
    coordinator.mark_traffic_check_done.assert_called_once_with(MOCK_NETWORK["id"])
    coordinator.add_network_status_message.assert_any_call(
        MOCK_NETWORK["id"], "VLANs are not enabled for this network."
    )
    coordinator.mark_vlan_check_done.assert_called_once_with(MOCK_NETWORK["id"])


@pytest.mark.asyncio
async def test_update_data_processes_devices(coordinator, mock_api_client):
    """Test that _async_update_data correctly processes device data."""
    mock_api_client.get_all_data.return_value = {
        "networks": [MOCK_NETWORK],
        "devices": [
            {
                "serial": "ABC-123",
                "name": "Switch",
                "model": "MS120",
                "status": "online",
            },
            {
                "serial": "DEF-456",
                "name": "AP",
                "model": "MR33",
                "status": "online",
            },
        ],
        "appliance_traffic": {},
        "vlans": {},
    }
    coordinator.mark_traffic_check_done = MagicMock()
    coordinator.mark_vlan_check_done = MagicMock()

    result = await coordinator._async_update_data()

    assert "devices" in result
    assert len(result["devices"]) == 2
    assert result["devices"][0]["serial"] == "ABC-123"


@pytest.mark.asyncio
async def test_update_data_with_empty_networks(coordinator, mock_api_client):
    """Test _async_update_data handles empty network list."""
    mock_api_client.get_all_data.return_value = {
        "networks": [],
        "devices": [],
        "appliance_traffic": {},
        "vlans": {},
    }

    result = await coordinator._async_update_data()

    assert "networks" in result
    assert len(result["networks"]) == 0


@pytest.mark.asyncio
async def test_update_data_with_empty_ssids(coordinator, mock_api_client):
    """Test _async_update_data processes empty SSID data."""
    mock_api_client.get_all_data.return_value = {
        "networks": [MOCK_NETWORK],
        "devices": [],
        "ssids": {},
        "appliance_traffic": {},
        "vlans": {},
    }
    coordinator.mark_traffic_check_done = MagicMock()
    coordinator.mark_vlan_check_done = MagicMock()

    result = await coordinator._async_update_data()

    assert "ssids" in result


@pytest.mark.asyncio
async def test_coordinator_api_failure_handling(coordinator, mock_api_client):
    """Test coordinator handles API failures gracefully."""
    mock_api_client.get_all_data.side_effect = Exception("API Error")

    with pytest.raises(Exception, match="API Error"):
        await coordinator._async_update_data()


@pytest.mark.asyncio
async def test_update_data_with_clients(coordinator, mock_api_client):
    """Test _async_update_data processes client data."""
    mock_api_client.get_all_data.return_value = {
        "networks": [MOCK_NETWORK],
        "devices": [],
        "clients": {
            MOCK_NETWORK["id"]: [
                {"id": "client1", "mac": "00:11:22:33:44:55", "ip": "192.168.1.100"},
            ]
        },
        "appliance_traffic": {},
        "vlans": {},
    }
    coordinator.mark_traffic_check_done = MagicMock()
    coordinator.mark_vlan_check_done = MagicMock()

    result = await coordinator._async_update_data()

    assert "clients" in result


def test_coordinator_has_required_attributes(coordinator):
    """Test coordinator has required attributes."""
    # Coordinator should have the data and last_update_success attributes
    assert hasattr(coordinator, "data")
    assert hasattr(coordinator, "last_update_success")
