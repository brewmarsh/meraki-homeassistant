"""Test CameraFetchStrategy."""

from unittest.mock import MagicMock

import pytest

from custom_components.meraki_ha.core.fetch_strategies.camera import (
    CameraFetchStrategy,
)
from custom_components.meraki_ha.core.models.device import MerakiDevice


@pytest.fixture
def mock_client():
    """Fixture for a mock Meraki API client."""
    client = MagicMock()
    # Mock run_with_semaphore to just return the coroutine/call
    client.run_with_semaphore.side_effect = lambda x: x
    return client


@pytest.fixture
def disabled_features():
    """Fixture for the disabled features set."""
    return set()


@pytest.fixture
def strategy(mock_client, disabled_features):
    """Fixture for the CameraFetchStrategy."""
    return CameraFetchStrategy(
        client=mock_client,
        _disabled_features=disabled_features,
    )


def test_build_device_tasks(strategy):
    """Test that build_device_tasks adds camera-specific tasks."""
    mock_device = MagicMock()
    mock_device.serial = "SERIAL1"
    tasks = {}

    # Must increment poll count so should_fetch_sense is True
    strategy.increment_poll_count()
    strategy.build_device_tasks(mock_device, tasks, capabilities=["camera_stream", "analytics"])

    assert f"video_settings_{mock_device.serial}" in tasks
    assert f"sense_settings_{mock_device.serial}" in tasks
    assert f"camera_analytics_{mock_device.serial}" in tasks


def test_build_device_tasks_skips_analytics_if_in_detail_data(strategy):
    """Test that build_device_tasks skips analytics if already in detail_data."""
    mock_device = MagicMock()
    mock_device.serial = "SERIAL1"
    tasks = {}
    detail_data = {f"camera_analytics_{mock_device.serial}": [{"some": "data"}]}

    # Must increment poll count so should_fetch_sense is True
    strategy.increment_poll_count()
    strategy.build_device_tasks(mock_device, tasks, capabilities=["camera_stream", "analytics"], detail_data=detail_data)

    assert f"video_settings_{mock_device.serial}" in tasks
    assert f"sense_settings_{mock_device.serial}" in tasks
    assert f"camera_analytics_{mock_device.serial}" not in tasks


def test_process_device_details_video_settings(strategy):
    """Test processing device details for camera video settings."""
    mock_device = MagicMock()
    mock_device.serial = "SERIAL1"
    key = f"video_settings_{mock_device.serial}"
    detail_data = {
        key: {
            "rtsp_url": "rtsp://test.com/stream",
            "rtspServerEnabled": True,
        }
    }

    strategy.process_device_details(mock_device, detail_data, None)

    assert mock_device.video_settings == detail_data[key]
    assert mock_device.rtsp_url == "rtsp://test.com/stream"


def test_process_device_details_sense_settings(strategy):
    """Test processing device details for camera sense settings."""
    mock_device = MagicMock()
    mock_device.serial = "SERIAL1"
    key = f"sense_settings_{mock_device.serial}"
    detail_data = {
        key: {
            "senseEnabled": True,
        }
    }

    strategy.process_device_details(mock_device, detail_data, None)

    assert mock_device.sense_settings == detail_data[key]


def test_process_device_details_analytics(strategy):
    """Test processing device details for camera analytics."""
    mock_device = MagicMock()
    mock_device.serial = "SERIAL1"
    key = f"camera_analytics_{mock_device.serial}"
    detail_data = {
        key: [{"zoneId": "1", "entrances": 5}]
    }

    strategy.process_device_details(mock_device, detail_data, None)

    assert mock_device.analytics == detail_data[key]


def test_process_device_details_fallback_to_prev(strategy):
    """Test processing device details falls back to previous data."""
    mock_device = MagicMock()
    mock_device.serial = "SERIAL1"
    detail_data = {}
    prev_device = MerakiDevice(
        serial="SERIAL1",
        video_settings={"rtsp_url": "rtsp://prev.com"},
        rtsp_url="rtsp://prev.com",
        sense_settings={"sense": "prev"},
        analytics=[{"prev": "data"}],
    )

    strategy.process_device_details(mock_device, detail_data, prev_device)

    assert mock_device.video_settings == prev_device.video_settings
    assert mock_device.rtsp_url == prev_device.rtsp_url
    assert mock_device.sense_settings == prev_device.sense_settings
    assert mock_device.analytics == prev_device.analytics
