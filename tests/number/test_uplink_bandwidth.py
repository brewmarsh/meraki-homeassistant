"""Tests for the Meraki uplink bandwidth number."""

import pytest
from unittest.mock import MagicMock, AsyncMock

from custom_components.meraki_ha.number.setup_helpers import async_setup_numbers
from custom_components.meraki_ha.const import (
    CONF_ENABLE_TRAFFIC_SHAPING,
)


@pytest.fixture
def mock_coordinator():
    """Fixture for a mocked MerakiDataUpdateCoordinator."""
    coordinator = MagicMock()
    coordinator.config_entry = MagicMock()
    coordinator.config_entry.options = {
        "device_name_format": "omit",
        CONF_ENABLE_TRAFFIC_SHAPING: True,
    }
    coordinator.data = {
        "networks": [
            {"id": "net1", "name": "Test Network", "productTypes": ["appliance"]}
        ],
        "traffic_shaping": {
            "net1": {
                "enabled": True,
                "bandwidthLimits": {
                    "wan1": {"limitUp": 1000, "limitDown": 10000},
                },
            }
        },
    }
    coordinator.is_pending.return_value = False
    coordinator.api = MagicMock()
    coordinator.api.appliance.update_traffic_shaping = AsyncMock()
    return coordinator


def test_uplink_bandwidth_number_creation(mock_coordinator):
    """Test that the uplink bandwidth numbers are created correctly."""
    hass = MagicMock()

    # Run the setup
    numbers = async_setup_numbers(
        hass, mock_coordinator.config_entry, mock_coordinator
    )

    # Find the specific numbers
    up_limit_number = next(s for s in numbers if "Up Limit" in s.name)
    down_limit_number = next(s for s in numbers if "Down Limit" in s.name)

    # Assertions for Up Limit Number
    assert (
        up_limit_number.unique_id == "uplink_bandwidth_net1_wan1_up"
    )
    assert up_limit_number.name == "Test Network Wan1 Up Limit"
    assert up_limit_number.native_value == 1000

    # Assertions for Down Limit Number
    assert (
        down_limit_number.unique_id == "uplink_bandwidth_net1_wan1_down"
    )
    assert down_limit_number.name == "Test Network Wan1 Down Limit"
    assert down_limit_number.native_value == 10000


@pytest.mark.asyncio
async def test_uplink_bandwidth_number_set_value(mock_coordinator):
    """Test setting the value of an uplink bandwidth number."""
    hass = MagicMock()
    numbers = async_setup_numbers(
        hass, mock_coordinator.config_entry, mock_coordinator
    )
    up_limit_number = next(s for s in numbers if "Up Limit" in s.name)
    up_limit_number.hass = hass

    await up_limit_number.async_set_native_value(2000)

    mock_coordinator.api.appliance.update_traffic_shaping.assert_called_once_with(
        network_id="net1",
        bandwidthLimits={"wan1": {"limitUp": 2000, "limitDown": 10000}},
    )
