"""Base entity for all Meraki entities."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Generic, TypeVar

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.components.sensor import SensorEntity
from homeassistant.core import callback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

if TYPE_CHECKING:
    from .coordinators.base import MerakiBaseCoordinator

T = TypeVar("T", bound="MerakiBaseCoordinator")

_LOGGER = logging.getLogger(__name__)


class MerakiEntity(CoordinatorEntity[T], Generic[T]):
    """Base Meraki entity."""

    _attr_has_entity_name = True

    def _get_identifier(self) -> str | None:
        """Extract the identifier (serial or network ID) for this entity."""
        # Extract identifier across various naming schemes
        identifier = getattr(self, "_serial", None) or getattr(
            self, "_device_serial", None
        )
        if not identifier and hasattr(self, "_device"):
            identifier = getattr(self._device, "serial", None)

        if not identifier:
            identifier = getattr(self, "_network_id", None)

        return identifier

    @property
    def available(self) -> bool:
        """Return if entity is available.

        An entity is available if its coordinator has data and the specific
        device or network data exists in the centralized payload.
        """
        if not self.coordinator.data:
            return False

        identifier = self._get_identifier()

        # If no specific identifier is found, fall back to general coordinator success
        if not identifier:
            return self.coordinator.last_update_success

        # Check O(1) maps if they exist on the coordinator
        if hasattr(self.coordinator, "devices_by_serial") and self.coordinator.devices_by_serial:
            if identifier in self.coordinator.devices_by_serial:
                return True

        if hasattr(self.coordinator, "networks_by_id") and self.coordinator.networks_by_id:
            if identifier in self.coordinator.networks_by_id:
                return True

        return identifier in self.coordinator.data

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the centralized coordinator."""
        if not self.coordinator.data:
            self._attr_available = False
        else:
            identifier = self._get_identifier()
            _LOGGER.debug(
                "Entity %s looking for %s in keys: %s",
                self.entity_id,
                identifier,
                list(self.coordinator.data.keys()),
            )

            if identifier and (data := self.coordinator.data.get(identifier)):
                self._attr_available = True
                
                # Proactively call the specific update method for the platform
                if hasattr(self, "_update_state_from_data"):
                    self._update_state_from_data(data)
                elif hasattr(self, "_update_sensor_data"):
                    self._update_sensor_data()
                elif hasattr(self, "_update_native_value"):
                    # For MerakiMtSensor and similar platform implementations
                    if hasattr(self, "_device") and hasattr(data, "serial"):
                        self._device = data
                    self._update_native_value()
            else:
                # If identifier exists but data is missing from payload, mark unavailable
                if identifier:
                    self._attr_available = identifier in self.coordinator.data
                    if not self._attr_available:
                        _LOGGER.debug(
                            "Entity %s could not find %s in coordinator data. Available keys: %s",
                            self.entity_id,
                            identifier,
                            list(self.coordinator.data.keys()),
                        )
                else:
                    self._attr_available = True

        self.async_write_ha_state()

    @property
    def unique_id(self) -> str | None:
        """Return a dynamic unique ID to prevent platform collisions.

        This logic attempts to find a serial number or network/SSID identifier
        across various internal naming schemes used in the integration.
        """
        # Prioritize manually assigned _attr_unique_id
        if manual_id := getattr(self, "_attr_unique_id", None):
            return manual_id

        serial = None

        # 1. Attempt to find a physical device serial
        if hasattr(self, "_device") and hasattr(self._device, "serial"):
            serial = self._device.serial
        elif hasattr(self, "_device_data") and hasattr(self._device_data, "serial"):
            serial = self._device_data.serial
        elif hasattr(self, "_device_serial"):
            serial = self._device_serial
        elif hasattr(self, "_serial"):
            serial = self._serial

        # 2. Fallback to Virtual SSID identifier if physical serial is missing
        elif hasattr(self, "_network_id") and hasattr(self, "_ssid_number"):
            serial = f"{self._network_id}ssid{self._ssid_number}"

        if serial:
            # Prefer using the entity description key for unique granularity
            if (
                hasattr(self, "entity_description")
                and self.entity_description
                and self.entity_description.key
            ):
                return f"{serial}_{self.entity_description.key}"

            # Fallback to class name for non-described entities
            return f"{serial}_{self.__class__.__name__.lower()}"

        return None


class MerakiSensor(MerakiEntity[T], SensorEntity, Generic[T]):
    """Base Meraki sensor entity."""


class MerakiBinarySensor(MerakiEntity[T], BinarySensorEntity, Generic[T]):
    """Base Meraki binary sensor entity."""
