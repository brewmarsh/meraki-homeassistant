"""Tests for the MTHandler."""

from typing import cast
from unittest.mock import MagicMock

import pytest

from custom_components.meraki_ha.binary_sensor.device.meraki_mt_binary_base import (
    MerakiMtBinarySensor,
)
from custom_components.meraki_ha.discovery.handlers.mt import MTHandler
from custom_components.meraki_ha.sensor.device.meraki_mt_base import MerakiMtSensor
from custom_components.meraki_ha.types import MerakiDevice


@pytest.fixture
def mock_coordinator_mt_handler(mock_coordinator: MagicMock) -> MagicMock:
    """Fixture for a mocked MerakiDataCoordinator."""
    return mock_coordinator


@pytest.fixture
def mock_control_service() -> MagicMock:
    """Fixture for a mocked DeviceControlService."""
    return MagicMock()


async def test_mt_handler_discover_entities_mt10(
    mock_coordinator_mt_handler: MagicMock,
    mock_config_entry: MagicMock,
    mock_control_service: MagicMock,
):
    """Test MTHandler discovers entities correctly for MT10."""
    device = cast(
        MerakiDevice,
        {
            "serial": "mt10-1",
            "model": "MT10",
            "name": "MT10 Sensor",
        },
    )

    handler = MTHandler(
        mock_coordinator_mt_handler,
        device,
        mock_config_entry,
        mock_control_service,
    )

    entities = await handler.discover_entities()

    # MT10 has Temperature, Humidity, Battery (3 sensors)
    # + USB Powered (1 binary) + Device Status = 5
    assert len(entities) == 5
    # Filter out device status sensor for MerakiMtSensor check
    mt_sensors = [e for e in entities if isinstance(e, MerakiMtSensor)]
    binary_sensors = [e for e in entities if isinstance(e, MerakiMtBinarySensor)]
    assert len(mt_sensors) == 3
    assert len(binary_sensors) == 1  # USB Powered
    assert any(e.entity_description.key == "temperature" for e in mt_sensors)
    assert any(e.entity_description.key == "humidity" for e in mt_sensors)
    assert any(e.entity_description.key == "battery" for e in mt_sensors)


async def test_mt_handler_discover_entities_mt12(
    mock_coordinator_mt_handler: MagicMock,
    mock_config_entry: MagicMock,
    mock_control_service: MagicMock,
):
    """Test MTHandler discovers entities correctly for MT12."""
    device = cast(
        MerakiDevice,
        {
            "serial": "mt12-1",
            "model": "MT12",
            "name": "MT12 Sensor",
        },
    )

    handler = MTHandler(
        mock_coordinator_mt_handler,
        device,
        mock_config_entry,
        mock_control_service,
    )

    entities = await handler.discover_entities()

    # MT12 has Temperature, Battery (2 Sensors)
    # + Water, Cable Connected, USB Powered (3 Binary) + Device Status = 6
    assert len(entities) == 6
    sensors = [e for e in entities if isinstance(e, MerakiMtSensor)]
    binary_sensors = [e for e in entities if isinstance(e, MerakiMtBinarySensor)]

    assert len(sensors) == 2  # Temp, Battery
    assert len(binary_sensors) == 3  # Water, Cable Connected, USB Powered

    assert any(e.entity_description.key == "temperature" for e in sensors)
    assert any(e.entity_description.key == "battery" for e in sensors)
    assert any(e.entity_description.key == "water" for e in binary_sensors)
    assert any(e.entity_description.key == "cable_connected" for e in binary_sensors)
    assert any(e.entity_description.key == "usb_powered" for e in binary_sensors)


async def test_mt_handler_discover_entities_mt20(
    mock_coordinator_mt_handler: MagicMock,
    mock_config_entry: MagicMock,
    mock_control_service: MagicMock,
):
    """Test MTHandler discovers entities correctly for MT20."""
    device = cast(
        MerakiDevice,
        {
            "serial": "mt20-1",
            "model": "MT20",
            "name": "MT20 Sensor",
        },
    )

    handler = MTHandler(
        mock_coordinator_mt_handler,
        device,
        mock_config_entry,
        mock_control_service,
    )

    entities = await handler.discover_entities()

    # MT20 has Battery, Temperature, Humidity (3 Sensors)
    # + Door, USB Powered (2 Binary) + Status = 6
    assert len(entities) == 6
    sensors = [e for e in entities if isinstance(e, MerakiMtSensor)]
    binary_sensors = [e for e in entities if isinstance(e, MerakiMtBinarySensor)]

    assert len(sensors) == 3  # Battery, Temperature, Humidity
    assert len(binary_sensors) == 2  # Door, USB Powered

    assert any(e.entity_description.key == "battery" for e in sensors)
    assert any(e.entity_description.key == "temperature" for e in sensors)
    assert any(e.entity_description.key == "humidity" for e in sensors)
    assert any(e.entity_description.key == "door" for e in binary_sensors)
    assert any(e.entity_description.key == "usb_powered" for e in binary_sensors)
