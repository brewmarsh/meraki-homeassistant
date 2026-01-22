"""Test the Meraki API client VPN gating logic."""

from unittest.mock import AsyncMock, MagicMock, patch
import pytest

from custom_components.meraki_ha.core.api.client import MerakiAPIClient


@pytest.fixture
def mock_hass():
    """Mock Home Assistant."""
    return AsyncMock()


@pytest.fixture
def mock_coordinator():
    """Mock Coordinator."""
    coordinator = MagicMock()
    # Configure sync methods to return True by default so checks pass
    coordinator.is_traffic_check_due.return_value = True
    coordinator.is_vlan_check_due.return_value = True
    return coordinator


@pytest.mark.asyncio
async def test_vpn_status_not_fetched_when_disabled(mock_hass, mock_coordinator):
    """Test that VPN status is not fetched when enable_vpn_management is False."""
    client = MerakiAPIClient(
        hass=mock_hass,
        api_key="test_key",
        org_id="test_org",
        coordinator=mock_coordinator,
        enable_vpn_management=False,
    )

    # Mock endpoint methods
    client.appliance = AsyncMock()
    client.appliance.get_vpn_status = AsyncMock()

    # Mock other methods called by get_all_data
    client._async_fetch_initial_data = AsyncMock(return_value={
        "networks": [{"id": "N_123", "productTypes": ["appliance"]}],
        "devices": [],
    })
    client._async_fetch_network_clients = AsyncMock(return_value=[])
    client._async_fetch_device_clients = AsyncMock(return_value={})

    # Run get_all_data
    await client.get_all_data()

    # Verify get_vpn_status was NOT called
    client.appliance.get_vpn_status.assert_not_called()


@pytest.mark.asyncio
async def test_vpn_status_fetched_when_enabled(mock_hass, mock_coordinator):
    """Test that VPN status is fetched when enable_vpn_management is True."""
    client = MerakiAPIClient(
        hass=mock_hass,
        api_key="test_key",
        org_id="test_org",
        coordinator=mock_coordinator,
        enable_vpn_management=True,
    )

    # Mock endpoint methods
    client.appliance = AsyncMock()
    client.appliance.get_vpn_status = AsyncMock()

    # Mock other methods called by get_all_data
    client._async_fetch_initial_data = AsyncMock(return_value={
        "networks": [{"id": "N_123", "productTypes": ["appliance"]}],
        "devices": [],
    })
    client._async_fetch_network_clients = AsyncMock(return_value=[])
    client._async_fetch_device_clients = AsyncMock(return_value={})

    # Mock parsers to avoid errors with minimal data
    with patch("custom_components.meraki_ha.core.api.client.parse_network_data", return_value={}), \
         patch("custom_components.meraki_ha.core.api.client.parse_wireless_data", return_value={}), \
         patch("custom_components.meraki_ha.core.api.client.parse_device_data"), \
         patch("custom_components.meraki_ha.core.api.client.parse_appliance_data"), \
         patch("custom_components.meraki_ha.core.api.client.parse_sensor_data"), \
         patch("custom_components.meraki_ha.core.api.client.parse_camera_data"), \
         patch("custom_components.meraki_ha.core.api.client.parse_switch_data"):

        # Run get_all_data
        await client.get_all_data()

    # Verify get_vpn_status WAS called
    client.appliance.get_vpn_status.assert_called_once_with("N_123")
