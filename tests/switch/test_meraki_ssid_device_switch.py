"""Tests for the Meraki SSID device switch."""

from unittest.mock import MagicMock

from homeassistant.core import HomeAssistant

from custom_components.meraki_ha.core.switch.meraki_ssid_device_switch import (
    MerakiSSIDEnabledSwitch,
    MerakiSSIDBroadcastSwitch,
)


async def test_meraki_ssid_enabled_switch(
    hass: HomeAssistant,
) -> None:
    """Test the Meraki SSID enabled switch."""
    coordinator = MagicMock()
    coordinator.data = {
        "ssid_0": {
            "number": 0,
            "name": "Test SSID",
            "enabled": True,
        }
    }
    meraki_client = MagicMock()
    config_entry = MagicMock()
    ssid_data = {
        "number": 0,
        "name": "Test SSID",
        "unique_id": "ssid_0",
    }
    switch = MerakiSSIDEnabledSwitch(
        coordinator, meraki_client, config_entry, "ssid_0", ssid_data
    )
    switch._update_internal_state()
    assert switch.is_on is True


async def test_meraki_ssid_broadcast_switch(
    hass: HomeAssistant,
) -> None:
    """Test the Meraki SSID broadcast switch."""
    coordinator = MagicMock()
    coordinator.data = {
        "ssid_0": {
            "number": 0,
            "name": "Test SSID",
            "visible": True,
        }
    }
    meraki_client = MagicMock()
    config_entry = MagicMock()
    ssid_data = {
        "number": 0,
        "name": "Test SSID",
        "unique_id": "ssid_0",
    }
    switch = MerakiSSIDBroadcastSwitch(
        coordinator, meraki_client, config_entry, "ssid_0", ssid_data
    )
    switch._update_internal_state()
    assert switch.is_on is True
