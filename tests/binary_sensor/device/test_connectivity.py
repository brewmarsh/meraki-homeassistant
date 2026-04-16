"""Tests for the Meraki connectivity binary sensor."""

from unittest.mock import MagicMock

import pytest

from custom_components.meraki_ha.binary_sensor.device.status import (
    MerakiConnectivityBinarySensor,
)
from custom_components.meraki_ha.core.models.device import MerakiDevice


@pytest.fixture
def mock_coordinator_connectivity(mock_coordinator: MagicMock) -> MagicMock:
    """Fixture for a mocked MerakiBaseCoordinator with connectivity data."""
    devices = [
        {
            "serial": "mx64-1",
            "name": "MX64 Appliance",
            "model": "MX64",
            "productType": "appliance",
            "status": "online",
        },
        {
            "serial": "mr33-1",
            "name": "MR33 AP",
            "model": "MR33",
            "productType": "wireless",
            "status": "offline",
        },
        {
            "serial": "ms120-1",
            "name": "MS120 Switch",
            "model": "MS120",
            "productType": "switch",
            "status": "alerting",
        },
        {
            "serial": "mt20-1",
            "name": "MT20 Sensor",
            "model": "MT20",
            "productType": "sensor",
            "status": "dormant",
        },
    ]
    mock_coordinator.data = {"devices": [MerakiDevice.from_dict(d) for d in devices]}
    mock_coordinator.get_device.side_effect = lambda serial: next(
        (d for d in mock_coordinator.data["devices"] if d.serial == serial), None
    )
    return mock_coordinator


def test_connectivity_sensor_online(mock_coordinator_connectivity: MagicMock):
    """Test connectivity sensor when device is online."""
    device = mock_coordinator_connectivity.get_device("mx64-1")
    sensor = MerakiConnectivityBinarySensor(mock_coordinator_connectivity, device)

    assert sensor.unique_id == "mx64-1_connectivity"
    assert sensor.is_on is True
    assert sensor.available is True
    assert sensor.extra_state_attributes["meraki_status"] == "online"


def test_connectivity_sensor_offline(mock_coordinator_connectivity: MagicMock):
    """Test connectivity sensor when device is offline."""
    device = mock_coordinator_connectivity.get_device("mr33-1")
    sensor = MerakiConnectivityBinarySensor(mock_coordinator_connectivity, device)

    assert sensor.unique_id == "mr33-1_connectivity"
    assert sensor.is_on is False
    assert sensor.available is True  # Should still be available to show 'off'
    assert sensor.extra_state_attributes["meraki_status"] == "offline"


def test_connectivity_sensor_alerting(mock_coordinator_connectivity: MagicMock):
    """Test connectivity sensor when device is alerting."""
    device = mock_coordinator_connectivity.get_device("ms120-1")
    sensor = MerakiConnectivityBinarySensor(mock_coordinator_connectivity, device)

    assert sensor.is_on is True
    assert sensor.available is True
    assert sensor.extra_state_attributes["meraki_status"] == "alerting"


def test_connectivity_sensor_dormant(mock_coordinator_connectivity: MagicMock):
    """Test connectivity sensor when device is dormant."""
    device = mock_coordinator_connectivity.get_device("mt20-1")
    sensor = MerakiConnectivityBinarySensor(mock_coordinator_connectivity, device)

    assert sensor.is_on is True
    assert sensor.available is True
    assert sensor.extra_state_attributes["meraki_status"] == "dormant"


def test_connectivity_sensor_unavailable(mock_coordinator_connectivity: MagicMock):
    """Test connectivity sensor when coordinator has no data."""
    device = mock_coordinator_connectivity.get_device("mx64-1")
    sensor = MerakiConnectivityBinarySensor(mock_coordinator_connectivity, device)

    mock_coordinator_connectivity.data = None
    assert sensor.available is False
