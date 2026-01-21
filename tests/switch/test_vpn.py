"""Tests for the Meraki VPN switch."""

from unittest.mock import AsyncMock, MagicMock

import pytest
from homeassistant.const import STATE_OFF, STATE_ON
from homeassistant.core import HomeAssistant

from custom_components.meraki_ha.const import (
    CONF_ENABLE_VPN_MANAGEMENT,
    DOMAIN,
)
from custom_components.meraki_ha.types import MerakiVpn

from tests.const import MOCK_NETWORK


@pytest.fixture
def mock_vpn_status():
    """Mock VPN status data."""
    return MerakiVpn(mode="hub", hubs=[], subnets=[])


@pytest.mark.asyncio
async def test_vpn_switch(
    hass: HomeAssistant,
    mock_coordinator,
    mock_vpn_status,
):
    """Test the VPN switch entity."""
    # Setup the coordinator with VPN status
    coordinator = mock_coordinator
    coordinator.data["vpn_status"] = {MOCK_NETWORK.id: mock_vpn_status}
    coordinator.is_pending.return_value = False
    coordinator.api.appliance.update_vpn_status = AsyncMock()

    # Setup the config entry with VPN management enabled
    config_entry = MagicMock()
    config_entry.options = {CONF_ENABLE_VPN_MANAGEMENT: True}
    coordinator.config_entry = config_entry

    # Create the switch
    from custom_components.meraki_ha.switch.vpn import MerakiVPNSwitch

    switch = MerakiVPNSwitch(coordinator, config_entry, MOCK_NETWORK)
    switch.hass = hass
    # Mock async_write_ha_state to prevent errors
    switch.async_write_ha_state = MagicMock()

    # Test initial state
    assert switch.is_on is True
    assert switch.name == "Site-to-Site VPN"
    assert switch.unique_id == f"vpn_{MOCK_NETWORK.id}"

    # Test turning off
    await switch.async_turn_off()
    assert switch.is_on is False
    coordinator.api.appliance.update_vpn_status.assert_called_with(
        network_id=MOCK_NETWORK.id,
        mode="none",
    )

    # Test turning on
    await switch.async_turn_on()
    assert switch.is_on is True
    coordinator.api.appliance.update_vpn_status.assert_called_with(
        network_id=MOCK_NETWORK.id,
        mode="hub",
    )
