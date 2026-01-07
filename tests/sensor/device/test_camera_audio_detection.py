"""Tests for the MerakiCameraAudioDetectionSensor."""

from unittest.mock import MagicMock

import pytest

from custom_components.meraki_ha.sensor.device.camera_audio_detection import (
    MerakiCameraAudioDetectionSensor,
)
from tests.const import MOCK_CAMERA_DEVICE


@pytest.fixture
def mock_camera_device_with_sense() -> dict:
    """Create a camera device with Sense settings enabled."""
    device = MOCK_CAMERA_DEVICE.copy()
    device["sense_settings"] = {
        "senseEnabled": True,
        "audioDetection": {"enabled": True},
    }
    return device


@pytest.fixture
def mock_camera_device_sense_disabled() -> dict:
    """Create a camera device with Sense audio detection disabled."""
    device = MOCK_CAMERA_DEVICE.copy()
    device["sense_settings"] = {
        "senseEnabled": True,
        "audioDetection": {"enabled": False},
    }
    return device


@pytest.fixture
def mock_camera_device_no_sense() -> dict:
    """Create a camera device without Sense settings."""
    device = MOCK_CAMERA_DEVICE.copy()
    device["sense_settings"] = {}
    return device


def test_sensor_initialization(
    mock_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_camera_device_with_sense: dict,
) -> None:
    """Test sensor initializes with correct unique_id and device_info."""
    mock_coordinator.data = {"devices": [mock_camera_device_with_sense]}

    sensor = MerakiCameraAudioDetectionSensor(
        coordinator=mock_coordinator,
        device_data=mock_camera_device_with_sense,
        config_entry=mock_config_entry,
    )

    assert sensor._device_serial == mock_camera_device_with_sense["serial"]
    assert (
        sensor._attr_unique_id
        == f"{mock_camera_device_with_sense['serial']}_camera_audio_detection_status"
    )
    assert sensor.entity_description.key == "camera_audio_detection_status"
    assert sensor.entity_description.name == "Audio Detection"


def test_sensor_enabled_state(
    mock_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_camera_device_with_sense: dict,
) -> None:
    """Test sensor shows 'enabled' when audio detection is enabled."""
    mock_coordinator.data = {"devices": [mock_camera_device_with_sense]}

    sensor = MerakiCameraAudioDetectionSensor(
        coordinator=mock_coordinator,
        device_data=mock_camera_device_with_sense,
        config_entry=mock_config_entry,
    )

    assert sensor._attr_native_value == "enabled"
    assert sensor._attr_icon == "mdi:microphone"


def test_sensor_disabled_state(
    mock_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_camera_device_sense_disabled: dict,
) -> None:
    """Test sensor shows 'disabled' when audio detection is disabled."""
    mock_coordinator.data = {"devices": [mock_camera_device_sense_disabled]}

    sensor = MerakiCameraAudioDetectionSensor(
        coordinator=mock_coordinator,
        device_data=mock_camera_device_sense_disabled,
        config_entry=mock_config_entry,
    )

    assert sensor._attr_native_value == "disabled"
    assert sensor._attr_icon == "mdi:microphone-off"


def test_sensor_not_configured_state(
    mock_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_camera_device_no_sense: dict,
) -> None:
    """Test sensor shows 'not_configured' when Sense is not licensed/configured."""
    mock_coordinator.data = {"devices": [mock_camera_device_no_sense]}

    sensor = MerakiCameraAudioDetectionSensor(
        coordinator=mock_coordinator,
        device_data=mock_camera_device_no_sense,
        config_entry=mock_config_entry,
    )

    assert sensor._attr_native_value == "not_configured"
    assert sensor._attr_icon == "mdi:microphone-off"


def test_sensor_unavailable_when_device_missing(
    mock_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_camera_device_with_sense: dict,
) -> None:
    """Test sensor becomes unavailable when device is missing from coordinator."""
    mock_coordinator.data = {"devices": [mock_camera_device_with_sense]}

    sensor = MerakiCameraAudioDetectionSensor(
        coordinator=mock_coordinator,
        device_data=mock_camera_device_with_sense,
        config_entry=mock_config_entry,
    )

    # Now remove the device from coordinator data
    mock_coordinator.data = {"devices": []}
    mock_coordinator.last_update_success = True

    assert sensor.available is False


def test_sensor_available_when_device_exists(
    mock_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_camera_device_with_sense: dict,
) -> None:
    """Test sensor is available when device exists in coordinator."""
    mock_coordinator.data = {"devices": [mock_camera_device_with_sense]}
    mock_coordinator.last_update_success = True

    sensor = MerakiCameraAudioDetectionSensor(
        coordinator=mock_coordinator,
        device_data=mock_camera_device_with_sense,
        config_entry=mock_config_entry,
    )

    assert sensor.available is True


def test_sensor_handle_coordinator_update(
    mock_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_camera_device_with_sense: dict,
) -> None:
    """Test sensor updates state when coordinator data changes."""
    mock_coordinator.data = {"devices": [mock_camera_device_with_sense]}

    sensor = MerakiCameraAudioDetectionSensor(
        coordinator=mock_coordinator,
        device_data=mock_camera_device_with_sense,
        config_entry=mock_config_entry,
    )

    # Initial state
    assert sensor._attr_native_value == "enabled"

    # Update device data to disable audio detection
    updated_device = mock_camera_device_with_sense.copy()
    updated_device["sense_settings"] = {
        "audioDetection": {"enabled": False},
    }
    mock_coordinator.data = {"devices": [updated_device]}

    # Simulate coordinator update
    sensor._update_sensor_data()

    assert sensor._attr_native_value == "disabled"
    assert sensor._attr_icon == "mdi:microphone-off"


def test_sensor_extra_state_attributes(
    mock_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_camera_device_with_sense: dict,
) -> None:
    """Test sensor includes serial number in extra state attributes."""
    mock_coordinator.data = {"devices": [mock_camera_device_with_sense]}

    sensor = MerakiCameraAudioDetectionSensor(
        coordinator=mock_coordinator,
        device_data=mock_camera_device_with_sense,
        config_entry=mock_config_entry,
    )

    assert sensor._attr_extra_state_attributes is not None
    assert (
        sensor._attr_extra_state_attributes["serial_number"]
        == mock_camera_device_with_sense["serial"]
    )
