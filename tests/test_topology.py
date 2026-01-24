"""Test the topology of the Meraki integration."""

from unittest.mock import MagicMock

from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr

from . import async_get_config_entry
from .const import MERAKI_TEST_NETWORK_ID, MERAKI_TEST_ORG_ID


async def test_network_device_creation(
    hass: HomeAssistant,
    mock_meraki_client: MagicMock,
    device_registry: dr.DeviceRegistry,
) -> None:
    """Test that a network device is created."""
    mock_dashboard = mock_meraki_client.return_value
    mock_dashboard.organizations.getOrganizations.return_value = [
        {"id": MERAKI_TEST_ORG_ID, "name": "Test Organization"}
    ]
    mock_dashboard.organizations.getOrganizationNetworks.return_value = [
        {"id": MERAKI_TEST_NETWORK_ID, "name": "Site A", "productTypes": ["appliance"]}
    ]
    mock_dashboard.organizations.getOrganizationDevices.return_value = []

    config_entry = await async_get_config_entry(hass)
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    device = device_registry.async_get_device(
        identifiers={("meraki_ha", MERAKI_TEST_NETWORK_ID)}
    )
    assert device is not None
    assert device.name == "Site A"
