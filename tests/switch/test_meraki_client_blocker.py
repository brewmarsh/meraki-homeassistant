"""Tests for the Meraki client blocker switch."""

from unittest.mock import AsyncMock, MagicMock

import pytest
from homeassistant.exceptions import HomeAssistantError

from custom_components.meraki_ha.switch.meraki_client_blocker import (
    MerakiClientBlockerSwitch,
)


@pytest.mark.asyncio
async def test_client_blocker_switch():
    """Test the MerakiClientBlockerSwitch."""
    mock_coordinator = MagicMock()
    mock_coordinator.is_pending.return_value = False
    mock_coordinator.data = {
        "clients": [{"mac": "11:22:33:44:55:66", "devicePolicy": "Blocked"}]
    }
    mock_coordinator.async_block_client = AsyncMock()
    mock_coordinator.async_unblock_client = AsyncMock()

    mock_config_entry = MagicMock()
    client_data = {
        "mac": "11:22:33:44:55:66",
        "ip": "192.168.1.100",
        "description": "Test Client",
        "networkId": "N_123",
        "devicePolicy": "Blocked",
    }

    # Instantiate switch
    switch = MerakiClientBlockerSwitch(mock_coordinator, mock_config_entry, client_data)
    switch.hass = MagicMock()
    switch.async_write_ha_state = MagicMock()

    # Assert properties
    assert switch.unique_id == "meraki-client-11:22:33:44:55:66-blocker"
    # Blocked policy means switch is OFF (Internet Access OFF)
    assert switch.is_on is False

    # Test update with normal policy (not blocked) -> switch is ON
    mock_coordinator.data = {
        "clients": [{"mac": "11:22:33:44:55:66", "devicePolicy": "Normal"}]
    }
    switch._handle_coordinator_update()
    assert switch.is_on is True

    # Test methods
    await switch.async_turn_on()
    mock_coordinator.async_unblock_client.assert_called_once_with(
        "11:22:33:44:55:66", "N_123"
    )

    await switch.async_turn_off()
    mock_coordinator.async_block_client.assert_called_once_with(
        "11:22:33:44:55:66", "N_123"
    )


@pytest.mark.asyncio
async def test_client_blocker_switch_no_network_id():
    """Test the MerakiClientBlockerSwitch with missing network ID."""
    mock_coordinator = MagicMock()
    mock_coordinator.is_pending.return_value = False
    mock_coordinator.data = {"clients": []}

    mock_config_entry = MagicMock()
    client_data = {"mac": "11:22:33:44:55:66", "description": "Test Client"}

    # Instantiate switch
    switch = MerakiClientBlockerSwitch(mock_coordinator, mock_config_entry, client_data)
    switch.hass = MagicMock()
    switch.async_write_ha_state = MagicMock()

    # If policy is unknown, it defaults to Normal -> is_on is True
    assert switch.is_on is True

    # Test error cases for turn_on/turn_off without networkId
    with pytest.raises(HomeAssistantError):
        await switch.async_turn_on()

    with pytest.raises(HomeAssistantError):
        await switch.async_turn_off()
