"""Tests for MerakiUplinkBandwidthNumber."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from custom_components.meraki_ha.number.uplink_bandwidth import (
    MerakiUplinkBandwidthNumber,
)
from tests.const import MOCK_NETWORK


@pytest.fixture
def mock_bandwidth_coordinator(mock_coordinator: MagicMock) -> MagicMock:
    """Create a mock coordinator with traffic shaping data."""
    mock_coordinator.data = {
        "traffic_shaping": {
            MOCK_NETWORK["id"]: {
                "bandwidthLimits": {
                    "wan1": {
                        "limitUp": 1000,
                        "limitDown": 5000,
                    },
                    "wan2": {
                        "limitUp": 2000,
                        "limitDown": 10000,
                    },
                }
            }
        }
    }
    mock_coordinator.is_pending = MagicMock(return_value=False)
    mock_coordinator.register_pending_update = MagicMock()
    mock_coordinator.api = MagicMock()
    mock_coordinator.api.appliance = MagicMock()
    mock_coordinator.api.appliance.update_traffic_shaping = AsyncMock()
    return mock_coordinator


def test_uplink_bandwidth_initialization(
    mock_bandwidth_coordinator: MagicMock,
    mock_config_entry: MagicMock,
) -> None:
    """Test uplink bandwidth number initialization."""
    number = MerakiUplinkBandwidthNumber(
        coordinator=mock_bandwidth_coordinator,
        config_entry=mock_config_entry,
        network=MOCK_NETWORK,
        uplink="wan1",
        direction="up",
    )

    assert number._uplink == "wan1"
    assert number._direction == "up"
    assert number._attr_name is not None and "Wan1" in number._attr_name
    assert number._attr_name is not None and "Up" in number._attr_name
    assert number._attr_native_unit_of_measurement == "kbps"
    assert number._attr_native_min_value == 0
    assert number._attr_native_max_value == 1000000


def test_uplink_bandwidth_wan1_up_value(
    mock_bandwidth_coordinator: MagicMock,
    mock_config_entry: MagicMock,
) -> None:
    """Test uplink bandwidth reads correct value for wan1 up."""
    number = MerakiUplinkBandwidthNumber(
        coordinator=mock_bandwidth_coordinator,
        config_entry=mock_config_entry,
        network=MOCK_NETWORK,
        uplink="wan1",
        direction="up",
    )

    assert number._attr_native_value == 1000.0


def test_uplink_bandwidth_wan1_down_value(
    mock_bandwidth_coordinator: MagicMock,
    mock_config_entry: MagicMock,
) -> None:
    """Test uplink bandwidth reads correct value for wan1 down."""
    number = MerakiUplinkBandwidthNumber(
        coordinator=mock_bandwidth_coordinator,
        config_entry=mock_config_entry,
        network=MOCK_NETWORK,
        uplink="wan1",
        direction="down",
    )

    assert number._attr_native_value == 5000.0


def test_uplink_bandwidth_wan2_values(
    mock_bandwidth_coordinator: MagicMock,
    mock_config_entry: MagicMock,
) -> None:
    """Test uplink bandwidth reads correct values for wan2."""
    number_up = MerakiUplinkBandwidthNumber(
        coordinator=mock_bandwidth_coordinator,
        config_entry=mock_config_entry,
        network=MOCK_NETWORK,
        uplink="wan2",
        direction="up",
    )

    number_down = MerakiUplinkBandwidthNumber(
        coordinator=mock_bandwidth_coordinator,
        config_entry=mock_config_entry,
        network=MOCK_NETWORK,
        uplink="wan2",
        direction="down",
    )

    assert number_up._attr_native_value == 2000.0
    assert number_down._attr_native_value == 10000.0


def test_uplink_bandwidth_no_data(
    mock_bandwidth_coordinator: MagicMock,
    mock_config_entry: MagicMock,
) -> None:
    """Test uplink bandwidth with no traffic shaping data."""
    mock_bandwidth_coordinator.data = {"traffic_shaping": {}}

    number = MerakiUplinkBandwidthNumber(
        coordinator=mock_bandwidth_coordinator,
        config_entry=mock_config_entry,
        network=MOCK_NETWORK,
        uplink="wan1",
        direction="up",
    )

    assert number._attr_native_value is None


@pytest.mark.asyncio
async def test_uplink_bandwidth_set_value(
    mock_bandwidth_coordinator: MagicMock,
    mock_config_entry: MagicMock,
) -> None:
    """Test setting uplink bandwidth value."""
    number = MerakiUplinkBandwidthNumber(
        coordinator=mock_bandwidth_coordinator,
        config_entry=mock_config_entry,
        network=MOCK_NETWORK,
        uplink="wan1",
        direction="up",
    )

    # Mock async_write_ha_state
    object.__setattr__(number, "async_write_ha_state", MagicMock())

    await number.async_set_native_value(2500.0)

    assert number._attr_native_value == 2500.0
    mock_bandwidth_coordinator.register_pending_update.assert_called()
    mock_bandwidth_coordinator.api.appliance.update_traffic_shaping.assert_called()


def test_uplink_bandwidth_unique_id_format(
    mock_bandwidth_coordinator: MagicMock,
    mock_config_entry: MagicMock,
) -> None:
    """Test uplink bandwidth unique ID format."""
    number = MerakiUplinkBandwidthNumber(
        coordinator=mock_bandwidth_coordinator,
        config_entry=mock_config_entry,
        network=MOCK_NETWORK,
        uplink="wan1",
        direction="up",
    )

    assert number._attr_unique_id == f"uplink_bandwidth_{MOCK_NETWORK['id']}_wan1_up"


def test_uplink_bandwidth_pending_update_skips_state(
    mock_bandwidth_coordinator: MagicMock,
    mock_config_entry: MagicMock,
) -> None:
    """Test that pending update prevents state update."""
    mock_bandwidth_coordinator.is_pending = MagicMock(return_value=True)

    _ = MerakiUplinkBandwidthNumber(
        coordinator=mock_bandwidth_coordinator,
        config_entry=mock_config_entry,
        network=MOCK_NETWORK,
        uplink="wan1",
        direction="up",
    )

    mock_bandwidth_coordinator.is_pending.assert_called()
