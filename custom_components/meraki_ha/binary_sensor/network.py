"""Binary sensor for Meraki network status."""

from __future__ import annotations

import asyncio

from custom_components.meraki_ha.const.integration import DOMAIN
from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from ..coordinators import MerakiMainCoordinator
from ..core.models.network import MerakiNetwork
from ..core.utils.naming_utils import standardize_device_name
from ..helpers.device_info_helpers import resolve_device_info


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Meraki network status binary sensor entities."""
    coordinator: MerakiMainCoordinator = hass.data[DOMAIN][config_entry.entry_id][
        "main_coordinator"
    ]

    networks = coordinator.data.get("networks")
    if asyncio.iscoroutine(networks):
        networks = await networks

    if networks:
        async_add_entities(
            [MerakiNetworkStatus(coordinator, network) for network in networks]
        )


class MerakiNetworkStatus(BinarySensorEntity):
    """Representation of a Meraki network status sensor."""

    _attr_device_class = BinarySensorDeviceClass.CONNECTIVITY
    _attr_has_entity_name = False

    def __init__(
        self,
        coordinator: MerakiMainCoordinator,
        network: MerakiNetwork,
    ) -> None:
        """Initialize the sensor."""
        self._coordinator = coordinator
        self._network = network

        # Ensure network ID is available
        network_id = network.id or "unknown_network"
        self._attr_unique_id = f"meraki-network-{network_id}-status"
        self._attr_name = f"{network.name} Uplink Status"

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        # Ensure network ID is available
        network_id = self._network.id or "unknown_network"

        if info := resolve_device_info(
            self._network.to_dict(), self._coordinator.config_entry
        ):
            return info

        return DeviceInfo(
            identifiers={(DOMAIN, network_id)},
            name=standardize_device_name(self._network.name),
        )

    @property
    def is_on(self) -> bool:
        """Return true if the binary sensor is on."""
        return True
