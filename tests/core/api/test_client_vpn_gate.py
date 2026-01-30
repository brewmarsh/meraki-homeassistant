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
    return MagicMock()


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
    client.network = AsyncMock()
    client.wireless = AsyncMock()
    client.device_fetcher = AsyncMock()
    client.device_fetcher.async_fetch_devices = AsyncMock(
        return_value={"devices": [], "battery_readings": None}
    )
    client.client_fetcher = AsyncMock()
    client.client_fetcher.async_fetch_network_clients = AsyncMock(return_value=[])
    client.client_fetcher.async_fetch_device_clients = AsyncMock(return_value={})
    client._run_with_semaphore = MagicMock(side_effect=lambda x: x)

    # Mock coordinator sync methods to avoid RuntimeWarning
    client.coordinator.is_traffic_check_due = MagicMock(return_value=True)
    client.coordinator.is_vlan_check_due = MagicMock(return_value=True)

    # Mock other methods called by get_all_data
    client._async_fetch_initial_data = AsyncMock(
        return_value={
            "networks": [{"id": "N_123", "productTypes": ["appliance"]}],
            "devices": [],
        }
    )

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
    client.network = AsyncMock()
    client.wireless = AsyncMock()
    client.device_fetcher = AsyncMock()
    client.device_fetcher.async_fetch_devices = AsyncMock(
        return_value={"devices": [], "battery_readings": None}
    )
    client.client_fetcher = AsyncMock()
    client.client_fetcher.async_fetch_network_clients = AsyncMock(return_value=[])
    client.client_fetcher.async_fetch_device_clients = AsyncMock(return_value={})
    client._run_with_semaphore = MagicMock(side_effect=lambda x: x)

    # Mock coordinator sync methods to avoid RuntimeWarning
    client.coordinator.is_traffic_check_due = MagicMock(return_value=True)
    client.coordinator.is_vlan_check_due = MagicMock(return_value=True)

    # Mock other methods called by get_all_data
    client._async_fetch_initial_data = AsyncMock(
        return_value={
            "networks": [{"id": "N_123", "productTypes": ["appliance"]}],
            "devices": [],
        }
    )

    # Mock parsers to avoid errors with minimal data
    with (
        patch(
            "custom_components.meraki_ha.core.coordinator_helpers.device_fetcher.parse_device_data"
        ),
        patch("custom_components.meraki_ha.core.api.client.parse_appliance_data"),
        patch("custom_components.meraki_ha.core.api.client.parse_sensor_data"),
    ):
        # Run get_all_data
        await client.get_all_data()

    # Verify get_vpn_status WAS called
    client.appliance.get_vpn_status.assert_called_once_with("N_123")
