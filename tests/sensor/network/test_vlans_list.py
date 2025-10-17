"""Tests for the Meraki VLANs list sensor."""
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
sys.modules['hass_frontend'] = MagicMock()


@pytest.mark.asyncio
async def test_vlans_list_sensor(hass: HomeAssistant):
    """Test the VLANs list sensor."""
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
                    "enabled": True,
                },
                {
                    "id": 2,
                    "name": "VLAN 2",
                    "subnet": "192.168.2.0/24",
                    "applianceIp": "192.168.2.1",
                    "enabled": True,
                },
            ]
        },
        "clients": [],
        "ssids": [],
    }

    with patch(
        "custom_components.meraki_ha.coordinator.ApiClient.get_all_data",
        return_value=mock_data,
    ), patch(
        "custom_components.meraki_ha.async_register_webhook", return_value=None
    ):
        assert await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()

        coordinator = hass.data[DOMAIN][config_entry.entry_id]["coordinator"]
        await coordinator.async_refresh()
        await hass.async_block_till_done()

        entity_id = "sensor.network_test_network_vlans"
        state = hass.states.get(entity_id)
        assert state
        assert state.state == "2"
        assert len(state.attributes["vlans"]) == 2
