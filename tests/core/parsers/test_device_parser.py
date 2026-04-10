"""Unit tests for device parser."""

from custom_components.meraki_ha.core.models.device import MerakiDevice
from custom_components.meraki_ha.core.parsers.devices import parse_device_data


def test_parse_device_data_normalization():
    """Test that device status is normalized to lowercase."""
    device = MerakiDevice(serial="TEST_SERIAL", name="Test Device")
    devices = [device]

    # Payload with uppercase status
    device_statuses = [
        {"serial": "TEST_SERIAL", "status": "Online", "lanIp": "192.168.1.1"}
    ]

    parse_device_data(devices, device_statuses)

    assert device.status == "online"
    assert device.lan_ip == "192.168.1.1"
    assert device.is_online is True


def test_parse_device_data_no_status():
    """Test that device handles missing status gracefully."""
    device = MerakiDevice(serial="TEST_SERIAL", name="Test Device")
    devices = [device]

    # Payload without status
    device_statuses = [{"serial": "TEST_SERIAL", "lanIp": "192.168.1.1"}]

    parse_device_data(devices, device_statuses)

    assert device.status is None
    assert device.lan_ip == "192.168.1.1"
    assert device.is_online is False
