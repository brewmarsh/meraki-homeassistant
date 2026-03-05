"""Tests for the DeviceDiscoveryService."""

from collections.abc import AsyncGenerator
from dataclasses import replace
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from homeassistant.config_entries import ConfigEntry

# Resolved: Using the centralized coordinator path from the 2.3.0-beta.120 refactor
from custom_components.meraki_ha.coordinators import MerakiMainCoordinator
from custom_components.meraki_ha.discovery.service import DeviceDiscoveryService
from custom_components.meraki_ha.services.camera_service import CameraService
from custom_components.meraki_ha.services.device_control_service import (
    DeviceControlService,
)
from tests.const import MOCK_DEVICE


@pytest.fixture
def mock_coordinator_with_devices(
    mock_coordinator: MagicMock,
) -> MagicMock:
    """Fixture for a mocked MerakiMainCoordinator with various devices."""
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
    mock_coordinator_with_devices: MerakiMainCoordinator,
    mock_config_entry: ConfigEntry,
    mock_camera_service: CameraService,
    mock_control_service: DeviceControlService,
) -> None:
    """Test the initialization of the DeviceDiscoveryService."""
    mock_meraki_client: MagicMock = MagicMock()
    mock_network_control_service: MagicMock = MagicMock()

    service: DeviceDiscoveryService = DeviceDiscoveryService(
        main_coordinator=mock_coordinator_with_devices,
        device_coordinator=mock_coordinator_with_devices,
        switch_coordinator=mock_coordinator_with_devices,
        camera_coordinator=mock_coordinator_with_devices,
        sensor_coordinator=mock_coordinator_with_devices,
        wireless_coordinator=mock_coordinator_with_devices,
        appliance_coordinator=mock_coordinator_with_devices,
        client_coordinator=mock_coordinator_with_devices,
        config_entry=mock_config_entry,
        meraki_client=mock_meraki_client,
        camera_service=mock_camera_service,
        control_service=mock_control_service,
        network_control_service=mock_network_control_service,
    )
    assert service._main_coordinator is mock_coordinator_with_devices
    assert len(service._devices) == 3


@pytest.mark.asyncio
async def test_discover_entities_delegates_to_handler(
    mock_coordinator_with_devices: MerakiMainCoordinator,
    mock_config_entry: ConfigEntry,
    mock_camera_service: CameraService,
    mock_control_service: DeviceControlService,
) -> None:
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
            "custom_components.meraki_ha.discovery.service.WirelessHandler"
        ) as MockWirelessHandler,
    ):

        async def mock_aiter_universal() -> AsyncGenerator[Any, None]:
            yield "universal_entity"

        mock_universal_handler_instance: MagicMock = MagicMock()
        mock_universal_handler_instance.discover_entities.side_effect = (
            mock_aiter_universal
        )
        MockUniversalHandler.return_value = mock_universal_handler_instance

        async def mock_aiter_empty() -> AsyncGenerator[Any, None]:
            # This function intentionally yields nothing, simulating an empty generator.
            if False:  # pylint: disable=using-constant-test
                yield

        mock_network_handler_instance: MagicMock = MagicMock()
        mock_network_handler_instance.discover_entities.side_effect = mock_aiter_empty
        MockNetworkHandler.return_value = mock_network_handler_instance

        mock_wireless_handler_instance: MagicMock = MagicMock()
        mock_wireless_handler_instance.discover_entities.side_effect = mock_aiter_empty
        MockWirelessHandler.return_value = mock_wireless_handler_instance

        mock_meraki_client: MagicMock = MagicMock()
        mock_network_control_service: MagicMock = MagicMock()

        service: DeviceDiscoveryService = DeviceDiscoveryService(
            main_coordinator=mock_coordinator_with_devices,
            device_coordinator=mock_coordinator_with_devices,
            switch_coordinator=mock_coordinator_with_devices,
            camera_coordinator=mock_coordinator_with_devices,
            sensor_coordinator=mock_coordinator_with_devices,
            wireless_coordinator=mock_coordinator_with_devices,
            appliance_coordinator=mock_coordinator_with_devices,
            client_coordinator=mock_coordinator_with_devices,
            config_entry=mock_config_entry,
            meraki_client=mock_meraki_client,
            camera_service=mock_camera_service,
            control_service=mock_control_service,
            network_control_service=mock_network_control_service,
        )

        # Act
        entities: list[Any] = await service.discover_entities()

        # Assert
        assert "universal_entity" in entities

        # Assert UniversalHandler called for each device
        assert MockUniversalHandler.call_count == 3
        MockUniversalHandler.assert_any_call(
            mock_coordinator_with_devices,
            mock_coordinator_with_devices.data["devices"][0],
            mock_config_entry,
            mock_camera_service,
            mock_control_service,
            mock_network_control_service,
        )
