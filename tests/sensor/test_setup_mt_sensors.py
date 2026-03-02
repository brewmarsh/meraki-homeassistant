"""Tests for the Meraki MT sensor setup."""

import copy
from typing import Any, Dict, List, Optional, Union, cast
from unittest.mock import MagicMock

import pytest
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from custom_components.meraki_ha.discovery.service import DeviceDiscoveryService
from custom_components.meraki_ha.types import MerakiDevice

# --- Fixtures ---


@pytest.fixture
def mock_coordinator_with_mt_devices(mock_coordinator: MagicMock) -> MagicMock:
    """Fixture for a mocked MerakiMainCoordinator with MT sensor data."""
    devices_data: list[dict[str, Any]] = [
        {
            "serial": "mt10-1",
            "name": "MT10 Sensor",
            "model": "MT10",
            "productType": "sensor",
            "readings": [
                {"metric": "temperature", "temperature": {"celsius": 25.5}},
                {"metric": "humidity", "humidity": {"relativePercentage": 60.0}},
                {"metric": "battery", "battery": {"percentage": 100}},
            ],
        },
        {
            "serial": "mt15-1",
            "name": "MT15 Sensor",
            "model": "MT15",
            "productType": "sensor",
            "readings": [
                {"metric": "temperature", "temperature": {"celsius": 22.1}},
                {"metric": "humidity", "humidity": {"relativePercentage": 45.2}},
                {"metric": "co2", "co2": {"concentration": 450}},
                {"metric": "tvoc", "tvoc": {"concentration": 150}},
                {"metric": "pm25", "pm25": {"concentration": 10.5}},
                {"metric": "noise", "noise": {"ambient": {"level": 35.2}}},
                {"metric": "battery", "battery": {"percentage": 100}},
            ],
        },
        {
            "serial": "mt12-1",
            "name": "MT12 Sensor",
            "model": "MT12",
            "productType": "sensor",
            "readings": [
                {"metric": "water", "water": {"present": False}},
                {"metric": "battery", "battery": {"percentage": 100}},
            ],
        },
        {
            "serial": "mt40-1",
            "name": "MT40 Power Controller",
            "model": "MT40",
            "productType": "sensor",
            "readings": [
                {"metric": "power", "power": {"draw": 120.5}},
                {"metric": "voltage", "voltage": {"level": 120.1}},
                {"metric": "current", "current": {"draw": 1.0}},
                {"metric": "powerFactor", "powerFactor": {"percentage": 98.0}},
                {"metric": "frequency", "frequency": {"level": 60.0}},
                {"metric": "energy", "energy": {"draw": 500.0}},
            ],
        },
    ]

    devices_objects: List[MerakiDevice] = []
    for d in devices_data:
        device = MerakiDevice.from_dict(d)
        # Manually populate attributes that parse_sensor_data would handle
        for reading in d.get("readings", []):
            metric = reading.get("metric")
            if metric == "noise":
                device.ambient_noise = (
                    reading.get("noise", {}).get("ambient", {}).get("level")
                )
            elif metric == "pm25":
                device.pm25 = reading.get("pm25", {}).get("concentration")
            elif metric == "power":
                device.real_power = reading.get("power", {}).get("draw")
            elif metric == "powerFactor":
                device.power_factor = reading.get("powerFactor", {}).get("percentage")
            elif metric == "current":
                device.current = reading.get("current", {}).get("draw")
            elif metric == "voltage":
                device.voltage = reading.get("voltage", {}).get("level")
            elif metric == "door":
                device.door_open = reading.get("door", {}).get("open")
            elif metric == "water":
                device.water_present = reading.get("water", {}).get("present")
        devices_objects.append(device)

    mock_coordinator.data = {"devices": devices_objects}
    mock_coordinator.devices_by_serial = {d.serial: d for d in devices_objects}

    def get_device(serial: str) -> Optional[MerakiDevice]:
        return mock_coordinator.devices_by_serial.get(serial)

    mock_coordinator.get_device.side_effect = get_device
    return mock_coordinator


# --- Helper Functions ---


async def _prepare_discovery_service_and_entities(
    mock_coordinator: MagicMock, devices: Union[MerakiDevice, List[MerakiDevice]]
) -> List[Entity]:
    """Prepare DeviceDiscoveryService and process discovered entities for testing."""
    if not isinstance(devices, list):
        devices = [devices]

    discovery_service = DeviceDiscoveryService(
        mock_coordinator,
        MagicMock(),  # entry
        MagicMock(),  # hass
        MagicMock(),  # config_entry
        MagicMock(),  # api_client
        MagicMock(),  # event_handler
    )
    discovery_service._devices = devices
    await discovery_service.discover_entities()
    entities: List[Entity] = discovery_service.all_entities

    for entity in entities:
        entity.hass = MagicMock()
        entity.platform = MagicMock()
        entity.platform.platform_name = "test_platform"
        entity.platform.domain = "test_domain"
        # Use platform and unique_id to create a more distinct entity_id for tests
        entity.entity_id = (
            f"{entity.platform}.test_{entity.unique_id}"
            if hasattr(entity, "unique_id")
            else "test_entity"
        )
        # Replaced object.__setattr__ with direct assignment for method mock
        entity.async_write_ha_state = MagicMock()
        if hasattr(entity, "_handle_coordinator_update"):
            cast(CoordinatorEntity, entity)._handle_coordinator_update()
    return entities


def _get_entities_map_by_key(entities: List[Entity]) -> Dict[str, Entity]:
    """Map entities by their entity_description.key."""
    entities_by_key: Dict[str, Entity] = {
        entity.entity_description.key: entity
        for entity in entities
        if hasattr(entity, "entity_description")
        and getattr(entity, "entity_description", None)
        and getattr(entity.entity_description, "key", None)
    }
    return entities_by_key


def _assert_sensor_entity(
    entity: SensorEntity,
    device_serial: str,
    key: str,
    expected_name: str,
    expected_value: Any,
    expected_availability: bool = True,
    expected_translation_key: Optional[str] = None,
) -> None:
    """Assert common properties of a SensorEntity."""
    assert isinstance(entity, SensorEntity)
    assert entity.unique_id == f"{device_serial}_{key}"
    assert entity.native_value == expected_value
    assert entity.available is expected_availability
    if expected_translation_key is not None:
        assert entity.translation_key == expected_translation_key
    else:
        assert entity.name == expected_name


def _assert_binary_sensor_entity(
    entity: BinarySensorEntity,
    device_serial: str,
    key: str,
    expected_name: str,
    expected_is_on: bool,
    expected_availability: bool = True,
    expected_translation_key: Optional[str] = None,
) -> None:
    """Assert common properties of a BinarySensorEntity."""
    assert isinstance(entity, BinarySensorEntity)
    assert entity.unique_id == f"{device_serial}_{key}"
    assert entity.name == expected_name
    assert entity.is_on is expected_is_on
    assert entity.available is expected_availability
    if expected_translation_key is not None:
        assert entity.translation_key == expected_translation_key


# --- Tests ---


async def test_async_setup_mt10_sensors(
    mock_coordinator_with_mt_devices: MagicMock,
) -> None:
    """Test the setup of sensors for an MT10 device."""
    mt10_device = mock_coordinator_with_mt_devices.get_device("mt10-1")
    assert mt10_device is not None
    entities = await _prepare_discovery_service_and_entities(
        mock_coordinator_with_mt_devices, mt10_device
    )

    # MT10 has Temperature, Humidity, Battery, Signal Strength (4 sensors)
    assert len(entities) == 4

    sensors_by_key = _get_entities_map_by_key(entities)

    _assert_sensor_entity(
        cast(SensorEntity, sensors_by_key["temperature"]),
        "mt10-1",
        "temperature",
        "Temperature",
        25.5,
    )
    _assert_sensor_entity(
        cast(SensorEntity, sensors_by_key["humidity"]),
        "mt10-1",
        "humidity",
        "Humidity",
        60.0,
    )


async def test_async_setup_mt15_sensors(
    mock_coordinator_with_mt_devices: MagicMock,
) -> None:
    """Test the setup of sensors for an MT15 device."""
    mt15_device = mock_coordinator_with_mt_devices.get_device("mt15-1")
    assert mt15_device is not None
    entities = await _prepare_discovery_service_and_entities(
        mock_coordinator_with_mt_devices, mt15_device
    )

    # MT15 typically has:
    # 6 reading-based sensors (temperature, humidity, co2, tvoc, pm25, noise) - Battery excluded
    # 1 common sensor (signal_strength)
    # 2 buttons (refresh, reboot)
    # 3 device info sensors (status, lan_ip, public_ip)
    # Total: 6 + 1 + 2 + 3 = 12 entities.
    assert len(entities) == 12

    sensors_by_key = _get_entities_map_by_key(entities)

    _assert_sensor_entity(
        cast(SensorEntity, sensors_by_key["temperature"]),
        "mt15-1",
        "temperature",
        "Temperature",
        22.1,
    )
    _assert_sensor_entity(
        cast(SensorEntity, sensors_by_key["humidity"]),
        "mt15-1",
        "humidity",
        "Humidity",
        45.2,
    )
    _assert_sensor_entity(
        cast(SensorEntity, sensors_by_key["co2"]), "mt15-1", "co2", "CO2", 450
    )
    _assert_sensor_entity(
        cast(SensorEntity, sensors_by_key["tvoc"]), "mt15-1", "tvoc", "TVOC", 150
    )
    _assert_sensor_entity(
        cast(SensorEntity, sensors_by_key["pm25"]), "mt15-1", "pm25", "PM2.5", 10.5
    )
    _assert_sensor_entity(
        cast(SensorEntity, sensors_by_key["noise"]),
        "mt15-1",
        "noise",
        "Ambient Noise",
        35.2,
    )


async def test_async_setup_mt12_sensors(
    mock_coordinator_with_mt_devices: MagicMock,
) -> None:
    """Test the setup of sensors for an MT12 device."""
    mt12_device = mock_coordinator_with_mt_devices.get_device("mt12-1")
    assert mt12_device is not None
    entities = await _prepare_discovery_service_and_entities(
        mock_coordinator_with_mt_devices, mt12_device
    )

    # MT12 is expected to have 5 entities based on prior tests:
    # Water Leak Binary Sensor, Battery Sensor, Signal Strength Sensor,
    # plus 2 other implicit sensors (e.g., Temperature, Humidity).
    assert len(entities) == 5

    entities_by_key = _get_entities_map_by_key(entities)

    _assert_binary_sensor_entity(
        cast(BinarySensorEntity, entities_by_key["water"]),
        "mt12-1",
        "water",
        "Water Leak",
        False,
    )


async def test_async_setup_mt40_sensors(
    mock_coordinator_with_mt_devices: MagicMock,
) -> None:
    """Test the setup of sensors for an MT40 device."""
    mt40_device = mock_coordinator_with_mt_devices.get_device("mt40-1")
    assert mt40_device is not None
    entities = await _prepare_discovery_service_and_entities(
        mock_coordinator_with_mt_devices, mt40_device
    )

    # MT40 has 6 Power sensors + 1 Outlet switch + 1 Signal Strength = 8 entities
    assert len(entities) == 8

    entities_by_key = _get_entities_map_by_key(entities)

    # For the outlet switch, which might not have an entity_description.key,
    # we can find it by unique_id if needed, or rely on other tests for its specific type.
    # The original test added it to the map with key "outlet".
    outlet_switch: Optional[Entity] = None
    for entity in entities:
        if hasattr(entity, "unique_id") and "outlet" in entity.unique_id:
            outlet_switch = entity
            break
    assert outlet_switch is not None, "Outlet switch entity not found for MT40"
    # Add it to the map for consistent access in assertions
    if outlet_switch and "outlet" not in entities_by_key:
        entities_by_key["outlet"] = outlet_switch

    _assert_sensor_entity(
        cast(SensorEntity, entities_by_key["realPower"]),
        "mt40-1",
        "realPower",
        "Power",
        120.5,
    )
    _assert_sensor_entity(
        cast(SensorEntity, entities_by_key["voltage"]),
        "mt40-1",
        "voltage",
        "Voltage",
        120.1,
        expected_translation_key="voltage",
    )
    _assert_sensor_entity(
        cast(SensorEntity, entities_by_key["current"]),
        "mt40-1",
        "current",
        "Current",
        1.0,
        expected_translation_key="current",
    )
    _assert_sensor_entity(
        cast(SensorEntity, entities_by_key["powerFactor"]),
        "mt40-1",
        "powerFactor",
        "Power Factor",
        98.0,
    )
    _assert_sensor_entity(
        cast(SensorEntity, entities_by_key["frequency"]),
        "mt40-1",
        "frequency",
        "Frequency",
        60.0,
    )
    _assert_sensor_entity(
        cast(SensorEntity, entities_by_key["energy"]),
        "mt40-1",
        "energy",
        "Energy",
        500.0,
    )


async def test_availability(mock_coordinator_with_mt_devices: MagicMock) -> None:
    """Test sensor availability."""
    mt10_device = mock_coordinator_with_mt_devices.get_device("mt10-1")
    assert mt10_device is not None
    entities = await _prepare_discovery_service_and_entities(
        mock_coordinator_with_mt_devices, mt10_device
    )

    sensors_by_key = _get_entities_map_by_key(entities)
    temp_sensor = cast(SensorEntity, sensors_by_key["temperature"])

    # Sensor should be available initially (checked by _prepare_discovery_service_and_entities)
    assert temp_sensor.available is True

    # Prepare a device without readings
    device_without_readings = copy.deepcopy(mt10_device)
    device_without_readings.readings = []

    # Update the mock coordinator's data to reflect the device without readings
    mock_coordinator_with_mt_devices.data["devices"] = [
        d
        for d in mock_coordinator_with_mt_devices.data["devices"]
        if d.serial != "mt10-1"
    ] + [device_without_readings]
    mock_coordinator_with_mt_devices.devices_by_serial["mt10-1"] = (
        device_without_readings
    )

    # Mock get_device to return the updated device for subsequent fetches by entities
    def get_device_updated(serial: str) -> Optional[MerakiDevice]:
        return mock_coordinator_with_mt_devices.devices_by_serial.get(serial)

    mock_coordinator_with_mt_devices.get_device.side_effect = get_device_updated

    # Explicitly clear native value, as done in the original test, to ensure clear state for update.
    temp_sensor._attr_native_value = None
    cast(CoordinatorEntity, temp_sensor)._handle_coordinator_update()

    # Sensor should now be unavailable
    assert temp_sensor.available is False
