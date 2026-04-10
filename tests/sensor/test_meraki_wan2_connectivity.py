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
    # Align WAN Connectivity Mocks: Use to_dict() and include structured uplinks
    online_device_dict = MOCK_DEVICE.to_dict()
    online_device_dict.update(
        {
            "status": "online",
            "wan2Ip": "1.2.3.4",
            "uplinks": [{"interface": "wan2", "status": "active"}],
        }
    )
    online_device = MerakiDevice.from_dict(online_device_dict)

    coordinator.get_device.return_value = online_device
    config_entry = MagicMock()
    config_entry.options = {}
    sensor = MerakiWAN2ConnectivitySensor(coordinator, online_device, config_entry)
    sensor.hass = MagicMock()
    object.__setattr__(sensor, "async_write_ha_state", MagicMock())
    sensor._handle_coordinator_update()
    assert sensor.native_value == "Connected"
    assert sensor.extra_state_attributes is not None
    assert sensor.extra_state_attributes["wan2_ip_address"] == "1.2.3.4"
