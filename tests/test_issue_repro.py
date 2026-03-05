
from unittest.mock import MagicMock

from custom_components.meraki_ha.core.models.device import MerakiDevice
from custom_components.meraki_ha.sensor.device.ap_client_count import (
    MerakiAPClientCountSensor,
)
from custom_components.meraki_ha.services.network_control_service import (
    NetworkControlService,
)


def test_ap_client_count_sensor_handles_none_clients():
    coordinator = MagicMock()
    coordinator.data = {"clients": None}
    device_data = MerakiDevice(serial="test_serial", name="test_device", model="MR33", product_type="wireless")
    config_entry = MagicMock()

    # This should not crash after fix
    sensor = MerakiAPClientCountSensor(coordinator, device_data, config_entry)
    assert sensor.native_value == 0

def test_ap_client_count_sensor_handles_strings_in_clients():
    coordinator = MagicMock()
    coordinator.data = {"clients": ["not_a_dict"]}
    device_data = MerakiDevice(serial="test_serial", name="test_device", model="MR33", product_type="wireless")
    config_entry = MagicMock()

    # This should not crash
    sensor = MerakiAPClientCountSensor(coordinator, device_data, config_entry)
    assert sensor.native_value == 0

def test_network_control_service_handles_strings_in_clients():
    coordinator = MagicMock()
    coordinator.data = {"clients": ["not_a_dict"]}
    api_client = MagicMock()
    service = NetworkControlService(api_client, coordinator)

    # This should not crash after fix
    assert service.get_network_client_count("N_1234") == 0

def test_network_control_service_handles_none_clients():
    coordinator = MagicMock()
    coordinator.data = {"clients": None}
    api_client = MagicMock()
    service = NetworkControlService(api_client, coordinator)

    # This is already safe in current code but good to keep
    assert service.get_network_client_count("N_1234") == 0
