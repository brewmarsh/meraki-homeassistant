"""Tests for the Meraki SSID device switch."""

from unittest.mock import AsyncMock, MagicMock

import pytest
from homeassistant.core import HomeAssistant

from custom_components.meraki_ha.switch.meraki_ssid_device_switch import (
    MerakiSSIDBroadcastSwitch,
    MerakiSSIDEnabledSwitch,
)


@pytest.fixture
def mock_coordinator_with_ssid_data(mock_coordinator: MagicMock) -> MagicMock:
    """Fixture for a mocked MerakiDataUpdateCoordinator with SSID data."""
    mock_coordinator.config_entry.options = {}
    mock_coordinator.async_request_refresh = AsyncMock()
    mock_coordinator.is_pending.return_value = False
    mock_coordinator.data = {
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
    return mock_coordinator


@pytest.fixture
def mock_meraki_client() -> MagicMock:
    """Fixture for a mocked MerakiAPIClient."""
    client = MagicMock()
    # Mock the specific method that will be called by the switch
    client.wireless.update_network_wireless_ssid = AsyncMock()
    return client


async def test_meraki_ssid_enabled_switch(
    hass: HomeAssistant,
    mock_coordinator_with_ssid_data: MagicMock,
    mock_meraki_client: MagicMock,
    mock_config_entry: MagicMock,
) -> None:
    """Test the Meraki SSID enabled switch."""
    ssid_data = mock_coordinator_with_ssid_data.data["ssids"][0]

    # Test with prefix format
    mock_config_entry.options = {"device_name_format": "prefix"}
    switch = MerakiSSIDEnabledSwitch(
        mock_coordinator_with_ssid_data,
        mock_meraki_client,
        mock_config_entry,
        ssid_data,
    )

    assert switch.is_on is True
    assert switch.name == "Enabled Control"
    device_info = switch.device_info
    assert device_info is not None
    assert device_info["name"] == "[SSID] Test SSID"

    # Test with omit format
    mock_config_entry.options = {"device_name_format": "omit"}
    switch = MerakiSSIDEnabledSwitch(
        mock_coordinator_with_ssid_data,
        mock_meraki_client,
        mock_config_entry,
        ssid_data,
    )
    assert switch.name == "Enabled Control"
    device_info = switch.device_info
    assert device_info is not None
    assert device_info["name"] == "Test SSID"

    switch.hass = hass
    switch.entity_id = "switch.test"
    await switch.async_turn_off()
    mock_meraki_client.wireless.update_network_wireless_ssid.assert_called_with(
        network_id="net-123", number=0, enabled=False
    )


async def test_meraki_ssid_broadcast_switch(
    hass: HomeAssistant,
    mock_coordinator_with_ssid_data: MagicMock,
    mock_meraki_client: MagicMock,
    mock_config_entry: MagicMock,
) -> None:
    """Test the Meraki SSID broadcast switch."""
    ssid_data = mock_coordinator_with_ssid_data.data["ssids"][0]

    # Test with prefix format
    mock_config_entry.options = {"device_name_format": "prefix"}
    switch = MerakiSSIDBroadcastSwitch(
        mock_coordinator_with_ssid_data,
        mock_meraki_client,
        mock_config_entry,
        ssid_data,
    )

    assert switch.is_on is True
    assert switch.name == "Broadcast Control"
    device_info = switch.device_info
    assert device_info is not None
    assert device_info["name"] == "[SSID] Test SSID"

    # Test with omit format
    mock_config_entry.options = {"device_name_format": "omit"}
    switch = MerakiSSIDBroadcastSwitch(
        mock_coordinator_with_ssid_data,
        mock_meraki_client,
        mock_config_entry,
        ssid_data,
    )
    assert switch.name == "Broadcast Control"
    device_info = switch.device_info
    assert device_info is not None
    assert device_info["name"] == "Test SSID"

    switch.hass = hass
    switch.entity_id = "switch.test"
    await switch.async_turn_off()
    mock_meraki_client.wireless.update_network_wireless_ssid.assert_called_with(
        network_id="net-123", number=0, visible=False
    )
