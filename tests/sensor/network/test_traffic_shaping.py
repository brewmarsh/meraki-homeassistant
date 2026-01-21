"""Tests for the Meraki Traffic Shaping sensor."""

from unittest.mock import MagicMock

import pytest

from custom_components.meraki_ha.const import CONF_ENABLE_TRAFFIC_SHAPING
from custom_components.meraki_ha.sensor.setup_helpers import async_setup_sensors
from custom_components.meraki_ha.types import MerakiNetwork


@pytest.fixture
def mock_coordinator():
    """Fixture for a mocked MerakiDataUpdateCoordinator."""
    coordinator = MagicMock()
    coordinator.config_entry = MagicMock()
    coordinator.config_entry.options = {}

    # Create a mock network
    mock_network = MerakiNetwork(
        id="net1",
        name="Test Network",
        organization_id="org1",
        product_types=["appliance"],
    )

    coordinator.data = {
        "networks": [mock_network],
        "traffic_shaping": {"net1": {"enabled": True}},
        "devices": [],
        "clients": [],
        "ssids": [],
    }
    return coordinator


def test_traffic_shaping_sensor_creation_enabled(mock_coordinator):
    """Test that Traffic Shaping sensor is created when enabled."""
    hass = MagicMock()

    # Enable the option
    mock_coordinator.config_entry.options = {CONF_ENABLE_TRAFFIC_SHAPING: True}

    # Run the setup
    sensors = async_setup_sensors(hass, mock_coordinator.config_entry, mock_coordinator)

    # Filter for TrafficShapingSensor
    ts_sensors = [s for s in sensors if s.__class__.__name__ == "TrafficShapingSensor"]
    assert len(ts_sensors) == 1

    sensor = ts_sensors[0]
    assert sensor.unique_id == "net1-traffic-shaping"
    assert sensor.name == "Traffic Shaping"

    # Mock hass for the sensor
    sensor.hass = hass

    # Mock async_write_ha_state
    sensor.async_write_ha_state = MagicMock()

    # Simulate update
    sensor._handle_coordinator_update()
    assert sensor.native_value == "Enabled"


def test_traffic_shaping_sensor_creation_disabled(mock_coordinator):
    """Test that Traffic Shaping sensor is NOT created when disabled."""
    hass = MagicMock()

    # Disable the option (default)
    mock_coordinator.config_entry.options = {CONF_ENABLE_TRAFFIC_SHAPING: False}

    # Run the setup
    sensors = async_setup_sensors(hass, mock_coordinator.config_entry, mock_coordinator)

    # Filter for TrafficShapingSensor
    ts_sensors = [s for s in sensors if s.__class__.__name__ == "TrafficShapingSensor"]
    assert len(ts_sensors) == 0
