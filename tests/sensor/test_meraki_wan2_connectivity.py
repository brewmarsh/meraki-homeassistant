"""Tests for the Meraki WAN2 connectivity sensor."""

from unittest.mock import MagicMock

from homeassistant.core import HomeAssistant

from custom_components.meraki_ha.sensor.device.meraki_wan2_connectivity import (
    MerakiWAN2ConnectivitySensor,
)
<<<<<<< HEAD
=======
from custom_components.meraki_ha.types import MerakiDevice
from tests.const import MOCK_DEVICE
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)


async def test_meraki_wan2_connectivity_sensor(
    hass: HomeAssistant,
) -> None:
    """Test the Meraki WAN2 connectivity sensor."""
    coordinator = MagicMock()
<<<<<<< HEAD
    coordinator.data = {
        "devices": [
            {
                "serial": "Q234-ABCD-5678",
                "wan2Ip": "1.2.3.4",
                "status": "online",
            }
        ]
    }
    device_data = {
        "serial": "Q234-ABCD-5678",
    }
    config_entry = MagicMock()
    config_entry.options = {}
    sensor = MerakiWAN2ConnectivitySensor(coordinator, device_data, config_entry)
    sensor._update_state()
    assert sensor.native_value == "Connected"
=======
    online_device = MerakiDevice.from_dict(
        {**MOCK_DEVICE.__dict__, "status": "online", "wan2Ip": "1.2.3.4"}
    )
    coordinator.get_device.return_value = online_device
    config_entry = MagicMock()
    config_entry.options = {}
    sensor = MerakiWAN2ConnectivitySensor(coordinator, online_device, config_entry)
    sensor.hass = MagicMock()
    sensor.async_write_ha_state = MagicMock()
    sensor._handle_coordinator_update()
    assert sensor.native_value == "Connected"
    assert sensor.extra_state_attributes["wan2_ip_address"] == "1.2.3.4"
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
