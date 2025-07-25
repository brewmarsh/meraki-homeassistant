"""Tests for the Meraki organization clients sensor."""

from unittest.mock import MagicMock

from homeassistant.core import HomeAssistant

from custom_components.meraki_ha.sensor.org_clients import (
    MerakiOrganizationSSIDClientsSensor,
    MerakiOrganizationWirelessClientsSensor,
    MerakiOrganizationApplianceClientsSensor,
)


async def test_meraki_organization_ssid_clients_sensor(
    hass: HomeAssistant,
) -> None:
    """Test the Meraki organization SSID clients sensor."""
    coordinator = MagicMock()
    coordinator.data = {
        "clients_on_ssids": 2,
    }
    sensor = MerakiOrganizationSSIDClientsSensor(coordinator, "org_id", "org_name")
    sensor._update_internal_state()
    assert sensor.native_value == 2


async def test_meraki_organization_wireless_clients_sensor(
    hass: HomeAssistant,
) -> None:
    """Test the Meraki organization wireless clients sensor."""
    coordinator = MagicMock()
    coordinator.data = {
        "clients_on_wireless": 3,
    }
    sensor = MerakiOrganizationWirelessClientsSensor(coordinator, "org_id", "org_name")
    sensor._update_internal_state()
    assert sensor.native_value == 3


async def test_meraki_organization_appliance_clients_sensor(
    hass: HomeAssistant,
) -> None:
    """Test the Meraki organization appliance clients sensor."""
    coordinator = MagicMock()
    coordinator.data = {
        "clients_on_appliances": 4,
    }
    sensor = MerakiOrganizationApplianceClientsSensor(coordinator, "org_id", "org_name")
    sensor._update_internal_state()
    assert sensor.native_value == 4
