"""Tests for Meraki services."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from custom_components.meraki_ha.const.integration import DOMAIN
from custom_components.meraki_ha.services import async_setup_services
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ServiceValidationError


@pytest.fixture
def mock_device():
    """Mock Meraki device."""
    device = MagicMock()
    device.serial = "ABC-123"
    return device


@pytest.fixture
def mock_api_client():
    """Mock Meraki API client."""
    client = MagicMock()
    client.async_reboot_device = AsyncMock()
    client.switch = MagicMock()
    client.switch.cycle_device_switch_ports = AsyncMock()
    return client


@pytest.fixture
def mock_coordinator(mock_device):
    """Mock Meraki coordinator."""
    coordinator = MagicMock()
    coordinator.data = {"devices": [mock_device]}
    return coordinator


@pytest.mark.asyncio
async def test_reboot_device_service(
    hass: HomeAssistant, mock_api_client, mock_coordinator
):
    """Test reboot_device service."""
    await async_setup_services(hass)

    hass.data[DOMAIN] = {
        "test_entry": {
            "api_client": mock_api_client,
            "main_coordinator": mock_coordinator,
        }
    }

    await hass.services.async_call(
        DOMAIN,
        "reboot_device",
        {"serial": "ABC-123"},
        blocking=True,
    )

    mock_api_client.async_reboot_device.assert_called_once_with("ABC-123")


@pytest.mark.asyncio
async def test_cycle_port_service(
    hass: HomeAssistant, mock_api_client, mock_coordinator
):
    """Test cycle_port service."""
    await async_setup_services(hass)

    hass.data[DOMAIN] = {
        "test_entry": {
            "api_client": mock_api_client,
            "main_coordinator": mock_coordinator,
        }
    }

    await hass.services.async_call(
        DOMAIN,
        "cycle_port",
        {"serial": "ABC-123", "port_id": "1"},
        blocking=True,
    )

    mock_api_client.switch.cycle_device_switch_ports.assert_called_once_with(
        "ABC-123", ["1"]
    )


@pytest.mark.asyncio
async def test_service_validation_error(
    hass: HomeAssistant, mock_api_client, mock_coordinator
):
    """Test service validation error when device not found."""
    await async_setup_services(hass)

    hass.data[DOMAIN] = {
        "test_entry": {
            "api_client": mock_api_client,
            "main_coordinator": mock_coordinator,
        }
    }

    with pytest.raises(
        ServiceValidationError, match="Device with serial NONEXISTENT not found"
    ):
        await hass.services.async_call(
            DOMAIN,
            "reboot_device",
            {"serial": "NONEXISTENT"},
            blocking=True,
        )
