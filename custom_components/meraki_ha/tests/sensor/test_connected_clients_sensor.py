import unittest
from unittest.mock import MagicMock, patch

from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.components.sensor import SensorStateClass

from custom_components.meraki_ha.sensor.connected_clients import MerakiDeviceConnectedClientsSensor
from custom_components.meraki_ha.coordinators.base_coordinator import MerakiDataUpdateCoordinator # For coordinator type
from custom_components.meraki_ha.const import DOMAIN

class TestMerakiDeviceConnectedClientsSensor(unittest.TestCase):

    def setUp(self):
        self.mock_coordinator = MagicMock(spec=MerakiDataUpdateCoordinator)

        self.device_serial = "QCLIENT-TEST-0001"
        self.initial_device_data_from_setup = { # Data passed during sensor __init__
            "serial": self.device_serial,
            "name": "Test AP Clients",
            "model": "MR42",
            "firmware": "29.0",
            "mac": "00:11:22:cc:dd:ee"
        }

        # Simulate coordinator having this device with client count info
        self.coordinator_device_data = self.initial_device_data_from_setup.copy()
        self.coordinator_device_data["connected_clients_count"] = 5

        self.mock_coordinator.data = {"devices": [self.coordinator_device_data]}

        self.sensor = MerakiDeviceConnectedClientsSensor(
            coordinator=self.mock_coordinator,
            device_data=self.initial_device_data_from_setup
        )
        self.sensor.async_write_ha_state = MagicMock()

        self.patcher_logger = patch('custom_components.meraki_ha.sensor.connected_clients._LOGGER', new_callable=MagicMock)
        self.mock_logger = self.patcher_logger.start()

    def tearDown(self):
        self.patcher_logger.stop()

    def test_initialization_and_state(self):
        """Test sensor initialization and initial state."""
        self.assertEqual(self.sensor.unique_id, f"{self.device_serial}_connected_clients")
        self.assertEqual(self.sensor.name, "Test AP Clients Connected Clients")

        self.assertEqual(self.sensor.native_value, 5) # From coordinator_device_data
        self.assertEqual(self.sensor.native_unit_of_measurement, "clients")
        self.assertEqual(self.sensor.state_class, SensorStateClass.MEASUREMENT)
        self.assertEqual(self.sensor.icon, "mdi:account-network")

        expected_attrs = {
            "device_name": "Test AP Clients",
            "model": "MR42",
            "serial_number": self.device_serial,
            "firmware_version": "29.0",
            "lan_ip": None, # Not in initial data
            "mac_address": "00:11:22:cc:dd:ee",
        }
        expected_attrs_filtered = {k: v for k, v in expected_attrs.items() if v is not None}
        self.assertDictEqual(self.sensor.extra_state_attributes, expected_attrs_filtered)

    def test_handle_coordinator_update_client_count_changes(self):
        """Test state update when client count changes."""
        updated_device_data = self.coordinator_device_data.copy()
        updated_device_data["connected_clients_count"] = 10

        self.mock_coordinator.data = {"devices": [updated_device_data]}

        self.sensor._handle_coordinator_update()

        self.assertEqual(self.sensor.native_value, 10)
        self.sensor.async_write_ha_state.assert_called_once()

    def test_handle_coordinator_update_device_not_found(self):
        """Test state update when device is no longer in coordinator data."""
        self.mock_coordinator.data = {"devices": []} # Device removed

        self.sensor._handle_coordinator_update()

        self.assertEqual(self.sensor.native_value, 0) # Defaults to 0 if device not found
        self.sensor.async_write_ha_state.assert_called_once()
        self.mock_logger.warning.assert_any_call(
            "Device data not found in coordinator for serial '%s' (sensor: %s). Defaulting client count to 0.",
            self.device_serial,
            self.sensor.unique_id,
        )

    def test_handle_coordinator_update_no_client_count_key(self):
        """Test state update when 'connected_clients_count' key is missing."""
        device_data_no_count_key = self.initial_device_data_from_setup.copy()
        # connected_clients_count key is missing

        self.mock_coordinator.data = {"devices": [device_data_no_count_key]}
        self.sensor._handle_coordinator_update()
        self.assertEqual(self.sensor.native_value, 0) # Defaults to 0
        self.mock_logger.warning.assert_any_call(
            "Connected clients data for device '%s' (Serial: %s) is not an integer: %s. Defaulting to 0.",
            "Test AP Clients", self.device_serial, None
        )


    def test_get_client_count_handles_none_data(self):
        """Test _get_client_count when coordinator data is None."""
        self.mock_coordinator.data = None
        self.assertIsNone(self.sensor._get_client_count())
        self.mock_logger.warning.assert_any_call(
            "Coordinator data or devices list is unavailable for %s.", self.sensor.unique_id
        )

    def test_device_info(self):
        """Test the device_info property."""
        dev_info = self.sensor.device_info
        self.assertIsNotNone(dev_info)
        self.assertEqual(dev_info["identifiers"], {(DOMAIN, self.device_serial)})
        # Other fields like name, model are not set here as they should be part of the main device registration


if __name__ == '__main__':
    unittest.main()
