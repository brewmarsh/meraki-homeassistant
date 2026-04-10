"""Tests for the Meraki Network Settings Sensors."""

from collections.abc import Callable
from unittest.mock import MagicMock

import pytest

from custom_components.meraki_ha.sensor.device.network_settings import (
    MerakiDeviceIPSensor,
)
from custom_components.meraki_ha.types import MerakiDevice


@pytest.fixture
def mock_device_coordinator() -> MagicMock:
    """Fixture for a mocked MerakiDeviceCoordinator."""
    coordinator = MagicMock()

    # Standard Wireless device with LAN IP
    device1: MerakiDevice = MerakiDevice(
        serial="Q2XX-XXXX-XXXX",
        name="Device 1",
        model="MR56",
        mac="00:11:22:33:44:55",
        status="online",
        product_type="wireless",
        lan_ip="192.168.1.1",
    )

    # MX Security Appliance with missing LAN IP
    device2: MerakiDevice = MerakiDevice(
        serial="Q2YY-YYYY-YYYY",
        name="Device 2",
        model="MX68",
        mac="00:11:22:33:44:66",
        status="online",
        product_type="appliance",
        lan_ip=None,
    )

    # Z3 Security Appliance with empty LAN IP
    device3: MerakiDevice = MerakiDevice(
        serial="Q2ZZ-ZZZZ-ZZZZ",
        name="Device 3",
        model="Z3",
        mac="00:11:22:33:44:77",
        status="online",
        product_type="appliance",
        lan_ip="",
    )

    # Standard Switch with missing LAN IP
    device4: MerakiDevice = MerakiDevice(
        serial="Q2WW-WWWW-WWWW",
        name="Device 4",
        model="MS120-8LP",
        mac="00:11:22:33:44:88",
        status="online",
        product_type="switch",
        lan_ip=None,
    )

    # MT Sensor - should show "N/A (Bluetooth)"
    device5: MerakiDevice = MerakiDevice(
        serial="Q2TT-TTTT-TTTT",
        name="Device 5",
        model="MT11",
        mac="00:11:22:33:44:99",
        status="online",
        product_type="sensor",
        lan_ip=None,
    )

    coordinator.data: dict[str, list[MerakiDevice]] = {
        "devices": [device1, device2, device3, device4, device5]
    }

    # Setup get_device return values
    def get_device(serial: str) -> MerakiDevice | None:
        for d in coordinator.data["devices"]:
            if d.serial == serial:
                return d
        return None

    coordinator.get_device.side_effect: Callable[[str], MerakiDevice | None] = (
        get_device
    )
    coordinator.last_update_success = True

    return coordinator


def test_lan_ip_sensor_logic(mock_device_coordinator: MagicMock) -> None:
    """Test the LAN IP sensor logic for different devices."""
    config_entry: MagicMock = MagicMock()
    config_entry.options = {}

    # 1. MR56 - should show its LAN IP
    device1 = mock_device_coordinator.data["devices"][0]
    sensor1 = MerakiDeviceIPSensor(
        mock_device_coordinator, device1, config_entry, "lanIp"
    )
    assert sensor1.native_value == "192.168.1.1"

    # 2. MX68 with None LAN IP - should show "Multiple (VLANs)" after fix
    device2 = mock_device_coordinator.data["devices"][1]
    sensor2 = MerakiDeviceIPSensor(
        mock_device_coordinator, device2, config_entry, "lanIp"
    )
    assert sensor2.native_value == "Multiple (VLANs)"

    # 3. Z3 with empty LAN IP - should show "Multiple (VLANs)" after fix
    device3 = mock_device_coordinator.data["devices"][2]
    sensor3 = MerakiDeviceIPSensor(
        mock_device_coordinator, device3, config_entry, "lanIp"
    )
    assert sensor3.native_value == "Multiple (VLANs)"

    # 4. MS120 with None LAN IP - should show None (Unknown)
    device4 = mock_device_coordinator.data["devices"][3]
    sensor4 = MerakiDeviceIPSensor(
        mock_device_coordinator, device4, config_entry, "lanIp"
    )
    assert sensor4.native_value is None

    # 5. MT11 - should show "N/A (Bluetooth)"
    device5 = mock_device_coordinator.data["devices"][4]
    sensor5 = MerakiDeviceIPSensor(
        mock_device_coordinator, device5, config_entry, "lanIp"
    )
    assert sensor5.native_value == "N/A (Bluetooth)"

    # 6. MT11 Public IP - should show "N/A (Bluetooth)"
    sensor6 = MerakiDeviceIPSensor(
        mock_device_coordinator, device5, config_entry, "publicIp"
    )
    assert sensor6.native_value == "N/A (Bluetooth)"
