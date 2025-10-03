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
                    "ipv6": {
                        "enabled": True,
                        "prefix": "2001:db8:1::/64",
                        "prefixAssignments": [
                            {
                                "origin": {
                                    "type": "internet",
                                    "interfaces": ["WAN 1", "WAN 2"],
                                }
                            }
                        ],
                    },
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

    # We expect 7 sensors for the one enabled VLAN
    vlan_sensors = [s for s in sensors if "VLAN" in s.__class__.__name__]
    assert len(vlan_sensors) == 7

    # Find the specific sensors
    id_sensor = next(s for s in vlan_sensors if "VLAN ID" in s.name)
    ipv4_enabled_sensor = next(s for s in vlan_sensors if "IPv4 Enabled" in s.name)
    ipv4_ip_sensor = next(s for s in vlan_sensors if "IPv4 Interface IP" in s.name)
    ipv4_uplink_sensor = next(s for s in vlan_sensors if "IPv4 Uplink" in s.name)
    ipv6_enabled_sensor = next(s for s in vlan_sensors if "IPv6 Enabled" in s.name)
    ipv6_ip_sensor = next(s for s in vlan_sensors if "IPv6 Interface IP" in s.name)
    ipv6_uplink_sensor = next(s for s in vlan_sensors if "IPv6 Uplink" in s.name)

    # Assertions for VLAN ID Sensor
    assert id_sensor.unique_id == "meraki_vlan_net1_1_vlan_id"
    assert id_sensor.name == "VLAN 1 VLAN ID"
    assert id_sensor.native_value == 1
    assert id_sensor.device_info["name"] == "VLAN 1"

    # Assertions for IPv4 Enabled Sensor
    assert ipv4_enabled_sensor.unique_id == "meraki_vlan_net1_1_ipv4_enabled"
    assert ipv4_enabled_sensor.name == "VLAN 1 IPv4 Enabled"
    assert ipv4_enabled_sensor.native_value is True

    # Assertions for IPv4 Interface IP Sensor
    assert ipv4_ip_sensor.unique_id == "meraki_vlan_net1_1_ipv4_interface_ip"
    assert ipv4_ip_sensor.name == "VLAN 1 IPv4 Interface IP"
    assert ipv4_ip_sensor.native_value == "192.168.1.1"

    # Assertions for IPv4 Uplink Sensor
    assert ipv4_uplink_sensor.unique_id == "meraki_vlan_net1_1_ipv4_uplink"
    assert ipv4_uplink_sensor.name == "VLAN 1 IPv4 Uplink"
    assert ipv4_uplink_sensor.native_value == "Any"

    # Assertions for IPv6 Enabled Sensor
    assert ipv6_enabled_sensor.unique_id == "meraki_vlan_net1_1_ipv6_enabled"
    assert ipv6_enabled_sensor.name == "VLAN 1 IPv6 Enabled"
    assert ipv6_enabled_sensor.native_value is True

    # Assertions for IPv6 Interface IP Sensor
    assert ipv6_ip_sensor.unique_id == "meraki_vlan_net1_1_ipv6_interface_ip"
    assert ipv6_ip_sensor.name == "VLAN 1 IPv6 Interface IP"
    assert ipv6_ip_sensor.native_value == "2001:db8:1::/64"

    # Assertions for IPv6 Uplink Sensor
    assert ipv6_uplink_sensor.unique_id == "meraki_vlan_net1_1_ipv6_uplink"
    assert ipv6_uplink_sensor.name == "VLAN 1 IPv6 Uplink"
    assert ipv6_uplink_sensor.native_value == "WAN 1, WAN 2"
