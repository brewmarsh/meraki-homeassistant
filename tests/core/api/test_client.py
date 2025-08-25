"""Tests for the Meraki API client."""

from unittest.mock import AsyncMock, patch

import pytest
from custom_components.meraki_ha.core.api.client import MerakiAPIClient
from tests.const import MOCK_DEVICE, MOCK_NETWORK


@pytest.fixture
def mock_dashboard():
    """Fixture for a mocked meraki.DashboardAPI."""
    with patch("meraki.DashboardAPI") as mock_dashboard_api:
        yield mock_dashboard_api


@pytest.mark.asyncio
async def test_get_all_data_concurrent(mock_dashboard):
    """Test that get_all_data fetches data concurrently."""
    # Arrange
    api_client = MerakiAPIClient(api_key="test-key", org_id="test-org")
    api_client.organization.get_organization_networks = AsyncMock(
        return_value=[MOCK_NETWORK]
    )
    api_client.organization.get_organization_devices = AsyncMock(
        return_value=[MOCK_DEVICE]
    )
    api_client.organization.get_organization_devices_availabilities = AsyncMock(
        return_value=[]
    )
    api_client.organization.get_organization_appliance_uplink_statuses = AsyncMock(
        return_value=[]
    )
    api_client.network.get_network_clients = AsyncMock(return_value=[])
    api_client.wireless.get_network_ssids = AsyncMock(return_value=[])
    api_client.wireless.get_wireless_settings = AsyncMock(return_value={})
    api_client.camera.get_camera_video_settings = AsyncMock(return_value={})
    api_client.switch.get_device_switch_ports_statuses = AsyncMock(return_value=[])
    api_client.appliance.get_network_appliance_settings = AsyncMock(return_value={})
    api_client.network.get_network_traffic = AsyncMock(return_value=[])
    api_client.appliance.get_vlans = AsyncMock(return_value=[])
    api_client.wireless.get_network_wireless_rf_profiles = AsyncMock(return_value=[])

    # Act
    data = await api_client.get_all_data()

    # Assert
    assert data is not None
    api_client.organization.get_organization_networks.assert_awaited_once()
    api_client.organization.get_organization_devices.assert_awaited_once()
    api_client.network.get_network_clients.assert_awaited_once_with(MOCK_NETWORK["id"])
    # Add more assertions as needed
