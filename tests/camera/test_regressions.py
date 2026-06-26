"""Tests for camera NameError and None fallback regressions."""

from unittest.mock import MagicMock

import pytest

from custom_components.meraki_ha.camera import MerakiRTSPStreamCamera
from tests.const import MOCK_CAMERA_DEVICE


@pytest.fixture
def mock_coordinator_no_device():
    """Coordinator that returns None for get_device."""
    coordinator = MagicMock()
    coordinator.get_device.return_value = None
    coordinator.data = {}  # Ensure available() fails
    return coordinator


@pytest.fixture
def camera_no_device(
    mock_coordinator_no_device,
    mock_config_entry,
    mock_camera_service,
):
    """Camera entity where coordinator returns None for device."""
    return MerakiRTSPStreamCamera(
        coordinator=mock_coordinator_no_device,
        device=MOCK_CAMERA_DEVICE,
        camera_service=mock_camera_service,
        config_entry=mock_config_entry,
    )


def test_camera_device_data_none_safe(camera_no_device):
    """Test that device_data returning None doesn't crash."""
    # This would have crashed before if it used MerakiDevice() fallback without import
    assert camera_no_device.device_data is None

    # Test property access safety
    assert camera_no_device.available is False
    assert camera_no_device.is_streaming is False
    assert camera_no_device.extra_state_attributes == {}


async def test_camera_image_none_safe(camera_no_device):
    """Test that async_camera_image handles None device_data."""
    assert await camera_no_device.async_camera_image() is None
