"""Tests for the MXHandler."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from custom_components.meraki_ha.button.reboot import MerakiRebootButton
from custom_components.meraki_ha.discovery.handlers.mx import MXHandler
from custom_components.meraki_ha.sensor.device.appliance_port import (
    MerakiAppliancePortSensor,
)
from custom_components.meraki_ha.sensor.device.appliance_uplink import (
    MerakiApplianceUplinkSensor,
)
from custom_components.meraki_ha.sensor.device.device_status import (
    MerakiDeviceStatusSensor,
)
from custom_components.meraki_ha.types import MerakiAppliancePort

from ...const import MOCK_CONFIG_ENTRY, MOCK_MX_DEVICE


@pytest.fixture
def mock_coordinator():
    """Fixture for a mock MerakiDataUpdateCoordinator."""
    coordinator = MagicMock()
    coordinator.data = {"devices": [MOCK_MX_DEVICE]}
    return coordinator


@pytest.fixture
def mock_control_service():
    """Fixture for a mock DeviceControlService."""
    return MagicMock()


@pytest.fixture
def mock_camera_service():
    """Fixture for a mocked CameraService."""
    return AsyncMock()


@pytest.fixture
def mock_network_control_service():
    """Fixture for a mock NetworkControlService."""
    return MagicMock()


@pytest.mark.asyncio
async def test_discover_entities_creates_reboot_button_and_status_sensor(
    mock_coordinator,
    mock_camera_service,
    mock_control_service,
    mock_network_control_service,
):
    """Test that discover_entities creates a MerakiRebootButton."""
    handler = MXHandler(
        mock_coordinator,
        MOCK_MX_DEVICE,
        MOCK_CONFIG_ENTRY,
        mock_control_service,
        mock_network_control_service,
    )

    entities = await handler.discover_entities()

    assert len(entities) >= 2
    assert any(isinstance(e, MerakiRebootButton) for e in entities)
    assert any(isinstance(e, MerakiDeviceStatusSensor) for e in entities)
    assert any(isinstance(e, MerakiApplianceUplinkSensor) for e in entities)


@pytest.mark.asyncio
async def test_discover_entities_creates_port_sensors(
    mock_coordinator,
    mock_camera_service,
    mock_control_service,
    mock_network_control_service,
):
    """Test that discover_entities creates MerakiAppliancePortSensor."""
    device = MOCK_MX_DEVICE
    device.appliance_ports = [
        MerakiAppliancePort(number=1, enabled=True, status="connected"),
        MerakiAppliancePort(number=2, enabled=True, status="disconnected"),
    ]

    handler = MXHandler(
        mock_coordinator,
        device,
        MOCK_CONFIG_ENTRY,
        mock_control_service,
        mock_network_control_service,
    )

    entities = await handler.discover_entities()

    port_sensors = [e for e in entities if isinstance(e, MerakiAppliancePortSensor)]
    assert len(port_sensors) == 2
    assert port_sensors[0].unique_id == f"{device.serial}_port_1"
    assert port_sensors[1].unique_id == f"{device.serial}_port_2"
