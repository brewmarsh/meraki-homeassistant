"""Tests for the Meraki firewall rule switch."""
import sys
from unittest.mock import MagicMock, patch

import pytest
from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.meraki_ha.const import (
    DOMAIN,
    CONF_ENABLE_FIREWALL_RULES,
)

# Mock the hass_frontend module
sys.modules["hass_frontend"] = MagicMock()


@pytest.mark.asyncio
async def test_firewall_rule_switch(hass: HomeAssistant):
    """Test the firewall rule switch."""
    config_entry = MockConfigEntry(
        domain=DOMAIN,
        data={"meraki_api_key": "fake_key", "meraki_org_id": "fake_org"},
        options={CONF_ENABLE_FIREWALL_RULES: True},
        entry_id="test_entry",
    )
    config_entry.add_to_hass(hass)

    mock_data = {
        "devices": [],
        "networks": [{"id": "net1", "name": "Test Network", "productTypes": ["appliance"]}],
        "l3_firewall_rules": {
            "net1": {
                "rules": [
                    {
                        "comment": "Allow all",
                        "policy": "allow",
                        "protocol": "any",
                        "destPort": "any",
                        "destCidr": "any",
                        "srcPort": "any",
                        "srcCidr": "any",
                        "syslogEnabled": False,
                    }
                ]
            }
        },
    }

    with patch(
        "custom_components.meraki_ha.coordinator.ApiClient.get_all_data",
        return_value=mock_data,
    ), patch(
        "custom_components.meraki_ha.async_register_webhook", return_value=None
    ), patch(
        "custom_components.meraki_ha.core.api.endpoints.appliance.ApplianceEndpoints.update_l3_firewall_rules"
    ) as mock_update:
        assert await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()

        coordinator = hass.data[DOMAIN][config_entry.entry_id]["coordinator"]
        await coordinator.async_refresh()
        await hass.async_block_till_done()

        # Test creation
        entity_id = "switch.firewall_rule_meraki_device_none_allow_all"
        state = hass.states.get(entity_id)
        assert state
        assert state.state == "on"

        # Test turn off
        await hass.services.async_call(
            "switch",
            "turn_off",
            {"entity_id": entity_id},
            blocking=True,
        )
        await hass.async_block_till_done()

        mock_update.assert_called_once_with(
            network_id="net1",
            rules=[
                {
                    "comment": "Allow all",
                    "policy": "deny",
                    "protocol": "any",
                    "destPort": "any",
                    "destCidr": "any",
                    "srcPort": "any",
                    "srcCidr": "any",
                    "syslogEnabled": False,
                }
            ],
        )
