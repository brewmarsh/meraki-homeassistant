"""Tests for Meraki Appliance Port switch."""

from unittest.mock import AsyncMock, MagicMock

import pytest
from homeassistant.core import HomeAssistant

from custom_components.meraki_ha.core.models.appliance import MerakiAppliancePort
from custom_components.meraki_ha.switch.switch_port import MerakiAppliancePortSwitch


@pytest.fixture
def mock_meraki_client():
    """Mock the Meraki API client."""
    client = MagicMock()
    client.dashboard = MagicMock()
    client.run_sync = AsyncMock()
    # Mock the appliance endpoints wrapper
    client.appliance = MagicMock()
    client.appliance.update_network_appliance_port = AsyncMock()
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
    coordinator.is_pending = MagicMock(return_value=False)
    coordinator.register_pending_update = MagicMock()
    coordinator.get_device = MagicMock()
    return coordinator


@pytest.fixture
def mock_device():
    """Mock a MerakiDevice."""
    device = MagicMock()
    device.serial = "Q2AA-BB33-CC44"
    device.network_id = "N_12345"
    device.status = "online"
    device.appliance_ports = [
        MerakiAppliancePort(number=1, enabled=True),
        MerakiAppliancePort(number=2, enabled=False),
    ]
    return device


@pytest.fixture
def mock_config_entry():
    """Mock a ConfigEntry."""
    entry = MagicMock()
    entry.options = {}
    return entry


@pytest.mark.asyncio
async def test_appliance_port_switch_init(
    hass: HomeAssistant,
    mock_coordinator,
    mock_device,
    mock_config_entry,
):
    """Test initialization of the appliance port switch."""
    port = MerakiAppliancePort(number=1, enabled=True)
    switch = MerakiAppliancePortSwitch(
        mock_coordinator, mock_device, port, mock_config_entry
    )
    switch.hass = hass

    assert switch.unique_id == "Q2AA-BB33-CC44_port_switch_1"
    assert switch.name == "Port 1 enabled"
    assert switch.is_on is True


@pytest.mark.asyncio
async def test_appliance_port_switch_turn_off(
    hass: HomeAssistant,
    mock_coordinator,
    mock_device,
    mock_config_entry,
):
    """Test turning the appliance port switch off."""
    port = MerakiAppliancePort(number=1, enabled=True)
    switch = MerakiAppliancePortSwitch(
        mock_coordinator, mock_device, port, mock_config_entry
    )
    switch.hass = hass
    switch.async_write_ha_state = MagicMock()  # type: ignore[method-assign]

    await switch.async_turn_off()

    # Verify API call
    mock_coordinator.api.appliance.update_network_appliance_port.assert_called_once_with(
        network_id="N_12345",
        port_id="1",
        enabled=False,
    )

    # Verify optimistic update
    assert switch.is_on is False
    mock_coordinator.register_pending_update.assert_called_once()


@pytest.mark.asyncio
async def test_appliance_port_switch_turn_on(
    hass: HomeAssistant,
    mock_coordinator,
    mock_device,
    mock_config_entry,
):
    """Test turning the appliance port switch on."""
    port = MerakiAppliancePort(number=2, enabled=False)
    switch = MerakiAppliancePortSwitch(
        mock_coordinator, mock_device, port, mock_config_entry
    )
    switch.hass = hass
    switch.async_write_ha_state = MagicMock()  # type: ignore[method-assign]

    await switch.async_turn_on()

    # Verify API call
    mock_coordinator.api.appliance.update_network_appliance_port.assert_called_once_with(
        network_id="N_12345",
        port_id="2",
        enabled=True,
    )

    # Verify optimistic update
    assert switch.is_on is True
    mock_coordinator.register_pending_update.assert_called_once()


@pytest.mark.asyncio
async def test_appliance_port_switch_update(
    hass: HomeAssistant,
    mock_coordinator,
    mock_device,
    mock_config_entry,
):
    """Test updating the appliance port switch from coordinator data."""
    port = MerakiAppliancePort(number=1, enabled=True)
    switch = MerakiAppliancePortSwitch(
        mock_coordinator, mock_device, port, mock_config_entry
    )
    switch.hass = hass
    switch.async_write_ha_state = MagicMock()  # type: ignore[method-assign]

    # Simulate update with new data (disabled)
    new_device = MagicMock()
    new_device.serial = "Q2AA-BB33-CC44"
    new_device.appliance_ports = [MerakiAppliancePort(number=1, enabled=False)]
    mock_coordinator.get_device.return_value = new_device

    switch._handle_coordinator_update()

    assert switch.is_on is False
