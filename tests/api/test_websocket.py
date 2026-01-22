"""Tests for the Meraki HA WebSocket API."""

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry, mock_component

from custom_components.meraki_ha.api.websocket import (
    ws_get_camera_snapshot,
    ws_get_camera_stream_url,
    ws_get_version,
    ws_subscribe_meraki_data,
)
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


@pytest.fixture
async def setup_integration(hass: HomeAssistant) -> MockConfigEntry:
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

        # Store mocks in hass data for retrieval in tests if needed,
        # or just rely on the fact they are patched globally in this scope
        hass.data[DOMAIN]["mocks"] = {
            "get_video_stream_url": mock_get_stream,
            "get_camera_snapshot": mock_get_snapshot,
        }

        yield config_entry

        await hass.config_entries.async_unload(config_entry.entry_id)
        await hass.async_block_till_done()


@pytest.mark.asyncio
async def test_subscribe_meraki_data(
    hass: HomeAssistant,
    setup_integration,
) -> None:
    """Test subscribing to Meraki data."""
    mock_connection = MagicMock()
    mock_connection.subscriptions = {}
    mock_msg = {
        "id": 1,
        "type": "meraki_ha/subscribe_meraki_data",
        "config_entry_id": setup_integration.entry_id,
    }

    # Call the handler directly
    ws_subscribe_meraki_data(hass, mock_connection, mock_msg)

    # Check that send_result was called with the correct data
    mock_connection.send_result.assert_called_once()
    args, _ = mock_connection.send_result.call_args
    msg_id, data = args

    assert msg_id == 1
    assert data["org_name"] == "Test Org"
    assert "data" not in data or "org_name" not in data["data"]

    # Cleanup subscription
    if 1 in mock_connection.subscriptions:
        mock_connection.subscriptions[1]()

    await hass.async_block_till_done()


@pytest.mark.asyncio
async def test_get_version(
    hass: HomeAssistant,
    setup_integration,
) -> None:
    """Test getting the version."""
    mock_connection = MagicMock()
    mock_msg = {
        "id": 1,
        "type": "meraki_ha/get_version",
    }

    # Call the wrapped function directly
    await ws_get_version.__wrapped__(hass, mock_connection, mock_msg)

    mock_connection.send_result.assert_called_once()
    args, _ = mock_connection.send_result.call_args
    msg_id, data = args
    assert msg_id == 1
    assert "version" in data


@pytest.mark.asyncio
async def test_get_camera_stream_url(
    hass: HomeAssistant,
    setup_integration,
) -> None:
    """Test getting camera stream URL."""
    mock_get_stream = hass.data[DOMAIN]["mocks"]["get_video_stream_url"]
    mock_get_stream.return_value = "rtsp://test-url"

    mock_connection = MagicMock()
    mock_msg = {
        "id": 1,
        "type": "meraki_ha/get_camera_stream_url",
        "config_entry_id": setup_integration.entry_id,
        "serial": "test-serial",
    }

    # Call the wrapped function directly
    await ws_get_camera_stream_url.__wrapped__(hass, mock_connection, mock_msg)

    mock_connection.send_result.assert_called_once()
    args, _ = mock_connection.send_result.call_args
    msg_id, data = args

    assert msg_id == 1
    assert data["url"] == "rtsp://test-url"

    mock_get_stream.assert_called_with("test-serial")


@pytest.mark.asyncio
async def test_get_camera_snapshot(
    hass: HomeAssistant,
    setup_integration,
) -> None:
    """Test getting camera snapshot."""
    mock_get_snapshot = hass.data[DOMAIN]["mocks"]["get_camera_snapshot"]
    mock_get_snapshot.return_value = "https://snapshot-url"

    mock_connection = MagicMock()
    mock_msg = {
        "id": 1,
        "type": "meraki_ha/get_camera_snapshot",
        "config_entry_id": setup_integration.entry_id,
        "serial": "test-serial",
    }

    # Call the wrapped function directly
    await ws_get_camera_snapshot.__wrapped__(hass, mock_connection, mock_msg)

    mock_connection.send_result.assert_called_once()
    args, _ = mock_connection.send_result.call_args
    msg_id, data = args

    assert msg_id == 1
    assert data["url"] == "https://snapshot-url"

    mock_get_snapshot.assert_called_with("test-serial")
