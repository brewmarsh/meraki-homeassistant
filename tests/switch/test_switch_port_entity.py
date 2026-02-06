"""Tests for Meraki Switch Port switch."""

from unittest.mock import AsyncMock, MagicMock

import pytest
from homeassistant.core import HomeAssistant

from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.meraki_ha.const import DOMAIN
from custom_components.meraki_ha.switch.switch_port import MerakiSwitchPortSwitch


@pytest.fixture
def mock_meraki_client():
    """Mock the Meraki API client."""
    client = MagicMock()
    client.switch.update_device_switch_port = AsyncMock()
    return client


@pytest.fixture
def mock_coordinator(hass, mock_meraki_client):
    """Mock the Meraki data update coordinator."""
    coordinator = MagicMock()
    coordinator.hass = hass
    coordinator.api = mock_meraki_client
    coordinator.config_entry = MockConfigEntry(domain=DOMAIN, data={})

    # Mock get_device to return updated device
    coordinator.get_device = MagicMock()

    return coordinator


@pytest.fixture
def mock_device():
    """Mock a Meraki device."""
    device = MagicMock()
    device.serial = "Q2AA-1111-2222"
    device.name = "Test Switch"
    device.status = "online"
    device.model = "MS220-8P"
    device.url = "https://dashboard.meraki.com"
    return device


async def test_switch_port_switch_init(
    hass: HomeAssistant, mock_coordinator, mock_device
):
    """Test switch initialization."""
    port_data = {"portId": "1", "enabled": True, "status": "Connected"}

    switch = MerakiSwitchPortSwitch(mock_coordinator, mock_device, port_data)

    assert switch.unique_id == "Q2AA-1111-2222_port_1_switch"
    assert switch.name == "Port 1 Enabled"
    assert switch.is_on is True
    assert switch.available is True


async def test_switch_port_turn_on(hass: HomeAssistant, mock_coordinator, mock_device):
    """Test turning the switch on."""
    port_data = {"portId": "1", "enabled": False}
    switch = MerakiSwitchPortSwitch(mock_coordinator, mock_device, port_data)
    switch.hass = hass
    switch.async_write_ha_state = MagicMock()

    await switch.async_turn_on()

    assert switch.is_on is True
    mock_coordinator.api.switch.update_device_switch_port.assert_called_once_with(
        "Q2AA-1111-2222", "1", enabled=True
    )


async def test_switch_port_turn_off(hass: HomeAssistant, mock_coordinator, mock_device):
    """Test turning the switch off."""
    port_data = {"portId": "1", "enabled": True}
    switch = MerakiSwitchPortSwitch(mock_coordinator, mock_device, port_data)
    switch.hass = hass
    switch.async_write_ha_state = MagicMock()

    await switch.async_turn_off()

    assert switch.is_on is False
    mock_coordinator.api.switch.update_device_switch_port.assert_called_once_with(
        "Q2AA-1111-2222", "1", enabled=False
    )


async def test_switch_port_update(hass: HomeAssistant, mock_coordinator, mock_device):
    """Test updating the switch state from coordinator."""
    port_data = {"portId": "1", "enabled": True}
    switch = MerakiSwitchPortSwitch(mock_coordinator, mock_device, port_data)
    switch.hass = hass
    switch.async_write_ha_state = MagicMock()

    # Simulate update
    new_port_data = {"portId": "1", "enabled": False}
    mock_device.ports_statuses = [new_port_data]
    mock_coordinator.get_device.return_value = mock_device

    switch._handle_coordinator_update()

    assert switch.is_on is False
    switch.async_write_ha_state.assert_called_once()


async def test_switch_port_update_error(
    hass: HomeAssistant, mock_coordinator, mock_device
):
    """Test error handling during update."""
    port_data = {"portId": "1", "enabled": True}
    switch = MerakiSwitchPortSwitch(mock_coordinator, mock_device, port_data)
    switch.hass = hass
    switch.async_write_ha_state = MagicMock()

    mock_coordinator.api.switch.update_device_switch_port.side_effect = Exception(
        "API Error"
    )

    with pytest.raises(Exception):
        await switch.async_turn_off()

    assert switch.is_on is True  # Should revert to True
