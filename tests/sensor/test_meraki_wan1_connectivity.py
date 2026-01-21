"""Tests for the Meraki WAN1 connectivity sensor."""

from unittest.mock import MagicMock

from homeassistant.core import HomeAssistant

from custom_components.meraki_ha.sensor.device.meraki_wan1_connectivity import (
    MerakiWAN1ConnectivitySensor,
)
<<<<<<< HEAD
=======
from custom_components.meraki_ha.types import MerakiDevice
from tests.const import MOCK_DEVICE
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)


async def test_meraki_wan1_connectivity_sensor(
    hass: HomeAssistant,
) -> None:
    """Test the Meraki WAN1 connectivity sensor."""
    coordinator = MagicMock()
<<<<<<< HEAD
    coordinator.data = {
        "devices": [
            {
                "serial": "Q234-ABCD-5678",
                "wan1Ip": "1.2.3.4",
                "status": "online",
            }
        ]
    }
    device_data = {
        "serial": "Q234-ABCD-5678",
    }
    config_entry = MagicMock()
    config_entry.options = {}
    sensor = MerakiWAN1ConnectivitySensor(coordinator, device_data, config_entry)
    sensor._update_state()
    assert sensor.native_value == "Connected"
=======
    online_device = MerakiDevice.from_dict(
        {**MOCK_DEVICE.__dict__, "status": "online", "wan1Ip": "1.2.3.4"}
    )
    coordinator.get_device.return_value = online_device
    config_entry = MagicMock()
    config_entry.options = {}
    sensor = MerakiWAN1ConnectivitySensor(coordinator, online_device, config_entry)
    sensor.hass = MagicMock()
    sensor.async_write_ha_state = MagicMock()
    sensor._handle_coordinator_update()
    assert sensor.native_value == "Connected"
    assert sensor.extra_state_attributes["wan1_ip_address"] == "1.2.3.4"
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
