"""Tests for IPv6 truncation and static naming in Meraki Network Settings Sensors."""

from unittest.mock import MagicMock

import pytest

from custom_components.meraki_ha.core.models.device import MerakiDevice
from custom_components.meraki_ha.sensor.device.network_settings import (
    MerakiDeviceDNSSensor,
    MerakiDeviceGatewaySensor,
    MerakiDeviceIPSensor,
)


@pytest.fixture
def mock_coordinator():
    """Fixture for a mocked Meraki coordinator."""
    coordinator = MagicMock()
    coordinator.data = {"devices_by_serial": {}}

    def get_device(serial):
        return coordinator.data["devices_by_serial"].get(serial)

    coordinator.get_device.side_effect = get_device
    return coordinator


def test_ipv6_truncation_logic(mock_coordinator):
    """Test that long IPv6 addresses are truncated correctly."""
    config_entry = MagicMock()
    config_entry.options = {}

    serial = "Q2XX-XXXX-XXXX"
    long_ipv6 = "2601:246:102:df00:fe5f:2a53:fe5f:2a53"
    short_ipv6 = "2001:db8::1"
    ipv4 = "192.168.1.1"

    device_data = MerakiDevice(
        serial=serial,
        name="Test Device",
        model="MR56",
        mac="00:11:22:33:44:55",
        status="online",
        public_ip=long_ipv6,
        lan_ip=ipv4,
    )
    mock_coordinator.data["devices_by_serial"][serial] = device_data

    # 1. Test Long IPv6 (Public IP)
    sensor = MerakiDeviceIPSensor(
        mock_coordinator, device_data, config_entry, "publicIp"
    )
    # Expected: 2601:246...fe5f:2a53
    assert sensor.native_value == "2601:246...fe5f:2a53"
    assert sensor.extra_state_attributes["full_ip_address"] == long_ipv6
    assert sensor.name == "PUBLIC IP"

    # 2. Test IPv4 (LAN IP)
    sensor_lan = MerakiDeviceIPSensor(
        mock_coordinator, device_data, config_entry, "lanIp"
    )
    assert sensor_lan.native_value == ipv4
    assert sensor_lan.extra_state_attributes["full_ip_address"] == ipv4
    assert sensor_lan.name == "LAN IP"

    # 3. Test Short IPv6
    device_data.public_ip = short_ipv6
    sensor_short = MerakiDeviceIPSensor(
        mock_coordinator, device_data, config_entry, "publicIp"
    )
    assert sensor_short.native_value == short_ipv6
    assert sensor_short.extra_state_attributes["full_ip_address"] == short_ipv6


def test_gateway_and_dns_truncation(mock_coordinator):
    """Test truncation for Gateway and DNS sensors."""
    config_entry = MagicMock()
    config_entry.options = {}

    serial = "Q2YY-YYYY-YYYY"
    long_ipv6_gw = "2601:246:102:df00:0000:0000:0000:0001"
    dns_list = ["2601:246:102:df00:fe5f:2a53:fe5f:2a53", "8.8.8.8"]

    device_data = MerakiDevice(
        serial=serial,
        name="Test Device 2",
        model="MX68",
        mac="00:11:22:33:44:66",
        status="online",
        uplinks=[
            {
                "interface": "wan1",
                "ip": "1.2.3.4",
                "gateway": long_ipv6_gw,
                "dns": dns_list,
            }
        ],
    )
    mock_coordinator.data["devices_by_serial"][serial] = device_data

    # Gateway Test
    gw_sensor = MerakiDeviceGatewaySensor(
        mock_coordinator, device_data, config_entry, "wan1"
    )
    assert gw_sensor.native_value == "2601:246...0000:0001"
    assert gw_sensor.extra_state_attributes["full_gateway_address"] == long_ipv6_gw
    assert gw_sensor.name == "WAN1 Gateway"

    # DNS Test
    dns_sensor = MerakiDeviceDNSSensor(
        mock_coordinator, device_data, config_entry, "wan1"
    )
    # Expected: "2601:246...fe5f:2a53, 8.8.8.8"
    assert dns_sensor.native_value == "2601:246...fe5f:2a53, 8.8.8.8"
    assert (
        dns_sensor.extra_state_attributes["full_dns_servers"]
        == "2601:246:102:df00:fe5f:2a53:fe5f:2a53, 8.8.8.8"
    )
    assert dns_sensor.name == "WAN1 DNS"
