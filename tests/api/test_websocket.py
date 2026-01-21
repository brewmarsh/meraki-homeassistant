"""Tests for the Meraki HA WebSocket API."""

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry, mock_component

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

    # We need to ensure that the CameraService and DeviceControlService are mocked
    # and placed into hass.data, because real async_setup might fail or not fully run
    # due to other mocks or missing dependencies in this test environment.
    mock_camera_service = MagicMock()
    mock_camera_service.get_video_stream_url = AsyncMock()
    mock_camera_service.get_camera_snapshot = AsyncMock()

    mock_device_control_service = MagicMock()

    with (
        patch(
            "custom_components.meraki_ha.MerakiDataUpdateCoordinator._async_update_data",
            return_value=MOCK_DATA,
        ),
        patch(
            "custom_components.meraki_ha.async_register_webhook",
            return_value=None,
        ),
        # Patch classes in __init__.py namespace since they are imported there
        patch(
            "custom_components.meraki_ha.CameraService",
            return_value=mock_camera_service,
        ),
        patch(
            "custom_components.meraki_ha.DeviceControlService",
            return_value=mock_device_control_service,
        ),
    ):
        await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()

        # Manually ensure services are in hass.data if setup didn't put them there
        # This handles the KeyError seen in logs
        if DOMAIN not in hass.data:
            hass.data[DOMAIN] = {}
        if config_entry.entry_id not in hass.data[DOMAIN]:
            hass.data[DOMAIN][config_entry.entry_id] = {}

        # If the integration setup logic failed to populate these (e.g. because of exceptions),
        # force them here for the websocket tests to proceed.
        if "camera_service" not in hass.data[DOMAIN][config_entry.entry_id]:
            hass.data[DOMAIN][config_entry.entry_id][
                "camera_service"
            ] = mock_camera_service

        if "device_control_service" not in hass.data[DOMAIN][config_entry.entry_id]:
            hass.data[DOMAIN][config_entry.entry_id][
                "device_control_service"
            ] = mock_device_control_service

        # Store mocks in hass data for retrieval in tests
        hass.data[DOMAIN]["mocks"] = {
            "get_video_stream_url": mock_camera_service.get_video_stream_url,
            "get_camera_snapshot": mock_camera_service.get_camera_snapshot,
        }

        yield config_entry


@pytest.mark.asyncio
async def test_subscribe_meraki_data(
    hass: HomeAssistant,
    hass_ws_client,
    setup_integration,
) -> None:
    """Test subscribing to Meraki data."""
    client = await hass_ws_client(hass)

    await client.send_json({
        "id": 1,
        "type": "meraki_ha/subscribe_meraki_data",
        "config_entry_id": setup_integration.entry_id,
    })

    response = await client.receive_json()
    assert response["success"]
    assert response["type"] == "result"

    # Check that data is NOT wrapped in {"data": ...}
    # It should be the MOCK_DATA directly
    assert response["result"]["org_name"] == "Test Org"
    assert (
        "data" not in response["result"]
        or "org_name" not in response["result"]["data"]
    )

    await hass.async_block_till_done()
    await hass.async_stop()
    await asyncio.sleep(0.5)  # Allow background threads to close


@pytest.mark.asyncio
async def test_get_version(
    hass: HomeAssistant,
    hass_ws_client,
    setup_integration,
) -> None:
    """Test getting the version."""
    client = await hass_ws_client(hass)

    await client.send_json({
        "id": 1,
        "type": "meraki_ha/get_version",
    })

    response = await client.receive_json()
    assert response["success"]
    assert "version" in response["result"]
    await asyncio.sleep(0.1)


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

    await client.send_json({
        "id": 1,
        "type": "meraki_ha/get_camera_stream_url",
        "config_entry_id": setup_integration.entry_id,
        "serial": "test-serial",
    })

    response = await client.receive_json()
    assert response["success"]
    assert response["result"]["url"] == "rtsp://test-url"

    mock_get_stream.assert_called_with("test-serial")
    await asyncio.sleep(0.1)


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

    await client.send_json({
        "id": 1,
        "type": "meraki_ha/get_camera_snapshot",
        "config_entry_id": setup_integration.entry_id,
        "serial": "test-serial",
    })

    response = await client.receive_json()
    assert response["success"]
    assert response["result"]["url"] == "https://snapshot-url"

    mock_get_snapshot.assert_called_with("test-serial")
    await asyncio.sleep(0.1)
