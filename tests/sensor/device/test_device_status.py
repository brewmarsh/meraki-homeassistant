"""Tests for the Meraki Device Status Sensor."""

from unittest.mock import MagicMock
import pytest
from custom_components.meraki_ha.sensor.device.device_status import MerakiDeviceStatusSensor
from custom_components.meraki_ha.types import MerakiDevice


@pytest.fixture
def mock_device_coordinator():
    """Fixture for a mocked MerakiDeviceCoordinator."""
    coordinator = MagicMock()

    device1 = MerakiDevice(
        serial="Q2XX-XXXX-XXXX",
        name="Device 1",
        model="MR56",
        mac="00:11:22:33:44:55",
        status="online",
        product_type="wireless",
        tags=["tag1", "tag2"],
        firmware="MR 27.1",
        address="123 Street",
        notes="Main AP",
        url="https://dashboard.meraki.com",
    )

    device2 = MerakiDevice(
        serial="Q2YY-YYYY-YYYY",
        name="Device 2",
        model="MX68",
        mac="00:11:22:33:44:66",
        status="alerting",
        product_type="appliance",
        firmware="MX 16.16",
        appliance_uplink_statuses=[
            {
                "interface": "wan1",
                "status": "active",
                "ip": "1.2.3.4",
                "gateway": "1.2.3.1",
                "publicIp": "8.8.8.8",
                "dns": "8.8.4.4",
            }
        ]
    )

    coordinator.data = {
        "devices": [device1, device2]
    }

    # Setup get_device return values
    def get_device(serial):
        for d in coordinator.data["devices"]:
            if d.serial == serial:
                return d
        return None

    coordinator.get_device.side_effect = get_device
    coordinator.last_update_success = True

    return coordinator


def test_device_status_sensor(mock_device_coordinator):
    """Test the device status sensor."""
    device1 = mock_device_coordinator.data["devices"][0]
    device2 = mock_device_coordinator.data["devices"][1]

    config_entry = MagicMock()
    config_entry.options = {}

    sensor1 = MerakiDeviceStatusSensor(mock_device_coordinator, device1, config_entry)
    assert sensor1.unique_id == "Q2XX-XXXX-XXXX_device_status"
    assert sensor1.native_value == "online"
    assert sensor1.icon == "mdi:access-point-network"
    assert sensor1.extra_state_attributes["model"] == "MR56"
    assert sensor1.extra_state_attributes["firmware_version"] == "MR 27.1"
    assert sensor1.extra_state_attributes["tags"] == ["tag1", "tag2"]

    # Verify DeviceInfo
    assert sensor1.device_info["sw_version"] == "MR 27.1"
    assert sensor1.device_info["suggested_area"] == "123 Street"

    sensor2 = MerakiDeviceStatusSensor(mock_device_coordinator, device2, config_entry)
    assert sensor2.unique_id == "Q2YY-YYYY-YYYY_device_status"
    assert sensor2.native_value == "alerting"
    assert sensor2.icon == "mdi:access-point-network-off"
    assert sensor2.extra_state_attributes["product_type"] == "appliance"

    # Check uplink attributes
    assert sensor2.extra_state_attributes["wan1_status"] == "active"
    assert sensor2.extra_state_attributes["wan1_ip"] == "1.2.3.4"
    assert sensor2.extra_state_attributes["wan1_public_ip"] == "8.8.8.8"
