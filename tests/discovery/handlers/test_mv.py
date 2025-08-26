"""Tests for the MVHandler."""

from unittest.mock import MagicMock
import pytest
from custom_components.meraki_ha.discovery.handlers.mv import MVHandler
from custom_components.meraki_ha.sensor.device.camera_rtsp_url import (
    MerakiCameraRTSPUrlSensor,
)
from tests.const import MOCK_DEVICE

@pytest.fixture
def mock_coordinator():
    """Fixture for a mocked MerakiDataCoordinator."""
    return MagicMock()

@pytest.fixture
def mock_config_entry():
    """Fixture for a mocked config entry."""
    return MagicMock()

def test_mv_handler_with_video_settings(mock_coordinator, mock_config_entry):
    """Test that the MVHandler discovers the RTSP sensor."""
    # Arrange
    device = MOCK_DEVICE.copy()
    device["video_settings"] = {"externalRtspEnabled": True}
    handler = MVHandler(mock_coordinator, device, mock_config_entry)

    # Act
    entities = handler.discover_entities()

    # Assert
    assert len(entities) == 1
    assert isinstance(entities[0], MerakiCameraRTSPUrlSensor)

def test_mv_handler_without_video_settings(mock_coordinator, mock_config_entry):
    """Test that the MVHandler discovers no sensors if video_settings are missing."""
    # Arrange
    device = MOCK_DEVICE.copy()
    handler = MVHandler(mock_coordinator, device, mock_config_entry)

    # Act
    entities = handler.discover_entities()

    # Assert
    assert len(entities) == 0
