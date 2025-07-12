import asyncio
import logging
from unittest.mock import AsyncMock, MagicMock, patch, call

import pytest
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import UpdateFailed
from meraki.exceptions import APIError as MerakiSDKAPIError

from custom_components.meraki_ha.coordinators.api_data_fetcher import MerakiApiDataFetcher
from custom_components.meraki_ha.meraki_api import MerakiAPIClient
from custom_components.meraki_ha.coordinators.meraki_device_types import MerakiDeviceType

import unittest

SAMPLE_ORG_ID = "org123"
SAMPLE_NETWORK_ID = "net123"
SAMPLE_DEVICE_SERIAL_MR = "QMR1-2345-6789"
SAMPLE_DEVICE_SERIAL_MX = "QMX1-2345-6789"
MOCK_HASS = MagicMock(spec=HomeAssistant)


class TestMerakiApiDataFetcher(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.mock_meraki_client = MagicMock(spec=MerakiAPIClient)
        self.mock_meraki_client.org_id = SAMPLE_ORG_ID

        self.mock_meraki_client.organizations = AsyncMock()
        self.mock_meraki_client.networks = AsyncMock()
        self.mock_meraki_client.devices = AsyncMock()
        self.mock_meraki_client.wireless = AsyncMock()
        self.mock_meraki_client.appliance = AsyncMock()

        self.fetcher = MerakiApiDataFetcher(meraki_client=self.mock_meraki_client)

        self.patcher_logger = patch('custom_components.meraki_ha.coordinators.api_data_fetcher._LOGGER', new_callable=MagicMock)
        self.mock_logger = self.patcher_logger.start()

        # Patch map_meraki_model_to_device_type as it's external to the class but used within
        self.patcher_map_model = patch('custom_components.meraki_ha.coordinators.api_data_fetcher.map_meraki_model_to_device_type')
        self.mock_map_model = self.patcher_map_model.start()
        self.mock_map_model.return_value = MerakiDeviceType.WIRELESS # Default mock

    def tearDown(self):
        self.patcher_logger.stop()
        self.patcher_map_model.stop()

    # 1. Test Parallelized API Calls in `fetch_all_data`
    async def test_fetch_all_data_parallel_calls_success(self):
        """Test fetch_all_data successful parallel API calls."""
        mock_networks = [{"id": SAMPLE_NETWORK_ID, "name": "Test Network"}]
        mock_devices = [{"serial": SAMPLE_DEVICE_SERIAL_MR, "model": "MR33", "networkId": SAMPLE_NETWORK_ID, "name": "AP1"}]
        mock_statuses = [{"serial": SAMPLE_DEVICE_SERIAL_MR, "status": "online"}]
        mock_firmware_upgrades = []
        mock_org_details = {"name": "Test Org"}

        self.fetcher.async_get_networks = AsyncMock(return_value=mock_networks)
        self.fetcher.async_get_organization_devices = AsyncMock(return_value=mock_devices)
        self.mock_meraki_client.organizations.getOrganizationDevicesStatuses = AsyncMock(return_value=mock_statuses)
        self.mock_meraki_client.organizations.getOrganizationFirmwareUpgrades = AsyncMock(return_value=mock_firmware_upgrades)
        self.fetcher._async_meraki_api_call = AsyncMock(return_value=mock_org_details) # For org details call

        # Mock other calls made within fetch_all_data if they are not covered by other tests explicitly
        self.mock_meraki_client.networks.getNetworkClients = AsyncMock(return_value=[]) # For all_clients
        self.fetcher.async_get_network_ssids = AsyncMock(return_value=[]) # For ssids

        with patch('asyncio.gather', new_callable=AsyncMock) as mock_gather:
            # Simulate specific results for the initial gather
            # The gather in fetch_all_data is for: networks, devices, statuses, firmware
            # The actual call inside fetch_all_data for these is now:
            # self.async_get_networks, self.async_get_organization_devices,
            # self.meraki_client.organizations.getOrganizationDevicesStatuses,
            # self.meraki_client.organizations.getOrganizationFirmwareUpgrades
            # So we need to ensure these mocks are what `gather` returns.

            # Redefine mocks for the specific calls that will be gathered
            gathered_networks_mock = AsyncMock(return_value=mock_networks)
            gathered_devices_mock = AsyncMock(return_value=mock_devices)
            gathered_statuses_mock = AsyncMock(return_value=mock_statuses)
            gathered_firmware_mock = AsyncMock(return_value=mock_firmware_upgrades)

            self.fetcher.async_get_networks = gathered_networks_mock
            self.fetcher.async_get_organization_devices = gathered_devices_mock
            self.mock_meraki_client.organizations.getOrganizationDevicesStatuses = gathered_statuses_mock
            self.mock_meraki_client.organizations.getOrganizationFirmwareUpgrades = gathered_firmware_mock

            mock_gather.return_value = [
                mock_networks,
                mock_devices,
                mock_statuses,
                mock_firmware_upgrades
            ]

            data = await self.fetcher.fetch_all_data(MOCK_HASS)

            self.assertEqual(data["networks"], mock_networks)
            self.assertEqual(data["devices"][0]["serial"], mock_devices[0]["serial"]) # Statuses are merged
            self.assertEqual(data["devices"][0]["status"], "online")
            self.assertEqual(data["org_name"], "Test Org")

            # Check that asyncio.gather was called with the correct coroutines
            # The actual coroutines passed to gather are instance methods or direct SDK calls
            self.assertTrue(mock_gather.called)
            self.assertEqual(mock_gather.call_args[0][0][0], gathered_networks_mock(SAMPLE_ORG_ID))
            self.assertEqual(mock_gather.call_args[0][0][1], gathered_devices_mock(SAMPLE_ORG_ID))


    async def test_fetch_all_data_critical_failure_networks(self):
        """Test fetch_all_data when fetching networks fails."""
        self.fetcher.async_get_networks = AsyncMock(return_value=None) # Simulate failure
        self.fetcher.async_get_organization_devices = AsyncMock(return_value=[]) # Devices call would succeed
        self.mock_meraki_client.organizations.getOrganizationDevicesStatuses = AsyncMock(return_value=[])
        self.mock_meraki_client.organizations.getOrganizationFirmwareUpgrades = AsyncMock(return_value=[])

        with patch('asyncio.gather', new_callable=AsyncMock) as mock_gather:
            mock_gather.return_value = [
                None, # Networks failed
                [],
                [],
                []
            ]
            with self.assertRaises(UpdateFailed):
                await self.fetcher.fetch_all_data(MOCK_HASS)
            self.mock_logger.error.assert_any_call(f"Could not fetch Meraki networks for org ID: {SAMPLE_ORG_ID}. Aborting update.")

    async def test_fetch_all_data_critical_failure_devices(self):
        """Test fetch_all_data when fetching devices fails."""
        self.fetcher.async_get_networks = AsyncMock(return_value=[{"id": "net1"}])
        self.fetcher.async_get_organization_devices = AsyncMock(return_value=None) # Simulate failure
        self.mock_meraki_client.organizations.getOrganizationDevicesStatuses = AsyncMock(return_value=[])
        self.mock_meraki_client.organizations.getOrganizationFirmwareUpgrades = AsyncMock(return_value=[])

        with patch('asyncio.gather', new_callable=AsyncMock) as mock_gather:
            mock_gather.return_value = [
                [{"id": "net1"}],
                None, # Devices failed
                [],
                []
            ]
            with self.assertRaises(UpdateFailed):
                await self.fetcher.fetch_all_data(MOCK_HASS)
            self.mock_logger.error.assert_any_call(f"Could not fetch Meraki devices for org ID: {SAMPLE_ORG_ID}. Aborting update.")

    async def test_fetch_all_data_non_critical_failure_statuses(self):
        """Test fetch_all_data when fetching statuses fails."""
        mock_networks = [{"id": SAMPLE_NETWORK_ID}]
        mock_devices = [{"serial": SAMPLE_DEVICE_SERIAL_MR, "model": "MR33"}]

        self.fetcher.async_get_networks = AsyncMock(return_value=mock_networks)
        self.fetcher.async_get_organization_devices = AsyncMock(return_value=mock_devices)
        # Simulate MerakiSDKAPIError for statuses
        status_error = MerakiSDKAPIError(MagicMock(status=500, reason="Server Error"), "get statuses")
        self.mock_meraki_client.organizations.getOrganizationDevicesStatuses = AsyncMock(side_effect=status_error)
        self.mock_meraki_client.organizations.getOrganizationFirmwareUpgrades = AsyncMock(return_value=[])
        self.fetcher._async_meraki_api_call = AsyncMock(return_value={"name": "Test Org"}) # For org details

        # Mock other calls
        self.mock_meraki_client.networks.getNetworkClients = AsyncMock(return_value=[])
        self.fetcher.async_get_network_ssids = AsyncMock(return_value=[])

        with patch('asyncio.gather', new_callable=AsyncMock) as mock_gather:
            mock_gather.return_value = [
                mock_networks,
                mock_devices,
                status_error, # Statuses failed with SDK error
                []
            ]
            data = await self.fetcher.fetch_all_data(MOCK_HASS)
            self.mock_logger.warning.assert_any_call(
                f"SDK API error fetching device statuses for org {SAMPLE_ORG_ID}: Status 500, Reason: Server Error. Device statuses may be incomplete."
            )
            self.assertIsNotNone(data) # Ensure it didn't abort

    # 2. Test `_async_meraki_api_call` Helper (indirectly and directly for 404)
    async def test_async_meraki_api_call_success(self):
        """Test _async_meraki_api_call successful execution (indirectly)."""
        mock_network_data = [{"id": "net1"}]
        self.mock_meraki_client.organizations.getOrganizationNetworks = AsyncMock(return_value=mock_network_data)

        result = await self.fetcher.async_get_networks(SAMPLE_ORG_ID)
        self.assertEqual(result, mock_network_data)
        self.mock_logger.debug.assert_any_call(f"Executing API call: getOrganizationNetworks(organizationId={SAMPLE_ORG_ID})")

    async def test_async_meraki_api_call_sdk_error(self):
        """Test _async_meraki_api_call handling MerakiSDKAPIError."""
        error_response = MagicMock(status=500, reason="Internal Server Error")
        sdk_error = MerakiSDKAPIError(error_response, "Test API Call")
        self.mock_meraki_client.organizations.getOrganizationNetworks = AsyncMock(side_effect=sdk_error)

        result = await self.fetcher.async_get_networks(SAMPLE_ORG_ID)
        self.assertIsNone(result)
        self.mock_logger.warning.assert_any_call(
            f"SDK API error during getOrganizationNetworks(organizationId={SAMPLE_ORG_ID}) for org {SAMPLE_ORG_ID}: Status 500, Reason: Internal Server Error. Returning None."
        )

    async def test_async_meraki_api_call_generic_exception(self):
        """Test _async_meraki_api_call handling generic Exception."""
        generic_error = Exception("Something went wrong")
        self.mock_meraki_client.organizations.getOrganizationNetworks = AsyncMock(side_effect=generic_error)

        result = await self.fetcher.async_get_networks(SAMPLE_ORG_ID)
        self.assertIsNone(result)
        self.mock_logger.exception.assert_any_call(
            f"Unexpected error during getOrganizationNetworks(organizationId={SAMPLE_ORG_ID}) for org {SAMPLE_ORG_ID}: {generic_error}. Returning None."
        )

    async def test_async_meraki_api_call_404_return_empty_list(self):
        """Test _async_meraki_api_call with return_empty_list_on_404=True."""
        error_response = MagicMock(status=404, reason="Not Found")
        sdk_error_404 = MerakiSDKAPIError(error_response, "Test API Call 404")

        # Use a direct call to test this behavior if possible, or use a method that employs it like async_get_network_ssids
        mock_api_coro = AsyncMock(side_effect=sdk_error_404)
        call_desc = "Test 404 with return_empty_list"

        result = await self.fetcher._async_meraki_api_call(mock_api_coro(), call_desc, return_empty_list_on_404=True)
        self.assertEqual(result, [])
        self.mock_logger.info.assert_any_call(f"Resource not found (404) for {call_desc} in org {SAMPLE_ORG_ID}.")

    async def test_async_meraki_api_call_404_return_none(self):
        """Test _async_meraki_api_call with return_empty_list_on_404=False (default)."""
        error_response = MagicMock(status=404, reason="Not Found")
        sdk_error_404 = MerakiSDKAPIError(error_response, "Test API Call 404 None")

        mock_api_coro = AsyncMock(side_effect=sdk_error_404)
        call_desc = "Test 404 with return_none"

        result = await self.fetcher._async_meraki_api_call(mock_api_coro(), call_desc) # Default is False
        self.assertIsNone(result)
        self.mock_logger.info.assert_any_call(f"Resource not found (404) for {call_desc} in org {SAMPLE_ORG_ID}.")


    # 3. Test Refactored Firmware Data Merging
    async def test_firmware_data_merging(self):
        """Test firmware data merging logic in fetch_all_data."""
        devices_data = [
            {"serial": "S1", "name": "Device1", "firmware": "current_fw_10"}, # Has upgrade
            {"serial": "S2", "name": "Device2", "firmware": "current_fw_stable"}, # Up to date
            {"serial": "S3", "name": "Device3", "firmware": "current_fw_old"}, # No info in upgrade data
            {"serial": "S4", "name": "Device4", "firmware": None}, # No current firmware known
        ]
        # Simulate that async_get_organization_devices will return this
        self.fetcher.async_get_organization_devices = AsyncMock(return_value=devices_data)

        firmware_data = [
            {"serial": "S1", "status": "has-newer-stable-version", "nextUpgrade": {"toVersion": {"version": "next_fw_11"}}},
            {"serial": "S2", "status": "up-to-date"},
            # S3 is missing from this data
        ]
        # Simulate that the gathered call for firmware returns this
        self.mock_meraki_client.organizations.getOrganizationFirmwareUpgrades = AsyncMock(return_value=firmware_data)

        # Mock other necessary calls for fetch_all_data to run
        self.fetcher.async_get_networks = AsyncMock(return_value=[{"id": "net1"}])
        self.mock_meraki_client.organizations.getOrganizationDevicesStatuses = AsyncMock(return_value=[])
        self.fetcher._async_meraki_api_call = AsyncMock(return_value={"name": "Test Org"})
        self.mock_meraki_client.networks.getNetworkClients = AsyncMock(return_value=[])
        self.fetcher.async_get_network_ssids = AsyncMock(return_value=[])

        # Patch asyncio.gather to return the pre-mocked values
        with patch('asyncio.gather', new_callable=AsyncMock) as mock_gather:
            mock_gather.return_value = [ # networks, devices, statuses, firmware_upgrades
                self.fetcher.async_get_networks.return_value,
                devices_data,
                self.mock_meraki_client.organizations.getOrganizationDevicesStatuses.return_value,
                firmware_data
            ]

            result_data = await self.fetcher.fetch_all_data(MOCK_HASS)

            processed_devices = {dev["serial"]: dev for dev in result_data["devices"]}

            # S1: Has upgrade
            self.assertFalse(processed_devices["S1"]["firmware_up_to_date"])
            self.assertEqual(processed_devices["S1"]["latest_firmware_version"], "next_fw_11")

            # S2: Up to date
            self.assertTrue(processed_devices["S2"]["firmware_up_to_date"])
            self.assertEqual(processed_devices["S2"]["latest_firmware_version"], "current_fw_stable") # Stays current

            # S3: No info in upgrade data - should be marked as up-to-date if current firmware exists
            self.assertTrue(processed_devices["S3"]["firmware_up_to_date"])
            self.assertEqual(processed_devices["S3"]["latest_firmware_version"], "current_fw_old")

            # S4: No current firmware, no API info - marked as not up-to-date, latest N/A
            self.assertFalse(processed_devices["S4"]["firmware_up_to_date"])
            self.assertEqual(processed_devices["S4"]["latest_firmware_version"], "N/A")

    async def test_firmware_data_empty_or_none(self):
        """Test firmware merging when firmware_upgrade_data is empty or None."""
        devices_data = [{"serial": "S1", "name": "Device1", "firmware": "fw_v1"}]
        self.fetcher.async_get_organization_devices = AsyncMock(return_value=devices_data)
        self.fetcher.async_get_networks = AsyncMock(return_value=[{"id": "net1"}])
        self.mock_meraki_client.organizations.getOrganizationDevicesStatuses = AsyncMock(return_value=[])
        self.fetcher._async_meraki_api_call = AsyncMock(return_value={"name": "Test Org"})
        self.mock_meraki_client.networks.getNetworkClients = AsyncMock(return_value=[])
        self.fetcher.async_get_network_ssids = AsyncMock(return_value=[])

        for firmware_test_data in [[], None, {}]: # Test empty list, None, and non-list (dict)
            self.mock_meraki_client.organizations.getOrganizationFirmwareUpgrades = AsyncMock(return_value=firmware_test_data)

            with patch('asyncio.gather', new_callable=AsyncMock) as mock_gather:
                mock_gather.return_value = [
                    [{"id": "net1"}], devices_data, [], firmware_test_data
                ]
                result_data = await self.fetcher.fetch_all_data(MOCK_HASS)
                processed_device = result_data["devices"][0]

                if firmware_test_data is None or not isinstance(firmware_test_data, list): # Bad data
                    self.assertFalse(processed_device["firmware_up_to_date"])
                    self.assertEqual(processed_device["latest_firmware_version"], "fw_v1")
                else: # Empty list
                    self.assertTrue(processed_device["firmware_up_to_date"])
                    self.assertEqual(processed_device["latest_firmware_version"], "fw_v1")


    # 4. Test Refactored DNS Fallback Logic in `_async_get_mx_device_uplink_settings`
    # This will test _extract_dns_servers_for_wan indirectly
    async def test_extract_dns_servers_svis(self):
        device = {"serial": SAMPLE_DEVICE_SERIAL_MX}
        uplink_settings = {
            "interfaces": {
                "wan1": {"svis": {"ipv4": {"nameservers": [{"addresses": ["1.1.1.1", "1.0.0.1"]}]}}}
            }
        }
        self.mock_meraki_client.appliance.getDeviceApplianceUplinksSettings = AsyncMock(return_value=uplink_settings)
        await self.fetcher._async_get_mx_device_uplink_settings(device, self.mock_meraki_client)
        self.assertEqual(device["wan1_dns_servers"], ["1.1.1.1", "1.0.0.1"])

    async def test_extract_dns_servers_dnsServers_list(self):
        device = {"serial": SAMPLE_DEVICE_SERIAL_MX}
        uplink_settings = {"interfaces": {"wan1": {"dnsServers": ["8.8.8.8", "8.8.4.4"]}}}
        self.mock_meraki_client.appliance.getDeviceApplianceUplinksSettings = AsyncMock(return_value=uplink_settings)
        await self.fetcher._async_get_mx_device_uplink_settings(device, self.mock_meraki_client)
        self.assertEqual(device["wan1_dns_servers"], ["8.8.8.8", "8.8.4.4"])

    async def test_extract_dns_servers_dnsServers_string(self):
        device = {"serial": SAMPLE_DEVICE_SERIAL_MX}
        # Meraki API sometimes returns comma-sep string, though our code handles single IP string
        uplink_settings = {"interfaces": {"wan1": {"dnsServers": "208.67.222.222"}}}
        self.mock_meraki_client.appliance.getDeviceApplianceUplinksSettings = AsyncMock(return_value=uplink_settings)
        await self.fetcher._async_get_mx_device_uplink_settings(device, self.mock_meraki_client)
        self.assertEqual(device["wan1_dns_servers"], ["208.67.222.222"])

    async def test_extract_dns_servers_device_level_fallback(self):
        # device_global_data (device dict) already contains these from status update
        device = {"serial": SAMPLE_DEVICE_SERIAL_MX, "wan1PrimaryDns": "4.4.4.4", "wan1SecondaryDns": "4.4.2.2"}
        uplink_settings = {"interfaces": {"wan1": {}}} # No DNS info in uplink settings
        self.mock_meraki_client.appliance.getDeviceApplianceUplinksSettings = AsyncMock(return_value=uplink_settings)
        await self.fetcher._async_get_mx_device_uplink_settings(device, self.mock_meraki_client)
        self.assertEqual(device["wan1_dns_servers"], ["4.4.4.4", "4.4.2.2"])

    async def test_extract_dns_no_info(self):
        device = {"serial": SAMPLE_DEVICE_SERIAL_MX}
        uplink_settings = {"interfaces": {"wan1": {}}}
        self.mock_meraki_client.appliance.getDeviceApplianceUplinksSettings = AsyncMock(return_value=uplink_settings)
        await self.fetcher._async_get_mx_device_uplink_settings(device, self.mock_meraki_client)
        self.assertEqual(device["wan1_dns_servers"], []) # Should be empty list

    # 5. Test `_async_get_mx_lan_dns_settings`
    async def test_get_mx_lan_dns_settings(self):
        device = {"serial": SAMPLE_DEVICE_SERIAL_MX, "networkId": SAMPLE_NETWORK_ID, "name": "MX1"}
        vlan_settings_response = [
            {"id": "1", "name": "VLAN1", "dnsNameservers": "google_dns"},
            {"id": "2", "name": "VLAN2", "dnsNameservers": "custom_servers", "customDnsServers": ["192.168.1.1"]},
            {"id": "3", "name": "VLAN3", "dnsNameservers": "upstream_dns"},
            {"id": "4", "name": "VLAN4", "dnsNameservers": "custom_servers", "customDnsServers": []}, # No IPs
            {"id": "5", "name": "VLAN5"} # No DNS setting
        ]
        self.mock_meraki_client.appliance.getNetworkApplianceVlansSettings = AsyncMock(return_value=vlan_settings_response)

        await self.fetcher._async_get_mx_lan_dns_settings(device, self.mock_meraki_client)

        expected_lan_dns = {
            "VLAN 1 (VLAN1)": "google_dns",
            "VLAN 2 (VLAN2)": ["192.168.1.1"],
            "VLAN 3 (VLAN3)": "upstream_dns",
            "VLAN 4 (VLAN4)": [],
            "VLAN 5 (VLAN5)": "Not configured"
        }
        self.assertEqual(device["lan_dns_settings"], expected_lan_dns)

    async def test_get_mx_lan_dns_single_vlan_dict_response(self):
        device = {"serial": SAMPLE_DEVICE_SERIAL_MX, "networkId": SAMPLE_NETWORK_ID, "name": "MX1"}
        # Simulate API returning a single dict instead of a list
        vlan_settings_response_single_dict = {"id": "10", "name": "MainVLAN", "dnsNameservers": "opendns"}
        self.mock_meraki_client.appliance.getNetworkApplianceVlansSettings = AsyncMock(return_value=vlan_settings_response_single_dict)

        await self.fetcher._async_get_mx_lan_dns_settings(device, self.mock_meraki_client)

        expected_lan_dns = {"VLAN 10 (MainVLAN)": "opendns"}
        self.assertEqual(device["lan_dns_settings"], expected_lan_dns)

    async def test_get_mx_lan_dns_404_error(self):
        device = {"serial": SAMPLE_DEVICE_SERIAL_MX, "networkId": SAMPLE_NETWORK_ID, "name": "MX1"}
        error_404 = MerakiSDKAPIError(MagicMock(status=404), "get VLANs")
        self.mock_meraki_client.appliance.getNetworkApplianceVlansSettings = AsyncMock(side_effect=error_404)

        # _async_meraki_api_call will catch the 404 and return [] because of return_empty_list_on_404=True
        await self.fetcher._async_get_mx_lan_dns_settings(device, self.mock_meraki_client)
        self.assertEqual(device["lan_dns_settings"], {}) # Empty dict as no VLANs processed

    async def test_get_mx_lan_dns_api_returns_none(self):
        device = {"serial": SAMPLE_DEVICE_SERIAL_MX, "networkId": SAMPLE_NETWORK_ID, "name": "MX1"}
        # Simulate API returning None (e.g. some other error handled by _async_meraki_api_call)
        self.mock_meraki_client.appliance.getNetworkApplianceVlansSettings = AsyncMock(return_value=None)

        await self.fetcher._async_get_mx_lan_dns_settings(device, self.mock_meraki_client)
        self.assertEqual(device["lan_dns_settings"], {}) # Empty dict as no VLANs processed

if __name__ == '__main__':
    unittest.main()

# Example of how to run with pytest if preferred:
# Create conftest.py for shared fixtures if needed
# Then run: pytest path/to/your/tests
# (Might need `pip install pytest pytest-asyncio`)

# To run with unittest:
# python -m unittest custom_components/meraki_ha/tests/coordinators/test_api_data_fetcher.py
