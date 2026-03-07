"""Tests for the Camera Endpoints."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from custom_components.meraki_ha.core.api.endpoints.camera import CameraEndpoints


@pytest.fixture
def mock_client():
    """Mock the Meraki API client."""
    client = MagicMock()
    client.dashboard = MagicMock()
    client.run_sync = AsyncMock()
    return client

@pytest.fixture
def camera_endpoints(mock_client):
    """Fixture for the CameraEndpoints."""
    return CameraEndpoints(mock_client)

@pytest.mark.asyncio
async def test_update_camera_sense_settings_repro(camera_endpoints, mock_client):
    """Test update_camera_sense_settings reproduction of snake_case issue."""
    serial = "cam123"

    # Simulating what AnalyticsSwitch._async_update_setting does
    await camera_endpoints.update_camera_sense_settings(
        serial=serial,
        sense_enabled=True,
    )

    mock_client.run_sync.assert_called_once()
    args, kwargs = mock_client.run_sync.call_args
    assert args[0] == mock_client.dashboard.camera.updateDeviceCameraSense
    assert kwargs["serial"] == serial
    # This should now PASS with the fix
    assert "sense_enabled" not in kwargs
    assert "senseEnabled" in kwargs
    assert kwargs["senseEnabled"] is True

@pytest.mark.asyncio
async def test_update_camera_video_settings(camera_endpoints, mock_client):
    """Test update_camera_video_settings correctly maps keys."""
    serial = "cam123"

    await camera_endpoints.update_camera_video_settings(
        serial=serial,
        external_rtsp_enabled=True,
    )

    mock_client.run_sync.assert_called_once()
    args, kwargs = mock_client.run_sync.call_args
    assert args[0] == mock_client.dashboard.camera.updateDeviceCameraVideoSettings
    assert kwargs["serial"] == serial
    assert "external_rtsp_enabled" not in kwargs
    assert "externalRtspEnabled" in kwargs
    assert kwargs["externalRtspEnabled"] is True
