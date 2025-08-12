"""Base entity class for Meraki Home Assistant integration."""

import logging
from typing import Any, Dict, Optional

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .core.coordinators.device import MerakiDeviceCoordinator
from .core.utils.icon_utils import get_device_type_icon
from .helpers.device_info_helpers import resolve_device_info

_LOGGER = logging.getLogger(__name__)


class MerakiEntity(CoordinatorEntity[MerakiDeviceCoordinator]):
    """Base class for Meraki entities."""

    _attr_has_entity_name = True
    entity_category = None

    def __init__(
        self,
        coordinator: MerakiDeviceCoordinator,
        device_data: Dict[str, Any],
        ssid_data: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialize the Meraki base entity."""
        super().__init__(coordinator)
        self._device_info_data = device_data
        self._ssid_info_data = ssid_data

        self._device_serial: Optional[str] = self._device_info_data.get("serial")
        self._device_name: Optional[str] = self._device_info_data.get(
            "name"
        ) or self._device_serial

    @property
    def device_info(self) -> Optional[DeviceInfo]:
        """Return device information for linking this entity to the registry."""
        return resolve_device_info(
            entity_data=self._device_info_data,
            config_entry=self.coordinator.config_entry,
            ssid_data=self._ssid_info_data,
        )

    @property
    def icon(self) -> Optional[str]:
        """Return the icon of the entity."""
        device_type = self._device_info_data.get("productType")
        if device_type:
            return get_device_type_icon(device_type)
        return None

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        if not self.coordinator.last_update_success:
            return False

        # A more robust availability check could be implemented in subclasses
        # by checking for specific keys in the coordinator data.
        # For a base class, we rely on the coordinator's success state.
        return True
