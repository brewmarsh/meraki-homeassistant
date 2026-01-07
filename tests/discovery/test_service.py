"""Tests for the DeviceDiscoveryService."""

from unittest.mock import ANY, AsyncMock, MagicMock, patch

import pytest

from custom_components.meraki_ha.discovery.service import DeviceDiscoveryService
from tests.const import MOCK_DEVICE


@pytest.fixture
def mock_coordinator_with_devices(mock_coordinator: MagicMock) -> MagicMock:
    """Fixture for a mocked MerakiDataCoordinator with various devices."""
    wireless_device = MOCK_DEVICE.copy()
    wireless_device["model"] = "MR36"
    camera_device = MOCK_DEVICE.copy()
    camera_device["serial"] = "camera_serial"
    camera_device["model"] = "MV12"
    unsupported_device = MOCK_DEVICE.copy()
    unsupported_device["serial"] = "unsupported_serial"
    unsupported_device["model"] = "unsupported"
    mock_coordinator.data = {
        "devices": [wireless_device, camera_device, unsupported_device],
        "networks": [],
        "ssids": [],
    }
    return mock_coordinator


@pytest.fixture
def mock_camera_service() -> AsyncMock:
    """Fixture for a mocked CameraService."""
    return AsyncMock()


@pytest.fixture
def mock_control_service() -> MagicMock:
    """Fixture for a mock DeviceControlService."""
    return MagicMock()


def test_discovery_service_init(
    mock_coordinator_with_devices: MagicMock,
    mock_config_entry: MagicMock,
    mock_camera_service: AsyncMock,
    mock_control_service: MagicMock,
):
    """Test the initialization of the DeviceDiscoveryService."""
    service = DeviceDiscoveryService(
        coordinator=mock_coordinator_with_devices,
        config_entry=mock_config_entry,
        meraki_client=MagicMock(),
        camera_service=mock_camera_service,
        control_service=mock_control_service,
        network_control_service=MagicMock(),
    )
    assert service._coordinator is mock_coordinator_with_devices
    assert len(service._devices) == 3


@pytest.mark.asyncio
async def test_discover_entities_delegates_to_handler(
    mock_coordinator_with_devices: MagicMock,
    mock_config_entry: MagicMock,
    mock_camera_service: AsyncMock,
    mock_control_service: MagicMock,
    caplog,
):
    """Test that discover_entities delegates to the correct handlers."""
    # We must mock the handlers directly to assert their instantiation arguments
    # The service uses the constructor directly, not create()
    mock_mr_handler_instance = MagicMock()
    mock_mr_handler_instance.discover_entities = AsyncMock(return_value=["mr_entity"])

    MockMRHandler = MagicMock(return_value=mock_mr_handler_instance)
    MockMRHandler.__name__ = "MRHandler"

    # Also mock MV handler since we have an MV device in the fixture
    mock_mv_handler_instance = MagicMock()
    mock_mv_handler_instance.discover_entities = AsyncMock(return_value=["mv_entity"])

    MockMVHandler = MagicMock(return_value=mock_mv_handler_instance)
    MockMVHandler.__name__ = "MVHandler"

    with (
        patch.dict(
            "custom_components.meraki_ha.discovery.service.HANDLER_MAPPING",
            {"MR": MockMRHandler, "MV": MockMVHandler},
        ),
        patch(
            "custom_components.meraki_ha.discovery.handlers.network.NetworkHandler"
        ) as MockNetworkHandler,
        patch("custom_components.meraki_ha.discovery.handlers.ssid.SSIDHandler"),
    ):
        mock_network_handler_instance = MagicMock()
        mock_network_handler_instance.discover_entities = AsyncMock(return_value=[])
        MockNetworkHandler.create.return_value = mock_network_handler_instance

        service = DeviceDiscoveryService(
            coordinator=mock_coordinator_with_devices,
            config_entry=mock_config_entry,
            meraki_client=MagicMock(),
            camera_service=mock_camera_service,
            control_service=mock_control_service,
            network_control_service=MagicMock(),
        )

        # Act
        entities = await service.discover_entities()

        # Assert
        assert "mr_entity" in entities
        assert "mv_entity" in entities

        # Assert correct services are passed to each handler via constructor
        MockMRHandler.assert_called_once_with(
            mock_coordinator_with_devices,
            mock_coordinator_with_devices.data["devices"][0],
            mock_config_entry,
            mock_control_service,
            ANY,  # network_control_service
        )
        assert "No handler found for model 'unsupported'" in caplog.text
