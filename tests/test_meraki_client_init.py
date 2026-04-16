"""Test the MerakiClient initialization."""

from custom_components.meraki_ha.core.api.client import MerakiClient
from homeassistant.core import HomeAssistant


def test_meraki_client_init(hass: HomeAssistant) -> None:
    """Test that MerakiClient initializes its endpoint handlers."""
    api_key = "test-api-key"
    org_id = "test-org-id"
    enabled_networks = ["Network 1", "Network 2"]

    client = MerakiClient(hass, api_key, org_id, enabled_networks=enabled_networks)

    # Check if all endpoint handlers are initialized
    assert client.organization is not None
    assert client.appliance is not None
    assert client.camera is not None
    assert client.devices is not None
    assert client.network is not None
    assert client.sensor is not None
    assert client.switch is not None
    assert client.wireless is not None
    assert client.enabled_networks == enabled_networks

    # Verify a specific endpoint call doesn't raise AttributeError on access
    # (though we won't call the actual API)
    assert hasattr(client.organization, "get_organizations")
