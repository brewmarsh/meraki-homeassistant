"""Tests for the Meraki integration."""
import asyncio
from unittest.mock import MagicMock, patch

from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_API_KEY

from custom_components.meraki_ha.const import DOMAIN
from custom_components.meraki_ha import async_setup_entry


async def test_async_setup_entry(
    hass: HomeAssistant,
) -> None:
    """Test the async_setup_entry function."""
    config_entry = MagicMock()
    config_entry.domain = DOMAIN
    config_entry.data = {
        "meraki_api_key": "test_api_key",
        "meraki_org_id": "org_id",
    }
    config_entry.options = {
        "scan_interval": 300,
        "device_name_format": "omitted",
    }
    with patch(
        "custom_components.meraki_ha.MerakiDataUpdateCoordinator"
    ) as mock_coordinator:
        future = asyncio.Future()
        future.set_result(None)
        mock_coordinator.return_value.async_config_entry_first_refresh.return_value = future
        mock_coordinator.return_value.async_register_organization_device = MagicMock(
            return_value=future
        )
        async def async_forward_entry_setups(entry, domains):
            return True

        hass.config_entries.async_forward_entry_setups = async_forward_entry_setups
        config_entry.title = "test_title"
        with patch(
            "custom_components.meraki_ha.async_unload_entry"
        ) as mock_unload:
            future = asyncio.Future()
            future.set_result(True)
            mock_unload.return_value = future
            result = await async_setup_entry(hass, config_entry)
            assert result is True
