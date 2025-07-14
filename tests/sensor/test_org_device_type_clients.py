"""Tests for the Meraki organization device type clients sensor."""
from unittest.mock import MagicMock

from homeassistant.core import HomeAssistant

from custom_components.meraki_ha.sensor.org_device_type_clients import (
    MerakiOrgDeviceTypeClientsSensor,
)


async def test_meraki_organization_device_type_clients_sensor(
    hass: HomeAssistant,
) -> None:
    """Test the Meraki organization device type clients sensor."""
    coordinator = MagicMock()
    coordinator.data = {
        "clients_on_ssids": 2,
        "clients_on_appliances": 3,
        "clients_on_wireless": 4,
    }
    sensor = MerakiOrgDeviceTypeClientsSensor(
        coordinator, "org_id", "org_name"
    )
    sensor._update_sensor_state()
    assert sensor.native_value == 9
