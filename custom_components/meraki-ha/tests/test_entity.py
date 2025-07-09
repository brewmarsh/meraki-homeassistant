import unittest
from unittest.mock import MagicMock, patch

from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo

from custom_components.meraki_ha.entity import MerakiEntity
from custom_components.meraki_ha.coordinators.base_coordinator import MerakiDataUpdateCoordinator # For type hint
from custom_components.meraki_ha.const import DOMAIN

MOCK_HASS = MagicMock(spec=HomeAssistant)

class TestMerakiEntity(unittest.TestCase):

    def setUp(self):
        self.mock_coordinator = MagicMock(spec=MerakiDataUpdateCoordinator)
        # Mock the device_name_format option on the coordinator
        self.mock_coordinator.device_name_format = "device_name_only" # Default for tests

    def test_device_info_physical_device_basic(self):
        """Test device_info for a basic physical device."""
        device_data = {
            "serial": "Q123-ABCD-EFGH",
            "name": "My AP",
            "model": "MR33",
            "firmware": "29.6.1",
            "networkId": "N_123"
        }
        entity = MerakiEntity(coordinator=self.mock_coordinator, device_data=device_data)

        device_info = entity.device_info
        self.assertIsNotNone(device_info)
        self.assertEqual(device_info["identifiers"], {(DOMAIN, "Q123-ABCD-EFGH")})
        self.assertEqual(device_info["name"], "My AP") # Default format
        self.assertEqual(device_info["manufacturer"], "Cisco Meraki")
        self.assertEqual(device_info["model"], "MR33")
        self.assertEqual(device_info["sw_version"], "29.6.1")

    def test_device_info_physical_device_name_formatting_prefix(self):
        """Test device_info name formatting with prefix."""
        self.mock_coordinator.device_name_format = "prefix_model"
        device_data = {"serial": "QXYZ", "name": "Office AP", "model": "MR42"}
        entity = MerakiEntity(coordinator=self.mock_coordinator, device_data=device_data)
        device_info = entity.device_info
        self.assertEqual(device_info["name"], "[MR42] Office AP")

    def test_device_info_physical_device_name_formatting_suffix(self):
        """Test device_info name formatting with suffix."""
        self.mock_coordinator.device_name_format = "suffix_model"
        device_data = {"serial": "QXYZ", "name": "Lobby Switch", "model": "MS220"}
        entity = MerakiEntity(coordinator=self.mock_coordinator, device_data=device_data)
        device_info = entity.device_info
        self.assertEqual(device_info["name"], "Lobby Switch [MS220]")

    def test_device_info_physical_device_name_formatting_org_name_omitted(self):
        """Test device_info name formatting with org name omitted (default for physical)."""
        self.mock_coordinator.device_name_format = "org_prefix_device_name" # This format is for org device
        # For physical devices, org name part should be ignored by format_device_name if is_org_device=False
        device_data = {"serial": "QABC", "name": "MX Firewall", "model": "MX67"}
        entity = MerakiEntity(coordinator=self.mock_coordinator, device_data=device_data)
        device_info = entity.device_info
        # format_device_name called with is_org_device=False, so org prefix shouldn't apply
        self.assertEqual(device_info["name"], "MX Firewall")


    def test_device_info_ssid_device(self):
        """Test device_info for an SSID 'device' entity."""
        # For an SSID entity, device_data and ssid_data are often the same,
        # representing the SSID itself as the HA "device".
        ssid_device_data = {
            "networkId": "N_456",
            "number": 0, # SSID number
            "name": "Guest WiFi",
            "unique_id": "N_456_0" # Assume coordinator populates this
            # model, serial, firmware are not typically part of SSID data from Meraki
        }
        # When entity is for an SSID, it's initialized with ssid_data also pointing to this
        entity = MerakiEntity(coordinator=self.mock_coordinator, device_data=ssid_device_data, ssid_data=ssid_device_data)

        device_info = entity.device_info
        self.assertIsNotNone(device_info)
        # Identifier should be based on networkId and SSID number
        self.assertEqual(device_info["identifiers"], {(DOMAIN, "N_456_0")})
        # Name, model etc. for SSID "device" are typically set when the device is registered,
        # MerakiEntity.device_info just provides the link via identifiers.
        # The actual name/model in DeviceInfo might be blank if not set during registration,
        # or could be derived. The current MerakiEntity.device_info for SSID only sets identifiers.

    def test_device_info_missing_serial_for_physical_device(self):
        """Test device_info when serial is missing for a physical device context."""
        device_data = {"name": "AP Without Serial", "model": "MR33"} # Missing "serial"
        entity = MerakiEntity(coordinator=self.mock_coordinator, device_data=device_data)

        with patch('custom_components.meraki_ha.entity._LOGGER') as mock_logger:
            device_info = entity.device_info
            self.assertIsNone(device_info)
            mock_logger.warning.assert_called_once()
            self.assertTrue("Missing serial for physical device context" in mock_logger.warning.call_args[0][0])


    def test_device_info_ssid_device_missing_networkid(self):
        """Test device_info for an SSID entity where networkId is missing."""
        ssid_device_data = {
            "number": 1,
            "name": "Orphan SSID",
            # "networkId": "N_789" // Missing networkId
            "unique_id": "orphan_1" # if unique_id was formed differently
        }
        # For an SSID entity, device_data = ssid_data
        entity = MerakiEntity(coordinator=self.mock_coordinator, device_data=ssid_device_data, ssid_data=ssid_device_data)

        with patch('custom_components.meraki_ha.entity._LOGGER') as mock_logger:
            device_info = entity.device_info
            # Falls back to physical device logic, which will fail if no serial
            self.assertIsNone(device_info)
            mock_logger.warning.assert_any_call(
                "SSID-specific entity for SSID '%s' (Number: %s) is missing 'networkId' in its data, cannot link to SSID device. Falling back to physical device linkage if possible.",
                "Orphan SSID", 1
            )


if __name__ == '__main__':
    unittest.main()
