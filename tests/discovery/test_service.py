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


@pytest.mark.asyncio
async def test_discover_entities_routes_cw_to_mr_handler(
    mock_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_camera_service: AsyncMock,
    mock_control_service: MagicMock,
):
    """Test that CW (Catalyst Wireless) devices are routed to MRHandler."""
    cw_device = MOCK_DEVICE.copy()
    cw_device["serial"] = "cw_serial"
    cw_device["model"] = "CW9166I"  # Catalyst Wireless
    mock_coordinator.data = {
        "devices": [cw_device],
        "networks": [],
        "ssids": [],
    }

    mock_mr_handler_instance = MagicMock()
    mock_mr_handler_instance.discover_entities = AsyncMock(return_value=["cw_entity"])

    MockMRHandler = MagicMock(return_value=mock_mr_handler_instance)
    MockMRHandler.__name__ = "MRHandler"

    with (
        patch.dict(
            "custom_components.meraki_ha.discovery.service.HANDLER_MAPPING",
            {"CW": MockMRHandler},
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
            coordinator=mock_coordinator,
            config_entry=mock_config_entry,
            meraki_client=MagicMock(),
            camera_service=mock_camera_service,
            control_service=mock_control_service,
            network_control_service=MagicMock(),
        )

        entities = await service.discover_entities()

        assert "cw_entity" in entities
        MockMRHandler.assert_called_once()


@pytest.mark.asyncio
async def test_discover_entities_routes_c9_to_ms_handler(
    mock_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_camera_service: AsyncMock,
    mock_control_service: MagicMock,
):
    """Test that C9 (Catalyst 9200/9300 Switch) devices are routed to MSHandler."""
    c9_device = MOCK_DEVICE.copy()
    c9_device["serial"] = "c9_serial"
    c9_device["model"] = "C9300-48P"  # Catalyst Switch
    mock_coordinator.data = {
        "devices": [c9_device],
        "networks": [],
        "ssids": [],
    }

    mock_ms_handler_instance = MagicMock()
    mock_ms_handler_instance.discover_entities = AsyncMock(return_value=["c9_entity"])

    MockMSHandler = MagicMock(return_value=mock_ms_handler_instance)
    MockMSHandler.__name__ = "MSHandler"

    with (
        patch.dict(
            "custom_components.meraki_ha.discovery.service.HANDLER_MAPPING",
            {"C9": MockMSHandler},
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
            coordinator=mock_coordinator,
            config_entry=mock_config_entry,
            meraki_client=MagicMock(),
            camera_service=mock_camera_service,
            control_service=mock_control_service,
            network_control_service=MagicMock(),
        )

        entities = await service.discover_entities()

        assert "c9_entity" in entities
        MockMSHandler.assert_called_once()


@pytest.mark.asyncio
async def test_discover_entities_routes_cs_to_ms_handler(
    mock_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_camera_service: AsyncMock,
    mock_control_service: MagicMock,
):
    """Test that CS (Catalyst Switch) devices are routed to MSHandler."""
    cs_device = MOCK_DEVICE.copy()
    cs_device["serial"] = "cs_serial"
    cs_device["model"] = "CS220-8P"  # Catalyst Switch
    mock_coordinator.data = {
        "devices": [cs_device],
        "networks": [],
        "ssids": [],
    }

    mock_ms_handler_instance = MagicMock()
    mock_ms_handler_instance.discover_entities = AsyncMock(return_value=["cs_entity"])

    MockMSHandler = MagicMock(return_value=mock_ms_handler_instance)
    MockMSHandler.__name__ = "MSHandler"

    with (
        patch.dict(
            "custom_components.meraki_ha.discovery.service.HANDLER_MAPPING",
            {"CS": MockMSHandler},
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
            coordinator=mock_coordinator,
            config_entry=mock_config_entry,
            meraki_client=MagicMock(),
            camera_service=mock_camera_service,
            control_service=mock_control_service,
            network_control_service=MagicMock(),
        )

        entities = await service.discover_entities()

        assert "cs_entity" in entities
        MockMSHandler.assert_called_once()


@pytest.mark.asyncio
async def test_discover_entities_routes_mg_to_mg_handler(
    mock_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_camera_service: AsyncMock,
    mock_control_service: MagicMock,
):
    """Test that MG (Cellular Gateway) devices are routed to MGHandler."""
    mg_device = MOCK_DEVICE.copy()
    mg_device["serial"] = "mg_serial"
    mg_device["model"] = "MG21"  # Cellular Gateway
    mg_device["productType"] = "cellularGateway"
    mock_coordinator.data = {
        "devices": [mg_device],
        "networks": [],
        "ssids": [],
    }

    mock_mg_handler_instance = MagicMock()
    mock_mg_handler_instance.discover_entities = AsyncMock(return_value=["mg_entity"])

    MockMGHandler = MagicMock(return_value=mock_mg_handler_instance)
    MockMGHandler.__name__ = "MGHandler"

    with (
        patch.dict(
            "custom_components.meraki_ha.discovery.service.HANDLER_MAPPING",
            {"MG": MockMGHandler},
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
            coordinator=mock_coordinator,
            config_entry=mock_config_entry,
            meraki_client=MagicMock(),
            camera_service=mock_camera_service,
            control_service=mock_control_service,
            network_control_service=MagicMock(),
        )

        entities = await service.discover_entities()

        assert "mg_entity" in entities
        MockMGHandler.assert_called_once()
