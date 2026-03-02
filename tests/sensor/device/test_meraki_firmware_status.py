"""Tests for the Meraki device firmware status sensor."""

from typing import List, Optional
from unittest.mock import MagicMock

import pytest

from custom_components.meraki_ha.coordinators import MerakiMainCoordinator
from custom_components.meraki_ha.sensor.device.meraki_firmware_status import (
    MerakiFirmwareStatusSensor,
)
from custom_components.meraki_ha.types import MerakiDevice


@pytest.fixture
def mock_device_coordinator() -> MagicMock:
    """Fixture for a mocked MerakiMainCoordinator.

    This mock provides a structured 'data' attribute and a 'get_device' method
    as expected by the Meraki firmware status sensor.
    """
    # Using spec=MerakiMainCoordinator allows type checkers to validate
    # interactions with the mock against the actual coordinator's interface.
    coordinator: MagicMock = MagicMock(spec=MerakiMainCoordinator)

    device1: MerakiDevice = MerakiDevice(
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

    device2: MerakiDevice = MerakiDevice(
        serial="dev2",
        name="Device 2",
        model="MS220-8P",
        mac="00:11:22:33:44:66",
        firmware="15.15",
        firmware_upgrades={
            "available": False,
        },
    )

    # Mimic the coordinator's data structure
    coordinator.data = {"devices": [device1, device2]}

    def get_device_side_effect(serial: str) -> Optional[MerakiDevice]:
        """Side effect function for coordinator.get_device to simulate lookup."""
        # Assume coordinator.data["devices"] holds a list of MerakiDevice objects
        devices: List[MerakiDevice] = coordinator.data["devices"]
        for d in devices:
            if d.serial == serial:
                return d
        return None

    # Assign the side effect to the mock's get_device method
    coordinator.get_device.side_effect = get_device_side_effect

    return coordinator


def test_firmware_status_sensor(mock_device_coordinator: MagicMock) -> None:
    """Test the firmware status sensor functionality."""
    # Retrieve mock devices from the coordinator's data
    device1: MerakiDevice = mock_device_coordinator.data["devices"][0]
    device2: MerakiDevice = mock_device_coordinator.data["devices"][1]

    # Mock a Home Assistant ConfigEntry, which is typically passed during setup
    config_entry: MagicMock = MagicMock()
    config_entry.options = {}

    # Test sensor for device1 (update available)
    sensor1: MerakiFirmwareStatusSensor = MerakiFirmwareStatusSensor(
        mock_device_coordinator, device1, config_entry
    )
    assert sensor1.unique_id == "dev1_firmware_status"
    assert sensor1.name == "Firmware Status"
    assert sensor1.state == "update_available"
    assert sensor1.extra_state_attributes["latest_available_firmware_version"] == "27.1"
    # Additional checks for expected attributes if needed, e.g., icon, device_info, etc.

    # Test sensor for device2 (up to date)
    sensor2: MerakiFirmwareStatusSensor = MerakiFirmwareStatusSensor(
        mock_device_coordinator, device2, config_entry
    )
    assert sensor2.unique_id == "dev2_firmware_status"
    assert sensor2.name == "Firmware Status"
    assert sensor2.state == "up_to_date"
    # Ensure the "latest_available_firmware_version" attribute is not present when no update is available.
    assert "latest_available_firmware_version" not in sensor2.extra_state_attributes
