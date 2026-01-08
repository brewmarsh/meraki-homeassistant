"""Tests for the MerakiCameraSenseStatusSensor."""

from unittest.mock import MagicMock

import pytest

from custom_components.meraki_ha.sensor.device.camera_sense_status import (
    MerakiCameraSenseStatusSensor,
)
from tests.const import MOCK_CAMERA_DEVICE


@pytest.fixture
def mock_camera_device_sense_enabled() -> dict:
    """Create a camera device with Sense enabled."""
    device = MOCK_CAMERA_DEVICE.copy()
    device["sense_settings"] = {
        "senseEnabled": True,
    }
    return device


@pytest.fixture
def mock_camera_device_sense_disabled() -> dict:
    """Create a camera device with Sense disabled."""
    device = MOCK_CAMERA_DEVICE.copy()
    device["sense_settings"] = {
        "senseEnabled": False,
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
    mock_camera_device_sense_enabled: dict,
) -> None:
    """Test sensor initializes with correct unique_id and device_info."""
    mock_coordinator.data = {"devices": [mock_camera_device_sense_enabled]}

    sensor = MerakiCameraSenseStatusSensor(
        coordinator=mock_coordinator,
        device_data=mock_camera_device_sense_enabled,
        config_entry=mock_config_entry,
    )

    assert sensor._device_serial == mock_camera_device_sense_enabled["serial"]
    assert (
        sensor._attr_unique_id
        == f"{mock_camera_device_sense_enabled['serial']}_camera_sense_status"
    )
    assert sensor.entity_description.key == "camera_sense_status"
    assert sensor.entity_description.name == "Sense Enabled"


def test_sensor_enabled_state(
    mock_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_camera_device_sense_enabled: dict,
) -> None:
    """Test sensor shows 'enabled' when Sense is enabled."""
    mock_coordinator.data = {"devices": [mock_camera_device_sense_enabled]}

    sensor = MerakiCameraSenseStatusSensor(
        coordinator=mock_coordinator,
        device_data=mock_camera_device_sense_enabled,
        config_entry=mock_config_entry,
    )

    assert sensor._attr_native_value == "enabled"
    assert sensor._attr_icon == "mdi:camera-iris"


def test_sensor_disabled_state(
    mock_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_camera_device_sense_disabled: dict,
) -> None:
    """Test sensor shows 'disabled' when Sense is disabled."""
    mock_coordinator.data = {"devices": [mock_camera_device_sense_disabled]}

    sensor = MerakiCameraSenseStatusSensor(
        coordinator=mock_coordinator,
        device_data=mock_camera_device_sense_disabled,
        config_entry=mock_config_entry,
    )

    assert sensor._attr_native_value == "disabled"
    assert sensor._attr_icon == "mdi:camera-off-outline"


def test_sensor_not_configured_state(
    mock_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_camera_device_no_sense: dict,
) -> None:
    """Test sensor shows 'not_configured' when Sense is not licensed."""
    mock_coordinator.data = {"devices": [mock_camera_device_no_sense]}

    sensor = MerakiCameraSenseStatusSensor(
        coordinator=mock_coordinator,
        device_data=mock_camera_device_no_sense,
        config_entry=mock_config_entry,
    )

    assert sensor._attr_native_value == "not_configured"
    assert sensor._attr_icon == "mdi:camera-off-outline"


def test_sensor_available_when_device_exists(
    mock_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_camera_device_sense_enabled: dict,
) -> None:
    """Test sensor is available when device exists in coordinator."""
    mock_coordinator.data = {"devices": [mock_camera_device_sense_enabled]}
    mock_coordinator.last_update_success = True

    sensor = MerakiCameraSenseStatusSensor(
        coordinator=mock_coordinator,
        device_data=mock_camera_device_sense_enabled,
        config_entry=mock_config_entry,
    )

    assert sensor.available is True


def test_sensor_unavailable_when_device_missing(
    mock_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_camera_device_sense_enabled: dict,
) -> None:
    """Test sensor is unavailable when device is missing from coordinator."""
    mock_coordinator.data = {"devices": [mock_camera_device_sense_enabled]}

    sensor = MerakiCameraSenseStatusSensor(
        coordinator=mock_coordinator,
        device_data=mock_camera_device_sense_enabled,
        config_entry=mock_config_entry,
    )

    # Remove device from coordinator
    mock_coordinator.data = {"devices": []}
    mock_coordinator.last_update_success = True

    assert sensor.available is False


def test_sensor_handle_coordinator_update(
    mock_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_camera_device_sense_enabled: dict,
) -> None:
    """Test sensor updates state when coordinator data changes."""
    mock_coordinator.data = {"devices": [mock_camera_device_sense_enabled]}

    sensor = MerakiCameraSenseStatusSensor(
        coordinator=mock_coordinator,
        device_data=mock_camera_device_sense_enabled,
        config_entry=mock_config_entry,
    )

    # Initial state
    assert sensor._attr_native_value == "enabled"

    # Update device data to disable Sense
    updated_device = mock_camera_device_sense_enabled.copy()
    updated_device["sense_settings"] = {"senseEnabled": False}
    mock_coordinator.data = {"devices": [updated_device]}

    # Simulate coordinator update
    sensor._update_sensor_data()

    assert sensor._attr_native_value == "disabled"
    assert sensor._attr_icon == "mdi:camera-off-outline"


def test_sensor_extra_state_attributes(
    mock_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_camera_device_sense_enabled: dict,
) -> None:
    """Test sensor includes serial number in extra state attributes."""
    mock_coordinator.data = {"devices": [mock_camera_device_sense_enabled]}

    sensor = MerakiCameraSenseStatusSensor(
        coordinator=mock_coordinator,
        device_data=mock_camera_device_sense_enabled,
        config_entry=mock_config_entry,
    )

    assert sensor._attr_extra_state_attributes is not None
    assert (
        sensor._attr_extra_state_attributes["serial_number"]
        == mock_camera_device_sense_enabled["serial"]
    )
