"""Base classes for Meraki camera switch entities."""

import logging
from collections.abc import Mapping
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ..const import DOMAIN
from ..core.api.client import MerakiAPIClient
from ..core.utils.naming_utils import format_device_name
from ..meraki_data_coordinator import MerakiDataCoordinator
from ..types import MerakiDevice

_LOGGER = logging.getLogger(__name__)


class MerakiCameraSettingSwitchBase(
    CoordinatorEntity,  # type: ignore[type-arg]
    SwitchEntity,
):
    """Base class for a Meraki Camera Setting Switch."""

    coordinator: MerakiDataCoordinator

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        meraki_client: MerakiAPIClient,
        device_data: Mapping[str, Any],
        key: str,
        api_field: str,
    ) -> None:
        """
        Initialize a camera setting switch.

        Args:
        ----
            coordinator: The data update coordinator.
            meraki_client: The Meraki API client.
            device_data: The device data.
            key: The key for the setting.
            api_field: The API field for the setting.

        """
        super().__init__(coordinator)
        self.client = meraki_client
        self._device_data = device_data
        self._key = key
        self._api_field = api_field
        self._attr_unique_id = f"{self._device_data['serial']}_{self._key}"
        self._attr_is_on = False
        self._update_state()  # Set initial state

    def _get_value_from_device(self, device: MerakiDevice | None) -> bool:
        """
        Drill down into the device dictionary to get the state value.

        Args:
        ----
            device: The device data.

        Returns
        -------
            The state value.

        """
        if device is None:
            return False
        keys = self._api_field.split(".")
        value: Any = device
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
            else:
                return False
        return bool(value)

    def _update_state(self) -> None:
        """Update the internal state of the switch."""
        device = self.coordinator.get_device(self._device_data["serial"])
        if device is not None:
            self._device_data = device
            self._attr_is_on = self._get_value_from_device(device)
        else:
            self._attr_is_on = False

    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_state()
        self.async_write_ha_state()

    @property
    def is_on(self) -> bool | None:
        """Return the current state of the switch."""
        return self._attr_is_on

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        if not self.coordinator.last_update_success:
            return False
        return self.coordinator.get_device(self._device_data["serial"]) is not None

    async def async_turn_on(self, **kwargs: Any) -> None:
        """
        Turn the setting on.

        Args:
        ----
            **kwargs: Additional arguments.

        """
        await self._async_update_setting(True)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """
        Turn the setting off.

        Args:
        ----
            **kwargs: Additional arguments.

        """
        await self._async_update_setting(False)

    async def _async_update_setting(self, is_on: bool) -> None:
        """
        Update the setting via the Meraki API.

        Args:
        ----
            is_on: Whether the setting is on or off.

        """
        raise NotImplementedError

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return device information."""
        if self.coordinator.config_entry is None:
            return None
        return DeviceInfo(
            identifiers={(DOMAIN, self._device_data["serial"])},
            name=format_device_name(
                self._device_data, self.coordinator.config_entry.options
            ),
            manufacturer="Cisco Meraki",
            model=self._device_data.get("model", "Unknown"),
        )
