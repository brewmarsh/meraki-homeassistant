"""Tests for the DeviceDiscoveryService."""

<<<<<<< HEAD
=======
from dataclasses import replace
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
from unittest.mock import ANY, AsyncMock, MagicMock, patch

import pytest

from custom_components.meraki_ha.discovery.service import DeviceDiscoveryService
from tests.const import MOCK_DEVICE


@pytest.fixture
def mock_coordinator_with_devices(mock_coordinator: MagicMock) -> MagicMock:
<<<<<<< HEAD
    """Fixture for a mocked MerakiDataCoordinator with various devices."""
    wireless_device = MOCK_DEVICE.copy()
    wireless_device["model"] = "MR36"
    camera_device = MOCK_DEVICE.copy()
    camera_device["serial"] = "camera_serial"
    camera_device["model"] = "MV12"
    unsupported_device = MOCK_DEVICE.copy()
    unsupported_device["serial"] = "unsupported_serial"
    unsupported_device["model"] = "unsupported"
=======
    """Fixture for a mocked MerakiDataUpdateCoordinator with various devices."""
    wireless_device = replace(MOCK_DEVICE, model="MR36")
    camera_device = replace(MOCK_DEVICE, serial="camera_serial", model="MV12")
    unsupported_device = replace(MOCK_DEVICE, serial="unsupported_serial", model="unsupported")
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
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
<<<<<<< HEAD
=======
        switch_port_coordinator=MagicMock(),
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
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
    MockMRHandler = MagicMock()
    MockMRHandler.__name__ = "MRHandler"
<<<<<<< HEAD
=======
    MockMVHandler = MagicMock()
    MockMVHandler.__name__ = "MVHandler"
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)

    mock_mr_handler_instance = MagicMock()
    mock_mr_handler_instance.discover_entities = AsyncMock(return_value=["mr_entity"])
    MockMRHandler.return_value = mock_mr_handler_instance

<<<<<<< HEAD
    with (
        patch.dict(
            "custom_components.meraki_ha.discovery.service.HANDLER_MAPPING",
            {"MR": MockMRHandler},
=======
    mock_mv_handler_instance = MagicMock()
    mock_mv_handler_instance.discover_entities = AsyncMock(return_value=["mv_entity"])
    MockMVHandler.return_value = mock_mv_handler_instance

    with (
        patch.dict(
            "custom_components.meraki_ha.discovery.service.HANDLER_MAPPING",
            {"MR": MockMRHandler, "MV": MockMVHandler},
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
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
<<<<<<< HEAD
=======
            switch_port_coordinator=MagicMock(),
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
            camera_service=mock_camera_service,
            control_service=mock_control_service,
            network_control_service=MagicMock(),
        )

        # Act
        entities = await service.discover_entities()

        # Assert
        assert "mr_entity" in entities
<<<<<<< HEAD
=======
        assert "mv_entity" in entities
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)

        # Assert correct services are passed to each handler
        MockMRHandler.assert_called_once_with(
            mock_coordinator_with_devices,
            mock_coordinator_with_devices.data["devices"][0],
            mock_config_entry,
            mock_control_service,
<<<<<<< HEAD
            ANY,  # network_control_service
=======
        )
        MockMVHandler.assert_called_once_with(
            mock_coordinator_with_devices,
            mock_coordinator_with_devices.data["devices"][1],
            mock_config_entry,
            mock_camera_service,
            mock_control_service,
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
        )
        assert "No handler found for model 'unsupported'" in caplog.text
