import asyncio
from datetime import timedelta
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import UpdateFailed
from homeassistant.config_entries import ConfigEntry

from custom_components.meraki_ha.coordinators.data_aggregation_coordinator import DataAggregationCoordinator
from custom_components.meraki_ha.coordinators.data_processor import MerakiDataProcessor
from custom_components.meraki_ha.coordinators.data_aggregator import DataAggregator
from custom_components.meraki_ha.helpers.ssid_status_calculator import SsidStatusCalculator # Needed for DataAggregator mock
from custom_components.meraki_ha.coordinators.base_coordinator import MerakiDataUpdateCoordinator # For parent coordinator type hint

import unittest

# Mock Home Assistant instance
MOCK_HASS = MagicMock(spec=HomeAssistant)

# Mock Config Entry
MOCK_CONFIG_ENTRY = MagicMock(spec=ConfigEntry)


class TestDataAggregationCoordinator(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.hass = MOCK_HASS
        self.config_entry = MOCK_CONFIG_ENTRY

        # Mock parent coordinator (MerakiDataUpdateCoordinator)
        self.mock_parent_coordinator = MagicMock(spec=MerakiDataUpdateCoordinator)
        self.mock_parent_coordinator.device_name_format = "device_name_only" # Example option

        self.scan_interval = timedelta(seconds=300)
        self.relaxed_tag_match = False

        # Patch dependencies of DataAggregationCoordinator
        self.patcher_data_processor = patch('custom_components.meraki_ha.coordinators.data_aggregation_coordinator.MerakiDataProcessor', spec=MerakiDataProcessor)
        self.mock_data_processor_class = self.patcher_data_processor.start()
        self.mock_data_processor_instance = self.mock_data_processor_class.return_value
        self.mock_data_processor_instance.process_devices = AsyncMock(return_value=[{"id": "processed_dev1"}])
        self.mock_data_processor_instance.process_networks = MagicMock(return_value=[{"id": "processed_net1"}])
        self.mock_data_processor_instance.process_ssids = MagicMock(return_value=[{"id": "processed_ssid1"}])

        self.patcher_data_aggregator = patch('custom_components.meraki_ha.coordinators.data_aggregation_coordinator.DataAggregator', spec=DataAggregator)
        self.mock_data_aggregator_class = self.patcher_data_aggregator.start()
        self.mock_data_aggregator_instance = self.mock_data_aggregator_class.return_value
        self.mock_data_aggregator_instance.aggregate_data = AsyncMock(return_value={"aggregated": "data"})

        self.patcher_ssid_calculator = patch('custom_components.meraki_ha.coordinators.data_aggregation_coordinator.SsidStatusCalculator', spec=SsidStatusCalculator)
        self.mock_ssid_calculator_class = self.patcher_ssid_calculator.start()
        self.mock_ssid_calculator_instance = self.mock_ssid_calculator_class.return_value


        self.coordinator = DataAggregationCoordinator(
            hass=self.hass,
            scan_interval=self.scan_interval,
            relaxed_tag_match=self.relaxed_tag_match,
            coordinator=self.mock_parent_coordinator
        )

        self.patcher_logger = patch('custom_components.meraki_ha.coordinators.data_aggregation_coordinator._LOGGER', new_callable=MagicMock)
        self.mock_logger = self.patcher_logger.start()

    def tearDown(self):
        self.patcher_data_processor.stop()
        self.patcher_data_aggregator.stop()
        self.patcher_ssid_calculator.stop()
        self.patcher_logger.stop()

    async def test_successful_update(self):
        """Test successful data update and aggregation."""
        raw_device_data = [{"id": "dev1"}]
        raw_ssid_data = [{"id": "ssid1"}]
        raw_network_data = [{"id": "net1"}]
        raw_client_data = [{"id": "client1"}]
        raw_network_client_counts = {"net1": 1}
        clients_on_ssids = 1
        clients_on_appliances = 0
        clients_on_wireless = 1

        expected_aggregated_data = {"aggregated": "data"}

        result = await self.coordinator._async_update_data(
            device_data=raw_device_data,
            ssid_data=raw_ssid_data,
            network_data=raw_network_data,
            client_data=raw_client_data,
            network_client_counts=raw_network_client_counts,
            clients_on_ssids=clients_on_ssids,
            clients_on_appliances=clients_on_appliances,
            clients_on_wireless=clients_on_wireless,
        )

        self.assertEqual(result, expected_aggregated_data)
        self.mock_data_processor_instance.process_devices.assert_called_once_with(raw_device_data)
        self.mock_data_processor_instance.process_networks.assert_called_once_with(raw_network_data)
        self.mock_data_processor_instance.process_ssids.assert_called_once_with(raw_ssid_data)

        self.mock_data_aggregator_instance.aggregate_data.assert_called_once_with(
            self.mock_data_processor_instance.process_devices.return_value,
            self.mock_data_processor_instance.process_ssids.return_value,
            self.mock_data_processor_instance.process_networks.return_value,
            raw_client_data,
            raw_network_client_counts,
            clients_on_ssids=clients_on_ssids,
            clients_on_appliances=clients_on_appliances,
            clients_on_wireless=clients_on_wireless,
        )
        self.mock_logger.debug.assert_any_call("Data aggregation successful. Processed %d devices (passed to aggregator), %d SSIDs, %d networks.", 1, 1, 1)


    async def test_update_with_none_input_data(self):
        """Test update when essential input data (devices, ssids, networks) is None."""
        for none_input_scenario in [
            {"device_data": None, "ssid_data": [{"id": "s1"}], "network_data": [{"id": "n1"}]},
            {"device_data": [{"id": "d1"}], "ssid_data": None, "network_data": [{"id": "n1"}]},
            {"device_data": [{"id": "d1"}], "ssid_data": [{"id": "s1"}], "network_data": None},
        ]:
            with self.subTest(scenario=none_input_scenario):
                self.mock_logger.reset_mock() # Reset logger for subtest
                result = await self.coordinator._async_update_data(
                    device_data=none_input_scenario["device_data"],
                    ssid_data=none_input_scenario["ssid_data"],
                    network_data=none_input_scenario["network_data"],
                    client_data=[], network_client_counts={} # Provide defaults for others
                )
                self.assertEqual(result, {}) # Expect empty dict
                self.mock_logger.warning.assert_called_once_with(
                    "Essential data (devices, SSIDs, or networks) is None. Skipping aggregation and returning empty data."
                )
                # Ensure processor and aggregator were not called
                self.mock_data_processor_instance.process_devices.assert_not_called()
                self.mock_data_aggregator_instance.aggregate_data.assert_not_called()
                # Reset mocks for next subtest iteration
                self.mock_data_processor_instance.reset_mock()
                self.mock_data_aggregator_instance.reset_mock()


    async def test_update_with_malformed_input_data_types(self):
        """Test update when input data is not a list where a list is expected."""
        # Example: device_data is a dict instead of list
        raw_device_data_malformed = {"id": "dev1"}
        raw_ssid_data = [{"id": "ssid1"}]
        raw_network_data = [{"id": "net1"}]

        await self.coordinator._async_update_data(
            device_data=raw_device_data_malformed, # type: ignore
            ssid_data=raw_ssid_data,
            network_data=raw_network_data,
            client_data=[], network_client_counts={}
        )
        self.mock_logger.warning.assert_any_call(
            "Device data is not a list as expected: %s. Proceeding with empty processed_devices.", type(raw_device_data_malformed)
        )
        # Aggregator should still be called, but with empty list for devices
        self.mock_data_aggregator_instance.aggregate_data.assert_called_once()
        # First arg to aggregate_data (processed_devices) should be []
        self.assertEqual(self.mock_data_aggregator_instance.aggregate_data.call_args[0][0], [])


    async def test_data_aggregator_raises_exception(self):
        """Test when DataAggregator.aggregate_data raises an exception."""
        self.mock_data_aggregator_instance.aggregate_data.side_effect = Exception("Aggregator exploded")

        with self.assertRaises(UpdateFailed) as context:
            await self.coordinator._async_update_data(
                device_data=[{"id": "d1"}], ssid_data=[{"id": "s1"}], network_data=[{"id": "n1"}],
                client_data=[], network_client_counts={}
            )

        self.assertTrue("Error aggregating Meraki data: Aggregator exploded" in str(context.exception))
        self.mock_logger.exception.assert_called_once_with("Error during Meraki data aggregation: %s", Exception("Aggregator exploded"))

    async def test_data_processor_raises_exception(self):
        """Test when MerakiDataProcessor.process_devices raises an exception."""
        self.mock_data_processor_instance.process_devices.side_effect = Exception("Processor exploded")

        with self.assertRaises(UpdateFailed) as context: # Should propagate as UpdateFailed
            await self.coordinator._async_update_data(
                device_data=[{"id": "d1"}], ssid_data=[{"id": "s1"}], network_data=[{"id": "n1"}],
                client_data=[], network_client_counts={}
            )

        self.assertTrue("Error aggregating Meraki data: Processor exploded" in str(context.exception))
        self.mock_logger.exception.assert_called_once_with("Error during Meraki data aggregation: %s", Exception("Processor exploded"))


if __name__ == '__main__':
    unittest.main()
```
