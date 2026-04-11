"""Test the MerakiClient initialization."""

from homeassistant.core import HomeAssistant

from custom_components.meraki_ha.core.api.client import MerakiClient


def test_meraki_client_init(hass: HomeAssistant) -> None:
    """Test that MerakiClient initializes its endpoint handlers."""
    api_key = "test-api-key"
    org_id = "test-org-id"

    client = MerakiClient(hass, api_key, org_id)

    # Check if all endpoint handlers are initialized
    assert client.organization is not None
    assert client.appliance is not None
    assert client.camera is not None
    assert client.devices is not None
    assert client.network is not None
    assert client.sensor is not None
    assert client.switch is not None
    assert client.wireless is not None

    # Verify a specific endpoint call doesn't raise AttributeError on access
    # (though we won't call the actual API)
    assert hasattr(client.organization, "get_organizations")
