"""Integration-level tests for the Meraki HA component."""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock

from homeassistant.core import HomeAssistant
from homeassistant.setup import async_setup_component
from homeassistant.helpers.device_registry import async_get as async_get_device_registry
from homeassistant.config_entries import ConfigEntryState

from custom_components.meraki_ha.const import DOMAIN
from custom_components.meraki_ha import async_setup_entry
from custom_components.meraki_ha.core.errors import MerakiConnectionError


from pytest_homeassistant_custom_component.common import MockConfigEntry


@pytest.fixture
async def mock_config_entry(hass):
    """Fixture for a mocked config entry."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={"meraki_api_key": "fake_key", "meraki_org_id": "fake_org"},
        options={},
        entry_id="test_entry",
    )
    await hass.config_entries.async_add(entry)
    return entry


@pytest.fixture
def mock_meraki_client():
    """Fixture for a mocked MerakiAPIClient."""
    client = MagicMock()
    client.get_all_data = AsyncMock(
        return_value={
            "devices": [
                {
                    "serial": "Q234-ABCD-5678",
                    "name": "Test AP",
                    "model": "MR33",
                    "networkId": "net1",
                    "productType": "wireless",
                }
            ],
            "networks": [
                {"id": "net1", "name": "Test Network", "productTypes": ["wireless"]}
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
    client.unregister_webhook = AsyncMock()
    return client


async def test_ssid_device_creation_and_unification(
    hass: HomeAssistant, mock_config_entry, mock_meraki_client
):
    """Test that a single device is created for an SSID with all its entities."""

    with patch(
        "custom_components.meraki_ha.MerakiAPIClient", return_value=mock_meraki_client
    ), patch(
            "homeassistant.helpers.network.get_url", return_value="http://localhost:8123"
        ) as mock_get_url, patch(
        "custom_components.meraki_ha.async_register_webhook"
    ) as mock_register_webhook:
        # Set up the component
        mock_config_entry.add_to_hass(hass)
        assert await async_setup_component(hass, DOMAIN, {})
        await hass.async_block_till_done()

        # Get the device registry
        device_registry = async_get_device_registry(hass)
        print(device_registry.devices)
        # Find devices related to the SSID
        ssid_device_identifier = (DOMAIN, "net1_0")
        ssid_device = device_registry.async_get_device({ssid_device_identifier})

        # Assert that a device was created
        assert ssid_device is not None
        print(f"Config entry state: {mock_config_entry.state}")

        # Assert that the device has the correct name (default prefix format)
        assert ssid_device.name == "[Ssid] Test SSID"

        # Find all entities associated with this device
        entities = [
            entity
            for entity in hass.states.async_all()
            if entity.attributes.get("device_id") == ssid_device.id
        ]

        # Assert that multiple entities have been created for this one device
        assert len(entities) > 1
