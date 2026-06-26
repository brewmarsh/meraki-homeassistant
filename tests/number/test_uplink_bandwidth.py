"""Tests for the Meraki uplink bandwidth number."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from custom_components.meraki_ha.core.models.network import MerakiNetwork
from custom_components.meraki_ha.number.uplink_bandwidth import (
    MerakiUplinkBandwidthNumber,
)


@pytest.mark.asyncio
async def test_uplink_bandwidth_number():
    """Test the MerakiUplinkBandwidthNumber."""
    mock_coordinator = MagicMock()
    mock_coordinator.api.appliance.update_traffic_shaping = AsyncMock()
    mock_coordinator.is_pending.return_value = False
    mock_coordinator.register_pending_update = MagicMock()

    # Mock data structure
    mock_coordinator.data = {
        "traffic_shaping": {
            "N123": {
                "bandwidthLimits": {
                    "wan1": {"limitUplink": 5000, "limitDownlink": 10000}
                }
            }
        }
    }

    mock_config_entry = MagicMock()
    mock_network = MagicMock(spec=MerakiNetwork)
    mock_network.id = "N123"

    # Instantiate number entity
    number = MerakiUplinkBandwidthNumber(
        mock_coordinator, mock_config_entry, mock_network, "wan1", "uplink"
    )
    number.hass = MagicMock()
    number.async_write_ha_state = MagicMock()

    # Assert properties
    assert number.unique_id == "uplink_bandwidth_N123_wan1_uplink"
    assert number.native_value == 5000.0
    assert number.native_unit_of_measurement == "kbps"

    # Test update_state
    mock_coordinator.data["traffic_shaping"]["N123"]["bandwidthLimits"]["wan1"][
        "limitUplink"
    ] = 6000
    number._handle_coordinator_update()
    assert number.native_value == 6000.0

    # Test set_native_value
    await number.async_set_native_value(7000.0)
    assert number.native_value == 7000.0
    mock_coordinator.api.appliance.update_traffic_shaping.assert_called_once()
    mock_coordinator.register_pending_update.assert_called_with(number.unique_id)

    # Test pending update (should skip update_state)
    mock_coordinator.is_pending.return_value = True
    mock_coordinator.data["traffic_shaping"]["N123"]["bandwidthLimits"]["wan1"][
        "limitUplink"
    ] = 8000
    number._handle_coordinator_update()
    assert number.native_value == 7000.0  # Still 7000 because update was skipped
