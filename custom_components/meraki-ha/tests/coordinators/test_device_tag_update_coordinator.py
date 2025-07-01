import asyncio
from datetime import timedelta
from unittest.mock import AsyncMock, MagicMock, patch

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import UpdateFailed
from homeassistant.config_entries import ConfigEntry
from homeassistant.exceptions import ConfigEntryAuthFailed
from meraki.exceptions import APIError as MerakiSDKAPIError

from custom_components.meraki_ha.coordinators.device_tag_update_coordinator import DeviceTagUpdateCoordinator
from custom_components.meraki_ha.coordinators.base_coordinator import MerakiDataUpdateCoordinator # For parent type hint
from custom_components.meraki_ha.meraki_api import MerakiAPIClient # For mocking client
from custom_components.meraki_ha.coordinators.api_data_fetcher import MerakiApiDataFetcher # For mocking

import unittest

MOCK_HASS = MagicMock(spec=HomeAssistant)
MOCK_CONFIG_ENTRY = MagicMock(spec=ConfigEntry)
SAMPLE_ORG_ID = "org789"
SAMPLE_API_KEY = "test_api_key"

class TestDeviceTagUpdateCoordinator(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.hass = MOCK_HASS

        self.mock_meraki_client = MagicMock(spec=MerakiAPIClient)
        self.mock_meraki_client.org_id = SAMPLE_ORG_ID

        self.mock_main_coordinator = MagicMock(spec=MerakiDataUpdateCoordinator)
        self.mock_main_coordinator.meraki_client = self.mock_meraki_client # Ensure main_coordinator has the client
        self.mock_main_coordinator.config_entry = MOCK_CONFIG_ENTRY # Main coordinator should have config_entry

        # Patch MerakiApiDataFetcher that DeviceTagUpdateCoordinator tries to instantiate
        self.patcher_api_fetcher = patch('custom_components.meraki_ha.coordinators.device_tag_update_coordinator.MerakiApiDataFetcher', spec=MerakiApiDataFetcher)
        self.mock_api_fetcher_class = self.patcher_api_fetcher.start()
        self.mock_api_fetcher_instance = self.mock_api_fetcher_class.return_value
        self.mock_api_fetcher_instance.async_update_device_tags = AsyncMock()

        self.coordinator = DeviceTagUpdateCoordinator(
            hass=self.hass,
            api_key=SAMPLE_API_KEY, # Though not directly used by coordinator anymore, it's in signature
            scan_interval=timedelta(seconds=600),
            org_id=SAMPLE_ORG_ID,
            main_coordinator=self.mock_main_coordinator
        )

        self.patcher_logger = patch('custom_components.meraki_ha.coordinators.device_tag_update_coordinator._LOGGER', new_callable=MagicMock)
        self.mock_logger = self.patcher_logger.start()

    def tearDown(self):
        self.patcher_api_fetcher.stop()
        self.patcher_logger.stop()

    async def test_initialization(self):
        """Test coordinator initializes correctly."""
        self.assertEqual(self.coordinator.org_id, SAMPLE_ORG_ID)
        self.mock_api_fetcher_class.assert_called_once_with(meraki_client=self.mock_main_coordinator.meraki_client)

    async def test_async_update_data_placeholder(self):
        """Test the placeholder _async_update_data method."""
        result = await self.coordinator._async_update_data()
        self.assertEqual(result, {})
        self.mock_logger.debug.assert_any_call(
            "DeviceTagUpdateCoordinator._async_update_data called, but it's a placeholder. Tag updates are on-demand via async_update_device_tags."
        )

    async def test_async_update_device_tags_success(self):
        """Test successful device tag update."""
        serial = "Q234-ABCD-0001"
        tags = ["tag1", "tag2"]
        self.mock_api_fetcher_instance.async_update_device_tags.return_value = True

        self.coordinator.async_request_refresh = AsyncMock() # Mock this method of DataUpdateCoordinator

        await self.coordinator.async_update_device_tags(serial, tags)

        self.mock_api_fetcher_instance.async_update_device_tags.assert_called_once_with(serial, tags)
        self.mock_logger.info.assert_called_once_with(
            "Successfully updated tags for device %s. Requesting refresh.", serial
        )
        self.coordinator.async_request_refresh.assert_called_once()

    async def test_async_update_device_tags_api_fetcher_reports_failure(self):
        """Test tag update when api_fetcher returns False."""
        serial = "Q234-ABCD-0002"
        tags = ["tag_fail"]
        self.mock_api_fetcher_instance.async_update_device_tags.return_value = False

        with self.assertRaises(UpdateFailed) as context:
            await self.coordinator.async_update_device_tags(serial, tags)

        self.assertTrue(f"Tag update for device {serial} failed (API fetcher indicated no success)" in str(context.exception))
        self.mock_logger.warning.assert_called_once_with(
            "Tag update for device %s reported as unsuccessful by API fetcher (returned False).", serial
        )

    async def test_async_update_device_tags_auth_error(self):
        """Test ConfigEntryAuthFailed during tag update."""
        serial = "Q234-ABCD-0003"
        tags = ["tag_auth"]
        self.mock_api_fetcher_instance.async_update_device_tags.side_effect = ConfigEntryAuthFailed("Auth error")

        with self.assertRaises(ConfigEntryAuthFailed):
            await self.coordinator.async_update_device_tags(serial, tags)
        self.mock_logger.error.assert_called_once_with(
            "Authentication failed while updating tags for device %s.", serial
        )

    async def test_async_update_device_tags_meraki_api_error(self):
        """Test MerakiApiError during tag update."""
        serial = "Q234-ABCD-0004"
        tags = ["tag_api_err"]
        # Simulate MerakiSDKAPIError as MerakiApiError is a custom base likely wrapping it or similar
        simulated_sdk_error = MerakiSDKAPIError(MagicMock(status=500), "SDK API Error")
        self.mock_api_fetcher_instance.async_update_device_tags.side_effect = MerakiApiError("Simulated API Error", original_exception=simulated_sdk_error)


        with self.assertRaises(UpdateFailed) as context:
            await self.coordinator.async_update_device_tags(serial, tags)

        self.assertTrue(f"API error updating tags for device {serial}" in str(context.exception))

    async def test_async_update_device_tags_unexpected_exception(self):
        """Test generic Exception during tag update."""
        serial = "Q234-ABCD-0005"
        tags = ["tag_generic_err"]
        self.mock_api_fetcher_instance.async_update_device_tags.side_effect = Exception("Generic error")

        with self.assertRaises(UpdateFailed) as context:
            await self.coordinator.async_update_device_tags(serial, tags)

        self.assertTrue(f"Unexpected error updating tags for device {serial}: Generic error" in str(context.exception))
        self.mock_logger.exception.assert_called_once_with(
            "Unexpected error updating tags for device %s: %s", serial, Exception("Generic error")
        )

if __name__ == '__main__':
    unittest.main()
