"""Platform for device tracker integration."""

from __future__ import annotations

import logging
from typing import Any, Dict

from homeassistant.components.device_tracker import (
    SourceType,
    TrackerEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, DATA_COORDINATOR
from .coordinator import MerakiDataUpdateCoordinator  # Corrected import

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the device tracker platform."""
    coordinator: MerakiDataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id][
        DATA_COORDINATOR
    ]
    devices = coordinator.data.get("devices", [])

    entities = []
    for device in devices:
        if device.get("model") is not None:
            entities.append(MerakiDeviceTracker(coordinator, device))
    async_add_entities(entities)


class MerakiDeviceTracker(TrackerEntity):
    """Representation of a Meraki device tracker."""

    def __init__(
        self, coordinator: MerakiDataUpdateCoordinator, device: Dict[str, Any]
    ) -> None:
        """Initialize the Meraki device tracker."""
        self.coordinator = coordinator
        self.device = device
        self._attr_name = f"{device['name']}"
        self._attr_unique_id = f"{device['serial']}_tracker"

    @property
    def is_connected(self) -> bool:
        """Return true if the device is connected."""
        # Implement logic to check if the device is connected
        # Based on the coordinator's data
        clients = self.coordinator.data.get("devices", [])
        for meraki_device in clients:
            if meraki_device.get("serial") == self.device.get("serial"):
                if (
                    meraki_device.get("clients") is not None
                    and len(meraki_device.get("clients")) > 0
                ):
                    return True
        return False

    @property
    def source_type(self) -> SourceType:
        """Return the source type of the device tracker."""
        return SourceType.ROUTER

    @property
    def device_info(self) -> Dict[str, Any]:
        """Return device information about this entity."""
        return {
            "identifiers": {(DOMAIN, self.device["serial"])},
            "name": self.device["name"],
            "manufacturer": "Cisco Meraki",
            "model": self.device["model"],
            "sw_version": self.device.get("firmware"),
        }
