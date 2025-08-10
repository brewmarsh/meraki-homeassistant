"""Tests for the Meraki radio settings sensor."""

import pytest
from unittest.mock import MagicMock

from custom_components.meraki_ha.sensor.device.radio_settings import MerakiRadioSettingsSensor
from custom_components.meraki_ha.const import DEVICE_NAME_FORMAT_PREFIX

@pytest.fixture
def mock_coordinator():
    """Fixture for a mocked MerakiDataCoordinator."""
    coordinator = MagicMock()
    coordinator.config_entry.options = {"device_name_format": DEVICE_NAME_FORMAT_PREFIX}
    coordinator.data = {
        "devices": [
            {
                "serial": "dev_wireless",
                "name": "Test AP",
                "model": "MR52",
                "productType": "wireless",
                "networkId": "net1",
                "radio_settings": {
                    "channel": 11,
                    "power": 20,
                }
            }
        ],
    }
    return coordinator


def test_radio_settings_sensor(mock_coordinator):
    """Test the radio settings sensor."""
    device = mock_coordinator.data["devices"][0]
    sensor = MerakiRadioSettingsSensor(mock_coordinator, device)

    # Test basic sensor properties
    assert sensor.unique_id == "dev_wireless_radio_settings"
    assert sensor.name == "Test AP Radio Settings"
    assert sensor.native_value == "11"

    # Test device_info from the helper
    device_info = sensor.device_info
    assert device_info["name"] == "[Wireless] Test AP"
    assert device_info["model"] == "MR52"
    assert device_info["identifiers"] == {("meraki_ha", "dev_wireless")}

    # Test extra attributes
    assert sensor.extra_state_attributes["power"] == 20
