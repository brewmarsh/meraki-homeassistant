import asyncio
from datetime import timedelta
from unittest.mock import AsyncMock, MagicMock, patch

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import UpdateFailed
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers import device_registry as dr # For mocking device_registry

from custom_components.meraki_ha.coordinators.ssid_device_coordinator import SSIDDeviceCoordinator
from custom_components.meraki_ha.coordinators.api_data_fetcher import MerakiApiDataFetcher # For type hint
from custom_components.meraki_ha.meraki_api import MerakiAPIClient # For mocking
from custom_components.meraki_ha.const import DOMAIN

import unittest

MOCK_HASS = MagicMock(spec=HomeAssistant)
MOCK_CONFIG_ENTRY_ID = "test_config_entry_id"

# Mock Config Entry with options
MOCK_CONFIG_ENTRY = MagicMock(spec=ConfigEntry)
MOCK_CONFIG_ENTRY.entry_id = MOCK_CONFIG_ENTRY_ID
MOCK_CONFIG_ENTRY.options = {"device_name_format": "omitted"}


class TestSSIDDeviceCoordinator(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.hass = MOCK_HASS
        self.config_entry = MOCK_CONFIG_ENTRY

        self.mock_api_data_fetcher = MagicMock(spec=MerakiApiDataFetcher)
        self.mock_meraki_client = MagicMock(spec=MerakiAPIClient)

        # Setup hass.data structure
        self.hass.data = {
            DOMAIN: {
                self.config_entry.entry_id: {
                    "client": self.mock_meraki_client
                }
            }
        }

        self.update_interval = timedelta(seconds=300)

        self.coordinator = SSIDDeviceCoordinator(
            hass=self.hass,
            config_entry=self.config_entry,
            api_data_fetcher=self.mock_api_data_fetcher,
            update_interval=self.update_interval
        )

        self.patcher_logger = patch('custom_components.meraki_ha.coordinators.ssid_device_coordinator._LOGGER', new_callable=MagicMock)
        self.mock_logger = self.patcher_logger.start()

        self.patcher_device_registry = patch('custom_components.meraki_ha.coordinators.ssid_device_coordinator.dr.async_get', new_callable=MagicMock)
        self.mock_device_registry_get = self.patcher_device_registry.start()
        self.mock_device_registry_instance = self.mock_device_registry_get.return_value
        self.mock_device_registry_instance.async_get_or_create = MagicMock()


    def tearDown(self):
        self.patcher_logger.stop()
        self.patcher_device_registry.stop()
        self.hass.data = {} # Clear hass.data

    async def test_initialization(self):
        """Test coordinator initializes correctly."""
        self.assertEqual(self.coordinator.config_entry, self.config_entry)
        self.assertEqual(self.coordinator.api_data_fetcher, self.mock_api_data_fetcher)

    async def test_async_update_data_no_fetcher_data(self):
        """Test update when api_data_fetcher has no data or failed."""
        self.mock_api_data_fetcher.last_update_success = False
        self.mock_api_data_fetcher.data = None

        with self.assertRaises(UpdateFailed) as context:
            await self.coordinator._async_update_data()
        self.assertTrue("Main API data fetcher has no data available for SSIDs" in str(context.exception))

        # Scenario: fetcher succeeded but data is None
        self.mock_api_data_fetcher.last_update_success = True
        self.mock_api_data_fetcher.data = None
        with self.assertRaises(UpdateFailed) as context:
            await self.coordinator._async_update_data()
        self.assertTrue("Main API data fetcher has no data available for SSIDs" in str(context.exception))


    async def test_async_update_data_no_ssids_from_fetcher(self):
        """Test update when api_data_fetcher returns no SSIDs."""
        self.mock_api_data_fetcher.last_update_success = True
        self.mock_api_data_fetcher.data = {"ssids": []} # No SSIDs

        result = await self.coordinator._async_update_data()
        self.assertEqual(result, {})
        self.mock_logger.info.assert_any_call("SSIDDeviceCoordinator: No enabled SSIDs found after filtering. No SSID devices to update/create.")


    async def test_async_update_data_one_enabled_ssid_no_clients(self):
        """Test update with one enabled SSID that has no clients."""
        ssid_info = {"networkId": "N_1", "number": 0, "name": "Test SSID", "enabled": True}
        self.mock_api_data_fetcher.last_update_success = True
        self.mock_api_data_fetcher.data = {"ssids": [ssid_info]}

        # Mock API calls made by _async_update_data
        self.mock_meraki_client.wireless.getNetworkWirelessSsid = AsyncMock(return_value=ssid_info) # Detail fetch
        self.mock_meraki_client.networks.getNetworkClients = AsyncMock(return_value=[]) # No clients on network

        result = await self.coordinator._async_update_data()

        expected_unique_id = f"{ssid_info['networkId']}_{ssid_info['number']}"
        self.assertIn(expected_unique_id, result)
        self.assertEqual(result[expected_unique_id]["client_count"], 0)
        self.assertEqual(result[expected_unique_id]["name"], "Test SSID")

        self.mock_device_registry_instance.async_get_or_create.assert_called_once()
        args, kwargs = self.mock_device_registry_instance.async_get_or_create.call_args
        self.assertEqual(kwargs["config_entry_id"], self.config_entry.entry_id)
        self.assertEqual(kwargs["identifiers"], {(DOMAIN, expected_unique_id)})
        self.assertEqual(kwargs["name"], "Test SSID") # Assuming "omitted" format

    async def test_async_update_data_one_enabled_ssid_with_clients(self):
        """Test update with one enabled SSID that has clients."""
        ssid_name = "CorpNet"
        ssid_info_summary = {"networkId": "N_2", "number": 1, "name": ssid_name, "enabled": True}
        ssid_info_detail = {**ssid_info_summary, "authMode": "psk"} # Detail fetch adds more

        self.mock_api_data_fetcher.last_update_success = True
        self.mock_api_data_fetcher.data = {"ssids": [ssid_info_summary]}

        clients_on_network = [
            {"mac": "c1", "ssid": ssid_name}, # Matches
            {"mac": "c2", "ssid": "OtherSSID"},
            {"mac": "c3", "ssid": ssid_name}, # Matches
        ]
        self.mock_meraki_client.wireless.getNetworkWirelessSsid = AsyncMock(return_value=ssid_info_detail)
        self.mock_meraki_client.networks.getNetworkClients = AsyncMock(return_value=clients_on_network)

        result = await self.coordinator._async_update_data()

        expected_unique_id = f"{ssid_info_summary['networkId']}_{ssid_info_summary['number']}"
        self.assertIn(expected_unique_id, result)
        self.assertEqual(result[expected_unique_id]["client_count"], 2) # Two clients match by SSID name
        self.assertEqual(result[expected_unique_id]["authMode"], "psk")


    async def test_async_update_data_disabled_ssid_not_processed(self):
        """Test that disabled SSIDs are filtered out and not processed."""
        ssid_info_disabled = {"networkId": "N_3", "number": 0, "name": "Disabled SSID", "enabled": False}
        self.mock_api_data_fetcher.last_update_success = True
        self.mock_api_data_fetcher.data = {"ssids": [ssid_info_disabled]}

        result = await self.coordinator._async_update_data()
        self.assertEqual(result, {}) # No enabled SSIDs, so map should be empty
        # Ensure no API calls were made for the disabled SSID
        self.mock_meraki_client.wireless.getNetworkWirelessSsid.assert_not_called()
        self.mock_meraki_client.networks.getNetworkClients.assert_not_called()
        self.mock_device_registry_instance.async_get_or_create.assert_not_called()

    async def test_device_name_formatting(self):
        """Test that the device name is formatted correctly based on the device_name_format option."""
        ssid_info = {"networkId": "N_4", "number": 0, "name": "Formatting Test", "enabled": True}
        self.mock_api_data_fetcher.last_update_success = True
        self.mock_api_data_fetcher.data = {"ssids": [ssid_info]}
        self.mock_meraki_client.wireless.getNetworkWirelessSsid = AsyncMock(return_value=ssid_info)
        self.mock_meraki_client.networks.getNetworkClients = AsyncMock(return_value=[])

        # Test with prefix
        self.coordinator.config_entry.options = {"device_name_format": "prefix"}
        await self.coordinator._async_update_data()
        args, kwargs = self.mock_device_registry_instance.async_get_or_create.call_args
        self.assertEqual(kwargs["name"], "[SSID] Formatting Test")

        # Test with suffix
        self.coordinator.config_entry.options = {"device_name_format": "suffix"}
        await self.coordinator._async_update_data()
        args, kwargs = self.mock_device_registry_instance.async_get_or_create.call_args
        self.assertEqual(kwargs["name"], "Formatting Test [SSID]")

        # Test with omitted
        self.coordinator.config_entry.options = {"device_name_format": "omitted"}
        await self.coordinator._async_update_data()
        args, kwargs = self.mock_device_registry_instance.async_get_or_create.call_args
        self.assertEqual(kwargs["name"], "Formatting Test")


if __name__ == '__main__':
    unittest.main()
