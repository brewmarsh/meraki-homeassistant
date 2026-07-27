"""Test that switch ports are generated and linked to the parent device."""

from unittest.mock import AsyncMock, patch

import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.meraki_ha.const.config import (
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
)
from custom_components.meraki_ha.types import MerakiDevice
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import entity_registry as er


@pytest.mark.asyncio
async def test_switch_port_generation_and_linkage(
    hass: HomeAssistant,
    mock_meraki_client,
    entity_registry: er.EntityRegistry,
    device_registry: dr.DeviceRegistry,
) -> None:
    """Test that switch ports are generated and linked to the parent device."""
    # Mock entry with ports enabled
    entry = MockConfigEntry(
        domain="meraki_ha",
        data={
            CONF_MERAKI_API_KEY: "test_key",
            CONF_MERAKI_ORG_ID: "test_org",
        },
        options={"enable_port_sensors": True},
        entry_id="test_entry_id",
    )
    entry.add_to_hass(hass)

    # We need to simulate the coordinator returning a switch with ports
    # Create a mock switch device with ports
    switch_device = MerakiDevice.from_dict(
        {
            "serial": "Q2KX-ACU9-ZAVN",
            "name": "Test Switch",
            "mac": "00:11:22:33:44:55",
            "model": "MS120-8",
            "networkId": "N_12345",
            "productType": "switch",
            "lanIp": "1.2.3.4",
            "status": "online",
        }
    )

    # Mock the port statuses for the switch
    switch_device.switch_ports = [
        {
            "portId": "1",
            "name": "Port 1",
            "status": "Connected",
            "enabled": True,
            "powerUsageInWh": 10.0,
        },
        {
            "portId": "2",
            "name": "Port 2",
            "status": "Disconnected",
            "enabled": False,
            "powerUsageInWh": 0.0,
        },
    ]

    mock_all_data = {
        "networks": [],
        "devices": [switch_device],
        "ssids": [],
        "clients": [],
        "l7_firewall_rules": {"rules": []},
    }

    # Patch the _async_update_data of all coordinators to return our mocked switch
    # This ensures that discovery service sees the switch and its ports.
    with (
        patch(
            "custom_components.meraki_ha.coordinators.MerakiDeviceCoordinator._async_update_data",
            new_callable=AsyncMock,
            return_value=mock_all_data,
        ),
        patch(
            "custom_components.meraki_ha.coordinators.MerakiMainCoordinator._async_update_data",
            new_callable=AsyncMock,
            return_value=mock_all_data,
        ),
        patch(
            "custom_components.meraki_ha.coordinators.MerakiSwitchCoordinator._async_update_data",
            new_callable=AsyncMock,
            return_value=mock_all_data,
        ),
        patch(
            "custom_components.meraki_ha.coordinators.MerakiCameraCoordinator._async_update_data",
            new_callable=AsyncMock,
            return_value=mock_all_data,
        ),
        patch(
            "custom_components.meraki_ha.coordinators.MerakiSensorCoordinator._async_update_data",
            new_callable=AsyncMock,
            return_value=mock_all_data,
        ),
        patch(
            "custom_components.meraki_ha.coordinators.MerakiWirelessCoordinator._async_update_data",
            new_callable=AsyncMock,
            return_value=mock_all_data,
        ),
        patch(
            "custom_components.meraki_ha.coordinators.MerakiApplianceCoordinator._async_update_data",
            new_callable=AsyncMock,
            return_value=mock_all_data,
        ),
        patch(
            "custom_components.meraki_ha.coordinators.MerakiClientCoordinator._async_update_data",
            new_callable=AsyncMock,
            return_value=mock_all_data,
        ),
    ):
        # Setup the integration
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    # Get port entities from registry
    port_entities = [
        entity_id for entity_id in entity_registry.entities if "_port_" in entity_id
    ]

    # We should have at least one port entity
    assert len(port_entities) > 0, "No switch port entities were generated"

    # Check that at least the specific status entities are registered
    # Updated to match the naming convention seen in logs
    port_1_status = "sensor.switch_test_switch_port_1_status"
    port_2_status = "sensor.switch_test_switch_port_2_status"

    assert entity_registry.async_is_registered(port_1_status)
    assert entity_registry.async_is_registered(port_2_status)

    for port_entity_id in [port_1_status, port_2_status]:
        registry_entry = entity_registry.async_get(port_entity_id)
        assert registry_entry is not None
        assert (
            registry_entry.device_id is not None
        ), f"Entity {port_entity_id} is orphaned (no device_id)"

        # Verify device actually exists and links properly
        device_entry = device_registry.async_get(registry_entry.device_id)
        assert (
            device_entry is not None
        ), f"Device {registry_entry.device_id} not found in registry"

        # In Meraki_HA, typically the device identifiers includes the domain and serial
        assert ("meraki_ha", "Q2KX-ACU9-ZAVN") in device_entry.identifiers
