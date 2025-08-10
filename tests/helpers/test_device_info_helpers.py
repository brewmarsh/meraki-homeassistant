"""Tests for the device info helpers."""

import pytest
from unittest.mock import MagicMock

from custom_components.meraki_ha.helpers.device_info_helpers import resolve_device_info
from custom_components.meraki_ha.const import (
    DEVICE_NAME_FORMAT_PREFIX,
    DEVICE_NAME_FORMAT_SUFFIX,
    DEVICE_NAME_FORMAT_OMIT,
    DEFAULT_DEVICE_NAME_FORMAT,
)


@pytest.fixture
def mock_config_entry():
    """Fixture for a mocked config entry."""
    entry = MagicMock()
    entry.options = {}
    return entry


def test_resolve_device_info_ssid_naming(mock_config_entry):
    """Test that SSID device names are formatted correctly."""
    entity_data = {"networkId": "net1"}
    ssid_data = {"number": 1, "name": "My Test SSID"}

    # Test with prefix
    mock_config_entry.options = {"device_name_format": DEVICE_NAME_FORMAT_PREFIX}
    device_info = resolve_device_info(entity_data, mock_config_entry, ssid_data)
    assert device_info["name"] == "[Ssid] My Test SSID"

    # Test with suffix
    mock_config_entry.options = {"device_name_format": DEVICE_NAME_FORMAT_SUFFIX}
    device_info = resolve_device_info(entity_data, mock_config_entry, ssid_data)
    assert device_info["name"] == "My Test SSID [Ssid]"

    # Test with omit
    mock_config_entry.options = {"device_name_format": DEVICE_NAME_FORMAT_OMIT}
    device_info = resolve_device_info(entity_data, mock_config_entry, ssid_data)
    assert device_info["name"] == "My Test SSID"

    # Test with default
    mock_config_entry.options = {}
    device_info = resolve_device_info(entity_data, mock_config_entry, ssid_data)
    assert device_info["name"] == "[Ssid] My Test SSID"


def test_resolve_device_info_physical_device_naming(mock_config_entry):
    """Test that physical device names are formatted correctly."""
    entity_data = {
        "serial": "dev1",
        "name": "My Test Device",
        "productType": "switch",
    }

    # Test with prefix
    mock_config_entry.options = {"device_name_format": DEVICE_NAME_FORMAT_PREFIX}
    device_info = resolve_device_info(entity_data, mock_config_entry)
    assert device_info["name"] == "[Switch] My Test Device"

    # Test with suffix
    mock_config_entry.options = {"device_name_format": DEVICE_NAME_FORMAT_SUFFIX}
    device_info = resolve_device_info(entity_data, mock_config_entry)
    assert device_info["name"] == "My Test Device [Switch]"

    # Test with omit
    mock_config_entry.options = {"device_name_format": DEVICE_NAME_FORMAT_OMIT}
    device_info = resolve_device_info(entity_data, mock_config_entry)
    assert device_info["name"] == "My Test Device"


def test_resolve_device_info_appliance_hostname(mock_config_entry):
    """Test that the hostname is added for an appliance."""
    entity_data = {
        "serial": "dev_appliance",
        "name": "My Appliance",
        "productType": "appliance",
        "dynamicDns": {
            "url": "my-appliance.dynamic.meraki.com"
        }
    }
    mock_config_entry.options = {}
    device_info = resolve_device_info(entity_data, mock_config_entry)
    assert device_info["configuration_url"] == "http://my-appliance.dynamic.meraki.com"
