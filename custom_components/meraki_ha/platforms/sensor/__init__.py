"""Support for Meraki sensor platforms."""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from ...core.utils import (
    DEVICE_TYPE_WIRELESS,
    DEVICE_TYPE_APPLIANCE,
    DEVICE_TYPE_CAMERA,
)
from ...coordinators import MerakiDataUpdateCoordinator
from ...const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up sensors based on a config entry."""
    coordinator: MerakiDataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    # List to collect all entities
    entities = []

    # Process devices
    if coordinator.data and "devices" in coordinator.data:
        for device_data in coordinator.data["devices"]:
            product_type = device_data.get("productType")
            if not product_type:
                _LOGGER.warning(
                    "Device %s has no productType, skipping sensor creation",
                    device_data.get("name", device_data.get("serial", "Unknown")),
                )
                continue

            # Add device-specific sensors based on product type
            if product_type == DEVICE_TYPE_WIRELESS:
                from .device.connected_clients import MerakiConnectedClientsSensor
                from .device.radio_settings import MerakiRadioSettingsSensor

                entities.extend(
                    [
                        MerakiConnectedClientsSensor(coordinator, device_data),
                        MerakiRadioSettingsSensor(coordinator, device_data),
                    ]
                )

            elif product_type == DEVICE_TYPE_APPLIANCE:
                from .device.uplink_status import MerakiUplinkStatusSensor

                entities.append(MerakiUplinkStatusSensor(coordinator, device_data))

            elif product_type == DEVICE_TYPE_CAMERA:
                from .device.camera_settings import MerakiCameraSettingsSensor

                entities.append(MerakiCameraSettingsSensor(coordinator, device_data))

    # Process networks
    if coordinator.data and "networks" in coordinator.data:
        from .network.meraki_network_info import MerakiNetworkInfoSensor
        from .network.network_clients import MerakiNetworkClientsSensor

        for network_data in coordinator.data["networks"]:
            entities.extend(
                [
                    MerakiNetworkInfoSensor(coordinator, network_data),
                    MerakiNetworkClientsSensor(coordinator, network_data),
                ]
            )

    # Process organization-level sensors
    if coordinator.data:
        from .org.org_clients import MerakiOrgClientsSensor
        from .org.org_device_type_clients import MerakiOrgDeviceTypeClientsSensor

        entities.extend(
            [
                MerakiOrgClientsSensor(coordinator),
                MerakiOrgDeviceTypeClientsSensor(coordinator),
            ]
        )

    if entities:
        async_add_entities(entities)
