"""Tests for the DeviceDiscoveryService."""

from dataclasses import replace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from custom_components.meraki_ha.discovery.service import DeviceDiscoveryService
from tests.const import MOCK_DEVICE


@pytest.fixture
def mock_coordinator_with_devices(mock_coordinator: MagicMock) -> MagicMock:
    """Fixture for a mocked MerakiDataUpdateCoordinator with various devices."""
    wireless_device = replace(MOCK_DEVICE, model="MR36")
    camera_device = replace(MOCK_DEVICE, serial="camera_serial", model="MV12")
    unsupported_device = replace(
        MOCK_DEVICE, serial="unsupported_serial", model="unsupported"
    )
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
):
    """Test that discover_entities delegates to the correct handlers."""
    # We must mock the handlers directly to assert their instantiation arguments
    with (
        patch(
            "custom_components.meraki_ha.discovery.service.UniversalHandler"
        ) as MockUniversalHandler,
        patch(
            "custom_components.meraki_ha.discovery.service.NetworkHandler"
        ) as MockNetworkHandler,
        patch(
            "custom_components.meraki_ha.discovery.service.SSIDHandler"
        ) as MockSSIDHandler,
    ):
        async def mock_aiter_universal():
            yield "universal_entity"

        mock_universal_handler_instance = MagicMock()
        mock_universal_handler_instance.discover_entities.side_effect = (
            mock_aiter_universal
        )
        MockUniversalHandler.return_value = mock_universal_handler_instance

        async def mock_aiter_empty():
            if False:
                yield

        mock_network_handler_instance = MagicMock()
        mock_network_handler_instance.discover_entities.side_effect = mock_aiter_empty
        MockNetworkHandler.return_value = mock_network_handler_instance

        mock_ssid_handler_instance = MagicMock()
        mock_ssid_handler_instance.discover_entities.side_effect = mock_aiter_empty
        MockSSIDHandler.return_value = mock_ssid_handler_instance

        mock_network_control_service = MagicMock()
        service = DeviceDiscoveryService(
            coordinator=mock_coordinator_with_devices,
            config_entry=mock_config_entry,
            meraki_client=MagicMock(),
            camera_service=mock_camera_service,
            control_service=mock_control_service,
            network_control_service=mock_network_control_service,
        )

        # Act
        entities = await service.discover_entities()

        # Assert
        assert "universal_entity" in entities

        # Assert UniversalHandler called for each device
        assert MockUniversalHandler.call_count == 3
        MockUniversalHandler.assert_any_call(
            mock_coordinator_with_devices,
            mock_coordinator_with_devices.data["devices"][0],
            mock_config_entry,
            # MR36 capabilities
            ["ssids", "client_count", "radio_utilization", "reboot", "status"],
            mock_camera_service,
            mock_control_service,
            mock_network_control_service,
        )
