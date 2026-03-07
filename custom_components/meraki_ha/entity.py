"""Base entity for all Meraki entities."""

from __future__ import annotations

from typing import TYPE_CHECKING, Generic, TypeVar

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

if TYPE_CHECKING:
    from .coordinators.base import MerakiBaseCoordinator

T = TypeVar("T", bound="MerakiBaseCoordinator")


class MerakiEntity(CoordinatorEntity[T], Generic[T]):
    """Base Meraki entity."""

    _attr_has_entity_name = True

    @property
    def available(self) -> bool:
        """Return if entity is available.

        An entity is available if its coordinator has data. We allow availability
        if data is present (even if seeded) to prevent 'unavailable' states during
        initial background synchronization of specialized coordinators.
        """
        if not self.coordinator.last_update_success and not self.coordinator.data:
            return False

        # 1. Check specialized device map for O(1) availability
        serial = None
        if hasattr(self, "_device_serial"):
            serial = self._device_serial
        elif hasattr(self, "_serial"):
            serial = self._serial
        elif hasattr(self, "_device"):
            serial = getattr(self._device, "serial", None)
        elif hasattr(self, "_device_data"):
            serial = getattr(self._device_data, "serial", None)

        if serial:
            if self.coordinator.devices_by_serial:
                return serial in self.coordinator.devices_by_serial
            return bool(self.coordinator.data)

        # 2. Check specialized network map
        network_id = getattr(self, "_network_id", None)
        ssid_number = getattr(self, "_ssid_number", None)

        if network_id and ssid_number is not None:
            # 3. Check specialized SSID map
            if self.coordinator.ssids_by_network_and_number:
                try:
                    ssid_key = (network_id, int(ssid_number))
                    return ssid_key in self.coordinator.ssids_by_network_and_number
                except (TypeError, ValueError):
                    pass
            return bool(self.coordinator.data)

        if network_id:
            if self.coordinator.networks_by_id:
                return network_id in self.coordinator.networks_by_id
            return bool(self.coordinator.data)

        # Fallback to general data presence for entities without specific identifiers
        return bool(self.coordinator.data)

    @property
    def unique_id(self) -> str | None:
        """Return a dynamic unique ID to prevent platform collisions.

        This logic attempts to find a serial number or network/SSID identifier
        across various internal naming schemes used in the integration.
        """
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
            # (e.g., 'serial_voltage')
            if (
                hasattr(self, "entity_description")
                and self.entity_description
                and self.entity_description.key
            ):
                return f"{serial}_{self.entity_description.key}"

            # Fallback to class name for non-described entities
            # (e.g., 'serial_merakirtspstreamcamera')
            return f"{serial}_{self.__class__.__name__.lower()}"

        # Final fallback to manually assigned _attr_unique_id
        return getattr(self, "_attr_unique_id", None)


class MerakiSensor(MerakiEntity[T], SensorEntity, Generic[T]):
    """Base Meraki sensor entity."""


class MerakiBinarySensor(MerakiEntity[T], BinarySensorEntity, Generic[T]):
    """Base Meraki binary sensor entity."""