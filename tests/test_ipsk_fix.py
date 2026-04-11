"""Tests for Meraki IPSK Services regression fix."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from custom_components.meraki_ha.const.integration import DOMAIN
from custom_components.meraki_ha.services import async_setup_services
from homeassistant.exceptions import ServiceValidationError


@pytest.fixture(autouse=True)
def auto_domain_init(hass):
    """Initialize DOMAIN data."""
    hass.data[DOMAIN] = {}


@pytest.fixture
def mock_ipsk_manager(hass):
    """Mock IPSK Manager."""
    manager = MagicMock()
    manager.create_guest_key = AsyncMock()
    manager.get_or_create_guest_policy = AsyncMock(return_value="GP_MOCK")
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
async def test_generate_guest_access_none_policy(
    hass, mock_ipsk_manager, mock_coordinator
):
    """Test NONE policy handling in generate_guest_access."""
    await async_setup_services(hass)

    service_data = {
        "network_id": "N_12345",
        "ssid": 1,
        "duration": 60,
        "guest_name": "Service Guest",
        "group_policy": "NONE",
    }

    await hass.services.async_call(
        DOMAIN, "generate_guest_access", service_data, blocking=True
    )

    # Should NOT call get_or_create_guest_policy
    assert not mock_ipsk_manager.get_or_create_guest_policy.called

    # Should call create_guest_key with group_policy_id="NONE"
    # Note: the services/__init__.py passes "NONE" to manager,
    # and manager converts it to None.
    mock_ipsk_manager.create_guest_key.assert_called_once_with(
        config_entry_id="test_entry_id",
        network_id="N_12345",
        ssid_number="1",
        duration_minutes=60,
        name="Service Guest",
        passphrase=None,
        group_policy_id="NONE",
    )

@pytest.mark.asyncio
async def test_create_guest_key_none_policy(
    hass, mock_ipsk_manager, mock_coordinator
):
    """Test NONE policy handling in create_guest_key service."""
    await async_setup_services(hass)

    service_data = {
        "network_id": "N_12345",
        "ssid_number": 1,
        "duration_minutes": 60,
        "name": "Technical Guest",
        "group_policy_id": "NONE",
    }

    await hass.services.async_call(
        DOMAIN, "create_guest_key", service_data, blocking=True
    )

    # Should NOT call get_or_create_guest_policy
    assert not mock_ipsk_manager.get_or_create_guest_policy.called

    mock_ipsk_manager.create_guest_key.assert_called_once_with(
        config_entry_id="test_entry_id",
        network_id="N_12345",
        ssid_number="1",
        duration_minutes=60,
        name="Technical Guest",
        passphrase=None,
        group_policy_id="NONE",
    )

@pytest.mark.asyncio
async def test_service_validation_error_on_policy_failure(
    hass, mock_ipsk_manager, mock_coordinator
):
    """Test ServiceValidationError when policy creation fails."""
    mock_ipsk_manager.get_or_create_guest_policy.return_value = None
    await async_setup_services(hass)

    service_data = {
        "network_id": "N_12345",
        "ssid": 1,
        "duration": 60,
        "guest_name": "Service Guest",
        "group_policy": "CREATE",
    }

    with pytest.raises(ServiceValidationError, match="A Group Policy ID is required"):
        await hass.services.async_call(
            DOMAIN, "generate_guest_access", service_data, blocking=True
        )
