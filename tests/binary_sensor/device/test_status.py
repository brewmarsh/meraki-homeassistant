"""Tests for Meraki hardware connectivity binary sensors."""

from unittest.mock import MagicMock, patch

import pytest

from custom_components.meraki_ha.binary_sensor.device.status import (
    MerakiConnectivityBinarySensor,
)
from homeassistant.components.binary_sensor import BinarySensorDeviceClass


@pytest.fixture
def mock_device():
    """Mock Meraki device."""
    device = MagicMock()
    device.serial = "Q2XX-XXXX-XXXX"
    device.model = "MR36"
    device.status = "online"
    device.status_messages = []
    return device


@pytest.fixture
def mock_coordinator():
    """Mock coordinator."""
    coordinator = MagicMock()
    coordinator.data = {"devices": []}
    return coordinator


def test_connectivity_binary_sensor_init(mock_coordinator, mock_device):
    """Test initial state of the connectivity binary sensor."""
    sensor = MerakiConnectivityBinarySensor(mock_coordinator, mock_device)

    assert sensor.unique_id == "Q2XX-XXXX-XXXX_connectivity"
    assert sensor.device_class == BinarySensorDeviceClass.CONNECTIVITY
    assert sensor.name == "Connectivity"


def test_connectivity_binary_sensor_state(mock_coordinator, mock_device):
    """Test the state mapping of the connectivity binary sensor."""
    sensor = MerakiConnectivityBinarySensor(mock_coordinator, mock_device)

    # Mock device_data property to return our mock_device
    with patch.object(MerakiConnectivityBinarySensor, "device_data", mock_device):
        # Online
        mock_device.status = "online"
        assert sensor.is_on is True

        # Alerting
        mock_device.status = "alerting"
        assert sensor.is_on is True

        # Offline
        mock_device.status = "offline"
        assert sensor.is_on is False

        # Unknown
        mock_device.status = "unknown"
        assert sensor.is_on is False


def test_connectivity_binary_sensor_availability(mock_coordinator, mock_device):
    """Test the availability of the connectivity binary sensor."""
    sensor = MerakiConnectivityBinarySensor(mock_coordinator, mock_device)

    # Coordinator has data and device is found
    mock_coordinator.data = {"devices": [mock_device]}
    with patch.object(MerakiConnectivityBinarySensor, "device_data", mock_device):
        assert sensor.available is True

    # Device not found
    with patch.object(MerakiConnectivityBinarySensor, "device_data", None):
        assert sensor.available is False

    # Coordinator has no data
    mock_coordinator.data = None
    assert sensor.available is False


def test_connectivity_binary_sensor_attributes(mock_coordinator, mock_device):
    """Test the extra state attributes of the connectivity binary sensor."""
    sensor = MerakiConnectivityBinarySensor(mock_coordinator, mock_device)
    mock_device.status = "alerting"
    mock_device.status_messages = ["Radio down"]

    with patch.object(MerakiConnectivityBinarySensor, "device_data", mock_device):
        attrs = sensor.extra_state_attributes
        assert attrs["meraki_status"] == "alerting"
        assert attrs["status_messages"] == "Radio down"
