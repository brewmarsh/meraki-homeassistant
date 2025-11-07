"""Tests for the SwitchPortSensor."""

from unittest.mock import MagicMock

from homeassistant.components.binary_sensor import BinarySensorDeviceClass

from custom_components.meraki_ha.binary_sensor.switch_port import SwitchPortSensor


def test_switch_port_sensor_connected():
    """Test the sensor when the port is connected."""
    # Arrange
    mock_coordinator = MagicMock()
    mock_device = {"serial": "s1", "name": "d1"}
    mock_port = {"portId": "p1", "status": "Connected"}

    sensor = SwitchPortSensor(mock_coordinator, mock_device, mock_port)

    # Assert
    assert sensor.is_on is True
    assert sensor.device_class == BinarySensorDeviceClass.CONNECTIVITY
    assert sensor.name == "Port p1"
    assert sensor.unique_id == "s1_p1"


def test_switch_port_sensor_disconnected():
    """Test the sensor when the port is disconnected."""
    # Arrange
    mock_coordinator = MagicMock()
    mock_device = {"serial": "s1", "name": "d1"}
    mock_port = {"portId": "p1", "status": "Disconnected"}

    sensor = SwitchPortSensor(mock_coordinator, mock_device, mock_port)

    # Assert
    assert sensor.is_on is False


def test_extra_state_attributes():
    """Test the extra state attributes of the sensor."""
    # Arrange
    mock_coordinator = MagicMock()
    mock_device = {"serial": "s1", "name": "d1"}
    mock_port = {
        "portId": "p1",
        "speed": "1000",
        "duplex": "full",
        "vlan": 1,
        "enabled": True,
    }

    sensor = SwitchPortSensor(mock_coordinator, mock_device, mock_port)

    # Assert
    attrs = sensor.extra_state_attributes
    assert attrs["port_id"] == "p1"
    assert attrs["speed"] == "1000"
    assert attrs["duplex"] == "full"
    assert attrs["vlan"] == 1
    assert attrs["enabled"] is True
