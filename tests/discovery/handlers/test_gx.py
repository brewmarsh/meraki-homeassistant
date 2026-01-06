"""Tests for the GXHandler."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from custom_components.meraki_ha.button.reboot import MerakiRebootButton
from custom_components.meraki_ha.discovery.handlers.gx import GXHandler
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

from ...const import MOCK_CONFIG_ENTRY, MOCK_GX_DEVICE


@pytest.fixture
def mock_control_service() -> MagicMock:
    """Fixture for a mock DeviceControlService."""
    return MagicMock()


@pytest.fixture
def mock_camera_service() -> AsyncMock:
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
    mock_coordinator: MagicMock,
    mock_camera_service: AsyncMock,
    mock_control_service: MagicMock,
) -> None:
<<<<<<< HEAD
<<<<<<< HEAD
    """Test that discover_entities creates a MerakiRebootButton."""
=======
    """Test that discover_entities creates a MerakiRebootButton and Status Sensor."""
>>>>>>> origin/fix/meraki-load-fail-cleanup-7732058548349983668
=======
    """Test that discover_entities creates a MerakiRebootButton and Status Sensor."""
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
    mock_coordinator.data = {"devices": [MOCK_GX_DEVICE]}
    handler = GXHandler(
        mock_coordinator,
        MOCK_GX_DEVICE,
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
=======
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
    # Should have Reboot Button and Device Status Sensor
    # (uplink disabled by default/mock)
    # The default mock config might enable device status.
    assert len(entities) >= 2
    assert any(isinstance(e, MerakiRebootButton) for e in entities)
    assert any(isinstance(e, MerakiDeviceStatusSensor) for e in entities)
<<<<<<< HEAD
>>>>>>> origin/fix/meraki-load-fail-cleanup-7732058548349983668
=======
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
