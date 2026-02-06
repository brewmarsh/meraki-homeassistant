"""Tests for Meraki Switch Port Switch."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from custom_components.meraki_ha.switch.switch_port import MerakiSwitchPortSwitch


@pytest.fixture
def mock_coordinator():
    """Mock the Meraki Data Update Coordinator."""
    coordinator = MagicMock()
    coordinator.api = MagicMock()
    coordinator.api.switch = MagicMock()
    coordinator.api.switch.update_device_switch_port = AsyncMock()
    coordinator.is_pending.return_value = False
    coordinator.register_pending_update = MagicMock()
    coordinator.data = {"devices": []}
    return coordinator

@pytest.fixture
def mock_device():
    """Mock Meraki Device."""
    device = MagicMock()
    device.serial = "Q2AA-BBBB-CCCC"
    device.status = "online"
    device.ports_statuses = []
    return device

@pytest.fixture
def mock_config_entry():
    """Mock Config Entry."""
    return MagicMock()

@pytest.mark.asyncio
async def test_meraki_switch_port_switch_initialization(
    mock_coordinator, mock_device, mock_config_entry
):
    """Test switch initialization."""
    port_data = {"portId": "1", "enabled": True}

    switch = MerakiSwitchPortSwitch(
        mock_coordinator, mock_device, port_data, mock_config_entry
    )

    assert switch.unique_id == "Q2AA-BBBB-CCCC_port_1_enabled"
    assert switch.name == "Port 1"
    assert switch.is_on is True
    assert switch.available is True

@pytest.mark.asyncio
async def test_meraki_switch_port_switch_turn_off(
    mock_coordinator, mock_device, mock_config_entry
):
    """Test turning the switch off."""
    port_data = {"portId": "1", "enabled": True}

    switch = MerakiSwitchPortSwitch(
        mock_coordinator, mock_device, port_data, mock_config_entry
    )
    # Mock hass for async_write_ha_state
    switch.hass = MagicMock()
    switch.async_write_ha_state = MagicMock()

    await switch.async_turn_off()

    # Check if API called
    mock_coordinator.api.switch.update_device_switch_port.assert_called_once_with(
        serial="Q2AA-BBBB-CCCC", port_id="1", enabled=False
    )

    # Check optimistic update
    assert switch.is_on is False

    # Check pending update registration
    mock_coordinator.register_pending_update.assert_called_once_with(
        "Q2AA-BBBB-CCCC_port_1_enabled"
    )

@pytest.mark.asyncio
async def test_meraki_switch_port_switch_turn_on(
    mock_coordinator, mock_device, mock_config_entry
):
    """Test turning the switch on."""
    port_data = {"portId": "1", "enabled": False}

    switch = MerakiSwitchPortSwitch(
        mock_coordinator, mock_device, port_data, mock_config_entry
    )
    # Mock hass for async_write_ha_state
    switch.hass = MagicMock()
    switch.async_write_ha_state = MagicMock()

    await switch.async_turn_on()

    # Check if API called
    mock_coordinator.api.switch.update_device_switch_port.assert_called_once_with(
        serial="Q2AA-BBBB-CCCC", port_id="1", enabled=True
    )

    # Check optimistic update
    assert switch.is_on is True

@pytest.mark.asyncio
async def test_meraki_switch_port_switch_update_from_coordinator(
    mock_coordinator, mock_device, mock_config_entry
):
    """Test updating state from coordinator data."""
    port_data = {"portId": "1", "enabled": True}

    switch = MerakiSwitchPortSwitch(
        mock_coordinator, mock_device, port_data, mock_config_entry
    )
    switch.hass = MagicMock()
    switch.async_write_ha_state = MagicMock()

    # Mock update
    new_port_data = {"portId": "1", "enabled": False}
    updated_device = MagicMock()
    updated_device.serial = "Q2AA-BBBB-CCCC"
    updated_device.ports_statuses = [new_port_data]
    mock_coordinator.data = {"devices": [updated_device]}

    switch._handle_coordinator_update()

    assert switch.is_on is False
