"""Tests for the Meraki client blocker switch."""

from unittest.mock import MagicMock, AsyncMock
import pytest

from custom_components.meraki_ha.switch.meraki_client_blocker import MerakiClientBlockerSwitch

@pytest.mark.asyncio
async def test_client_blocker_switch():
    """Test the MerakiClientBlockerSwitch."""
    mock_coordinator = MagicMock()
    mock_coordinator.data = {"rules": [{"policy": "deny", "value": "192.168.1.100"}]}
    mock_coordinator.async_block_client = AsyncMock()
    mock_coordinator.async_unblock_client = AsyncMock()

    mock_config_entry = MagicMock()
    client_data = {"mac": "11:22:33:44:55:66", "ip": "192.168.1.100", "description": "Test Client"}

    # Instantiate switch
    switch = MerakiClientBlockerSwitch(mock_coordinator, mock_config_entry, client_data)
    switch.hass = MagicMock()
    switch.async_write_ha_state = MagicMock()

    # Assert properties
    assert switch.unique_id == "meraki-client-11:22:33:44:55:66-blocker"
    assert switch.is_on is True

    # Test update with no rule (not blocked)
    mock_coordinator.data = {"rules": []}
    switch._handle_coordinator_update()
    assert switch.is_on is False

    # Test methods
    await switch.async_turn_on()
    mock_coordinator.async_block_client.assert_called_once_with("192.168.1.100")

    await switch.async_turn_off()
    mock_coordinator.async_unblock_client.assert_called_once_with("192.168.1.100")

@pytest.mark.asyncio
async def test_client_blocker_switch_no_ip():
    """Test the MerakiClientBlockerSwitch with missing client IP."""
    mock_coordinator = MagicMock()
    mock_coordinator.data = {"rules": [{"policy": "deny", "value": ""}]}

    mock_config_entry = MagicMock()
    client_data = {"mac": "11:22:33:44:55:66", "description": "Test Client"}

    # Instantiate switch
    switch = MerakiClientBlockerSwitch(mock_coordinator, mock_config_entry, client_data)
    switch.hass = MagicMock()
    switch.async_write_ha_state = MagicMock()

    assert switch.is_on is False

    # Test error cases for turn_on/turn_off without IP
    with pytest.raises(Exception):
        await switch.async_turn_on()

    with pytest.raises(Exception):
        await switch.async_turn_off()
