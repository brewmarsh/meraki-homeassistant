"""Test the Meraki intent handler."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from baml_client.types import MerakiIntent, MerakiIntentResponse
from custom_components.meraki_ha.const.integration import DOMAIN
from custom_components.meraki_ha.intent import MerakiSmartCommandHandler
from homeassistant.helpers import intent


@pytest.fixture
def intent_handler():
    """Fixture for the intent handler."""
    return MerakiSmartCommandHandler()


async def test_handle_reboot_success(hass, intent_handler):
    """Test successful reboot intent handling."""
    # Mock BAML response
    baml_response = MerakiIntentResponse(
        intent=MerakiIntent.RebootDevice,
        target_device="Garage Switch",
        guest_name=None,
        duration_minutes=None,
        network_name=None,
    )

    # Setup mock data in hass
    serial = "ABCD-1234-EFGH"
    entry_id = "test_entry"
    device_control_service = AsyncMock()

    device = {"name": "Garage Switch"}

    main_coordinator = MagicMock()
    main_coordinator.devices_by_serial = {serial: device}

    hass.data[DOMAIN] = {
        entry_id: {
            "main_coordinator": main_coordinator,
            "device_control_service": device_control_service,
        }
    }

    # Prepare intent object
    intent_obj = intent.Intent(
        hass,
        "MerakiSmartCommand",
        "reboot Garage Switch",
        None,
        None,
        None,
        None,
    )
    intent_obj.slots = {"command": {"value": "reboot Garage Switch"}}

    with patch("baml_client.b.RouteMerakiIntent", return_value=baml_response):
        response = await intent_handler.async_handle(intent_obj)

    assert response.speech["plain"]["speech"] == "Restarting Garage Switch now."
    device_control_service.async_reboot.assert_called_once_with(serial)


async def test_handle_guest_access_success(hass, intent_handler):
    """Test successful guest access intent handling."""
    # Mock BAML response
    baml_response = MerakiIntentResponse(
        intent=MerakiIntent.GenerateGuestAccess,
        target_device=None,
        guest_name="GuestUser",
        duration_minutes=30,
        network_name="Main Network",
    )

    # Setup mock data in hass
    network_id = "N_123"
    entry_id = "test_entry"
    ipsk_manager = AsyncMock()
    ipsk_manager.create_guest_key.return_value = {"passphrase": "secretpassword"}

    network = {"name": "Main Network"}

    main_coordinator = MagicMock()
    main_coordinator.networks_by_id = {network_id: network}

    hass.data[DOMAIN] = {
        entry_id: {
            "main_coordinator": main_coordinator,
        },
        "ipsk_manager": ipsk_manager
    }

    # Prepare intent object
    intent_obj = intent.Intent(
        hass,
        "MerakiSmartCommand",
        "create guest wifi for GuestUser for 30 minutes on Main Network",
        None,
        None,
        None,
        None,
    )
    intent_obj.slots = {"command": {"value": "create guest wifi for GuestUser for 30 minutes on Main Network"}}

    with patch("baml_client.b.RouteMerakiIntent", return_value=baml_response):
        response = await intent_handler.async_handle(intent_obj)

    assert "Generated guest access for GuestUser" in response.speech["plain"]["speech"]
    assert "secretpassword" in response.speech["plain"]["speech"]
    ipsk_manager.create_guest_key.assert_called_once()


async def test_handle_unknown_intent(hass, intent_handler):
    """Test unknown intent handling."""
    # Mock BAML response
    baml_response = MerakiIntentResponse(
        intent=MerakiIntent.Unknown,
        target_device=None,
        guest_name=None,
        duration_minutes=None,
        network_name=None,
    )

    # Prepare intent object
    intent_obj = intent.Intent(
        hass,
        "MerakiSmartCommand",
        "what is for lunch",
        None,
        None,
        None,
        None,
    )
    intent_obj.slots = {"command": {"value": "what is for lunch"}}

    with patch("baml_client.b.RouteMerakiIntent", return_value=baml_response):
        response = await intent_handler.async_handle(intent_obj)

    assert response.speech["plain"]["speech"] == "I'm not sure how to help with that Meraki command."
