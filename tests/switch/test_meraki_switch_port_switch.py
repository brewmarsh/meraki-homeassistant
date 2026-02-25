"""Tests for Meraki Switch Port switch."""

from unittest.mock import AsyncMock, MagicMock

import pytest
from homeassistant.core import HomeAssistant

from custom_components.meraki_ha.switch.switch_port import MerakiSwitchPortToggle


@pytest.fixture
def mock_meraki_client():
    """Mock the Meraki API client."""
    client = MagicMock()
    client.dashboard = MagicMock()
    # Ensure run_sync is a proper AsyncMock for await expressions
    client.run_sync = AsyncMock()
    # Mock the switch endpoints wrapper
    client.switch = MagicMock()
    client.switch.update_device_switch_port = AsyncMock()
    return client


@pytest.fixture
def mock_coordinator(hass, mock_meraki_client):
    """Mock the Meraki Data Coordinator."""
    coordinator = MagicMock()
    coordinator.hass = hass
    coordinator.api = mock_meraki_client
    coordinator.data = {
        "devices": [],
    }
    # Mock is_pending to return False by default
    coordinator.is_pending = MagicMock(return_value=False)
    # Mock register_pending_update
    coordinator.register_pending_update = MagicMock()
    return coordinator


@pytest.fixture
def mock_device():
    """Mock a MerakiDevice."""
    device = MagicMock()
    device.serial = "Q2AA-BB33-CC44"
    device.status = "online"
    device.switch_ports = [
        {"portId": "1", "enabled": True},
        {"portId": "2", "enabled": False},
    ]
    return device


@pytest.fixture
def mock_config_entry():
    """Mock a ConfigEntry."""
    entry = MagicMock()
    return entry


@pytest.mark.asyncio
async def test_switch_port_init(
    hass: HomeAssistant,
    mock_coordinator,
    mock_device,
    mock_config_entry,
):
    """Test initialization of the switch."""
    port_data = {"portId": "1", "enabled": True}
    switch = MerakiSwitchPortToggle(
        mock_coordinator, mock_device, port_data, mock_config_entry
    )
    switch.hass = hass

    assert switch.unique_id == "Q2AA-BB33-CC44_port_switch_1"
    assert switch.name == "Port 1 enabled"
    assert switch.is_on is True


@pytest.mark.asyncio
async def test_switch_port_turn_off(
    hass: HomeAssistant,
    mock_coordinator,
    mock_device,
    mock_config_entry,
):
    """Test turning the switch off."""
    port_data = {"portId": "1", "enabled": True}
    switch = MerakiSwitchPortToggle(
        mock_coordinator, mock_device, port_data, mock_config_entry
    )
    switch.hass = hass
    switch.async_write_ha_state = MagicMock()  # type: ignore[method-assign]

    await switch.async_turn_off()

    # Verify API call
    mock_coordinator.api.switch.update_device_switch_port.assert_called_once_with(
        serial="Q2AA-BB33-CC44",
        port_id="1",
        enabled=False,
    )

    # Verify optimistic update
    assert switch.is_on is False
    mock_coordinator.register_pending_update.assert_called_once()


@pytest.mark.asyncio
async def test_switch_port_turn_on(
    hass: HomeAssistant,
    mock_coordinator,
    mock_device,
    mock_config_entry,
):
    """Test turning the switch on."""
    port_data = {"portId": "2", "enabled": False}
    switch = MerakiSwitchPortToggle(
        mock_coordinator, mock_device, port_data, mock_config_entry
    )
    switch.hass = hass
    switch.async_write_ha_state = MagicMock()  # type: ignore[method-assign]

    await switch.async_turn_on()

    # Verify API call
    mock_coordinator.api.switch.update_device_switch_port.assert_called_once_with(
        serial="Q2AA-BB33-CC44",
        port_id="2",
        enabled=True,
    )

    # Verify optimistic update
    assert switch.is_on is True
    mock_coordinator.register_pending_update.assert_called_once()


@pytest.mark.asyncio
async def test_switch_port_update(
    hass: HomeAssistant,
    mock_coordinator,
    mock_device,
    mock_config_entry,
):
    """Test updating the switch from coordinator data."""
    port_data = {"portId": "1", "enabled": True}
    switch = MerakiSwitchPortToggle(
        mock_coordinator, mock_device, port_data, mock_config_entry
    )
    switch.hass = hass
    switch.async_write_ha_state = MagicMock()  # type: ignore[method-assign]

    # Simulate update with new data (disabled)
    mock_device.switch_ports = [{"portId": "1", "enabled": False}]
    mock_coordinator.data["devices"] = [mock_device]

    switch._handle_coordinator_update()

    assert switch.is_on is False


@pytest.mark.asyncio
async def test_switch_port_update_pending(
    hass: HomeAssistant,
    mock_coordinator,
    mock_device,
    mock_config_entry,
):
    """Test updating the switch when pending update is active."""
    port_data = {"portId": "1", "enabled": True}
    switch = MerakiSwitchPortToggle(
        mock_coordinator, mock_device, port_data, mock_config_entry
    )
    switch.hass = hass
    switch.async_write_ha_state = MagicMock()  # type: ignore[method-assign]

    # Mock pending update
    mock_coordinator.is_pending.return_value = True

    # Simulate update with new data (disabled)
    mock_device.switch_ports = [{"portId": "1", "enabled": False}]
    mock_coordinator.data["devices"] = [mock_device]

    switch._handle_coordinator_update()

    # Should still be True because pending
    assert switch.is_on is True


@pytest.mark.asyncio
async def test_switch_port_update_error(
    hass: HomeAssistant,
    mock_coordinator,
    mock_device,
    mock_config_entry,
):
    """Test error handling during update."""
    port_data = {"portId": "1", "enabled": True}
    switch = MerakiSwitchPortToggle(
        mock_coordinator, mock_device, port_data, mock_config_entry
    )
    switch.hass = hass
    switch.async_write_ha_state = MagicMock()  # type: ignore[method-assign]

    mock_coordinator.api.switch.update_device_switch_port.side_effect = RuntimeError(
        "API Error"
    )

    with pytest.raises(RuntimeError):
        await switch.async_turn_off()

    # State in UI was changed optimistically to False, but should be reverted
    # to True on failure
    assert switch.is_on is True
