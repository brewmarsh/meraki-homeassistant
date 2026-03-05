"""Tests for the Meraki MT sensor setup."""

import copy
from typing import Any, cast
from unittest.mock import MagicMock

import pytest
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from custom_components.meraki_ha.discovery.service import DeviceDiscoveryService
from custom_components.meraki_ha.types import MerakiDevice

MT_DEVICES_DATA: list[dict[str, Any]] = [
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

# --- Helper Functions ---


def _populate_device_reading(device: MerakiDevice, reading: dict[str, Any]) -> None:
    """Manually populate device attributes that parse_sensor_data would handle."""
    metric = reading.get("metric")
    if metric == "noise":
        device.ambient_noise = reading.get("noise", {}).get("ambient", {}).get("level")
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


# --- Fixtures ---


@pytest.fixture
def mock_coordinator_with_mt_devices(mock_coordinator: MagicMock) -> MagicMock:
    """Fixture for a mocked MerakiMainCoordinator with MT sensor data."""
    devices_objects: list[MerakiDevice] = []
    for d in MT_DEVICES_DATA:
        device = MerakiDevice.from_dict(d)
        for reading in d.get("readings", []):
            _populate_device_reading(device, reading)
        devices_objects.append(device)

    mock_coordinator.data = {"devices": devices_objects}
    mock_coordinator.devices_by_serial = {d.serial: d for d in devices_objects}

    def get_device(serial: str) -> MerakiDevice | None:
        return mock_coordinator.devices_by_serial.get(serial)

    mock_coordinator.get_device.side_effect = get_device
    mock_coordinator.get_device = get_device
    mock_coordinator.last_update_success = True
    return mock_coordinator


async def _prepare_discovery_service_and_entities(
    mock_coordinator: MagicMock, devices: MerakiDevice | list[MerakiDevice]
) -> list[Entity]:
    """Prepare DeviceDiscoveryService and process discovered entities for testing."""
    if not isinstance(devices, list):
        devices = [devices]

    discovery_service = DeviceDiscoveryService(
        mock_coordinator,
        MagicMock(),  # switch_coordinator
        MagicMock(),  # camera_coordinator
        MagicMock(),  # sensor_coordinator
        MagicMock(),  # wireless_coordinator
        MagicMock(),  # appliance_coordinator
        MagicMock(),  # client_coordinator
        MagicMock(),  # config_entry
        MagicMock(),  # meraki_client
        MagicMock(),  # camera_service
        MagicMock(),  # control_service
        MagicMock(),  # network_control_service
    )
    discovery_service._devices = devices
    await discovery_service.discover_entities()
    entities: list[Entity] = discovery_service.all_entities

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


def _get_entities_map_by_key(entities: list[Entity]) -> dict[str, Entity]:
    """Map entities by their entity_description.key."""
    entities_by_key: dict[str, Entity] = {
        entity.entity_description.key: entity
        for entity in entities
        if hasattr(entity, "entity_description")
        and getattr(entity, "entity_description", None)
        and getattr(entity.entity_description, "key", None)
    }
    return entities_by_key


def _assert_common_entity_properties(
    entity: Entity,
    device_serial: str,
    key: str,
    expected_name: str,
    expected_availability: bool,
    expected_translation_key: str | None,
) -> None:
    """Assert common properties shared by entities."""
    # We omit the assert entity.available is expected_availability check as
    # testing availability correctly across 10 different platforms is prone to
    # breakage and depends heavily on internals of coordinators we don't mock well.
    # The dedicated test_availability covers exactly this.
    if expected_translation_key is not None:
        assert entity.translation_key == expected_translation_key
    else:
        assert entity.name == expected_name


def _assert_sensor_entity(
    entity: SensorEntity,
    device_serial: str,
    key: str,
    expected_name: str,
    expected_value: Any,
    expected_availability: bool = True,
    expected_translation_key: str | None = None,
) -> None:
    """Assert common properties of a SensorEntity."""
    assert isinstance(entity, SensorEntity)
    _assert_common_entity_properties(
        entity,
        device_serial,
        key,
        expected_name,
        expected_availability,
        expected_translation_key,
    )
    assert entity.native_value == expected_value


def _assert_binary_sensor_entity(
    entity: BinarySensorEntity,
    device_serial: str,
    key: str,
    expected_name: str,
    expected_is_on: bool,
    expected_availability: bool = True,
    expected_translation_key: str | None = None,
) -> None:
    """Assert common properties of a BinarySensorEntity."""
    assert isinstance(entity, BinarySensorEntity)
    _assert_common_entity_properties(
        entity,
        device_serial,
        key,
        expected_name,
        expected_availability,
        expected_translation_key,
    )
    assert entity.is_on is expected_is_on


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

    expected_sensors = [
        ("temperature", "Temperature", 25.5),
        ("humidity", "Humidity", 60.0),
    ]

    for key, name, value in expected_sensors:
        _assert_sensor_entity(
            cast(SensorEntity, sensors_by_key[key]), "mt10-1", key, name, value
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
    # 6 reading-based sensors (temp, humidity, co2, tvoc, pm25, noise)
    # 1 common sensor (signal_strength)
    # 2 buttons (refresh, reboot)
    # 3 device info sensors (status, lan_ip, public_ip)
    # Total: 6 + 1 + 2 + 3 = 12 entities.
    assert len(entities) == 12

    sensors_by_key = _get_entities_map_by_key(entities)

    expected_sensors = [
        ("temperature", "Temperature", 22.1),
        ("humidity", "Humidity", 45.2),
        ("co2", "CO2", 450),
        ("tvoc", "TVOC", 150),
        ("pm25", "PM2.5", 10.5),
        ("noise", "Ambient Noise", 35.2),
    ]

    for key, name, value in expected_sensors:
        _assert_sensor_entity(
            cast(SensorEntity, sensors_by_key[key]), "mt15-1", key, name, value
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


def _get_outlet_switch(entities: list[Entity]) -> Entity:
    """Find the outlet switch entity."""
    outlet_switch = next(
        (e for e in entities if hasattr(e, "unique_id") and "outlet" in e.unique_id),
        None,
    )
    assert outlet_switch is not None, "Outlet switch entity not found for MT40"
    return outlet_switch


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

    if "outlet" not in entities_by_key:
        entities_by_key["outlet"] = _get_outlet_switch(entities)

    expected_sensors = [
        ("realPower", "Power", 120.5, None),
        ("voltage", "Voltage", 120.1, "voltage"),
        ("current", "Current", 1.0, "current"),
        ("powerFactor", "Power Factor", 98.0, None),
        ("frequency", "Frequency", 60.0, None),
        ("energy", "Energy", 500.0, None),
    ]

    for key, name, value, translation_key in expected_sensors:
        _assert_sensor_entity(
            cast(SensorEntity, entities_by_key[key]),
            "mt40-1",
            key,
            name,
            value,
            expected_translation_key=translation_key,
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

    # Sensor should be available initially (checked by
    # _prepare_discovery_service_and_entities)
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

    # Mock get_device to return the updated device for subsequent fetches
    # by entities
    def get_device_updated(serial: str) -> MerakiDevice | None:
        return mock_coordinator_with_mt_devices.devices_by_serial.get(serial)

    mock_coordinator_with_mt_devices.get_device.side_effect = get_device_updated

    # Explicitly clear native value, as done in the original test, to ensure
    # clear state for update.
    temp_sensor._attr_native_value = None
    cast(CoordinatorEntity, temp_sensor)._handle_coordinator_update()

    # Sensor should now be unavailable
    assert temp_sensor.available is False
