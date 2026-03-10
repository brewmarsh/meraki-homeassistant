"""Tests for Meraki IPSK Services."""

from unittest.mock import AsyncMock, MagicMock

import pytest
from homeassistant.exceptions import HomeAssistantError

from custom_components.meraki_ha.const.integration import DOMAIN
from custom_components.meraki_ha.services import async_setup_services


@pytest.fixture(autouse=True)
def auto_domain_init(hass):
    """Initialize DOMAIN data."""
    hass.data[DOMAIN] = {}


@pytest.fixture
def mock_ipsk_manager(hass):
    """Mock IPSK Manager."""
    manager = MagicMock()
    manager.create_guest_key = AsyncMock()
    hass.data[DOMAIN]["ipsk_manager"] = manager
    return manager


@pytest.fixture
def mock_coordinator(hass):
    """Mock Main Coordinator."""
    coordinator = MagicMock()
    coordinator.networks_by_id = {"N_12345": MagicMock()}

    hass.data[DOMAIN]["test_entry_id"] = {"main_coordinator": coordinator}
    return coordinator


@pytest.mark.asyncio
async def test_service_registration(hass):
    """Test service registration."""
    await async_setup_services(hass)
    assert hass.services.has_service(DOMAIN, "create_guest_key")
    assert hass.services.has_service(DOMAIN, "generate_guest_access")


@pytest.mark.asyncio
async def test_generate_guest_access_service_success(
    hass, mock_ipsk_manager, mock_coordinator
):
    """Test successful creation of guest key via UI-friendly alias service."""
    # This test verifies the mapping from frontend-style keys to manager-style keys
    await async_setup_services(hass)

    service_data = {
        "network_id": "N_12345",
        "ssid": 1,
        "duration": 60,
        "guest_name": "Service Guest",
        "passphrase": "secretpassword",
    }

    await hass.services.async_call(
        DOMAIN, "generate_guest_access", service_data, blocking=True
    )

    # Verify that 'ssid' maps to 'ssid_number' and 'guest_name' maps to 'name'
    mock_ipsk_manager.create_guest_key.assert_called_once_with(
        config_entry_id="test_entry_id",
        network_id="N_12345",
        ssid_number="1",  # Coerced to string
        duration_minutes=60,
        name="Service Guest",
        passphrase="secretpassword",
    )


@pytest.mark.asyncio
async def test_create_guest_key_service_success(
    hass, mock_ipsk_manager, mock_coordinator
):
    """Test successful creation of guest key via technical service."""
    await async_setup_services(hass)

    service_data = {
        "network_id": "N_12345",
        "ssid_number": 1,
        "duration_minutes": 60,
        "name": "Technical Guest",
        "passphrase": "secretpassword",
        "group_policy_id": "GP_987",
    }

    await hass.services.async_call(
        DOMAIN, "create_guest_key", service_data, blocking=True
    )

    mock_ipsk_manager.create_guest_key.assert_called_once_with(
        config_entry_id="test_entry_id",
        network_id="N_12345",
        ssid_number="1",
        duration_minutes=60,
        name="Technical Guest",
        passphrase="secretpassword",
        group_policy_id="GP_987",
    )


@pytest.mark.asyncio
async def test_create_guest_key_service_invalid_network(
    hass, mock_ipsk_manager, mock_coordinator
):
    """Test guest key creation with invalid network ID."""
    await async_setup_services(hass)

    service_data = {
        "network_id": "INVALID_NETWORK",
        "ssid_number": 1,
        "duration_minutes": 60,
    }

    with pytest.raises(
        HomeAssistantError, match="Network ID INVALID_NETWORK not found"
    ):
        await hass.services.async_call(
            DOMAIN, "create_guest_key", service_data, blocking=True
        )


@pytest.mark.asyncio
async def test_create_guest_key_service_no_manager(hass, mock_coordinator):
    """Test guest key creation when manager is missing."""
    if "ipsk_manager" in hass.data[DOMAIN]:
        del hass.data[DOMAIN]["ipsk_manager"]

    await async_setup_services(hass)

    service_data = {
        "network_id": "N_12345",
        "ssid_number": 1,
        "duration_minutes": 60,
    }

    with pytest.raises(HomeAssistantError, match="IPSK Manager not initialized"):
        await hass.services.async_call(
            DOMAIN, "create_guest_key", service_data, blocking=True
        )


@pytest.mark.asyncio
async def test_create_guest_key_service_safe_iteration(
    hass, mock_ipsk_manager, mock_coordinator
):
    """Test that service call doesn't crash if hass.data[DOMAIN] contains non-dict objects."""
    # Mimics presence of other managers/objects in the data dictionary
    hass.data[DOMAIN]["services_manager"] = MagicMock()

    await async_setup_services(hass)

    service_data = {
        "network_id": "N_12345",
        "ssid_number": 1,
        "duration_minutes": 60,
    }

    await hass.services.async_call(
        DOMAIN, "create_guest_key", service_data, blocking=True
    )

    assert mock_ipsk_manager.create_guest_key.called
