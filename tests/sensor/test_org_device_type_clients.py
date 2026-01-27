"""Tests for the Meraki organization device type clients sensor."""

from unittest.mock import MagicMock

from homeassistant.core import HomeAssistant

from custom_components.meraki_ha.sensor.org.org_device_type_clients import (
    MerakiOrganizationDeviceTypeClientsSensor,
)


async def test_meraki_organization_device_type_clients_sensor(
    hass: HomeAssistant,
) -> None:
    """Test the Meraki organization device type clients sensor."""
    coordinator = MagicMock()
    coordinator.data = {
        "clients": [
            {"deviceType": "wireless"},
            {"deviceType": "wireless"},
            {"deviceType": "appliance"},
        ]
    }
    config_entry = MagicMock()
    config_entry.options = {}
    sensor = MerakiOrganizationDeviceTypeClientsSensor(
        coordinator, config_entry, "wireless"
    )
    sensor.hass = MagicMock()
    sensor.async_write_ha_state = MagicMock()
    sensor._handle_coordinator_update()
    assert sensor.native_value == 2
