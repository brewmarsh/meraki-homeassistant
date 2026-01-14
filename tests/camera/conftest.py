"""Fixtures for camera tests."""

from unittest.mock import AsyncMock, MagicMock

import pytest


@pytest.fixture
def mock_camera_service() -> MagicMock:
    """Fixture for a mocked CameraService."""
    service = MagicMock()
    service.get_camera_snapshot = AsyncMock(return_value=b"test_snapshot")
    service.get_rtsp_stream_url = AsyncMock(return_value="rtsp://test.com/stream")
    service.generate_snapshot = AsyncMock(return_value="http://test.com/snapshot.jpg")
    return service
