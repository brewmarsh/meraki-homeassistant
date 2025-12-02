"""Test the Meraki SSID Client Count sensor."""

from unittest.mock import MagicMock

from custom_components.meraki_ha.sensor.network.ssid_client_count import (
    MerakiSSIDClientCountSensor,
)
from homeassistant.components.sensor import SensorStateClass


async def test_ssid_client_count_sensor() -> None:
    """Test the SSID client count sensor."""
    coordinator = MagicMock()
    config_entry = MagicMock()
    ssid_data = {
        "networkId": "N_123",
        "number": 0,
        "name": "Test SSID",
        "enabled": True,
    }

    # Setup initial coordinator data
    coordinator.data = {
        "ssids": [ssid_data],
        "clients": [
            {
                "networkId": "N_123",
                "ssid": "Test SSID",
                "status": "Online",
            },
            {
                "networkId": "N_123",
                "ssid": "Test SSID",
                "status": "Offline",
            },
            {
                "networkId": "N_123",
                "ssid": "Other SSID",
                "status": "Online",
            },
            {
                "networkId": "N_456",
                "ssid": "Test SSID",
                "status": "Online",
            },
            {
                "networkId": "N_123",
                "ssid": "Test SSID",
                "status": "online",  # Lowercase test
            },
        ],
    }

    sensor = MerakiSSIDClientCountSensor(coordinator, config_entry, ssid_data)

    assert sensor.name == "Client Count"
    assert sensor.unique_id == "ssid-N_123-0-clientCount"
    assert sensor.state_class == SensorStateClass.MEASUREMENT
    assert sensor.native_unit_of_measurement == "clients"

    # Check initial calculation
    assert sensor.native_value == 2  # One "Online" and one "online" for this SSID/Network

    # Test update
    coordinator.data["clients"].append(
        {
            "networkId": "N_123",
            "ssid": "Test SSID",
            "status": "Online",
        }
    )
    # Mock async_write_ha_state since hass is not set
    sensor.async_write_ha_state = MagicMock()

    sensor._handle_coordinator_update()
    assert sensor.native_value == 3

    # Test no clients
    coordinator.data["clients"] = []
    sensor._handle_coordinator_update()
    assert sensor.native_value == 0

    # Test coordinator data None
    coordinator.data = None
    sensor._handle_coordinator_update()
    assert sensor.native_value == 0
