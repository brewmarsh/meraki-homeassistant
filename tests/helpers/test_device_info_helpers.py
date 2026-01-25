"""Tests for the device_info_helpers module."""

from unittest.mock import MagicMock

import pytest

from custom_components.meraki_ha.const import (
    DOMAIN,
)
from custom_components.meraki_ha.helpers.device_info_helpers import resolve_device_info


@pytest.fixture
def mock_config_entry():
    """Fixture for a mocked config entry."""
    return MagicMock()


def test_resolve_device_info_ssid_naming(mock_config_entry):
    """Test that SSID device names are formatted correctly."""
    ssid_data = {"number": 1, "name": "My Test SSID", "networkId": "net1"}

    device_info = resolve_device_info(
        entity_data=ssid_data, config_entry=mock_config_entry
    )
    assert device_info["name"] == "My Test SSID"
    assert device_info["identifiers"] == {(DOMAIN, "net1_1")}


def test_resolve_device_info_physical_device(mock_config_entry):
    """Test that physical device info is resolved correctly."""
    device_data = {
        "serial": "Q234-ABCD-5678",
        "model": "MR33",
        "name": "Living Room AP",
        "firmware": "29.1.1",
        "productType": "wireless",
    }
    device_info = resolve_device_info(
        entity_data=device_data, config_entry=mock_config_entry
    )
    assert device_info["name"] == "[Wireless] Living Room AP"
    assert device_info["identifiers"] == {(DOMAIN, "Q234-ABCD-5678")}
    assert device_info["model"] == "MR33"
    assert device_info["sw_version"] == "29.1.1"
