"""Base entity classes for Meraki Home Assistant integration."""

from __future__ import annotations

import logging
from typing import Any, Dict

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...coordinators import MerakiDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


class MerakiEntity(CoordinatorEntity[MerakiDataUpdateCoordinator], Entity):
    """Base class for all Meraki entities."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        name: str,
        unique_id: str,
        device_info: DeviceInfo,
    ) -> None:
        """Initialize the base entity.

        Args:
            coordinator: The data update coordinator.
            name: The name of the entity.
            unique_id: Unique identifier for the entity.
            device_info: Device registry information.
        """
        super().__init__(coordinator)
        self._attr_name = name
        self._attr_unique_id = unique_id
        self._attr_device_info = device_info
        self._attr_extra_state_attributes: Dict[str, Any] = {}
