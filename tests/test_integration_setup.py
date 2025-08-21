"""Integration-level tests for the Meraki HA component."""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock

from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import async_get as async_get_device_registry
from homeassistant.helpers.entity_registry import async_get as async_get_entity_registry
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.meraki_ha.const import DOMAIN

@pytest.fixture
def config_entry():
    """Fixture for a mocked config entry."""
    return MockConfigEntry(
        domain=DOMAIN,
        data={"meraki_api_key": "fake_key", "meraki_org_id": "fake_org"},
        options={},
        entry_id="test_entry",
    )

@pytest.fixture
def mock_meraki_client():
    """Fixture for a mocked MerakiAPIClient."""
    client = MagicMock()
    client.get_all_data = AsyncMock(
        return_value={
            "devices": [],
            "networks": [
                {"id": "net1", "name": "Test Network", "productTypes": ["wireless", "appliance"]}
            ],
            "ssids": [
                {
                    "number": 0,
                    "name": "Test SSID",
                    "enabled": True,
                    "networkId": "net1",
                }
            ],
            "clients": [],
            "vlans": {},
            "appliance_uplink_statuses": [],
            "rf_profiles": {},
        }
    )
    client.unregister_webhook = AsyncMock(return_value=None)

    # Mock for SsidContentFilteringCoordinator
    client.wireless = MagicMock()
    client.wireless.get_network_wireless_ssid = AsyncMock(
        return_value={"number": 0, "name": "Test SSID", "contentFiltering": {}}
    )

    # Mock for NetworkContentFilteringCoordinator and ClientFirewallCoordinator
    client.appliance = MagicMock()
    client.appliance.get_network_appliance_content_filtering = AsyncMock(
        return_value={"allowedUrlPatterns": [], "blockedUrlPatterns": []}
    )
    client.appliance.get_network_appliance_firewall_l7_firewall_rules = AsyncMock(
        return_value={'rules': []}
    )

    # Mock for ClientFirewallCoordinator
    client.network = MagicMock()
    client.network.get_network_clients = AsyncMock(return_value=[])

    return client


async def test_ssid_device_creation_and_unification(
    hass: HomeAssistant, config_entry, mock_meraki_client
):
    """Test that a single device is created for an SSID with all its entities."""
    config_entry.add_to_hass(hass)

    with patch(
        "custom_components.meraki_ha.MerakiAPIClient", return_value=mock_meraki_client
    ), patch(
        "custom_components.meraki_ha.async_register_webhook", return_value=None
    ):
        # Set up the component
        assert await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()

        # Get the device and entity registries
        device_registry = async_get_device_registry(hass)
        entity_registry = async_get_entity_registry(hass)

        # Find devices related to the SSID
        ssid_device_identifier = (DOMAIN, "net1_0")
        ssid_device = device_registry.async_get_device({ssid_device_identifier})

        # Assert that a device was created
        assert ssid_device is not None

        # Assert that the device has the correct name (default prefix format)
        assert ssid_device.name == "[Ssid] Test SSID"

        # Find all entities associated with this device by querying the entity registry
        entities = [
            entity.entity_id
            for entity in entity_registry.entities.values()
            if entity.device_id == ssid_device.id
        ]

        # Assert that multiple entities have been created for this one device
        assert len(entities) > 1
