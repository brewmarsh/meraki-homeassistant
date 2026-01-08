"""Tests for the MerakiCellularUplinkSensor and MerakiCellularSignalSensor."""

from unittest.mock import MagicMock

import pytest

from custom_components.meraki_ha.sensor.device.cellular_uplink import (
    MerakiCellularSignalSensor,
    MerakiCellularUplinkSensor,
)
from custom_components.meraki_ha.types import MerakiDevice

MOCK_MG_DEVICE: MerakiDevice = {
    "serial": "MG-001-TEST",
    "name": "Test MG Gateway",
    "model": "MG21",
    "networkId": "N_12345",
    "productType": "cellularGateway",
    "lanIp": "10.0.0.1",
    "status": "online",
}


@pytest.fixture
def mock_mg_device_with_uplinks() -> dict:
    """Create an MG device with cellular uplink data."""
    device = dict(MOCK_MG_DEVICE)
    device["cellular_uplinks"] = [
        {
            "status": "active",
            "connectionType": "LTE",
            "signalType": "4G",
            "provider": "Verizon",
            "publicIp": "203.0.113.1",
            "ip": "10.0.0.1",
            "apn": "vzwinternet",
            "iccid": "89012345678901234567",
            "interface": "cellular0",
            "roaming": {"status": "not_roaming"},
            "signalStat": {
                "rsrp": "-85",
                "rsrq": "-10",
            },
        }
    ]
    return device


@pytest.fixture
def mock_mg_device_5g() -> dict:
    """Create an MG device with 5G connection."""
    device = dict(MOCK_MG_DEVICE)
    device["cellular_uplinks"] = [
        {
            "status": "active",
            "connectionType": "5G NR",
            "signalStat": {"rsrp": "-75"},
        }
    ]
    return device


@pytest.fixture
def mock_mg_device_3g() -> dict:
    """Create an MG device with 3G connection."""
    device = dict(MOCK_MG_DEVICE)
    device["cellular_uplinks"] = [
        {
            "status": "active",
            "connectionType": "3G HSPA+",
            "signalStat": {"rsrp": "-95"},
        }
    ]
    return device


@pytest.fixture
def mock_mg_device_no_uplinks() -> dict:
    """Create an MG device without uplink data."""
    device = dict(MOCK_MG_DEVICE)
    device["cellular_uplinks"] = []
    return device


# ===== MerakiCellularUplinkSensor Tests =====


def test_uplink_sensor_initialization(
    mock_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_mg_device_with_uplinks: dict,
) -> None:
    """Test uplink sensor initializes correctly."""
    mock_coordinator.data = {"devices": [mock_mg_device_with_uplinks]}

    sensor = MerakiCellularUplinkSensor(
        coordinator=mock_coordinator,
        device_data=mock_mg_device_with_uplinks,
        config_entry=mock_config_entry,
    )

    assert sensor._device_serial == mock_mg_device_with_uplinks["serial"]
    assert (
        sensor._attr_unique_id
        == f"{mock_mg_device_with_uplinks['serial']}_cellular_uplink"
    )
    assert sensor.entity_description.key == "cellular_uplink"
    assert sensor.entity_description.name == "Cellular Status"


def test_uplink_sensor_active_status(
    mock_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_mg_device_with_uplinks: dict,
) -> None:
    """Test uplink sensor shows active status."""
    mock_coordinator.data = {"devices": [mock_mg_device_with_uplinks]}

    sensor = MerakiCellularUplinkSensor(
        coordinator=mock_coordinator,
        device_data=mock_mg_device_with_uplinks,
        config_entry=mock_config_entry,
    )

    assert sensor._attr_native_value == "active"


def test_uplink_sensor_lte_icon(
    mock_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_mg_device_with_uplinks: dict,
) -> None:
    """Test uplink sensor shows 4G icon for LTE connection."""
    mock_coordinator.data = {"devices": [mock_mg_device_with_uplinks]}

    sensor = MerakiCellularUplinkSensor(
        coordinator=mock_coordinator,
        device_data=mock_mg_device_with_uplinks,
        config_entry=mock_config_entry,
    )

    assert sensor._attr_icon == "mdi:signal-4g"


def test_uplink_sensor_5g_icon(
    mock_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_mg_device_5g: dict,
) -> None:
    """Test uplink sensor shows 5G icon for 5G connection."""
    mock_coordinator.data = {"devices": [mock_mg_device_5g]}

    sensor = MerakiCellularUplinkSensor(
        coordinator=mock_coordinator,
        device_data=mock_mg_device_5g,
        config_entry=mock_config_entry,
    )

    assert sensor._attr_icon == "mdi:signal-5g"


def test_uplink_sensor_3g_icon(
    mock_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_mg_device_3g: dict,
) -> None:
    """Test uplink sensor shows 3G icon for 3G connection."""
    mock_coordinator.data = {"devices": [mock_mg_device_3g]}

    sensor = MerakiCellularUplinkSensor(
        coordinator=mock_coordinator,
        device_data=mock_mg_device_3g,
        config_entry=mock_config_entry,
    )

    assert sensor._attr_icon == "mdi:signal-3g"


def test_uplink_sensor_extra_attributes(
    mock_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_mg_device_with_uplinks: dict,
) -> None:
    """Test uplink sensor includes extra state attributes."""
    mock_coordinator.data = {"devices": [mock_mg_device_with_uplinks]}

    sensor = MerakiCellularUplinkSensor(
        coordinator=mock_coordinator,
        device_data=mock_mg_device_with_uplinks,
        config_entry=mock_config_entry,
    )

    attrs = sensor._attr_extra_state_attributes
    assert attrs["provider"] == "Verizon"
    assert attrs["connection_type"] == "LTE"
    assert attrs["public_ip"] == "203.0.113.1"
    assert attrs["rsrp"] == "-85"
    assert attrs["rsrq"] == "-10"
    assert attrs["roaming_status"] == "not_roaming"


def test_uplink_sensor_unknown_when_no_uplinks(
    mock_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_mg_device_no_uplinks: dict,
) -> None:
    """Test uplink sensor shows unknown when no uplinks available."""
    mock_coordinator.data = {"devices": [mock_mg_device_no_uplinks]}

    sensor = MerakiCellularUplinkSensor(
        coordinator=mock_coordinator,
        device_data=mock_mg_device_no_uplinks,
        config_entry=mock_config_entry,
    )

    assert sensor._attr_native_value == "unknown"
    assert sensor._attr_icon == "mdi:signal-cellular-outline"


def test_uplink_sensor_available(
    mock_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_mg_device_with_uplinks: dict,
) -> None:
    """Test uplink sensor availability."""
    mock_coordinator.data = {"devices": [mock_mg_device_with_uplinks]}
    mock_coordinator.last_update_success = True

    sensor = MerakiCellularUplinkSensor(
        coordinator=mock_coordinator,
        device_data=mock_mg_device_with_uplinks,
        config_entry=mock_config_entry,
    )

    assert sensor.available is True


# ===== MerakiCellularSignalSensor Tests =====


def test_signal_sensor_initialization(
    mock_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_mg_device_with_uplinks: dict,
) -> None:
    """Test signal sensor initializes correctly."""
    mock_coordinator.data = {"devices": [mock_mg_device_with_uplinks]}

    sensor = MerakiCellularSignalSensor(
        coordinator=mock_coordinator,
        device_data=mock_mg_device_with_uplinks,
        config_entry=mock_config_entry,
    )

    assert (
        sensor._attr_unique_id
        == f"{mock_mg_device_with_uplinks['serial']}_cellular_signal"
    )
    assert sensor.entity_description.key == "cellular_signal"
    assert sensor.entity_description.name == "Signal Strength (RSRP)"
    assert sensor.entity_description.native_unit_of_measurement == "dBm"


def test_signal_sensor_rsrp_value(
    mock_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_mg_device_with_uplinks: dict,
) -> None:
    """Test signal sensor parses RSRP value correctly."""
    mock_coordinator.data = {"devices": [mock_mg_device_with_uplinks]}

    sensor = MerakiCellularSignalSensor(
        coordinator=mock_coordinator,
        device_data=mock_mg_device_with_uplinks,
        config_entry=mock_config_entry,
    )

    # RSRP is "-85" as a string, should be parsed to -85 int
    assert sensor._attr_native_value == -85


def test_signal_sensor_null_rsrp(
    mock_coordinator: MagicMock,
    mock_config_entry: MagicMock,
) -> None:
    """Test signal sensor handles null RSRP value."""
    device = dict(MOCK_MG_DEVICE)
    device["cellular_uplinks"] = [
        {
            "status": "active",
            "signalStat": {},  # No RSRP
        }
    ]
    mock_coordinator.data = {"devices": [device]}

    sensor = MerakiCellularSignalSensor(
        coordinator=mock_coordinator,
        device_data=device,
        config_entry=mock_config_entry,
    )

    assert sensor._attr_native_value is None


def test_signal_sensor_invalid_rsrp(
    mock_coordinator: MagicMock,
    mock_config_entry: MagicMock,
) -> None:
    """Test signal sensor handles invalid RSRP value."""
    device = dict(MOCK_MG_DEVICE)
    device["cellular_uplinks"] = [
        {
            "status": "active",
            "signalStat": {"rsrp": "invalid"},
        }
    ]
    mock_coordinator.data = {"devices": [device]}

    sensor = MerakiCellularSignalSensor(
        coordinator=mock_coordinator,
        device_data=device,
        config_entry=mock_config_entry,
    )

    assert sensor._attr_native_value is None


def test_signal_sensor_no_uplinks_available(
    mock_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_mg_device_no_uplinks: dict,
) -> None:
    """Test signal sensor unavailable when no uplinks."""
    mock_coordinator.data = {"devices": [mock_mg_device_no_uplinks]}
    mock_coordinator.last_update_success = True

    sensor = MerakiCellularSignalSensor(
        coordinator=mock_coordinator,
        device_data=mock_mg_device_no_uplinks,
        config_entry=mock_config_entry,
    )

    assert sensor.available is False


def test_signal_sensor_available_with_uplinks(
    mock_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_mg_device_with_uplinks: dict,
) -> None:
    """Test signal sensor available when uplinks exist."""
    mock_coordinator.data = {"devices": [mock_mg_device_with_uplinks]}
    mock_coordinator.last_update_success = True

    sensor = MerakiCellularSignalSensor(
        coordinator=mock_coordinator,
        device_data=mock_mg_device_with_uplinks,
        config_entry=mock_config_entry,
    )

    assert sensor.available is True


def test_signal_sensor_coordinator_update(
    mock_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_mg_device_with_uplinks: dict,
) -> None:
    """Test signal sensor updates on coordinator refresh."""
    mock_coordinator.data = {"devices": [mock_mg_device_with_uplinks]}

    sensor = MerakiCellularSignalSensor(
        coordinator=mock_coordinator,
        device_data=mock_mg_device_with_uplinks,
        config_entry=mock_config_entry,
    )

    # Initial value
    assert sensor._attr_native_value == -85

    # Update coordinator data
    updated_device = dict(mock_mg_device_with_uplinks)
    updated_device["cellular_uplinks"] = [
        {
            "status": "active",
            "signalStat": {"rsrp": "-70"},
        }
    ]
    mock_coordinator.data = {"devices": [updated_device]}

    sensor._update_sensor_data()

    assert sensor._attr_native_value == -70
