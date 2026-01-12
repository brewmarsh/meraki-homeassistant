"""Tests for the Meraki device status sensor."""

from unittest.mock import MagicMock

from homeassistant.core import HomeAssistant

from custom_components.meraki_ha.sensor.device.device_status import (
    MerakiDeviceStatusSensor,
)


async def test_meraki_device_status_sensor_online(
    hass: HomeAssistant,
) -> None:
    """Test the Meraki device status sensor when the device is online."""
    coordinator = MagicMock()
    device = {
        "serial": "Q234-ABCD-5678",
        "status": "online",
    }
    coordinator.data = {"devices": [device]}
    # Set up the O(1) lookup table used by the optimized _get_current_device_data
    coordinator.devices_by_serial = {"Q234-ABCD-5678": device}
    device_data = {
        "serial": "Q234-ABCD-5678",
    }
    config_entry = MagicMock()
    config_entry.options = {}
    sensor = MerakiDeviceStatusSensor(coordinator, device_data, config_entry)
    sensor._update_sensor_data()
    assert sensor.native_value == "online"


async def test_meraki_device_status_sensor_offline(
    hass: HomeAssistant,
) -> None:
    """Test the Meraki device status sensor when the device is offline."""
    coordinator = MagicMock()
    device = {
        "serial": "Q234-ABCD-5678",
        "status": "offline",
    }
    coordinator.data = {"devices": [device]}
    # Set up the O(1) lookup table used by the optimized _get_current_device_data
    coordinator.devices_by_serial = {"Q234-ABCD-5678": device}
    device_data = {
        "serial": "Q234-ABCD-5678",
    }
    config_entry = MagicMock()
    config_entry.options = {}
    sensor = MerakiDeviceStatusSensor(coordinator, device_data, config_entry)
    sensor._update_sensor_data()
    assert sensor.native_value == "offline"
