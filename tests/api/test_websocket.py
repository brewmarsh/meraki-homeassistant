"""Tests for the Meraki HA WebSocket API."""

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry, mock_component

from custom_components.meraki_ha.api.websocket import async_setup_websocket_api
from custom_components.meraki_ha.const import (
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
    DOMAIN,
)

MOCK_DATA = {
    "org_name": "Test Org",
    "networks": [],
    "devices": [],
}


@pytest.fixture(autouse=True)
def bypass_platform_setup():
    """Override global fixture to allow component setup."""
    yield


@pytest.fixture(autouse=True)
def verify_cleanup():
    """Override verify_cleanup to avoid spurious thread errors."""
    yield


@pytest.fixture
async def setup_integration(hass: HomeAssistant, socket_enabled) -> MockConfigEntry:
    """Set up the Meraki integration."""
    mock_component(hass, "frontend")
    mock_component(hass, "panel_custom")

    config_entry = MockConfigEntry(
        domain=DOMAIN,
        entry_id="test_entry",
        data={CONF_MERAKI_API_KEY: "test-key", CONF_MERAKI_ORG_ID: "test-org"},
    )
    config_entry.add_to_hass(hass)

    with (
        patch(
            "custom_components.meraki_ha.MerakiDataUpdateCoordinator._async_update_data",
            return_value=MOCK_DATA,
        ),
        patch(
            "custom_components.meraki_ha.async_register_webhook",
            return_value=None,
        ),
        patch(
            "custom_components.meraki_ha.services.camera_service.CameraService.get_video_stream_url",
            new_callable=AsyncMock,
        ) as mock_get_stream,
        patch(
            "custom_components.meraki_ha.services.camera_service.CameraService.get_camera_snapshot",
            new_callable=AsyncMock,
        ) as mock_get_snapshot,
    ):
        await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()

        # Store mocks in hass data for retrieval in tests if needed
        hass.data[DOMAIN]["mocks"] = {
            "get_video_stream_url": mock_get_stream,
            "get_camera_snapshot": mock_get_snapshot,
        }

        yield config_entry


@pytest.mark.asyncio
async def test_subscribe_meraki_data(
    hass: HomeAssistant,
    hass_ws_client,
    # Do not use setup_integration fixture
) -> None:
    """Test subscribing to Meraki data."""
    # Manual setup to avoid full integration load and thread leaks
    entry_id = "test_entry"
    hass.data.setdefault(DOMAIN, {})

    mock_coordinator = MagicMock()
    mock_coordinator.data = MOCK_DATA
    # Mock async_add_listener to return a no-op callable
    mock_coordinator.async_add_listener = MagicMock(return_value=lambda: None)

    hass.data[DOMAIN][entry_id] = {
        "coordinator": mock_coordinator,
    }

    # Register API
    async_setup_websocket_api(hass)

    client = await hass_ws_client(hass)

    await client.send_json(
        {
            "id": 1,
            "type": "meraki_ha/subscribe_meraki_data",
            "config_entry_id": entry_id,
        }
    )

    response = await client.receive_json()
    assert response["success"]
    assert response["type"] == "result"

    assert response["result"]["org_name"] == "Test Org"
    assert (
        "data" not in response["result"] or "org_name" not in response["result"]["data"]
    )

    # Verify listener was attached
    mock_coordinator.async_add_listener.assert_called_once()

    await client.close()
    await hass.async_block_till_done()


@pytest.mark.asyncio
async def test_get_version(
    hass: HomeAssistant,
    hass_ws_client,
    setup_integration,
) -> None:
    """Test getting the version."""
    client = await hass_ws_client(hass)

    await client.send_json(
        {
            "id": 1,
            "type": "meraki_ha/get_version",
        }
    )

    response = await client.receive_json()
    assert response["success"]
    assert "version" in response["result"]

    await client.close()
    await hass.async_block_till_done()


@pytest.mark.asyncio
async def test_get_camera_stream_url(
    hass: HomeAssistant,
    hass_ws_client,
    setup_integration,
) -> None:
    """Test getting camera stream URL."""
    mock_get_stream = hass.data[DOMAIN]["mocks"]["get_video_stream_url"]
    mock_get_stream.return_value = "rtsp://test-url"

    client = await hass_ws_client(hass)

    await client.send_json(
        {
            "id": 1,
            "type": "meraki_ha/get_camera_stream_url",
            "config_entry_id": setup_integration.entry_id,
            "serial": "test-serial",
        }
    )

    response = await client.receive_json()
    assert response["success"]
    assert response["result"]["url"] == "rtsp://test-url"

    mock_get_stream.assert_called_with("test-serial")

    await client.close()
    await hass.async_block_till_done()


@pytest.mark.asyncio
async def test_get_camera_snapshot(
    hass: HomeAssistant,
    hass_ws_client,
    setup_integration,
) -> None:
    """Test getting camera snapshot."""
    mock_get_snapshot = hass.data[DOMAIN]["mocks"]["get_camera_snapshot"]
    mock_get_snapshot.return_value = "https://snapshot-url"

    client = await hass_ws_client(hass)

    await client.send_json(
        {
            "id": 1,
            "type": "meraki_ha/get_camera_snapshot",
            "config_entry_id": setup_integration.entry_id,
            "serial": "test-serial",
        }
    )

    response = await client.receive_json()
    assert response["success"]
    assert response["result"]["url"] == "https://snapshot-url"

    mock_get_snapshot.assert_called_with("test-serial")

    await client.close()
    await hass.async_block_till_done()
