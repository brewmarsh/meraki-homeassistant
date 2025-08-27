"""Tests for the DeviceDiscoveryService."""

from unittest.mock import AsyncMock, MagicMock, patch, ANY
import pytest
from custom_components.meraki_ha.discovery.service import DeviceDiscoveryService
from tests.const import MOCK_DEVICE


@pytest.fixture
def mock_coordinator():
    """Fixture for a mocked MerakiDataCoordinator."""
    coordinator = MagicMock()
    wireless_device = MOCK_DEVICE.copy()
    wireless_device["model"] = "MR36"
    camera_device = MOCK_DEVICE.copy()
    camera_device["serial"] = "camera_serial"
    camera_device["model"] = "MV12"
    unsupported_device = MOCK_DEVICE.copy()
    unsupported_device["serial"] = "unsupported_serial"
    unsupported_device["model"] = "unsupported"
    coordinator.data = {
        "devices": [wireless_device, camera_device, unsupported_device],
        "networks": [],
        "ssids": [],
    }
    return coordinator


@pytest.fixture
def mock_camera_service():
    """Fixture for a mocked CameraService."""
    return AsyncMock()


@pytest.fixture
def mock_config_entry():
    """Fixture for a mocked config entry."""
    return MagicMock()


@pytest.fixture
def mock_control_service():
    """Fixture for a mock DeviceControlService."""
    return MagicMock()


def test_discovery_service_init(
    mock_coordinator, mock_config_entry, mock_camera_service, mock_control_service
):
    """Test the initialization of the DeviceDiscoveryService."""
    service = DeviceDiscoveryService(
        coordinator=mock_coordinator,
        config_entry=mock_config_entry,
        meraki_client=MagicMock(),
        switch_port_coordinator=MagicMock(),
        camera_service=mock_camera_service,
        control_service=mock_control_service,
        network_control_service=MagicMock(),
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
    MockMRHandler = MagicMock()
    MockMRHandler.__name__ = "MRHandler"
    MockMVHandler = MagicMock()
    MockMVHandler.__name__ = "MVHandler"

    mock_mr_handler_instance = MagicMock()
    mock_mr_handler_instance.discover_entities = AsyncMock(return_value=["mr_entity"])
    MockMRHandler.return_value = mock_mr_handler_instance

    mock_mv_handler_instance = MagicMock()
    mock_mv_handler_instance.discover_entities = AsyncMock(return_value=["mv_entity"])
    MockMVHandler.return_value = mock_mv_handler_instance


    with patch.dict(
        "custom_components.meraki_ha.discovery.service.HANDLER_MAPPING",
        {"MR": MockMRHandler, "MV": MockMVHandler},
    ), patch("custom_components.meraki_ha.discovery.handlers.network.NetworkHandler") as MockNetworkHandler, patch("custom_components.meraki_ha.discovery.handlers.ssid.SSIDHandler"):
        mock_network_handler_instance = MagicMock()
        mock_network_handler_instance.discover_entities = AsyncMock(return_value=[])
        MockNetworkHandler.create.return_value = mock_network_handler_instance

        service = DeviceDiscoveryService(
            coordinator=mock_coordinator,
            config_entry=mock_config_entry,
            meraki_client=MagicMock(),
            switch_port_coordinator=MagicMock(),
            camera_service=mock_camera_service,
            control_service=mock_control_service,
            network_control_service=MagicMock(),
        )

        # Act
        entities = await service.discover_entities()

        # Assert
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
        assert "No handler found for model 'unsupported'" in caplog.text
