"""Tests for traffic shaping sensor."""

from unittest.mock import MagicMock

import pytest

from custom_components.meraki_ha.sensor.network.traffic_shaping import (
    TrafficShapingSensor,
)


@pytest.fixture
def mock_traffic_shaping_coordinator(mock_coordinator: MagicMock) -> MagicMock:
    """Create a mock coordinator with traffic shaping data."""
    mock_coordinator.data = {
        "networks": [{"id": "N_123", "name": "Test Network"}],
        "traffic_shaping": {
            "N_123": {"enabled": True},
        },
    }
    return mock_coordinator


def test_traffic_shaping_sensor_initialization(
    mock_traffic_shaping_coordinator: MagicMock,
    mock_config_entry: MagicMock,
) -> None:
    """Test traffic shaping sensor initialization."""
    sensor = TrafficShapingSensor(
        coordinator=mock_traffic_shaping_coordinator,
        config_entry=mock_config_entry,
        network_id="N_123",
    )

    assert sensor._attr_unique_id == "N_123-traffic-shaping"
    assert sensor._attr_name == "Traffic Shaping"


def test_traffic_shaping_sensor_handle_update_enabled(
    mock_traffic_shaping_coordinator: MagicMock,
    mock_config_entry: MagicMock,
) -> None:
    """Test traffic shaping sensor updates to enabled."""
    mock_traffic_shaping_coordinator.data = {
        "networks": [{"id": "N_123", "name": "Test Network"}],
        "traffic_shaping": {"N_123": {"enabled": True}},
    }

    sensor = TrafficShapingSensor(
        coordinator=mock_traffic_shaping_coordinator,
        config_entry=mock_config_entry,
        network_id="N_123",
    )
    object.__setattr__(sensor, "async_write_ha_state", MagicMock())
    sensor._handle_coordinator_update()

    assert sensor._attr_native_value == "Enabled"


def test_traffic_shaping_sensor_handle_update_disabled(
    mock_traffic_shaping_coordinator: MagicMock,
    mock_config_entry: MagicMock,
) -> None:
    """Test traffic shaping sensor updates to disabled."""
    mock_traffic_shaping_coordinator.data = {
        "networks": [{"id": "N_123", "name": "Test Network"}],
        "traffic_shaping": {"N_123": {"enabled": False}},
    }

    sensor = TrafficShapingSensor(
        coordinator=mock_traffic_shaping_coordinator,
        config_entry=mock_config_entry,
        network_id="N_123",
    )
    object.__setattr__(sensor, "async_write_ha_state", MagicMock())
    sensor._handle_coordinator_update()

    assert sensor._attr_native_value == "Disabled"
