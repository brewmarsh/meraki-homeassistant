"""Tests for the Meraki integration."""

# import asyncio
# from unittest.mock import AsyncMock, MagicMock, patch

# import pytest
# from homeassistant.core import HomeAssistant

# from custom_components.meraki_ha.const import DOMAIN
# from custom_components.meraki_ha import async_setup_entry, async_setup


# @pytest.mark.parametrize("skip_lingering_timers", [True])
# async def test_async_setup_entry(
#     hass: HomeAssistant, skip_lingering_timers: bool
# ) -> None:
#     """Test the async_setup_entry function."""
#     with patch("homeassistant.components.analytics.async_setup", return_value=True):
#         hass.http = AsyncMock()
#         await async_setup(hass, {})
#         config_entry = MagicMock()
#         config_entry.entry_id = "test_entry"
#         config_entry.domain = DOMAIN
#         config_entry.data = {
#             "meraki_api_key": "test_api_key",
#             "meraki_org_id": "org_id",
#         }
#         config_entry.options = {
#             "scan_interval": 300,
#             "device_name_format": "omitted",
#         }
#         with (
#             patch(
#                 "custom_components.meraki_ha.MerakiDataUpdateCoordinator"
#             ) as mock_coordinator,
#             patch(
#                 "custom_components.meraki_ha.async_register_webhook"
#             ) as mock_register_webhook,
#         ):
#             future: asyncio.Future = asyncio.Future()
#             future.set_result(None)
#             mock_coordinator.return_value.async_refresh = AsyncMock()
#             (
#                 mock_coordinator.return_value.async_config_entry_first_refresh
#             ).return_value = future
#             (
#                 mock_coordinator.return_value.async_register_organization_device
#             ) = MagicMock(return_value=future)

#             async def async_forward_entry_setups(entry, domains):
#                 return True

#             hass.config_entries.async_forward_entry_setups = async_forward_entry_setups
#             hass.config_entries.async_update_entry = MagicMock(return_value=True)
#             hass.config_entries._entries = {config_entry.entry_id: config_entry}
#             config_entry.title = "test_title"
#             with patch("custom_components.meraki_ha.async_unload_entry") as mock_unload:
#                 future2: asyncio.Future = asyncio.Future()
#                 future2.set_result(True)
#                 mock_unload.return_value = future2
#                 result = await async_setup_entry(hass, config_entry)
#                 assert result is True
#                 mock_register_webhook.assert_called_once()
