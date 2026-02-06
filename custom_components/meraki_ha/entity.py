"""Base entity for all Meraki entities."""

from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .coordinator import MerakiDataUpdateCoordinator


class MerakiEntity(CoordinatorEntity):
    """Base Meraki entity."""

    coordinator: MerakiDataUpdateCoordinator

    _attr_has_entity_name = True

    @property
    def unique_id(self) -> str | None:
        """Return a unique ID."""
        # Standard format: f"{serial}{class_name_lower}"
        serial = None
        if hasattr(self, "_device") and hasattr(self._device, "serial"):
            serial = self._device.serial
        elif hasattr(self, "_device_data") and hasattr(self._device_data, "serial"):
            serial = self._device_data.serial
        elif hasattr(self, "_device_serial"):
            serial = self._device_serial
        elif hasattr(self, "_serial"):
            serial = self._serial

        if serial:
            return f"{serial}{self.__class__.__name__.lower()}"

        return getattr(self, "_attr_unique_id", None)
