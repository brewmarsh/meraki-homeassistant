"""Test for entity naming conventions."""

from __future__ import annotations

from unittest.mock import MagicMock

from custom_components.meraki_ha.binary_sensor.device.camera_motion import (
    MerakiMotionSensor,
)
from custom_components.meraki_ha.camera import MerakiCamera
from custom_components.meraki_ha.sensor.device.connected_clients import (
    MerakiDeviceConnectedClientsSensor,
)
from custom_components.meraki_ha.sensor.device.device_status import (
    MerakiDeviceStatusSensor,
)
from custom_components.meraki_ha.types import MerakiDevice


async def test_naming_conventions():
    """Test that entities have the correct naming conventions."""
    mock_coordinator = MagicMock()
    mock_camera_service = MagicMock()
    mock_config_entry = MagicMock()

    device = MerakiDevice(
        serial="Q234-ABCD-5678",
        name="Office Camera",
        model="MV12",
        lan_ip="1.2.3.4",
        mac="00:11:22:33:44:55",
        network_id="N_12345",
        status="online",
    )

    camera = MerakiCamera(
        coordinator=mock_coordinator,
        device=device,
        camera_service=mock_camera_service,
        config_entry=mock_config_entry,
    )
    assert camera.name is None

    motion_sensor = MerakiMotionSensor(
        coordinator=mock_coordinator,
        device=device,
        camera_service=mock_camera_service,
        config_entry=mock_config_entry,
    )
    assert motion_sensor.name == "Motion"
    assert motion_sensor.has_entity_name is True

    status_sensor = MerakiDeviceStatusSensor(
        coordinator=mock_coordinator,
        device_data=device,
        config_entry=mock_config_entry,
    )
    assert status_sensor.name == "Status"
    assert status_sensor.has_entity_name is True

    connected_clients_sensor = MerakiDeviceConnectedClientsSensor(
        coordinator=mock_coordinator,
        device_data=device,
        config_entry=mock_config_entry,
    )
    assert connected_clients_sensor.name == "Connected Clients"
    assert connected_clients_sensor.has_entity_name is True
