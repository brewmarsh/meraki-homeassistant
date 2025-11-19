"""Test Meraki AP LED switch."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from custom_components.meraki_ha.switch.access_point_leds import MerakiAPLEDSwitch


@pytest.fixture
def mock_coordinator():
    """Mock the MerakiDataCoordinator."""
    coordinator = AsyncMock()
    coordinator.data = {
        "wireless_settings": {
            "N_12345": {"ledLightsOn": True},
        }
    }
    coordinator.is_pending = MagicMock(return_value=False)
    coordinator.register_pending_update = MagicMock()
    return coordinator


@pytest.fixture
def mock_config_entry():
    """Mock the ConfigEntry."""
    entry = AsyncMock()
    entry.options = {}
    return entry


@pytest.fixture
def mock_network():
    """Mock a Meraki network."""
    return {"id": "N_12345", "name": "Test Network", "productTypes": ["wireless"]}


async def test_switch_state(mock_coordinator, mock_config_entry, mock_network):
    """Test the switch state."""
    switch = MerakiAPLEDSwitch(mock_coordinator, mock_config_entry, mock_network)
    assert switch.is_on is True
    assert switch.available is True


async def test_switch_turn_on(mock_coordinator, mock_config_entry, mock_network):
    """Test turning the switch on."""
    switch = MerakiAPLEDSwitch(mock_coordinator, mock_config_entry, mock_network)
    with (
        patch.object(
            switch.coordinator.api.wireless, "update_network_wireless_settings"
        ) as mock_update,
        patch.object(switch, "async_write_ha_state") as mock_write_state,
    ):
        await switch.async_turn_on()
        mock_update.assert_called_once_with(network_id="N_12345", ledLightsOn=True)
        mock_write_state.assert_called_once()
        mock_coordinator.register_pending_update.assert_called_once()


async def test_switch_turn_off(mock_coordinator, mock_config_entry, mock_network):
    """Test turning the switch off."""
    switch = MerakiAPLEDSwitch(mock_coordinator, mock_config_entry, mock_network)
    with (
        patch.object(
            switch.coordinator.api.wireless, "update_network_wireless_settings"
        ) as mock_update,
        patch.object(switch, "async_write_ha_state") as mock_write_state,
    ):
        await switch.async_turn_off()
        mock_update.assert_called_once_with(network_id="N_12345", ledLightsOn=False)
        mock_write_state.assert_called_once()
        mock_coordinator.register_pending_update.assert_called_once()
