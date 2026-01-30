"""Tests for the Meraki VPN switch."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from custom_components.meraki_ha.const import (
    CONF_ENABLE_VPN_MANAGEMENT,
)
from custom_components.meraki_ha.switch.setup_helpers import async_setup_switches
from custom_components.meraki_ha.switch.vpn import MerakiVPNSwitch
from custom_components.meraki_ha.types import MerakiNetwork, MerakiVpn


@pytest.fixture
def mock_coordinator_with_vpn_data(
    mock_coordinator: MagicMock,
) -> MagicMock:
    """Fixture for a mocked MerakiDataUpdateCoordinator with VPN data."""
    vpn_enabled = MerakiVpn(mode="hub")
    vpn_disabled = MerakiVpn(mode="none")

    # We need to mock get_network because MerakiVPNSwitch calls it
    network1 = MerakiNetwork(
        id="net1",
        name="Network 1",
        organization_id="org1",
        product_types=["appliance"],
    )
    network2 = MerakiNetwork(
        id="net2",
        name="Network 2",
        organization_id="org1",
        product_types=["appliance"],
    )

    mock_coordinator.get_network.side_effect = lambda nid: (
        network1 if nid == "net1" else (network2 if nid == "net2" else None)
    )

    mock_coordinator.data = {
        "vpn_status": {
            "net1": vpn_enabled,
            "net2": vpn_disabled,
        },
    }
    mock_coordinator.is_pending.return_value = False
    return mock_coordinator


@pytest.fixture
def mock_config_entry_with_vpn(mock_config_entry: MagicMock) -> MagicMock:
    """Fixture for a mocked ConfigEntry with VPN enabled."""
    mock_config_entry.options = {CONF_ENABLE_VPN_MANAGEMENT: True}
    return mock_config_entry


@pytest.fixture
def mock_meraki_client() -> MagicMock:
    """Fixture for a mocked MerakiAPIClient."""
    return MagicMock()


def test_vpn_switch_creation(
    mock_coordinator_with_vpn_data: MagicMock,
    mock_config_entry_with_vpn: MagicMock,
    mock_meraki_client: MagicMock,
) -> None:
    """Test that the VPN switches are created correctly."""
    hass = MagicMock()
    entities = async_setup_switches(
        hass,
        mock_config_entry_with_vpn,
        mock_coordinator_with_vpn_data,
        mock_meraki_client,
    )

    assert len(entities) == 2
    switch1 = next(e for e in entities if e.unique_id == "vpn_net1")
    switch2 = next(e for e in entities if e.unique_id == "vpn_net2")

    assert isinstance(switch1, MerakiVPNSwitch)
    assert switch1.name == "Site-to-Site VPN"
    assert switch1.is_on is True

    assert isinstance(switch2, MerakiVPNSwitch)
    assert switch2.name == "Site-to-Site VPN"
    assert switch2.is_on is False


def test_vpn_switch_creation_disabled(
    mock_coordinator_with_vpn_data: MagicMock,
    mock_config_entry: MagicMock,
    mock_meraki_client: MagicMock,
) -> None:
    """VPN switches are not created when the feature is disabled."""
    mock_config_entry.options = {CONF_ENABLE_VPN_MANAGEMENT: False}
    hass = MagicMock()
    entities = async_setup_switches(
        hass,
        mock_config_entry,
        mock_coordinator_with_vpn_data,
        mock_meraki_client,
    )
    assert len(entities) == 0


async def test_vpn_turn_on_off(
    mock_coordinator_with_vpn_data: MagicMock,
    mock_config_entry_with_vpn: MagicMock,
) -> None:
    """Test turning the switch on and off."""
    hass = MagicMock()
    # Mock the API client in the coordinator
    mock_api = MagicMock()
    mock_api.appliance = MagicMock()
    mock_api.appliance.update_vpn_status = AsyncMock()
    mock_coordinator_with_vpn_data.api = mock_api

    # Get the network data from the mock fixture logic
    network1 = MerakiNetwork(
        id="net1",
        name="Network 1",
        organization_id="org1",
        product_types=["appliance"],
    )

    switch = MerakiVPNSwitch(
        mock_coordinator_with_vpn_data,
        mock_config_entry_with_vpn,
        network1,
    )
    switch.hass = hass
    switch.entity_id = "switch.net1_vpn"
    switch.async_write_ha_state = MagicMock()

    await switch.async_turn_on()
    assert switch.is_on is True
    mock_api.appliance.update_vpn_status.assert_called_with(
        network_id="net1",
        mode="hub",
    )

    await switch.async_turn_off()
    assert switch.is_on is False
    mock_api.appliance.update_vpn_status.assert_called_with(
        network_id="net1",
        mode="none",
    )
