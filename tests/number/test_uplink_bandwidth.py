"""Tests for the Meraki uplink bandwidth number."""
import sys
from unittest.mock import MagicMock, patch

import pytest
from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.meraki_ha.const import (
    DOMAIN,
    CONF_ENABLE_TRAFFIC_SHAPING,
)

# Mock the hass_frontend module
sys.modules["hass_frontend"] = MagicMock()


@pytest.mark.asyncio
async def test_uplink_bandwidth_number(hass: HomeAssistant):
    """Test uplink bandwidth number entities."""
    config_entry = MockConfigEntry(
        domain=DOMAIN,
        data={"meraki_api_key": "fake_key", "meraki_org_id": "fake_org"},
        options={CONF_ENABLE_TRAFFIC_SHAPING: True},
        entry_id="test_entry",
    )
    config_entry.add_to_hass(hass)

    mock_data = {
        "devices": [],
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

    with patch(
        "custom_components.meraki_ha.coordinator.ApiClient.get_all_data",
        return_value=mock_data,
    ), patch(
        "custom_components.meraki_ha.async_register_webhook", return_value=None
    ), patch(
        "custom_components.meraki_ha.core.api.endpoints.appliance.ApplianceEndpoints.update_traffic_shaping"
    ) as mock_update:
        assert await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()

        # Test creation
        up_limit_entity_id = "number.test_network_wan1_up_limit"
        down_limit_entity_id = "number.test_network_wan1_down_limit"

        up_limit_state = hass.states.get(up_limit_entity_id)
        assert up_limit_state
        assert up_limit_state.state == "1000.0"

        down_limit_state = hass.states.get(down_limit_entity_id)
        assert down_limit_state
        assert down_limit_state.state == "10000.0"

        # Test set value
        await hass.services.async_call(
            "number",
            "set_value",
            {"entity_id": up_limit_entity_id, "value": 2000},
            blocking=True,
        )
        await hass.async_block_till_done()

        mock_update.assert_called_once_with(
            network_id="net1",
            bandwidthLimits={"wan1": {"limitUp": 2000, "limitDown": 10000}},
        )
