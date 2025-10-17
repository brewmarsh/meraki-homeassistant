"""Integration-level tests for the Meraki HA component."""
import sys
from unittest.mock import MagicMock, patch, AsyncMock

import pytest
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import async_get as async_get_device_registry
from homeassistant.helpers.entity_registry import async_get as async_get_entity_registry
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.meraki_ha.const import DOMAIN
from tests.const import MOCK_DEVICE, MOCK_MX_DEVICE, MOCK_GX_DEVICE

# Mock the hass_frontend module
sys.modules['hass_frontend'] = MagicMock()


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
    client = AsyncMock()
    client.get_all_data = AsyncMock(
        return_value={
            "devices": [MOCK_DEVICE, MOCK_MX_DEVICE, MOCK_GX_DEVICE],
            "networks": [
                {
                    "id": "net1",
                    "name": "Test Network",
                    "productTypes": ["wireless", "appliance"],
                }
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
            "appliance_traffic": {},
        }
    )
    client.unregister_webhook = AsyncMock(return_value=None)
    return client


@pytest.mark.enable_socket
async def test_ssid_device_creation_and_unification(
    hass: HomeAssistant, config_entry, mock_meraki_client
):
    """Test that a single device is created for an SSID with all its entities."""
    config_entry.add_to_hass(hass)

    with (
        patch(
            "custom_components.meraki_ha.coordinator.ApiClient",
            return_value=mock_meraki_client,
        ),
        patch("custom_components.meraki_ha.async_register_webhook", return_value=None),
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
        assert ssid_device.name == "[SSID] Test SSID"

        # Find all entities associated with this device by querying the entity registry
        entities = [
            entity.entity_id
            for entity in entity_registry.entities.values()
            if entity.device_id == ssid_device.id
        ]

        # Assert that multiple entities have been created for this one device
        assert len(entities) > 1


@pytest.mark.enable_socket
async def test_integration_reload(
    hass: HomeAssistant, config_entry, mock_meraki_client
):
    """Test that the integration reloads successfully."""
    config_entry.add_to_hass(hass)

    with (
        patch(
            "custom_components.meraki_ha.coordinator.ApiClient",
            return_value=mock_meraki_client,
        ),
        patch("custom_components.meraki_ha.async_register_webhook", return_value=None),
    ):
        # Set up the component
        assert await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()

        # Reload the integration
        assert await hass.config_entries.async_reload(config_entry.entry_id)
        await hass.async_block_till_done()

        # Check that the coordinator is still there, indicating a successful reload
        assert DOMAIN in hass.data
        assert config_entry.entry_id in hass.data[DOMAIN]
        assert "coordinator" in hass.data[DOMAIN][config_entry.entry_id]
