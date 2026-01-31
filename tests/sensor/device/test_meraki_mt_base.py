"""Tests for the Meraki MT sensor entity ID."""

from unittest.mock import MagicMock

import pytest
from homeassistant.components.sensor import SensorEntityDescription

from custom_components.meraki_ha.descriptions import MT_VOLTAGE_DESCRIPTION
from custom_components.meraki_ha.sensor.device.meraki_mt_base import MerakiMtSensor
from custom_components.meraki_ha.types import MerakiDevice


@pytest.fixture
def mock_coordinator() -> MagicMock:
    """Fixture for a mocked MerakiDataUpdateCoordinator."""
    coordinator = MagicMock()
    coordinator.data = {}
    return coordinator


def test_meraki_mt_sensor_entity_id(mock_coordinator: MagicMock) -> None:
    """Test the entity ID of a MerakiMtSensor."""
    device_data = {
        "serial": "Q3CA-2CG4-6LBK",
        "name": "Upstairs Hallway",
        "model": "MT10",
        "productType": "sensor",
        "readings": [{"metric": "temperature", "temperature": {"celsius": 25.5}}],
    }
    device = MerakiDevice.from_dict(device_data)
    entity_description = SensorEntityDescription(
        key="temperature",
        name="Temperature",
    )

    sensor = MerakiMtSensor(
        coordinator=mock_coordinator,
        device=device,
        entity_description=entity_description,
    )
    sensor.hass = MagicMock()

    # With _attr_has_entity_name = True, HA will generate the entity_id
    # The entity_id should be based on the device name and entity description name
    # Let's assume the device has a name in HA of "Upstairs Hallway"
    # and the entity name is "Temperature".
    # HA should generate "sensor.upstairs_hallway_temperature"
    # However, we can't easily test the full HA entity ID generation here.
    # Instead, we will check that the components we provide are correct.

    assert sensor.unique_id == "Q3CA-2CG4-6LBK_temperature"
    assert sensor.name == "Temperature"
    assert sensor.has_entity_name is True
    assert sensor.entity_id is None


def test_mt40_voltage_sensor(mock_coordinator):
    """Test the MT40 voltage sensor."""
    device_data = {
        "serial": "Q3CA-2CG4-6LBM",
        "name": "Power Controller",
        "model": "MT40",
        "productType": "sensor",
        "readings": [{"metric": "voltage", "voltage": {"level": 120.5}}],
    }
    device = MerakiDevice.from_dict(device_data)
    device.voltage = 120.5  # Simulate the parser's behavior
    mock_coordinator.get_device.return_value = device

    sensor = MerakiMtSensor(
        coordinator=mock_coordinator,
        device=device,
        entity_description=MT_VOLTAGE_DESCRIPTION,
    )
    sensor.hass = MagicMock()
    sensor.async_write_ha_state = MagicMock()

    sensor._handle_coordinator_update()
    assert sensor.native_value == 120.5
