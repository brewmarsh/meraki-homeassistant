"""Tests for the Meraki MT binary sensor base class."""

from typing import cast
from unittest.mock import MagicMock

import pytest
from homeassistant.components.binary_sensor import BinarySensorEntityDescription

from custom_components.meraki_ha.binary_sensor.device.meraki_mt_binary_base import (
    MerakiMtBinarySensor,
)
from custom_components.meraki_ha.const import DOMAIN
from custom_components.meraki_ha.types import MerakiDevice

MOCK_MT_DEVICE: MerakiDevice = cast(
    MerakiDevice,
    {
        "serial": "MT20-ABCD-1234",
        "name": "Door Sensor",
        "model": "MT20",
        "networkId": "N_12345",
        "productType": "sensor",
        "readings_raw": [
            {"metric": "door", "door": {"open": True}},
            {"metric": "temperature", "temperature": {"celsius": 22.5}},
        ],
    },
)


@pytest.fixture
def mock_coordinator() -> MagicMock:
    """Create a mock coordinator."""
    coordinator = MagicMock()
    coordinator.data = {"devices": [MOCK_MT_DEVICE]}
    coordinator.last_update_success = True
    coordinator.config_entry = MagicMock()
    coordinator.config_entry.options = {}
    return coordinator


@pytest.fixture
def door_entity_description() -> BinarySensorEntityDescription:
    """Create a door entity description."""
    return BinarySensorEntityDescription(key="door", name="Door")


@pytest.fixture
def water_entity_description() -> BinarySensorEntityDescription:
    """Create a water entity description."""
    return BinarySensorEntityDescription(key="water", name="Water")


class TestMerakiMtBinarySensor:
    """Tests for MerakiMtBinarySensor class."""

    def test_initialization(
        self,
        mock_coordinator: MagicMock,
        door_entity_description: BinarySensorEntityDescription,
    ) -> None:
        """Test sensor initialization."""
        sensor = MerakiMtBinarySensor(
            mock_coordinator, MOCK_MT_DEVICE, door_entity_description
        )

        assert sensor._device == MOCK_MT_DEVICE
        assert sensor.entity_description == door_entity_description
        assert sensor.unique_id == f"{MOCK_MT_DEVICE['serial']}_door"
        assert sensor.name and "Door Sensor Door" in str(sensor.name)

    def test_device_info(
        self,
        mock_coordinator: MagicMock,
        door_entity_description: BinarySensorEntityDescription,
    ) -> None:
        """Test device_info property."""
        sensor = MerakiMtBinarySensor(
            mock_coordinator, MOCK_MT_DEVICE, door_entity_description
        )

        device_info = sensor.device_info

        assert device_info is not None
        assert (DOMAIN, MOCK_MT_DEVICE["serial"]) in device_info["identifiers"]
        assert device_info["model"] == "MT20"
        assert device_info["manufacturer"] == "Cisco Meraki"

    def test_get_current_device_data_found(
        self,
        mock_coordinator: MagicMock,
        door_entity_description: BinarySensorEntityDescription,
    ) -> None:
        """Test _get_current_device_data when device is found."""
        sensor = MerakiMtBinarySensor(
            mock_coordinator, MOCK_MT_DEVICE, door_entity_description
        )

        result = sensor._get_current_device_data()

        assert result == MOCK_MT_DEVICE

    def test_get_current_device_data_not_found(
        self,
        mock_coordinator: MagicMock,
        door_entity_description: BinarySensorEntityDescription,
    ) -> None:
        """Test _get_current_device_data when device is not found."""
        mock_coordinator.data = {"devices": []}
        sensor = MerakiMtBinarySensor(
            mock_coordinator, MOCK_MT_DEVICE, door_entity_description
        )

        result = sensor._get_current_device_data()

        assert result is None

    def test_get_current_device_data_no_data(
        self,
        mock_coordinator: MagicMock,
        door_entity_description: BinarySensorEntityDescription,
    ) -> None:
        """Test _get_current_device_data when coordinator has no data."""
        mock_coordinator.data = None
        sensor = MerakiMtBinarySensor(
            mock_coordinator, MOCK_MT_DEVICE, door_entity_description
        )

        result = sensor._get_current_device_data()

        assert result is None

    def test_get_readings_from_readings_raw(
        self,
        mock_coordinator: MagicMock,
        door_entity_description: BinarySensorEntityDescription,
    ) -> None:
        """Test _get_readings returns readings_raw list."""
        sensor = MerakiMtBinarySensor(
            mock_coordinator, MOCK_MT_DEVICE, door_entity_description
        )

        result = sensor._get_readings()

        assert result == MOCK_MT_DEVICE["readings_raw"]  # type: ignore[typeddict-item]

    def test_get_readings_from_readings(
        self,
        mock_coordinator: MagicMock,
        door_entity_description: BinarySensorEntityDescription,
    ) -> None:
        """Test _get_readings falls back to readings."""
        device = dict(MOCK_MT_DEVICE)
        del device["readings_raw"]
        device["readings"] = [{"metric": "door", "door": {"open": False}}]
        mock_coordinator.data = {"devices": [device]}

        sensor = MerakiMtBinarySensor(
            mock_coordinator, cast(MerakiDevice, device), door_entity_description
        )

        result = sensor._get_readings()

        assert result == device["readings"]

    def test_get_readings_no_readings(
        self,
        mock_coordinator: MagicMock,
        door_entity_description: BinarySensorEntityDescription,
    ) -> None:
        """Test _get_readings when no readings available."""
        device = dict(MOCK_MT_DEVICE)
        del device["readings_raw"]
        mock_coordinator.data = {"devices": [device]}

        sensor = MerakiMtBinarySensor(
            mock_coordinator, cast(MerakiDevice, device), door_entity_description
        )

        result = sensor._get_readings()

        assert result is None

    def test_handle_coordinator_update(
        self,
        mock_coordinator: MagicMock,
        door_entity_description: BinarySensorEntityDescription,
    ) -> None:
        """Test _handle_coordinator_update updates device data."""
        sensor = MerakiMtBinarySensor(
            mock_coordinator, MOCK_MT_DEVICE, door_entity_description
        )
        sensor.async_write_ha_state = MagicMock()

        # Update coordinator with new data
        new_device = dict(MOCK_MT_DEVICE)
        new_device["readings_raw"] = [{"metric": "door", "door": {"open": False}}]
        mock_coordinator.data = {"devices": [new_device]}

        sensor._handle_coordinator_update()

        sensor.async_write_ha_state.assert_called_once()

    def test_available_true_when_metric_exists(
        self,
        mock_coordinator: MagicMock,
        door_entity_description: BinarySensorEntityDescription,
    ) -> None:
        """Test available is True when metric exists in readings."""
        sensor = MerakiMtBinarySensor(
            mock_coordinator, MOCK_MT_DEVICE, door_entity_description
        )

        assert sensor.available is True

    def test_available_false_when_coordinator_failed(
        self,
        mock_coordinator: MagicMock,
        door_entity_description: BinarySensorEntityDescription,
    ) -> None:
        """Test available is False when coordinator update failed."""
        mock_coordinator.last_update_success = False
        sensor = MerakiMtBinarySensor(
            mock_coordinator, MOCK_MT_DEVICE, door_entity_description
        )

        assert sensor.available is False

    def test_available_false_when_no_readings(
        self,
        mock_coordinator: MagicMock,
        door_entity_description: BinarySensorEntityDescription,
    ) -> None:
        """Test available is False when no readings."""
        device = dict(MOCK_MT_DEVICE)
        del device["readings_raw"]
        mock_coordinator.data = {"devices": [device]}

        sensor = MerakiMtBinarySensor(
            mock_coordinator, cast(MerakiDevice, device), door_entity_description
        )

        assert sensor.available is False

    def test_available_false_when_metric_not_found(
        self,
        mock_coordinator: MagicMock,
        water_entity_description: BinarySensorEntityDescription,
    ) -> None:
        """Test available is False when metric not in readings."""
        # MOCK_MT_DEVICE has door and temperature, not water
        sensor = MerakiMtBinarySensor(
            mock_coordinator, MOCK_MT_DEVICE, water_entity_description
        )

        assert sensor.available is False

    def test_is_on_door_open(
        self,
        mock_coordinator: MagicMock,
        door_entity_description: BinarySensorEntityDescription,
    ) -> None:
        """Test is_on returns True when door is open."""
        sensor = MerakiMtBinarySensor(
            mock_coordinator, MOCK_MT_DEVICE, door_entity_description
        )

        assert sensor.is_on is True

    def test_is_on_door_closed(
        self,
        mock_coordinator: MagicMock,
        door_entity_description: BinarySensorEntityDescription,
    ) -> None:
        """Test is_on returns False when door is closed."""
        device = dict(MOCK_MT_DEVICE)
        device["readings_raw"] = [{"metric": "door", "door": {"open": False}}]
        mock_coordinator.data = {"devices": [device]}

        sensor = MerakiMtBinarySensor(
            mock_coordinator, cast(MerakiDevice, device), door_entity_description
        )

        assert sensor.is_on is False

    def test_is_on_water_present(
        self,
        mock_coordinator: MagicMock,
        water_entity_description: BinarySensorEntityDescription,
    ) -> None:
        """Test is_on returns True when water is present."""
        device = dict(MOCK_MT_DEVICE)
        device["readings_raw"] = [{"metric": "water", "water": {"present": True}}]
        mock_coordinator.data = {"devices": [device]}

        sensor = MerakiMtBinarySensor(
            mock_coordinator, cast(MerakiDevice, device), water_entity_description
        )

        assert sensor.is_on is True

    def test_is_on_no_readings(
        self,
        mock_coordinator: MagicMock,
        door_entity_description: BinarySensorEntityDescription,
    ) -> None:
        """Test is_on returns None when no readings."""
        device = dict(MOCK_MT_DEVICE)
        del device["readings_raw"]
        mock_coordinator.data = {"devices": [device]}

        sensor = MerakiMtBinarySensor(
            mock_coordinator, cast(MerakiDevice, device), door_entity_description
        )

        assert sensor.is_on is None

    def test_is_on_with_direct_boolean(
        self,
        mock_coordinator: MagicMock,
        door_entity_description: BinarySensorEntityDescription,
    ) -> None:
        """Test is_on with direct boolean value."""
        device = dict(MOCK_MT_DEVICE)
        device["readings_raw"] = [{"metric": "door", "door": True}]
        mock_coordinator.data = {"devices": [device]}

        sensor = MerakiMtBinarySensor(
            mock_coordinator, cast(MerakiDevice, device), door_entity_description
        )

        assert sensor.is_on is True

    def test_is_on_with_legacy_value_format(
        self,
        mock_coordinator: MagicMock,
        door_entity_description: BinarySensorEntityDescription,
    ) -> None:
        """Test is_on with legacy value format."""
        device = dict(MOCK_MT_DEVICE)
        device["readings_raw"] = [{"metric": "door", "value": True}]
        mock_coordinator.data = {"devices": [device]}

        sensor = MerakiMtBinarySensor(
            mock_coordinator, cast(MerakiDevice, device), door_entity_description
        )

        assert sensor.is_on is True

    def test_is_on_with_string_value(
        self,
        mock_coordinator: MagicMock,
        door_entity_description: BinarySensorEntityDescription,
    ) -> None:
        """Test is_on with string value format."""
        device = dict(MOCK_MT_DEVICE)
        device["readings_raw"] = [{"metric": "door", "value": "open"}]
        mock_coordinator.data = {"devices": [device]}

        sensor = MerakiMtBinarySensor(
            mock_coordinator, cast(MerakiDevice, device), door_entity_description
        )

        assert sensor.is_on is True
