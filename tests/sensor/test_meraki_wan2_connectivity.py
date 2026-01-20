
"""Tests for the Meraki WAN2 connectivity sensor."""

from unittest.mock import MagicMock

from homeassistant.core import HomeAssistant

from custom_components.meraki_ha.sensor.device.meraki_wan2_connectivity import (
    MerakiWAN2ConnectivitySensor,
)
from custom_components.meraki_ha.types import MerakiDevice
from tests.const import MOCK_DEVICE


async def test_meraki_wan2_connectivity_sensor(
    hass: HomeAssistant,
) -> None:
    """Test the Meraki WAN2 connectivity sensor."""
    coordinator = MagicMock()
    online_device = MerakiDevice.from_dict({**MOCK_DEVICE.__dict__, "status": "online", "wan2Ip": "1.2.3.4"})
    coordinator.get_device.return_value = online_device
    config_entry = MagicMock()
    config_entry.options = {}
    sensor = MerakiWAN2ConnectivitySensor(coordinator, online_device, config_entry)
    sensor._update_state()
    assert sensor.native_value == "Connected"
    assert sensor.extra_state_attributes["wan2_ip_address"] == "1.2.3.4"
