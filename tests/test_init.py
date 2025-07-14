"""Tests for the Meraki integration."""
from unittest.mock import patch

from homeassistant.config_entries import ConfigEntryState
from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.meraki_ha.const import DOMAIN


async def test_setup_entry(hass: HomeAssistant) -> None:
    """Test setup entry."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={"meraki_api_key": "test-api-key", "meraki_org_id": "test-org-id"},
    )
    entry.add_to_hass(hass)

    with patch(
        "custom_components.meraki_ha.MerakiDataUpdateCoordinator.async_config_entry_first_refresh"
    ), patch(
        "custom_components.meraki_ha.SSIDDeviceCoordinator.async_config_entry_first_refresh"
    ):
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    assert entry.state is ConfigEntryState.LOADED


async def test_unload_entry(hass: HomeAssistant) -> None:
    """Test unload entry."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={"meraki_api_key": "test-api-key", "meraki_org_id": "test-org-id"},
    )
    entry.add_to_hass(hass)

    with patch(
        "custom_components.meraki_ha.MerakiDataUpdateCoordinator.async_config_entry_first_refresh"
    ), patch(
        "custom_components.meraki_ha.SSIDDeviceCoordinator.async_config_entry_first_refresh"
    ):
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    assert await hass.config_entries.async_unload(entry.entry_id)
    await hass.async_block_till_done()

    assert entry.state is ConfigEntryState.NOT_LOADED
