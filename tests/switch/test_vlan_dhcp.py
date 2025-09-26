"""Tests for the Meraki VLAN DHCP switch."""
import sys
from unittest.mock import MagicMock, patch

import pytest
from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.meraki_ha.const import (
    DOMAIN,
    CONF_ENABLE_VLAN_MANAGEMENT,
)

# Mock the hass_frontend module
sys.modules["hass_frontend"] = MagicMock()


@pytest.mark.asyncio
async def test_vlan_dhcp_switch(hass: HomeAssistant):
    """Test the VLAN DHCP switch."""
    config_entry = MockConfigEntry(
        domain=DOMAIN,
        data={"meraki_api_key": "fake_key", "meraki_org_id": "fake_org"},
        options={CONF_ENABLE_VLAN_MANAGEMENT: True},
        entry_id="test_entry",
    )
    config_entry.add_to_hass(hass)

    mock_data = {
        "devices": [],
        "networks": [{"id": "net1", "name": "Test Network", "productTypes": ["appliance"]}],
        "vlans": {
            "net1": [
                {
                    "id": 1,
                    "name": "VLAN 1",
                    "subnet": "192.168.1.0/24",
                    "applianceIp": "192.168.1.1",
                    "dhcpHandling": "Run a DHCP server",
                },
            ]
        },
    }

    with patch(
        "custom_components.meraki_ha.coordinator.ApiClient.get_all_data",
        return_value=mock_data,
    ), patch(
        "custom_components.meraki_ha.async_register_webhook", return_value=None
    ), patch(
        "custom_components.meraki_ha.core.api.endpoints.appliance.ApplianceEndpoints.update_network_vlan"
    ) as mock_update:
        assert await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()

        coordinator = hass.data[DOMAIN][config_entry.entry_id]["coordinator"]
        await coordinator.async_refresh()
        await hass.async_block_till_done()

        # Test creation
        entity_id = "switch.vlan_vlan_1_vlan_1_dhcp"
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
            vlan_id=1,
            dhcpHandling="Do not respond to DHCP requests",
        )
