"""Tests for the MXHandler."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from custom_components.meraki_ha.button.reboot import MerakiRebootButton
from custom_components.meraki_ha.discovery.handlers.mx import MXHandler
<<<<<<< HEAD
<<<<<<< HEAD
=======
from custom_components.meraki_ha.sensor.device.device_status import (
    MerakiDeviceStatusSensor,
)
>>>>>>> origin/fix/meraki-load-fail-cleanup-7732058548349983668
=======
from custom_components.meraki_ha.sensor.device.device_status import (
    MerakiDeviceStatusSensor,
)
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129

from ...const import MOCK_CONFIG_ENTRY, MOCK_MX_DEVICE


@pytest.fixture
def mock_coordinator():
    """Fixture for a mock MerakiDataCoordinator."""
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


@pytest.mark.asyncio
<<<<<<< HEAD
<<<<<<< HEAD
async def test_discover_entities_creates_reboot_button(
=======
async def test_discover_entities_creates_reboot_button_and_status_sensor(
>>>>>>> origin/fix/meraki-load-fail-cleanup-7732058548349983668
=======
async def test_discover_entities_creates_reboot_button_and_status_sensor(
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
    mock_coordinator, mock_camera_service, mock_control_service
):
    """Test that discover_entities creates a MerakiRebootButton."""
    handler = MXHandler(
        mock_coordinator,
        MOCK_MX_DEVICE,
        MOCK_CONFIG_ENTRY,
        mock_camera_service,
        mock_control_service,
    )

    entities = await handler.discover_entities()

<<<<<<< HEAD
<<<<<<< HEAD
    assert len(entities) == 1
    assert isinstance(entities[0], MerakiRebootButton)
=======
    assert len(entities) >= 2
    assert any(isinstance(e, MerakiRebootButton) for e in entities)
    assert any(isinstance(e, MerakiDeviceStatusSensor) for e in entities)
>>>>>>> origin/fix/meraki-load-fail-cleanup-7732058548349983668
=======
    assert len(entities) >= 2
    assert any(isinstance(e, MerakiRebootButton) for e in entities)
    assert any(isinstance(e, MerakiDeviceStatusSensor) for e in entities)
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
