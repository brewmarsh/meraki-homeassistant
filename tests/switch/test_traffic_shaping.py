"""Tests for the Meraki Traffic Shaping switch."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from custom_components.meraki_ha.const import (
    CONF_ENABLE_TRAFFIC_SHAPING,
)
from custom_components.meraki_ha.switch.setup_helpers import async_setup_switches
from custom_components.meraki_ha.switch.traffic_shaping import MerakiTrafficShapingSwitch
from custom_components.meraki_ha.types import MerakiNetwork, MerakiTrafficShaping


@pytest.fixture
def mock_coordinator_with_traffic_shaping_data(mock_coordinator: MagicMock) -> MagicMock:
    """Fixture for a mocked MerakiDataUpdateCoordinator with Traffic Shaping data."""
    ts_enabled = MerakiTrafficShaping(enabled=True)
    ts_disabled = MerakiTrafficShaping(enabled=False)

    # We need to mock get_network because MerakiTrafficShapingSwitch calls it
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
        "traffic_shaping": {
            "net1": ts_enabled,
            "net2": ts_disabled,
        },
    }
    mock_coordinator.is_pending.return_value = False
    return mock_coordinator


@pytest.fixture
def mock_config_entry_with_traffic_shaping(mock_config_entry: MagicMock) -> MagicMock:
    """Fixture for a mocked ConfigEntry with Traffic Shaping enabled."""
    mock_config_entry.options = {CONF_ENABLE_TRAFFIC_SHAPING: True}
    return mock_config_entry


@pytest.fixture
def mock_meraki_client() -> MagicMock:
    """Fixture for a mocked MerakiAPIClient."""
    return MagicMock()


def test_traffic_shaping_switch_creation(
    mock_coordinator_with_traffic_shaping_data: MagicMock,
    mock_config_entry_with_traffic_shaping: MagicMock,
    mock_meraki_client: MagicMock,
) -> None:
    """Test that the traffic shaping switches are created correctly."""
    hass = MagicMock()
    entities = async_setup_switches(
        hass,
        mock_config_entry_with_traffic_shaping,
        mock_coordinator_with_traffic_shaping_data,
        mock_meraki_client,
    )

    assert len(entities) == 2
    switch1 = next(e for e in entities if e.unique_id == "net1_traffic_shaping_switch")
    switch2 = next(e for e in entities if e.unique_id == "net2_traffic_shaping_switch")

    assert isinstance(switch1, MerakiTrafficShapingSwitch)
    assert switch1.name == "Traffic Shaping"
    assert switch1.is_on is True

    assert isinstance(switch2, MerakiTrafficShapingSwitch)
    assert switch2.name == "Traffic Shaping"
    assert switch2.is_on is False


def test_traffic_shaping_switch_creation_disabled(
    mock_coordinator_with_traffic_shaping_data: MagicMock,
    mock_config_entry: MagicMock,
    mock_meraki_client: MagicMock,
) -> None:
    """Test that the traffic shaping switches are not created if the feature is disabled."""
    mock_config_entry.options = {CONF_ENABLE_TRAFFIC_SHAPING: False}
    hass = MagicMock()
    entities = async_setup_switches(
        hass,
        mock_config_entry,
        mock_coordinator_with_traffic_shaping_data,
        mock_meraki_client,
    )
    # entities might contain other switches if data present, but in our mock only traffic shaping data is present
    # wait, setup_helpers checks for other things. But coordinator data only has "traffic_shaping".
    # so others should return empty.
    assert len(entities) == 0


async def test_traffic_shaping_turn_on_off(
    mock_coordinator_with_traffic_shaping_data: MagicMock,
    mock_config_entry_with_traffic_shaping: MagicMock,
) -> None:
    """Test turning the switch on and off."""
    hass = MagicMock()
    # Mock the API client in the coordinator
    mock_api = MagicMock()
    mock_api.appliance = MagicMock()
    # update_traffic_shaping should be async
    mock_api.appliance.update_traffic_shaping = AsyncMock()
    mock_coordinator_with_traffic_shaping_data.api = mock_api

    ts_data = MerakiTrafficShaping(enabled=False)
    switch = MerakiTrafficShapingSwitch(
        mock_coordinator_with_traffic_shaping_data,
        mock_config_entry_with_traffic_shaping,
        "net1",
        ts_data,
    )
    switch.hass = hass
    switch.entity_id = "switch.net1_traffic_shaping"
    switch.async_write_ha_state = MagicMock()

    await switch.async_turn_on()
    assert switch.is_on is True
    mock_api.appliance.update_traffic_shaping.assert_called_with(
        network_id="net1",
        enabled=True,
    )

    await switch.async_turn_off()
    assert switch.is_on is False
    mock_api.appliance.update_traffic_shaping.assert_called_with(
        network_id="net1",
        enabled=False,
    )
