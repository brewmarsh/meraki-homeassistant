"""Tests for SSID channel sensor."""

from unittest.mock import MagicMock

import pytest

from custom_components.meraki_ha.sensor.network.ssid_channel import (
    MerakiSSIDChannelSensor,
)


@pytest.fixture
def mock_ssid_data() -> dict:
    """Create mock SSID data."""
    return {
        "number": 0,
        "name": "Test SSID",
        "enabled": True,
        "channel": 6,
        "networkId": "N_123",
    }


@pytest.fixture
def mock_ssid_coordinator(mock_coordinator: MagicMock) -> MagicMock:
    """Create a mock coordinator with SSID data."""
    mock_coordinator.data = {
        "ssids": [
            {"number": 0, "name": "Test SSID", "channel": 6, "networkId": "N_123"}
        ]
    }
    return mock_coordinator


def test_ssid_channel_sensor_initialization(
    mock_ssid_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_ssid_data: dict,
) -> None:
    """Test SSID channel sensor initialization."""
    sensor = MerakiSSIDChannelSensor(
        coordinator=mock_ssid_coordinator,
        config_entry=mock_config_entry,
        ssid_data=mock_ssid_data,
    )

    assert sensor._attr_native_value == 6
    assert sensor.entity_description.key == "channel"
    assert sensor.entity_description.name == "Channel"


def test_ssid_channel_sensor_no_channel(
    mock_ssid_coordinator: MagicMock,
    mock_config_entry: MagicMock,
) -> None:
    """Test SSID channel sensor with no channel data."""
    ssid_data = {
        "number": 0,
        "name": "Test SSID",
        "enabled": True,
        "networkId": "N_123",
    }

    sensor = MerakiSSIDChannelSensor(
        coordinator=mock_ssid_coordinator,
        config_entry=mock_config_entry,
        ssid_data=ssid_data,
    )

    assert sensor._attr_native_value is None

