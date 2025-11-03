"""Fixtures for camera tests."""
from unittest.mock import AsyncMock

import pytest


@pytest.fixture
def mock_camera_service() -> AsyncMock:
    """Fixture for a mocked CameraService."""
    return AsyncMock()
