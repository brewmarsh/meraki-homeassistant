"""Sensor platform for the Meraki Home Assistant integration.

This platform sets up sensor entities discovered by the DeviceDiscoveryService.
It filters the discovered entities to only include SensorEntity instances.
"""

from __future__ import annotations

import asyncio
import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from ..const import DOMAIN

# Re-export for backwards compatibility
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

    return True
