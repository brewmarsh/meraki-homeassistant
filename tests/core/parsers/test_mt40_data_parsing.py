"""Tests for MT40 sensor data parsing."""

from custom_components.meraki_ha.core.parsers.sensors import parse_sensor_data
from custom_components.meraki_ha.types import MerakiDevice


def test_parse_mt40_sensor_data_camel_case():
    """Test parsing MT40 sensor data with CamelCase keys."""
    device = MerakiDevice(serial="mt40-test", model="MT40")
    devices = [device]

    sensor_readings = [
        {
            "serial": "mt40-test",
            "readings": [
                {"metric": "powerFactor", "powerFactor": {"percentage": 95.5}},
                {"metric": "frequency", "frequency": {"level": 50.1}},
                {"metric": "energyUsage", "energyUsage": 1234.5},
            ],
        }
    ]

    parse_sensor_data(devices, sensor_readings, [])

    assert device.power_factor == 95.5
    assert device.frequency == 50.1
    assert device.energy == 1234.5


def test_parse_mt40_sensor_data_nested_energy():
    """Test parsing MT40 sensor data with nested energyUsage."""
    device = MerakiDevice(serial="mt40-test", model="MT40")
    devices = [device]

    sensor_readings = [
        {
            "serial": "mt40-test",
            "readings": [
                {"metric": "energy", "energy": {"energyUsage": 5678.9}},
            ],
        }
    ]

    parse_sensor_data(devices, sensor_readings, [])

    assert device.energy == 5678.9


def test_parse_mt40_sensor_data_apparent_power():
    """Test parsing MT40 sensor data with apparentPower."""
    device = MerakiDevice(serial="mt40-test", model="MT40")
    devices = [device]

    sensor_readings = [
        {
            "serial": "mt40-test",
            "readings": [
                {"metric": "energy", "energy": {"apparentPower": 999.9}},
            ],
        }
    ]

    parse_sensor_data(devices, sensor_readings, [])

    assert device.energy == 999.9


def test_parse_mt40_sensor_data_snake_case_fallback():
    """Test parsing MT40 sensor data with snake_case keys (existing support)."""
    device = MerakiDevice(serial="mt40-test", model="MT40")
    devices = [device]

    sensor_readings = [
        {
            "serial": "mt40-test",
            "readings": [
                {"metric": "power_factor", "power_factor": {"factor": 0.98}},
            ],
        }
    ]

    parse_sensor_data(devices, sensor_readings, [])

    assert device.power_factor == 0.98


def test_parse_mt40_sensor_data_outlet_status():
    """Test parsing MT40 sensor data with downstreamPower metric."""
    device = MerakiDevice(serial="mt40-test", model="MT40")
    devices = [device]

    sensor_readings = [
        {
            "serial": "mt40-test",
            "readings": [
                {"metric": "downstreamPower", "downstreamPower": {"enabled": True}},
            ],
        }
    ]

    parse_sensor_data(devices, sensor_readings, [])

    assert device.outlet_status is True


def test_parse_mt40_sensor_data_outlet_status_legacy():
    """Test parsing MT40 sensor data with legacy downstream_power metric."""
    device = MerakiDevice(serial="mt40-test", model="MT40")
    devices = [device]

    sensor_readings = [
        {
            "serial": "mt40-test",
            "readings": [
                {"metric": "downstream_power", "value": False},
            ],
        }
    ]

    parse_sensor_data(devices, sensor_readings, [])

    assert device.outlet_status is False
