"""Tests for Meraki API client initialization."""

from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.meraki_ha.const.config import (
    CONF_ENABLED_NETWORKS,
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
)
from custom_components.meraki_ha.const.integration import DOMAIN
from custom_components.meraki_ha.core.api.factory import create_meraki_client


async def test_create_meraki_client_initialization(hass: HomeAssistant):
    """Test that create_meraki_client correctly initializes the client with filtered networks."""
    # Mock data
    api_key = "test_api_key"
    org_id = "test_org_id"
    enabled_networks = ["Network 1", "N_12345"]

    # Create a mock config entry
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={
            CONF_MERAKI_API_KEY: api_key,
            CONF_MERAKI_ORG_ID: org_id,
            CONF_ENABLED_NETWORKS: [],  # Initial data is empty
        },
        options={
            CONF_ENABLED_NETWORKS: enabled_networks,  # Options has the filtered list
        },
        entry_id="test_entry_id",
    )
    entry.add_to_hass(hass)

    # Call the factory function
    client = create_meraki_client(hass, entry)

    # Verify client attributes
    assert client._api_key == api_key
    assert client._org_id == org_id
    assert client.enabled_networks == enabled_networks


async def test_create_meraki_client_fallback_to_data(hass: HomeAssistant):
    """Test that create_meraki_client falls back to data if options are missing."""
    # Mock data
    api_key = "test_api_key"
    org_id = "test_org_id"
    enabled_networks = ["Network 2"]

    # Create a mock config entry without options for enabled_networks
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={
            CONF_MERAKI_API_KEY: api_key,
            CONF_MERAKI_ORG_ID: org_id,
            CONF_ENABLED_NETWORKS: enabled_networks,
        },
        options={},
        entry_id="test_entry_id_2",
    )
    entry.add_to_hass(hass)

    # Call the factory function
    client = create_meraki_client(hass, entry)

    # Verify client attributes
    assert client.enabled_networks == enabled_networks
