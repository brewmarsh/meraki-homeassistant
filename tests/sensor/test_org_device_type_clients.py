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
    sensor = MerakiOrganizationDeviceTypeClientsSensor(
        coordinator, MagicMock(), "wireless"
    )
    assert sensor.native_value == 2
