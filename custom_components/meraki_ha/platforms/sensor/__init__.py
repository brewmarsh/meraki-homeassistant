"""Support for Meraki sensor platforms."""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from ...core.utils.device_types import (
    DEVICE_TYPE_WIRELESS,
    DEVICE_TYPE_APPLIANCE,
    DEVICE_TYPE_CAMERA,
)
from ...core.coordinators.device import MerakiDeviceDataUpdateCoordinator
from ...const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up sensors based on a config entry."""
    coordinator: MerakiDeviceDataUpdateCoordinator = hass.data[DOMAIN][
        config_entry.entry_id
    ]

    # List to collect all entities
    entities = []

    # Process devices
    if coordinator.data:
        for device_serial, device_data in coordinator.data.items():
            product_type = device_data.get("productType")
            if not product_type:
                _LOGGER.warning(
                    "Device %s has no productType, skipping sensor creation",
                    device_data.get("name", device_serial),
                )
                continue

            # Add device-specific sensors based on product type
            if product_type == DEVICE_TYPE_WIRELESS:
                from .device.connected_clients import MerakiConnectedClientsSensor
                from .device.radio_settings import MerakiRadioSettingsSensor

                entities.extend(
                    [
                        MerakiConnectedClientsSensor(coordinator, device_serial),
                        MerakiRadioSettingsSensor(coordinator, device_serial),
                    ]
                )

            elif product_type == DEVICE_TYPE_APPLIANCE:
                from .device.uplink_status import MerakiUplinkStatusSensor

                entities.append(MerakiUplinkStatusSensor(coordinator, device_serial))

            elif product_type == DEVICE_TYPE_CAMERA:
                from .device.camera_settings import MerakiCameraSettingsSensor

                entities.append(MerakiCameraSettingsSensor(coordinator, device_serial))

    # Process networks
    if coordinator.data:
        from .network.info import MerakiNetworkInfoSensor

        for network_id, network_data in coordinator.data.items():
            entities.append(MerakiNetworkInfoSensor(coordinator, network_id))

    if entities:
        async_add_entities(entities)
