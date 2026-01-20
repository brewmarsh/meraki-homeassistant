
"""Tests for the Meraki WAN1 connectivity sensor."""

from unittest.mock import MagicMock

from homeassistant.core import HomeAssistant

from custom_components.meraki_ha.sensor.device.meraki_wan1_connectivity import (
    MerakiWAN1ConnectivitySensor,
)
from custom_components.meraki_ha.types import MerakiDevice
from tests.const import MOCK_DEVICE


async def test_meraki_wan1_connectivity_sensor(
    hass: HomeAssistant,
) -> None:
    """Test the Meraki WAN1 connectivity sensor."""
    coordinator = MagicMock()
    online_device = MerakiDevice.from_dict({**MOCK_DEVICE.__dict__, "status": "online", "wan1Ip": "1.2.3.4"})
    coordinator.get_device.return_value = online_device
    config_entry = MagicMock()
    config_entry.options = {}
    sensor = MerakiWAN1ConnectivitySensor(coordinator, online_device, config_entry)
    sensor._update_state()
    assert sensor.native_value == "Connected"
    assert sensor.extra_state_attributes["wan1_ip_address"] == "1.2.3.4"
