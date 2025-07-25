"""Tests for the Meraki SSID name text entity."""

from unittest.mock import MagicMock

from homeassistant.core import HomeAssistant

from custom_components.meraki_ha.text.meraki_ssid_name import (
    MerakiSSIDNameText,
)


async def test_meraki_ssid_name_text(
    hass: HomeAssistant,
) -> None:
    """Test the Meraki SSID name text entity."""
    coordinator = MagicMock()
    coordinator.data = {
        "ssid_0": {
            "number": 0,
            "name": "Test SSID",
        }
    }
    meraki_client = MagicMock()
    config_entry = MagicMock()
    ssid_data = {
        "number": 0,
        "name": "Test SSID",
        "unique_id": "ssid_0",
    }
    text = MerakiSSIDNameText(
        coordinator, meraki_client, config_entry, "ssid_0", ssid_data
    )
    text._update_internal_state()
    assert text.native_value == "Test SSID"
