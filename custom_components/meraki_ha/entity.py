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
        """Return if entity is available via O(1) dictionary lookup."""
        if not isinstance(self.coordinator.data, dict):
            return False

        identifier = self._get_identifier()
        if not identifier:
            return self.coordinator.last_update_success

        data = self.coordinator.data.get(identifier)
        if not data:
            return False

        # Status-based availability for devices
        if hasattr(data, "status"):
            return data.status in ["online", "alerting"]

        return True

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the centralized coordinator."""
        if not isinstance(self.coordinator.data, dict):
            self._attr_available = False
            _LOGGER.debug("Coordinator data for %s is not a dictionary", self.entity_id)
        else:
            identifier = self._get_identifier()
            # O(1) Lookup: Directly fetch data by serial/ID instead of iterating lists
            data = self.coordinator.data.get(identifier) if identifier else None

            if identifier and data:
                # Device status check for availability
                if hasattr(data, "status"):
                    self._attr_available = data.status in ["online", "alerting"]
                else:
                    self._attr_available = True
                
                if self._attr_available:
                    # Update local device reference if applicable
                    if hasattr(self, "_device") and hasattr(data, "serial"):
                        self._device = data

                    # Proactively call the specific update method for the platform
                    if hasattr(self, "_update_state_from_data"):
                        self._update_state_from_data(data)
                    elif hasattr(self, "_update_sensor_data"):
                        self._update_sensor_data()
                    elif hasattr(self, "_update_native_value"):
                        self._update_native_value()
            else:
                # If identifier exists but data is missing from payload, mark unavailable
                if identifier:
                    self._attr_available = False
                    _LOGGER.debug(
                        "Entity %s could not find %s in coordinator data. Available keys: %s",
                        self.entity_id,
                        identifier,
                        list(self.coordinator.data.keys()),
                    )
                else:
                    self._attr_available = self.coordinator.last_update_success

        self.async_write_ha_state()

    @property
    def unique_id(self) -> str | None:
        """Return a dynamic unique ID to prevent platform collisions."""
        if manual_id := getattr(self, "_attr_unique_id", None):
            return manual_id

        serial = None

        if hasattr(self, "_device") and hasattr(self._device, "serial"):
            serial = self._device.serial
        elif hasattr(self, "_device_data") and hasattr(self._device_data, "serial"):
            serial = self._device_data.serial
        elif hasattr(self, "_device_serial"):
            serial = self._device_serial
        elif hasattr(self, "_serial"):
            serial = self._serial
        elif hasattr(self, "_network_id") and hasattr(self, "_ssid_number"):
            serial = f"{self._network_id}ssid{self._ssid_number}"

        if serial:
            if (
                hasattr(self, "entity_description")
                and self.entity_description
                and self.entity_description.key
            ):
                return f"{serial}_{self.entity_description.key}"

            return f"{serial}_{self.__class__.__name__.lower()}"

        return None


class MerakiSensor(MerakiEntity[T], SensorEntity, Generic[T]):
    """Base Meraki sensor entity."""


class MerakiBinarySensor(MerakiEntity[T], BinarySensorEntity, Generic[T]):
    """Base Meraki binary sensor entity."""