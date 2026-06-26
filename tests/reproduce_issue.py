"""Reproduction test for MX LAN IP bug."""

from unittest.mock import MagicMock
import pytest
from custom_components.meraki_ha.sensor.device.network_settings import MerakiDeviceIPSensor
from custom_components.meraki_ha.core.models.device import MerakiDevice

def test_mx_lan_ip_fallback_bug():
    """Reproduce the bug where MX LAN IP falls back to WAN IP."""
    coordinator = MagicMock()
    config_entry = MagicMock()
    config_entry.options = {}

    # Mock MX device with no lan_ip but with uplinks having WAN IP
    mx_device = MerakiDevice(
        serial="MX123",
        name="MX Appliance",
        model="MX64",
        product_type="appliance",
        lan_ip=None,
        public_ip="8.8.8.8",
        uplinks=[
            {
                "interface": "wan1",
                "ip": "8.8.8.8",
                "publicIp": "8.8.8.8",
                "status": "active"
            }
        ]
    )

    coordinator.get_device.return_value = mx_device
    coordinator.last_update_success = True

    sensor = MerakiDeviceIPSensor(coordinator, mx_device, config_entry, "lanIp")

    # The bug is that it returns "8.8.8.8" instead of "Multiple (VLANs)" or None
    print(f"LAN IP Sensor value: {sensor.native_value}")
    assert sensor.native_value == "Multiple (VLANs)"

if __name__ == "__main__":
    test_mx_lan_ip_fallback_bug()
