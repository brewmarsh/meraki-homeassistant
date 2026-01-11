"""Tests for the Meraki Scanning API."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest
from homeassistant.core import HomeAssistant

from custom_components.meraki_ha.const import (
    CONF_ENABLE_SCANNING_API,
    CONF_SCANNING_API_SECRET,
    CONF_SCANNING_API_VALIDATOR,
)
from custom_components.meraki_ha.webhook import (
    _handle_scanning_api_data,
    async_handle_scanning_api,
    async_handle_webhook,
)


@pytest.fixture
def mock_request():
    """Create a mock aiohttp request for direct Scanning API endpoint."""
    request = AsyncMock()
    request.method = "POST"
    request.json = AsyncMock(
        return_value={
            "secret": "test_secret",
            "type": "DevicesSeen",
            "data": {
                "apMac": "00:11:22:33:44:55",
                "observations": [
                    {
                        "clientMac": "aa:bb:cc:dd:ee:ff",
                        "seenTime": "2024-01-15T12:00:00Z",
                        "rssi": -45,
                        "location": {"lat": 37.7749, "lng": -122.4194},
                    }
                ],
            },
        }
    )
    return request


async def test_scanning_api_get_validator(hass: HomeAssistant, mock_config_entry):
    """Test the GET validator for the Scanning API."""
    mock_config_entry.options = {
        CONF_ENABLE_SCANNING_API: True,
        CONF_SCANNING_API_VALIDATOR: "test_validator",
    }
    request = AsyncMock()
    request.method = "GET"
    hass.config_entries.async_get_entry = MagicMock(return_value=mock_config_entry)
    response = await async_handle_scanning_api(
        hass, mock_config_entry.entry_id, request
    )
    assert response.text == "test_validator"


async def test_scanning_api_get_without_validator(
    hass: HomeAssistant, mock_config_entry
):
    """Test GET returns 404 when validator is not configured."""
    mock_config_entry.options = {CONF_ENABLE_SCANNING_API: True}
    request = AsyncMock()
    request.method = "GET"
    hass.config_entries.async_get_entry = MagicMock(return_value=mock_config_entry)
    response = await async_handle_scanning_api(
        hass, mock_config_entry.entry_id, request
    )
    assert response.status == 404


async def test_scanning_api_post_invalid_secret(
    hass: HomeAssistant, mock_config_entry, mock_request
):
    """Test the POST data processing with an invalid secret."""
    mock_config_entry.options = {
        CONF_ENABLE_SCANNING_API: True,
        CONF_SCANNING_API_SECRET: "wrong_secret",
    }
    hass.config_entries.async_get_entry = MagicMock(return_value=mock_config_entry)
    response = await async_handle_scanning_api(
        hass, mock_config_entry.entry_id, mock_request
    )
    assert response.status == 401


async def test_scanning_api_post_valid_data(
    hass: HomeAssistant, mock_config_entry, mock_request, mock_coordinator
):
    """Test the POST data processing with valid data."""
    mock_config_entry.options = {
        CONF_ENABLE_SCANNING_API: True,
        CONF_SCANNING_API_SECRET: "test_secret",
    }
    hass.data["meraki_ha"] = {
        mock_config_entry.entry_id: {"coordinator": mock_coordinator}
    }
    mock_coordinator.async_handle_scanning_api_data = AsyncMock()
    hass.config_entries.async_get_entry = MagicMock(return_value=mock_config_entry)
    response = await async_handle_scanning_api(
        hass, mock_config_entry.entry_id, mock_request
    )
    assert response.status == 200
    mock_coordinator.async_handle_scanning_api_data.assert_called_once()


async def test_scanning_api_unsupported_method(hass: HomeAssistant, mock_config_entry):
    """Test unsupported HTTP method returns 405."""
    mock_config_entry.options = {CONF_ENABLE_SCANNING_API: True}
    request = AsyncMock()
    request.method = "PUT"  # Unsupported method
    hass.config_entries.async_get_entry = MagicMock(return_value=mock_config_entry)
    response = await async_handle_scanning_api(
        hass, mock_config_entry.entry_id, request
    )
    assert response.status == 405


async def test_scanning_api_missing_config_entry(hass: HomeAssistant, mock_request):
    """Test handling when config entry is not found."""
    hass.config_entries.async_get_entry = MagicMock(return_value=None)
    response = await async_handle_scanning_api(
        hass, "nonexistent_entry_id", mock_request
    )
    assert response.status == 404


async def test_handle_scanning_api_data_helper(
    hass: HomeAssistant, mock_config_entry, mock_coordinator
):
    """Test the _handle_scanning_api_data helper function directly."""
    mock_config_entry.options = {
        CONF_ENABLE_SCANNING_API: True,
        CONF_SCANNING_API_SECRET: "test_secret",
    }
    hass.data["meraki_ha"] = {
        mock_config_entry.entry_id: {"coordinator": mock_coordinator}
    }
    mock_coordinator.async_handle_scanning_api_data = AsyncMock()
    hass.config_entries.async_get_entry = MagicMock(return_value=mock_config_entry)

    data = {
        "secret": "test_secret",
        "type": "DevicesSeen",
        "data": {
            "apMac": "00:11:22:33:44:55",
            "observations": [
                {"clientMac": "aa:bb:cc:dd:ee:ff", "seenTime": "2024-01-15T12:00:00Z"}
            ],
        },
    }

    response = await _handle_scanning_api_data(hass, mock_config_entry.entry_id, data)
    assert response.status == 200
    mock_coordinator.async_handle_scanning_api_data.assert_called_once_with(
        data["data"]
    )


async def test_webhook_router_detects_scanning_api(
    hass: HomeAssistant, mock_config_entry, mock_coordinator
):
    """Test that webhook router correctly identifies and routes Scanning API data."""
    mock_config_entry.options = {
        CONF_ENABLE_SCANNING_API: True,
        CONF_SCANNING_API_SECRET: "test_secret",
    }
    hass.data["meraki_ha"] = {
        mock_config_entry.entry_id: {"coordinator": mock_coordinator}
    }
    mock_coordinator.async_handle_scanning_api_data = AsyncMock()
    hass.config_entries.async_get_entry = MagicMock(return_value=mock_config_entry)

    # Mock request with Scanning API data
    request = AsyncMock()
    request.method = "POST"
    request.json = AsyncMock(
        return_value={
            "secret": "test_secret",
            "type": "DevicesSeen",
            "data": {
                "apMac": "00:11:22:33:44:55",
                "observations": [],
            },
        }
    )

    response = await async_handle_webhook(hass, mock_config_entry.entry_id, request)
    assert response.status == 200
    mock_coordinator.async_handle_scanning_api_data.assert_called_once()


async def test_webhook_router_invalid_json(hass: HomeAssistant):
    """Test webhook router handles invalid JSON."""
    request = AsyncMock()
    request.json = AsyncMock(side_effect=ValueError("Invalid JSON"))

    response = await async_handle_webhook(hass, "test_entry", request)
    assert response.status == 400


async def test_scanning_api_non_devices_seen_type(
    hass: HomeAssistant, mock_config_entry, mock_coordinator
):
    """Test that non-DevicesSeen types are handled gracefully."""
    mock_config_entry.options = {
        CONF_ENABLE_SCANNING_API: True,
        CONF_SCANNING_API_SECRET: "test_secret",
    }
    hass.data["meraki_ha"] = {
        mock_config_entry.entry_id: {"coordinator": mock_coordinator}
    }
    mock_coordinator.async_handle_scanning_api_data = AsyncMock()
    hass.config_entries.async_get_entry = MagicMock(return_value=mock_config_entry)

    data = {
        "secret": "test_secret",
        "type": "BluetoothDevicesSeen",  # Different type
        "data": {"apMac": "00:11:22:33:44:55", "observations": []},
    }

    response = await _handle_scanning_api_data(hass, mock_config_entry.entry_id, data)
    assert response.status == 200
    # Should not call coordinator for non-DevicesSeen types
    mock_coordinator.async_handle_scanning_api_data.assert_not_called()
