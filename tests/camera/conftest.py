"""Fixtures for camera tests."""

from unittest.mock import AsyncMock

import pytest


@pytest.fixture
def mock_camera_service() -> AsyncMock:
    """Fixture for a mocked CameraService."""
    service = AsyncMock()
    service.get_camera_snapshot = AsyncMock(return_value=b"test_snapshot")
    service.get_rtsp_stream_url = AsyncMock(return_value="rtsp://test.com/stream")
    service.generate_snapshot = AsyncMock(return_value="http://test.com/snapshot.jpg")
    service.async_set_rtsp_stream_enabled = AsyncMock()
    service.get_supported_analytics = AsyncMock(return_value=[])
    service.get_motion_history = AsyncMock(return_value=[])
    return service
