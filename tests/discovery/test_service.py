"""Tests for the DeviceDiscoveryService."""

from unittest.mock import AsyncMock, MagicMock, patch
import pytest
from custom_components.meraki_ha.discovery.service import DeviceDiscoveryService
from tests.const import MOCK_DEVICE


@pytest.fixture
def mock_coordinator():
    """Fixture for a mocked MerakiDataCoordinator."""
    coordinator = MagicMock()
    wireless_device = MOCK_DEVICE.copy()
    camera_device = MOCK_DEVICE.copy()
    camera_device["serial"] = "camera_serial"
    camera_device["productType"] = "camera"
    unsupported_device = MOCK_DEVICE.copy()
    unsupported_device["serial"] = "unsupported_serial"
    unsupported_device["productType"] = "unsupported"
    coordinator.data = {
        "devices": [wireless_device, camera_device, unsupported_device]
    }
    return coordinator


@pytest.fixture
def mock_camera_service():
    """Fixture for a mocked CameraService."""
    return AsyncMock()


@pytest.fixture
def mock_control_service():
    """Fixture for a mock DeviceControlService."""
    return MagicMock()


def test_discovery_service_init(
    mock_coordinator, mock_config_entry, mock_camera_service, mock_control_service
):
    """Test the initialization of the DeviceDiscoveryService."""
    service = DeviceDiscoveryService(
        mock_coordinator, mock_config_entry, mock_camera_service, mock_control_service
    )
    assert service._coordinator is mock_coordinator
    assert len(service._devices) == 3


@pytest.mark.asyncio
async def test_discover_entities_delegates_to_handler(
    mock_coordinator,
    mock_config_entry,
    mock_camera_service,
    mock_control_service,
    caplog,
):
    """Test that discover_entities delegates to the correct handlers."""
    # We must mock the handlers directly to assert their instantiation arguments
    with patch(
        "custom_components.meraki_ha.discovery.service.MRHandler"
    ) as MockMRHandler, patch(
        "custom_components.meraki_ha.discovery.service.MVHandler"
    ) as MockMVHandler:

        # Mock the discover_entities method of the handler instances
        MockMRHandler.return_value.discover_entities = AsyncMock(
            return_value=["mr_entity"]
        )
        MockMVHandler.return_value.discover_entities = AsyncMock(
            return_value=["mv_entity"]
        )

        service = DeviceDiscoveryService(
            mock_coordinator,
            mock_config_entry,
            mock_camera_service,
            mock_control_service,
        )

        # Act
        entities = await service.discover_entities()

        # Assert
        assert len(entities) == 2
        assert "mr_entity" in entities
        assert "mv_entity" in entities

        # Assert correct services are passed to each handler
        MockMRHandler.assert_called_once_with(
            mock_coordinator,
            mock_coordinator.data["devices"][0],
            mock_config_entry,
            mock_control_service,
        )
        MockMVHandler.assert_called_once_with(
            mock_coordinator,
            mock_coordinator.data["devices"][1],
            mock_config_entry,
            mock_camera_service,
            mock_control_service,
        )
        assert "No handler found for product type 'unsupported'" in caplog.text

