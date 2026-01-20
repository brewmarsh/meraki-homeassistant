
"""Tests for the Meraki device status sensor."""

from unittest.mock import MagicMock

from homeassistant.core import HomeAssistant

from custom_components.meraki_ha.sensor.device.device_status import (
    MerakiDeviceStatusSensor,
)
from custom_components.meraki_ha.types import MerakiDevice
from tests.const import MOCK_DEVICE_INIT


async def test_meraki_device_status_sensor_online(
    hass: HomeAssistant,
) -> None:
    """Test the Meraki device status sensor when the device is online."""
    coordinator = MagicMock()
    online_device = MerakiDevice.from_dict({**MOCK_DEVICE_INIT, "status": "online"})
    coordinator.get_device.return_value = online_device
    config_entry = MagicMock()
    config_entry.options = {}
    sensor = MerakiDeviceStatusSensor(coordinator, online_device, config_entry)
    sensor._update_sensor_data()
    assert sensor.native_value == "online"


async def test_meraki_device_status_sensor_offline(
    hass: HomeAssistant,
) -> None:
    """Test the Meraki device status sensor when the device is offline."""
    coordinator = MagicMock()
    offline_device = MerakiDevice.from_dict({**MOCK_DEVICE_INIT, "status": "offline"})
    coordinator.get_device.return_value = offline_device
    config_entry = MagicMock()
    config_entry.options = {}
    sensor = MerakiDeviceStatusSensor(coordinator, offline_device, config_entry)
    sensor._update_sensor_data()
    assert sensor.native_value == "offline"
