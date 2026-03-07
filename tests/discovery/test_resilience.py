
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from custom_components.meraki_ha.discovery.service import DeviceDiscoveryService
from custom_components.meraki_ha.core.errors import MerakiInformationalError, MerakiHAException
from homeassistant.exceptions import HomeAssistantError

@pytest.mark.asyncio
async def test_discovery_service_resilience(hass):
    """Test that discovery service continues even if one handler fails."""
    # Mock all coordinators
    mock_coordinators = {
        name: MagicMock() for name in [
            "main_coordinator", "device_coordinator", "switch_coordinator",
            "camera_coordinator", "sensor_coordinator", "wireless_coordinator",
            "appliance_coordinator", "client_coordinator"
        ]
    }

    # Setup device_coordinator to return some devices
    mock_device = MagicMock()
    mock_device.serial = "SERIAL1"
    mock_device.model = "MODEL1"
    mock_device.product_type = "wireless"
    mock_coordinators["device_coordinator"].devices_by_serial = {"SERIAL1": mock_device}

    # Mock config entry and other services
    mock_config_entry = MagicMock()
    mock_config_entry.options = {}
    mock_meraki_client = MagicMock()
    mock_camera_service = MagicMock()
    mock_control_service = MagicMock()
    mock_network_control_service = MagicMock()

    service = DeviceDiscoveryService(
        **mock_coordinators,
        config_entry=mock_config_entry,
        meraki_client=mock_meraki_client,
        camera_service=mock_camera_service,
        control_service=mock_control_service,
        network_control_service=mock_network_control_service
    )

    # Patch _discover_network_entities to fail
    with patch.object(service, "_discover_network_entities") as mock_net:
        # Use an async generator that raises an error
        async def async_gen_fail():
            raise MerakiHAException("Network discovery failed")
            yield # Keep it a generator

        mock_net.side_effect = async_gen_fail

        # Patch UniversalHandler to return one entity
        with patch("custom_components.meraki_ha.discovery.service.UniversalHandler") as mock_handler_class:
            mock_handler = MagicMock()
            async def async_gen_entity():
                yield MagicMock()
            mock_handler.discover_entities.side_effect = async_gen_entity
            mock_handler_class.return_value = mock_handler

            entities = await service.discover_entities()

            # Should have entities from device discovery despite network failure
            assert len(entities) > 0
            mock_net.assert_called_once()

@pytest.mark.asyncio
async def test_universal_handler_resilience(hass):
    """Test that UniversalHandler continues even if one capability fails."""
    from custom_components.meraki_ha.discovery.handlers.universal import UniversalHandler

    mock_coordinator = MagicMock()
    mock_device = MagicMock()
    mock_device.serial = "SERIAL1"
    mock_device.model = "MR33"
    mock_device.product_type = "wireless"

    mock_config_entry = MagicMock()
    mock_config_entry.options = {}

    handler = UniversalHandler(
        mock_coordinator,
        mock_device,
        mock_config_entry,
        MagicMock(), MagicMock(), MagicMock()
    )

    # Set capabilities
    handler.capabilities = ["status", "wireless"]

    # Mock _discover_capability to fail for "status" but succeed for "wireless"
    async def mock_discover_cap(cap):
        if cap == "status":
            raise MerakiInformationalError("Status disabled")
        if cap == "wireless":
            yield MagicMock()

    with patch.object(handler, "_discover_capability", side_effect=mock_discover_cap):
        entities = []
        async for entity in handler.discover_entities():
            entities.append(entity)

        assert len(entities) == 1
