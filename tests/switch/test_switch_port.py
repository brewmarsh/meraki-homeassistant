"""Tests for the Meraki Switch Port switch."""

from unittest.mock import AsyncMock, MagicMock
import pytest

from custom_components.meraki_ha.coordinator import MerakiDataUpdateCoordinator
from custom_components.meraki_ha.core.models.device import MerakiDevice
from custom_components.meraki_ha.switch.switch_port import MerakiSwitchPortSwitch

@pytest.fixture
def mock_coordinator(hass):
    """Mock the Meraki Data Update Coordinator."""
    coordinator = MagicMock(spec=MerakiDataUpdateCoordinator)
    coordinator.hass = hass
    coordinator.data = {"devices": []}
    coordinator.is_pending.return_value = False
    coordinator.register_pending_update = MagicMock()
    coordinator.cancel_pending_update = MagicMock()
    coordinator.api = MagicMock()
    coordinator.api.switch = MagicMock()
    coordinator.api.switch.update_device_switch_port = AsyncMock()
    return coordinator

@pytest.fixture
def mock_device():
    """Mock a Meraki device."""
    device = MagicMock(spec=MerakiDevice)
    device.serial = "Q234-5678-90AB"
    device.model = "MS120-8"
    device.status = "online"
    device.ports_statuses = [{"portId": "1", "enabled": True}]
    return device

@pytest.fixture
def mock_config_entry():
    """Mock Config Entry."""
    return MagicMock()

@pytest.fixture
def switch_port(mock_coordinator, mock_device, mock_config_entry, hass):
    """Create a switch port entity."""
    mock_coordinator.data["devices"] = [mock_device]
    entity = MerakiSwitchPortSwitch(
        mock_coordinator,
        mock_device,
        mock_device.ports_statuses[0],
        mock_config_entry,
    )
    entity.hass = hass
    entity.async_write_ha_state = MagicMock()
    return entity

@pytest.mark.asyncio
async def test_switch_port_initialization(switch_port):
    """Test that the switch initializes correctly."""
    # Matches the standardized unique_id logic: {serial}_{key}
    assert switch_port.unique_id == "Q234-5678-90AB_port_switch_1"
    assert switch_port.name == "Port 1 Enabled"
    assert switch_port.is_on is True

@pytest.mark.asyncio
async def test_switch_port_turn_off(switch_port, mock_coordinator):
    """Test turning the switch off."""
    await switch_port.async_turn_off()

    assert switch_port.is_on is False
    mock_coordinator.api.switch.update_device_switch_port.assert_called_once_with(
        serial="Q234-5678-90AB",
        port_id="1",
        enabled=False,
    )
    mock_coordinator.register_pending_update.assert_called_once()

@pytest.mark.asyncio
async def test_switch_port_turn_on(switch_port, mock_coordinator):
    """Test turning the switch on."""
    # First set it to off manually
    switch_port._attr_is_on = False

    await switch_port.async_turn_on()

    assert switch_port.is_on is True
    mock_coordinator.api.switch.update_device_switch_port.assert_called_once_with(
        serial="Q234-5678-90AB",
        port_id="1",
        enabled=True,
    )
    mock_coordinator.register_pending_update.assert_called_once()

@pytest.mark.asyncio
async def test_update_internal_state(switch_port, mock_coordinator, mock_device):
    """Test updating internal state from coordinator data."""
    # Simulate an update where port is disabled
    mock_device.ports_statuses[0]["enabled"] = False
    mock_coordinator.data["devices"] = [mock_device]

    switch_port._handle_coordinator_update()

    assert switch_port.is_on is False