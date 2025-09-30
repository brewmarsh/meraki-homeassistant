"""Tests for the Meraki SSID device switch."""

import pytest
from unittest.mock import MagicMock, AsyncMock
from homeassistant.core import HomeAssistant

from custom_components.meraki_ha.switch.meraki_ssid_device_switch import (
    MerakiSSIDEnabledSwitch,
    MerakiSSIDBroadcastSwitch,
)


@pytest.fixture
def mock_coordinator():
    """Fixture for a mocked MerakiDataUpdateCoordinator."""
    coordinator = MagicMock()
    coordinator.config_entry.options = {}
    coordinator.async_request_refresh = AsyncMock()
    coordinator.is_pending.return_value = False
    coordinator.data = {
        "ssids": [
            {
                "number": 0,
                "name": "Test SSID",
                "enabled": True,
                "visible": True,
                "networkId": "net-123",
                "productType": "ssid",
            }
        ]
    }
    return coordinator


@pytest.fixture
def mock_meraki_client():
    """Fixture for a mocked MerakiAPIClient."""
    client = MagicMock()
    # Mock the specific method that will be called by the switch
    client.wireless.update_network_wireless_ssid = AsyncMock()
    return client


@pytest.fixture
def mock_config_entry():
    """Fixture for a mocked ConfigEntry."""
    entry = MagicMock()
    entry.options = {}
    return entry


async def test_meraki_ssid_enabled_switch(
    hass: HomeAssistant, mock_coordinator, mock_meraki_client, mock_config_entry
) -> None:
    """Test the Meraki SSID enabled switch."""
    ssid_data = mock_coordinator.data["ssids"][0]

    # Test with prefix format
    mock_config_entry.options = {"device_name_format": "prefix"}
    switch = MerakiSSIDEnabledSwitch(
        mock_coordinator,
        mock_meraki_client,
        mock_config_entry,
        ssid_data,
    )

    assert switch.is_on is True
    assert switch.name == "Enabled Control"
    assert switch.device_info["name"] == "[SSID] Test SSID"

    # Test with omit format
    mock_config_entry.options = {"device_name_format": "omit"}
    switch = MerakiSSIDEnabledSwitch(
        mock_coordinator,
        mock_meraki_client,
        mock_config_entry,
        ssid_data,
    )
    assert switch.name == "Enabled Control"
    assert switch.device_info["name"] == "Test SSID"

    switch.hass = hass
    switch.entity_id = "switch.test"
    await switch.async_turn_off()
    mock_meraki_client.wireless.update_network_wireless_ssid.assert_called_with(
        networkId="net-123", number=0, enabled=False
    )


async def test_meraki_ssid_broadcast_switch(
    hass: HomeAssistant, mock_coordinator, mock_meraki_client, mock_config_entry
) -> None:
    """Test the Meraki SSID broadcast switch."""
    ssid_data = mock_coordinator.data["ssids"][0]

    # Test with prefix format
    mock_config_entry.options = {"device_name_format": "prefix"}
    switch = MerakiSSIDBroadcastSwitch(
        mock_coordinator,
        mock_meraki_client,
        mock_config_entry,
        ssid_data,
    )

    assert switch.is_on is True
    assert switch.name == "Broadcast Control"
    assert switch.device_info["name"] == "[SSID] Test SSID"

    # Test with omit format
    mock_config_entry.options = {"device_name_format": "omit"}
    switch = MerakiSSIDBroadcastSwitch(
        mock_coordinator,
        mock_meraki_client,
        mock_config_entry,
        ssid_data,
    )
    assert switch.name == "Broadcast Control"
    assert switch.device_info["name"] == "Test SSID"

    switch.hass = hass
    switch.entity_id = "switch.test"
    await switch.async_turn_off()
    mock_meraki_client.wireless.update_network_wireless_ssid.assert_called_with(
        networkId="net-123", number=0, visible=False
    )
