"""Tests for Meraki SSID auth mode sensor."""

from unittest.mock import MagicMock

import pytest

from custom_components.meraki_ha.sensor.network.ssid_auth_mode import (
    MerakiSSIDAuthModeSensor,
)


@pytest.mark.asyncio
async def test_ssid_auth_mode_sensor():
    """Test the MerakiSSIDAuthModeSensor."""
    mock_coordinator = MagicMock()
    mock_coordinator.data = {
        "wireless_settings": {
            "N123": [
                {"number": 1, "name": "Test SSID", "enabled": True, "authMode": "open"}
            ]
        }
    }

    mock_network = MagicMock()
    mock_network.name = "Test Network"
    mock_coordinator.get_network.return_value = mock_network

    ssid_data = {
        "networkId": "N123",
        "number": 1,
        "name": "Test SSID",
        "authMode": "open",
    }
    mock_config_entry = MagicMock()

    # Instantiate sensor
    sensor = MerakiSSIDAuthModeSensor(mock_coordinator, mock_config_entry, ssid_data)
    sensor.hass = MagicMock()
    sensor.async_write_ha_state = MagicMock()

    # Assert properties
    assert sensor.unique_id == "N123ssid1_auth_mode"
    assert sensor.native_value == "open"
    assert sensor.available is True

    # Test update
    mock_coordinator.data["wireless_settings"]["N123"][0]["authMode"] = "psk"
    sensor._handle_coordinator_update()
    assert sensor.native_value == "psk"

    # Test unavailable when disabled
    mock_coordinator.data["wireless_settings"]["N123"][0]["enabled"] = False
    sensor._handle_coordinator_update()
    assert sensor.available is False
