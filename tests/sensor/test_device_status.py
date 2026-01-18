"""Tests for the Meraki device status sensor."""

from unittest.mock import MagicMock

from homeassistant.core import HomeAssistant

from custom_components.meraki_ha.sensor.device.device_status import (
    MerakiDeviceStatusSensor,
)
from custom_components.meraki_ha.types import MerakiDevice


async def test_meraki_device_status_sensor_online(
    hass: HomeAssistant,
) -> None:
    """Test the Meraki device status sensor when the device is online."""
    coordinator = MagicMock()
    device = MerakiDevice(
        serial="Q234-ABCD-5678",
        name="Test Device",
        model="MR33",
        mac="00:11:22:33:44:55",
        status="online",
        product_type="wireless",
    )
    coordinator.data = {
        "devices": [device],
    }
    device_data = {
        "serial": "Q234-ABCD-5678",
        "name": "Test Device",
        "model": "MR33",
        "firmware": "wired-1.2.3",
        "productType": "wireless",
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
    device = MerakiDevice(
        serial="Q234-ABCD-5678",
        name="Test Device",
        model="MR33",
        mac="00:11:22:33:44:55",
        status="offline",
        product_type="wireless",
    )
    coordinator.data = {
        "devices": [device],
    }
    device_data = {
        "serial": "Q234-ABCD-5678",
        "name": "Test Device",
        "model": "MR33",
        "firmware": "wired-1.2.3",
        "productType": "wireless",
    }
    config_entry = MagicMock()
    config_entry.options = {}
    sensor = MerakiDeviceStatusSensor(coordinator, device_data, config_entry)
    sensor._update_sensor_data()
    assert sensor.native_value == "offline"
