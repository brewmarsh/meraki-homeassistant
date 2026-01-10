"""Sensor platform for the Meraki Home Assistant integration.

This platform sets up sensor entities discovered by the DeviceDiscoveryService.
It filters the discovered entities to only include SensorEntity instances.

It also sets up client sensors dynamically based on coordinator data,
providing separate entities for VLAN, SSID, connected device, and data usage.
"""

from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from ..const import CONF_ENABLE_DEVICE_TRACKER, DOMAIN

if TYPE_CHECKING:
    from ..meraki_data_coordinator import MerakiDataCoordinator

# Re-export for backwards compatibility
# Client sensor imports
from .client import (
    MerakiClientConnectedDeviceSensor,
    MerakiClientConnectionTypeSensor,
    MerakiClientReceivedBytesSensor,
    MerakiClientSentBytesSensor,
    MerakiClientSSIDSensor,
    MerakiClientSwitchportSensor,
    MerakiClientVLANSensor,
)
from .device.appliance_port import MerakiAppliancePortSensor
from .device.rtsp_url import MerakiRtspUrlSensor as MerakiCameraRTSPUrlSensor
from .network.meraki_network_info import MerakiNetworkInfoSensor
from .network.network_clients import MerakiNetworkClientsSensor
from .network.network_identity import MerakiNetworkIdentitySensor

__all__ = [
    "async_setup_entry",
    "MerakiNetworkClientsSensor",
    "MerakiNetworkIdentitySensor",
    "MerakiNetworkInfoSensor",
    "MerakiAppliancePortSensor",
    "MerakiCameraRTSPUrlSensor",
    # Client sensors
    "MerakiClientVLANSensor",
    "MerakiClientSSIDSensor",
    "MerakiClientConnectedDeviceSensor",
    "MerakiClientConnectionTypeSensor",
    "MerakiClientSwitchportSensor",
    "MerakiClientSentBytesSensor",
    "MerakiClientReceivedBytesSensor",
]


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> bool:
    """Set up Meraki sensor entities from a config entry.

    This uses entities discovered by the DeviceDiscoveryService rather than
    creating them directly, to avoid duplicates.

    It also sets up client sensors dynamically based on coordinator data.
    """
    entry_data = hass.data[DOMAIN][config_entry.entry_id]

    # Get all discovered entities and filter for sensors
    discovered_entities = entry_data.get("entities", [])
    sensor_entities = [e for e in discovered_entities if isinstance(e, SensorEntity)]

    if sensor_entities:
        _LOGGER.debug("Adding %d sensor entities", len(sensor_entities))
        # Add entities in chunks to avoid overwhelming HA
        chunk_size = 50
        for i in range(0, len(sensor_entities), chunk_size):
            chunk = sensor_entities[i : i + chunk_size]
            async_add_entities(chunk)
            if len(sensor_entities) > chunk_size:
                await asyncio.sleep(0.5)
    else:
        _LOGGER.debug("No sensor entities discovered")

    # Set up client sensors if device tracker is enabled and coordinator exists
    if config_entry.options.get(CONF_ENABLE_DEVICE_TRACKER, True):
        if "coordinator" in entry_data:
            await _async_setup_client_sensors(hass, config_entry, async_add_entities)
        else:
            _LOGGER.debug("Coordinator not available, skipping client sensors")

    return True


async def _async_setup_client_sensors(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up client sensor entities dynamically.

    Creates sensor entities for each connected client, providing separate
    entities for VLAN, SSID, connected device, connection type, and data usage.
    These sensors are linked to the same device as the device_tracker entity.
    """
    entry_data = hass.data[DOMAIN][config_entry.entry_id]
    coordinator: MerakiDataCoordinator = entry_data["coordinator"]

    # Track which clients we've already added sensors for
    tracked_clients: set[str] = set()

    @callback
    def async_add_client_sensors() -> None:
        """Add sensor entities for new clients."""
        if not coordinator.data or not coordinator.data.get("clients"):
            return

        # Build a set of Meraki device MACs to filter out
        meraki_device_macs: set[str] = set()
        for device in coordinator.data.get("devices", []):
            device_mac = device.get("mac")
            if device_mac:
                meraki_device_macs.add(device_mac.lower())

        new_entities: list[SensorEntity] = []

        for client_data in coordinator.data["clients"]:
            client_mac = client_data.get("mac")
            if not client_mac:
                continue

            # Skip if this "client" is actually a Meraki device
            if client_mac.lower() in meraki_device_macs:
                continue

            if client_mac not in tracked_clients:
                tracked_clients.add(client_mac)

                # Create all client sensors for this client
                new_entities.extend(
                    _create_client_sensors(
                        hass=hass,
                        coordinator=coordinator,
                        config_entry=config_entry,
                        client_data=client_data,
                    )
                )

        if new_entities:
            _LOGGER.debug("Adding %d new client sensor entities", len(new_entities))
            async_add_entities(new_entities)

    # Add initial client sensors
    async_add_client_sensors()

    # Register listener for future updates to add sensors for new clients
    config_entry.async_on_unload(
        coordinator.async_add_listener(async_add_client_sensors)
    )


def _create_client_sensors(
    hass: HomeAssistant,
    coordinator: MerakiDataCoordinator,
    config_entry: ConfigEntry,
    client_data: dict,
) -> list[SensorEntity]:
    """Create all sensor entities for a single client.

    Parameters
    ----------
    hass : HomeAssistant
        The Home Assistant instance.
    coordinator : MerakiDataCoordinator
        The data update coordinator.
    config_entry : ConfigEntry
        The config entry for this integration.
    client_data : dict
        The client data from the Meraki API.

    Returns
    -------
    list[SensorEntity]
        List of sensor entities for this client.

    """
    return [
        MerakiClientVLANSensor(
            hass=hass,
            coordinator=coordinator,
            config_entry=config_entry,
            client_data=client_data,
        ),
        MerakiClientSSIDSensor(
            hass=hass,
            coordinator=coordinator,
            config_entry=config_entry,
            client_data=client_data,
        ),
        MerakiClientConnectedDeviceSensor(
            hass=hass,
            coordinator=coordinator,
            config_entry=config_entry,
            client_data=client_data,
        ),
        MerakiClientConnectionTypeSensor(
            hass=hass,
            coordinator=coordinator,
            config_entry=config_entry,
            client_data=client_data,
        ),
        MerakiClientSwitchportSensor(
            hass=hass,
            coordinator=coordinator,
            config_entry=config_entry,
            client_data=client_data,
        ),
        MerakiClientSentBytesSensor(
            hass=hass,
            coordinator=coordinator,
            config_entry=config_entry,
            client_data=client_data,
        ),
        MerakiClientReceivedBytesSensor(
            hass=hass,
            coordinator=coordinator,
            config_entry=config_entry,
            client_data=client_data,
        ),
    ]
