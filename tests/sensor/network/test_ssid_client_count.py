"""Test the Meraki SSID Client Count sensor."""

from unittest.mock import MagicMock

from custom_components.meraki_ha.sensor.network.ssid_client_count import (
    MerakiSSIDClientCountSensor,
)


async def test_ssid_client_count_sensor_wireless_settings() -> None:
    """Test the SSID client count sensor using wireless_settings."""
    coordinator = MagicMock()
    config_entry = MagicMock()
    ssid_data = {
        "networkId": "N_123",
        "number": 0,
        "name": "Test SSID",
        "enabled": True,
        "clientCount": 5,
    }

    # Setup initial coordinator data with new structure
    coordinator.data = {
        "wireless_settings": {
            "N_123": [ssid_data]
        }
    }

    sensor = MerakiSSIDClientCountSensor(coordinator, config_entry, ssid_data)

    assert sensor.name == "Client count"
    assert sensor.native_value == 5

    # Test update
    new_ssid_data = ssid_data.copy()
    new_ssid_data["clientCount"] = 10
    coordinator.data["wireless_settings"]["N_123"] = [new_ssid_data]

    # Mock async_write_ha_state since hass is not set
    object.__setattr__(sensor, "async_write_ha_state", MagicMock())

    sensor._handle_coordinator_update()
    assert sensor.native_value == 10

async def test_ssid_client_count_sensor_fallback() -> None:
    """Test the SSID client count sensor using fallback logic."""
    coordinator = MagicMock()
    config_entry = MagicMock()
    ssid_data = {
        "networkId": "N_123",
        "number": 0,
        "name": "Test SSID",
        "enabled": True,
    }

    # Setup initial coordinator data with legacy structure
    coordinator.data = {
        "ssids": [ssid_data],
        "clients": [
            {"networkId": "N_123", "ssid": "Test SSID", "status": "Online"},
            {"networkId": "N_123", "ssid": "Test SSID", "status": "Online"},
        ],
    }

    sensor = MerakiSSIDClientCountSensor(coordinator, config_entry, ssid_data)

    assert sensor.native_value == 2

    # Test update
    coordinator.data["clients"].append(
        {"networkId": "N_123", "ssid": "Test SSID", "status": "Online"}
    )
    object.__setattr__(sensor, "async_write_ha_state", MagicMock())

    sensor._handle_coordinator_update()
    assert sensor.native_value == 3
