"""
Button entity for Meraki MT15 refresh data button.
"""
from __future__ import annotations

import logging
from typing import Any, Dict

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.device_registry import DeviceInfo

from ...coordinator import MerakiDataUpdateCoordinator
from ...helpers.device_info_helpers import resolve_device_info
from ...core.api.client import MerakiAPIClient

_LOGGER = logging.getLogger(__name__)


class MerakiMt15RefreshDataButton(
    CoordinatorEntity[MerakiDataUpdateCoordinator], ButtonEntity
):
    """Representation of a Meraki MT15 refresh data button."""

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        device_info: Dict[str, Any],
        config_entry: ConfigEntry,
        meraki_client: MerakiAPIClient,
    ) -> None:
        """Initialize the button."""
        super().__init__(coordinator)
        self._device_info = device_info
        self._config_entry = config_entry
        self._meraki_client = meraki_client
        self._attr_unique_id = f"{self._device_info['serial']}-refresh"
        self._attr_name = f"{self._device_info['name']} Refresh Data"

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return resolve_device_info(self._device_info, self._config_entry)

    async def async_press(self) -> None:
        """Handle the button press."""
        serial = self._device_info["serial"]
        _LOGGER.info("MT15 refresh data button pressed for %s", serial)
        try:
            await self._meraki_client.sensor.create_device_sensor_command(
                serial=serial, operation="refreshData"
            )
            _LOGGER.debug("Successfully triggered refresh for MT15 sensor %s", serial)
        except Exception as e:
            _LOGGER.error("Error refreshing MT15 data for %s: %s", serial, e)

    @property
    def available(self) -> bool:
        """Return if the entity is available."""
        return self._device_info.get("model", "").startswith("MT15") and super().available