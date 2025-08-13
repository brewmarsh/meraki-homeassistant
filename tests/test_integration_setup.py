"""Integration-level tests for the Meraki HA component."""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock

from homeassistant.core import HomeAssistant
from custom_components.meraki_ha import async_setup_entry
from homeassistant.helpers.device_registry import async_get as async_get_device_registry
from homeassistant.config_entries import ConfigEntryState

from custom_components.meraki_ha.const import DOMAIN


from pytest_homeassistant_custom_component.common import MockConfigEntry


@pytest.fixture
def mock_meraki_client():
    """Fixture for a mocked MerakiAPIClient."""
    client = MagicMock()
    client.get_all_data = AsyncMock(
        return_value={
            "devices": [],
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
    client.register_webhook = AsyncMock()
    return client


async def test_ssid_device_creation_and_unification(
    hass: HomeAssistant, mock_meraki_client
):
    """Test that a single device is created for an SSID with all its entities."""

    mock_config_entry = MockConfigEntry(
        domain=DOMAIN,
        data={"meraki_api_key": "fake_key", "meraki_org_id": "fake_org"},
        options={},
        state=ConfigEntryState.LOADED,
    )
    mock_config_entry.add_to_hass(hass)

    with patch(
        "custom_components.meraki_ha.MerakiAPIClient", return_value=mock_meraki_client
    ), patch(
        "custom_components.meraki_ha.sensor.async_setup_entry", return_value=True
    ), patch(
        "custom_components.meraki_ha.switch.async_setup_entry", return_value=True
    ), patch(
        "custom_components.meraki_ha.text.async_setup_entry", return_value=True
    ), patch(
        "custom_components.meraki_ha.camera.async_setup_entry", return_value=True
    ), patch(
        "custom_components.meraki_ha.async_register_webhook",
        return_value=None,
    ):
        # Set up the component
        assert await async_setup_entry(hass, mock_config_entry)

        # Get the device registry
        device_registry = async_get_device_registry(hass)

        # Find devices related to the SSID
        ssid_device_identifier = (DOMAIN, "net1_0")
        ssid_device = device_registry.async_get_device({ssid_device_identifier})

        # Assert that a device was created
        assert ssid_device is not None

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
