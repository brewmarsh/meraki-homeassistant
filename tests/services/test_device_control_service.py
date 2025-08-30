"""
Tests for the DeviceControlService.
"""

from unittest.mock import AsyncMock, MagicMock
import pytest

from custom_components.meraki_ha.services.device_control_service import (
    DeviceControlService,
)


@pytest.fixture
def mock_repository():
    """Fixture for a mock MerakiRepository."""
    repo = MagicMock()
    repo.async_reboot_device = AsyncMock()
    return repo


async def test_async_reboot_calls_repository(mock_repository):
    """Test that async_reboot calls the repository's async_reboot_device."""
    service = DeviceControlService(mock_repository)
    serial = "Q234-ABCD-5678"

    await service.async_reboot(serial)

    mock_repository.async_reboot_device.assert_awaited_once_with(serial)
