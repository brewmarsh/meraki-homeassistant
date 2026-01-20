"""Tests for the switch port cycle button."""

from unittest.mock import AsyncMock, MagicMock

import pytest
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant

from custom_components.meraki_ha.button.device.switch_port_cycle import (
    MerakiSwitchPortCycleButton,
)
from custom_components.meraki_ha.types import MerakiDevice

@pytest.fixture
def mock_service():
    """Mock the switch port service."""
    service = AsyncMock()
    service.async_cycle_port = AsyncMock()
    return service

@pytest.fixture
def mock_device():
    """Mock the Meraki device."""
    return MerakiDevice.from_dict({
        "serial": "Q234-5678-90AB",
        "name": "Test Switch",
        "productType": "switch",
        "model": "MS120-8",
    })

@pytest.fixture
def mock_config_entry():
    """Mock the config entry."""
    entry = MagicMock()
    entry.options = {CONF_NAME: "Meraki"}
    return entry

async def test_button_setup(
    mock_service, mock_device, mock_config_entry
):
    """Test button setup."""
    port_id = "1"
    port_info = {"portId": "1", "enabled": True}

    button = MerakiSwitchPortCycleButton(
        mock_service, mock_device, mock_config_entry, port_id, port_info
    )

    assert button.unique_id == "Q234-5678-90AB_cycle_port_1"
    # The name formatting depends on config options, assuming standard behavior here.
    assert "Cycle Port 1" in button.name

    assert button.device_info["identifiers"] == {("meraki_ha", "Q234-5678-90AB")}

async def test_button_press(
    mock_service, mock_device, mock_config_entry
):
    """Test button press."""
    port_id = "1"
    port_info = {"portId": "1", "enabled": True}

    button = MerakiSwitchPortCycleButton(
        mock_service, mock_device, mock_config_entry, port_id, port_info
    )

    await button.async_press()

    mock_service.async_cycle_port.assert_called_once_with(
        "Q234-5678-90AB", "1"
    )
