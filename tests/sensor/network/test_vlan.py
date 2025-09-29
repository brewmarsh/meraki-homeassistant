"""Tests for the Meraki VLAN sensors."""

import pytest
from unittest.mock import MagicMock

from custom_components.meraki_ha.sensor.setup_helpers import async_setup_sensors


@pytest.fixture
def mock_coordinator():
    """Fixture for a mocked MerakiDataUpdateCoordinator."""
    coordinator = MagicMock()
    coordinator.config_entry = MagicMock()
    coordinator.config_entry.options = {"device_name_format": "omit"}
    coordinator.data = {
        "networks": [{"id": "net1", "name": "Test Network"}],
        "vlans": {
            "net1": [
                {
                    "id": 1,
                    "name": "VLAN 1",
                    "subnet": "192.168.1.0/24",
                    "applianceIp": "192.168.1.1",
                    "enabled": True,
                },
                {
                    "id": 2,
                    "name": "VLAN 2",
                    "subnet": "192.168.2.0/24",
                    "applianceIp": "192.168.2.1",
                    "enabled": False,
                },
            ]
        },
        "devices": [],
        "clients": [],
        "ssids": [],
    }
    return coordinator


def test_vlan_sensor_creation(mock_coordinator):
    """Test that VLAN sensors are created correctly."""
    hass = MagicMock()
    camera_service = MagicMock()

    # Run the setup
    sensors = async_setup_sensors(
        hass, mock_coordinator.config_entry, mock_coordinator, camera_service
    )

    # We expect 2 sensors for the one enabled VLAN (subnet and IP)
    # and we also have the network sensors that are created by default
    # so we filter to just the vlan sensors
    vlan_sensors = [s for s in sensors if "VLAN" in s.__class__.__name__]
    assert len(vlan_sensors) == 2

    # Find the specific sensors
    subnet_sensor = next(s for s in vlan_sensors if "Subnet" in s.name)
    ip_sensor = next(s for s in vlan_sensors if "Appliance IP" in s.name)

    # Assertions for Subnet Sensor
    assert subnet_sensor.unique_id == "meraki_vlan_net1_1_subnet"
    assert subnet_sensor.name == "VLAN 1 Subnet"
    assert subnet_sensor.native_value == "192.168.1.0/24"
    assert subnet_sensor.device_info["name"] == "VLAN 1"

    # Assertions for Appliance IP Sensor
    assert ip_sensor.unique_id == "meraki_vlan_net1_1_appliance_ip"
    assert ip_sensor.name == "VLAN 1 Appliance IP"
    assert ip_sensor.native_value == "192.168.1.1"
    assert ip_sensor.device_info["name"] == "VLAN 1"
