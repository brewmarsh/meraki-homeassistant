"""Tests for the Meraki device firmware status sensor."""

from unittest.mock import MagicMock

import pytest

from custom_components.meraki_ha.sensor.device.meraki_firmware_status import (
    MerakiFirmwareStatusSensor,
)
from custom_components.meraki_ha.types import MerakiDevice


@pytest.fixture
def mock_device_coordinator():
    """Fixture for a mocked MerakiDeviceCoordinator."""
    coordinator = MagicMock()

    device1 = MerakiDevice(
        serial="dev1",
        name="Device 1",
        model="MR52",
        mac="00:11:22:33:44:55",
        firmware="26.6",
        firmware_upgrades={
            "available": True,
            "latestVersion": {"shortName": "27.1"},
            "nextUpgrade": {
                "toVersion": {"shortName": "27.1"},
                "time": "2025-08-01T00:00:00Z",
            },
        },
    )

    device2 = MerakiDevice(
        serial="dev2",
        name="Device 2",
        model="MS220-8P",
        mac="00:11:22:33:44:66",
        firmware="15.15",
        firmware_upgrades={
            "available": False,
        },
    )

    coordinator.data = {"devices": [device1, device2]}

    def get_device(serial):
        for d in coordinator.data["devices"]:
            if d.serial == serial:
                return d
        return None

    coordinator.get_device.side_effect = get_device

    return coordinator


def test_firmware_status_sensor(mock_device_coordinator):
    """Test the firmware status sensor."""
    device1 = mock_device_coordinator.data["devices"][0]
    device2 = mock_device_coordinator.data["devices"][1]

    config_entry = MagicMock()
    config_entry.options = {}

    sensor1 = MerakiFirmwareStatusSensor(mock_device_coordinator, device1, config_entry)
    assert sensor1.unique_id == "dev1_firmware_status"
    assert sensor1.name == "Firmware Status"
    assert sensor1.state == "update_available"
    assert sensor1.extra_state_attributes["latest_available_firmware_version"] == "27.1"

    sensor2 = MerakiFirmwareStatusSensor(mock_device_coordinator, device2, config_entry)
    assert sensor2.unique_id == "dev2_firmware_status"
    assert sensor2.name == "Firmware Status"
    assert sensor2.state == "up_to_date"
    assert "latest_version" not in sensor2.extra_state_attributes
