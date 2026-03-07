"""Tests for the Meraki Client Status Sensor."""

from unittest.mock import MagicMock

import pytest

from custom_components.meraki_ha.const.integration import DOMAIN, from custom_components.meraki_ha.sensor.client.status import MerakiClientStatusSensor


@pytest.fixture
def mock_coordinator():
    """Fixture for a mocked MerakiMainCoordinator."""
    coordinator = MagicMock()

    client1 = {
        "mac": "00:11:22:33:44:55",
        "description": "My Laptop",
        "ip": "192.168.1.100",
        "status": "Online",
        "manufacturer": "Apple",
        "os": "macOS",
        "usage": {"sent": 100, "recv": 200},
        "recentDeviceSerial": "Q2XX-XXXX-XXXX",
    }

    client2 = {
        "mac": "AA:BB:CC:DD:EE:FF",
        "ip": "192.168.1.101",
        "status": "Offline",
    }

    coordinator.data = {"clients": [client1, client2]}

    coordinator.last_update_success = True
    return coordinator


def test_client_status_sensor(mock_coordinator):
    """Test the client status sensor."""
    client1_data = mock_coordinator.data["clients"][0]
    client2_data = mock_coordinator.data["clients"][1]

    config_entry = MagicMock()
    config_entry.options = {}

    # Test Online Client
    sensor1 = MerakiClientStatusSensor(mock_coordinator, client1_data, config_entry)
    sensor1.hass = MagicMock()
    sensor1.async_write_ha_state = MagicMock()

    assert sensor1.unique_id == "00:11:22:33:44:55_client_status"
    assert sensor1.name == "My Laptop status"
    assert sensor1.native_value == "online"
    assert sensor1.icon == "mdi:lan-connect"
    assert sensor1.extra_state_attributes["ip_address"] == "192.168.1.100"
    assert sensor1.extra_state_attributes["manufacturer"] == "Apple"
    assert sensor1.extra_state_attributes["usage_sent"] == 100

    # Verify DeviceInfo
    assert sensor1.device_info["identifiers"] == {(DOMAIN, "00:11:22:33:44:55")}
    assert sensor1.device_info["name"] == "Meraki My Laptop"
    assert sensor1.device_info["model"] == "Client"
    assert sensor1.device_info["via_device"] == (DOMAIN, "Q2XX-XXXX-XXXX")

    # Test Offline Client
    sensor2 = MerakiClientStatusSensor(mock_coordinator, client2_data, config_entry)
    sensor2.hass = MagicMock()
    sensor2.async_write_ha_state = MagicMock()

    assert sensor2.unique_id == "AA:BB:CC:DD:EE:FF_client_status"
    assert sensor2.name == "192.168.1.101 status"
    assert sensor2.native_value == "offline"
    assert sensor2.icon == "mdi:lan-disconnect"
    assert sensor2.extra_state_attributes["ip_address"] == "192.168.1.101"
    # Name fallback to IP/MAC
    assert sensor2.device_info["name"] == "Meraki 192.168.1.101"

    # Test Update Logic
    # Simulate client going offline
    mock_coordinator.data["clients"][0]["status"] = "Offline"
    sensor1._handle_coordinator_update()
    assert sensor1.native_value == "offline"
    assert sensor1.icon == "mdi:lan-disconnect"

    # Simulate client disappearing (should report offline)
    mock_coordinator.data["clients"] = [client2_data]
    sensor1._handle_coordinator_update()
    assert sensor1.native_value == "offline"
