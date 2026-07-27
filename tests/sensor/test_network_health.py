"""Tests for the Meraki network health sensor."""

from unittest.mock import MagicMock

from custom_components.meraki_ha.sensor.network_health import MerakiNetworkHealthSensor
from homeassistant.core import HomeAssistant


class MockDevice:
    """Mock Meraki device for testing."""

    def __init__(self, serial, network_id, model, status):
        self.serial = serial
        self.network_id = network_id
        self.model = model
        self.status = status


async def test_network_health_sensor_states(hass: HomeAssistant) -> None:
    """Test the Meraki network health sensor states."""
    coordinator = MagicMock()
    coordinator.data = {}
    config_entry = MagicMock()

    # Mock network data
    network = MagicMock()
    network.id = "N_123"
    network.name = "Test Network"

    # Define devices
    devices = [
        MockDevice("MX1", "N_123", "MX64", "online"),
        MockDevice("MX2", "N_123", "MX64", "online"),
        MockDevice("MS1", "N_123", "MS120", "online"),
        MockDevice("MR1", "N_123", "MR33", "offline"),
    ]

    coordinator.data = {"devices_by_serial": {d.serial: d for d in devices}}

    # MX Health Sensor (All online)
    mx_sensor = MerakiNetworkHealthSensor(
        coordinator, config_entry, network, "MX", "Gateways"
    )
    assert mx_sensor.native_value == "Online"
    assert mx_sensor.extra_state_attributes["total_devices"] == 2
    assert mx_sensor.extra_state_attributes["online_devices"] == 2

    # MS Health Sensor (All online)
    ms_sensor = MerakiNetworkHealthSensor(
        coordinator, config_entry, network, "MS", "Switches"
    )
    assert ms_sensor.native_value == "Online"

    # MR Health Sensor (One offline)
    mr_sensor = MerakiNetworkHealthSensor(
        coordinator, config_entry, network, "MR", "Access Points"
    )
    assert mr_sensor.native_value == "Offline"
    assert mr_sensor.extra_state_attributes["total_devices"] == 1
    assert mr_sensor.extra_state_attributes["online_devices"] == 0
    assert "MR1" in mr_sensor.extra_state_attributes["offline_devices"]


async def test_network_health_sensor_degraded(hass: HomeAssistant) -> None:
    """Test the Meraki network health sensor degraded state."""
    coordinator = MagicMock()
    coordinator.data = {}
    config_entry = MagicMock()
    network = MagicMock()
    network.id = "N_123"
    network.name = "Test Network"

    devices = [
        MockDevice("MX1", "N_123", "MX64", "online"),
        MockDevice("MX2", "N_123", "MX64", "offline"),
    ]
    coordinator.data = {"devices_by_serial": {d.serial: d for d in devices}}

    mx_sensor = MerakiNetworkHealthSensor(
        coordinator, config_entry, network, "MX", "Gateways"
    )
    assert mx_sensor.native_value == "Degraded"
    assert mx_sensor.extra_state_attributes["total_devices"] == 2
    assert mx_sensor.extra_state_attributes["online_devices"] == 1
