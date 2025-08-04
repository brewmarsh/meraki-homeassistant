"""Tests for the Meraki device tracker."""

from unittest.mock import MagicMock

from homeassistant.core import HomeAssistant

from custom_components.meraki_ha.device_tracker import (
    async_setup_entry,
)


async def test_async_setup_entry(
    hass: HomeAssistant,
) -> None:
    """Test the async_setup_entry function."""
    config_entry = MagicMock()
    config_entry.entry_id = "test_entry_id"
    async_add_entities = MagicMock()
    coordinator = MagicMock()
    coordinator.data = {
        "clients": [
            {"id": "1", "description": "Client 1", "mac": "00:00:00:00:00:01"},
            {"id": "2", "description": "Client 2", "mac": "00:00:00:00:00:02"},
        ]
    }
    hass.data["meraki_ha"] = {config_entry.entry_id: {"coordinator": coordinator}}
    await async_setup_entry(hass, config_entry, async_add_entities)
    assert async_add_entities.call_count == 1
