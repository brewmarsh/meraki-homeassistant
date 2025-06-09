import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime # Added import

from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from custom_components.meraki_ha.sensor.device_status import MerakiDeviceStatusSensor
from custom_components.meraki_ha.coordinators.base_coordinator import MerakiDataUpdateCoordinator # For coordinator type
from custom_components.meraki_ha.const import DOMAIN

MOCK_HASS = MagicMock(spec=HomeAssistant)

class TestMerakiDeviceStatusSensor(unittest.TestCase):

    def setUp(self):
        self.hass = MOCK_HASS
        self.mock_coordinator = MagicMock(spec=MerakiDataUpdateCoordinator)

        self.device_serial = "QTEST-SERIAL-0001"
        self.initial_device_data = {
            "serial": self.device_serial,
            "name": "Test AP",
            "model": "MR33",
            "status": "online",
            "firmware": "29.1",
            "mac": "00:11:22:aa:bb:cc",
            "lanIp": "192.168.1.10",
            "publicIp": "1.2.3.4",
            "wan1Ip": "1.2.3.4",
            "tags": ["tag1", "critical"],
            "networkId": "N_123"
        }
        # Simulate coordinator having this device in its data
        self.mock_coordinator.data = {"devices": [self.initial_device_data]}

        self.sensor = MerakiDeviceStatusSensor(
            coordinator=self.mock_coordinator,
            device_data=self.initial_device_data
        )
        self.sensor.hass = self.hass # Simulate being added to HASS for async_write_ha_state
        self.sensor.async_write_ha_state = MagicMock()

        self.patcher_logger = patch('custom_components.meraki_ha.sensor.device_status._LOGGER', new_callable=MagicMock)
        self.mock_logger = self.patcher_logger.start()

    def tearDown(self):
        self.patcher_logger.stop()

    def test_initialization_and_state(self):
        """Test sensor initialization and initial state."""
        self.assertEqual(self.sensor.unique_id, f"{self.device_serial}_device_status")
        # After EntityDescription update, sensor.name should be "Status"
        self.assertEqual(self.sensor.name, "Status")
        self.assertTrue(self.sensor.has_entity_name)
        # Verify state_class directly on the sensor instance
        self.assertIsNone(self.sensor.state_class)
        # Verify options property
        self.assertIsNone(self.sensor.options)
        # Verify native_unit_of_measurement
        self.assertIsNone(self.sensor.native_unit_of_measurement)
        # Verify suggested_unit_of_measurement
        self.assertIsNone(self.sensor.suggested_unit_of_measurement)
        # Verify suggested_display_precision
        self.assertIsNone(self.sensor.suggested_display_precision)
        # Verify last_reset
        self.assertIsNone(self.sensor.last_reset)

        self.assertEqual(self.sensor.native_value, "online")
        self.assertEqual(self.sensor.icon, "mdi:access-point-network") # MR model

        expected_attrs = {
            "model": "MR33",
            "serial_number": self.device_serial,
            "firmware_version": "29.1",
            "product_type": None, # Not in initial_device_data
            "mac_address": "00:11:22:aa:bb:cc",
            "lan_ip": "192.168.1.10",
            "public_ip": "1.2.3.4",
            "wan1_ip": "1.2.3.4",
            "wan2_ip": None,
            "tags": ["tag1", "critical"],
            "network_id": "N_123",
        }
        # Filter None from expected if not present
        expected_attrs_filtered = {k: v for k, v in expected_attrs.items() if v is not None}
        self.assertDictEqual(self.sensor.extra_state_attributes, expected_attrs_filtered)

    def test_handle_coordinator_update_device_offline(self):
        """Test state update when device goes offline."""
        updated_device_data = self.initial_device_data.copy()
        updated_device_data["status"] = "offline"
        updated_device_data["model"] = "MX64" # Change model to test icon change

        self.mock_coordinator.data = {"devices": [updated_device_data]}

        # Simulate coordinator update call
        self.sensor._handle_coordinator_update()

        self.assertEqual(self.sensor.native_value, "offline")
        self.assertEqual(self.sensor.icon, "mdi:router-network") # MX model
        self.sensor.async_write_ha_state.assert_called_once()

    def test_handle_coordinator_update_device_not_found(self):
        """Test state update when device is no longer in coordinator data."""
        self.mock_coordinator.data = {"devices": []} # Device removed

        self.sensor._handle_coordinator_update()

        self.assertIsNone(self.sensor.native_value) # Or "unknown"
        self.assertEqual(self.sensor.icon, "mdi:help-rhombus") # Unknown icon
        self.sensor.async_write_ha_state.assert_called_once()
        self.mock_logger.debug.assert_any_call(
            "Device data for serial '%s' not found in coordinator for sensor '%s'.",
            self.device_serial,
            self.sensor.unique_id,
        )

    def test_available_property(self):
        """Test the available property."""
        # Initially available
        self.mock_coordinator.last_update_success = True
        self.assertTrue(self.sensor.available)

        # Coordinator update failed
        self.mock_coordinator.last_update_success = False
        self.assertFalse(self.sensor.available)
        self.mock_coordinator.last_update_success = True # Reset

        # Device not in coordinator data
        self.mock_coordinator.data = {"devices": []}
        self.assertFalse(self.sensor.available)

        # Coordinator data is None
        self.mock_coordinator.data = None
        self.assertFalse(self.sensor.available)

if __name__ == '__main__':
    unittest.main()
```
