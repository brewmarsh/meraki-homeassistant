"""Test the Meraki switch port cycle button."""

import asyncio
from unittest.mock import AsyncMock, MagicMock

import pytest
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from custom_components.meraki_ha.button.device.switch_port_cycle import (
    MerakiSwitchPortCycleButton,
)
from custom_components.meraki_ha.services.switch_port_service import SwitchPortService
from custom_components.meraki_ha.types import MerakiDevice


@pytest.fixture
def mock_service():
    """Mock the SwitchPortService."""
    service = MagicMock(spec=SwitchPortService)
    service.async_cycle_ports = AsyncMock()
    return service


@pytest.fixture
def mock_device():
    """Mock a MerakiDevice."""
    return MerakiDevice(
        serial="Q2XX-XXXX-XXXX",
        name="Test Switch",
        model="MS120-8",
        mac="00:11:22:33:44:55",
        product_type="switch",
        ports_statuses=[
            {"portId": "1", "enabled": True, "status": "Connected"},
            {"portId": "2", "enabled": True, "status": "Disconnected"},
        ],
    )


@pytest.fixture
def mock_config_entry():
    """Mock a ConfigEntry."""
    entry = MagicMock(spec=ConfigEntry)
    entry.entry_id = "test_entry_id"
    entry.options = {}
    return entry


async def test_button_initialization(
    hass: HomeAssistant,
    mock_service: SwitchPortService,
    mock_device: MerakiDevice,
    mock_config_entry: ConfigEntry,
):
    """Test the button initialization."""
    port_info = mock_device.ports_statuses[0]
    button = MerakiSwitchPortCycleButton(
        mock_service, mock_device, port_info, mock_config_entry
    )

    assert button.name == "Test Switch Port 1 Cycle"
    assert button.unique_id == "Q2XX-XXXX-XXXX_port_1_cycle"
    assert button.icon == "mdi:restart"
    assert button.device_info["identifiers"] == {("meraki_ha", "Q2XX-XXXX-XXXX")}


async def test_button_press(
    hass: HomeAssistant,
    mock_service: SwitchPortService,
    mock_device: MerakiDevice,
    mock_config_entry: ConfigEntry,
):
    """Test the button press action."""
    port_info = mock_device.ports_statuses[0]
    button = MerakiSwitchPortCycleButton(
        mock_service, mock_device, port_info, mock_config_entry
    )

    await button.async_press()

    mock_service.async_cycle_ports.assert_called_once_with(
        "Q2XX-XXXX-XXXX", ["1"]
    )
