"""Tests for the Meraki VPN switch."""

import pytest
from unittest.mock import MagicMock, AsyncMock

from custom_components.meraki_ha.switch.setup_helpers import async_setup_switches
from custom_components.meraki_ha.const import (
    CONF_ENABLE_VPN,
)


@pytest.fixture
def mock_coordinator():
    """Fixture for a mocked MerakiDataUpdateCoordinator."""
    coordinator = MagicMock()
    coordinator.config_entry = MagicMock()
    coordinator.config_entry.options = {
        "device_name_format": "omit",
        CONF_ENABLE_VPN: True,
    }
    coordinator.data = {
        "networks": [
            {"id": "net1", "name": "Test Network", "productTypes": ["appliance"]}
        ],
        "vpn_status": {"net1": {"mode": "hub"}},
    }
    coordinator.is_pending.return_value = False
    coordinator.api = MagicMock()
    coordinator.api.appliance.update_vpn_status = AsyncMock()
    return coordinator


def test_vpn_switch_creation(mock_coordinator):
    """Test that the VPN switch is created correctly."""
    hass = MagicMock()

    # Run the setup
    switches = async_setup_switches(
        hass, mock_coordinator.config_entry, mock_coordinator
    )

    # Find the specific switch
    vpn_switch = next(s for s in switches if "VPN" in s.name)

    # Assertions for VPN Switch
    assert vpn_switch.unique_id == "vpn_net1"
    assert vpn_switch.name == "Test Network Site-to-Site VPN"
    assert vpn_switch.is_on is True


@pytest.mark.asyncio
async def test_vpn_switch_turn_off(mock_coordinator):
    """Test turning off the VPN switch."""
    hass = MagicMock()
    switches = async_setup_switches(
        hass, mock_coordinator.config_entry, mock_coordinator
    )
    vpn_switch = next(s for s in switches if "VPN" in s.name)
    vpn_switch.hass = hass

    await vpn_switch.async_turn_off()

    mock_coordinator.api.appliance.update_vpn_status.assert_called_once_with(
        network_id="net1", mode="disabled"
    )


@pytest.mark.asyncio
async def test_vpn_switch_turn_on(mock_coordinator):
    """Test turning on the VPN switch."""
    hass = MagicMock()
    # Set initial state to off
    mock_coordinator.data["vpn_status"]["net1"]["mode"] = "disabled"
    switches = async_setup_switches(
        hass, mock_coordinator.config_entry, mock_coordinator
    )
    vpn_switch = next(s for s in switches if "VPN" in s.name)
    vpn_switch.hass = hass

    await vpn_switch.async_turn_on()

    mock_coordinator.api.appliance.update_vpn_status.assert_called_once_with(
        network_id="net1", mode="hub"
    )
