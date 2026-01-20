"""Base classes for Meraki camera switch entities."""

import dataclasses
import logging
from dataclasses import asdict
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from custom_components.meraki_ha.coordinator import MerakiDataUpdateCoordinator

from ..core.api.client import MerakiAPIClient
<<<<<<< HEAD
from ..types import MerakiDevice
=======
from ..meraki_data_coordinator import MerakiDataCoordinator
>>>>>>> 651bc8a (Refactor MerakiDevice to Dataclass)

_LOGGER = logging.getLogger(__name__)


class MerakiCameraSettingSwitchBase(
    CoordinatorEntity,
    SwitchEntity,
):
    """Base class for a Meraki Camera Setting Switch."""

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        meraki_client: MerakiAPIClient,
        device_data: dict[str, Any] | Any,
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
        serial = (
            device_data.serial
            if hasattr(device_data, "serial")
            else device_data["serial"]
        )
        self._attr_unique_id = f"{serial}_{self._key}"
        self._attr_is_on = False
        self._update_state()  # Set initial state

    def _get_value_from_device(self, device: dict[str, Any] | None) -> bool:
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
            elif dataclasses.is_dataclass(value) and hasattr(value, key):
                value = getattr(value, key)
            else:
                return False
        return bool(value)

    def _update_state(self) -> None:
        """Update the internal state of the switch."""
        serial = (
            self._device_data.serial
            if hasattr(self._device_data, "serial")
            else self._device_data["serial"]
        )
        device = self.coordinator.get_device(serial)
        if device is not None:
            self._device_data = asdict(device)
            self._attr_is_on = self._get_value_from_device(self._device_data)
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
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        serial = (
            self._device_data.serial
            if hasattr(self._device_data, "serial")
            else self._device_data["serial"]
        )
        name = (
            self._device_data.name
            if hasattr(self._device_data, "name")
            else self._device_data["name"]
        )
        model = (
            self._device_data.model
            if hasattr(self._device_data, "model")
            else self._device_data.get("model")
        )
        return DeviceInfo(
            identifiers={("meraki_ha", serial)},
            name=name,
            manufacturer="Cisco Meraki",
            model=model,
        )
