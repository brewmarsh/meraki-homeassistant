# custom_components/meraki_ha/switch/meraki_ssid_device_switch.py
"""Switch entities for controlling Meraki SSID devices."""

import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import EntityCategory
from ..coordinator import MerakiDataUpdateCoordinator
from ..entity import MerakiEntity
from ..core.api.client import MerakiAPIClient
from ..core.utils.icon_utils import get_device_type_icon
from ..helpers.device_info_helpers import resolve_device_info

_LOGGER = logging.getLogger(__name__)


class MerakiSSIDBaseSwitch(MerakiEntity, SwitchEntity):
    """Base class for Meraki SSID Switches."""

    entity_category = EntityCategory.CONFIG

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        meraki_client: MerakiAPIClient,
        config_entry: ConfigEntry,
        ssid_data: dict[str, Any],
        switch_type: str,  # "enabled" or "broadcast"
        attribute_to_check: str,  # "enabled" or "visible"
    ) -> None:
        """Initialize the base SSID switch."""
        super().__init__(coordinator)
        self._meraki_client = meraki_client
        self._config_entry = config_entry
        self._ssid_data_at_init = ssid_data

        self._network_id = ssid_data.get("networkId")
        self._ssid_number = ssid_data.get("number")
        self._attribute_to_check = attribute_to_check
        self._switch_type = switch_type

        # The unique ID is now handled by the dynamic @property below
        self._attr_has_entity_name = True
        self._attr_optimistic = True
        self._attr_is_on = False

        self._update_internal_state()

    def _get_current_ssid_data(self) -> dict[str, Any] | None:
        """Retrieve the latest data for this SSID from the coordinator."""
        if not self.coordinator.data or "ssids" not in self.coordinator.data:
            return None
        for ssid in self.coordinator.data["ssids"]:
            if ssid.get("networkId") == self._network_id and str(
                ssid.get("number")
            ) == str(self._ssid_number):
                return ssid
        return None

    @property
    def unique_id(self) -> str | None:
        """Return a unique ID that prevents platform collisions.
        
        By combining the network ID, SSID number, and the lowercased class name,
        we ensure that the registry stays unique for different switch types.
        """
        return (
            f"{self._network_id}ssid{self._ssid_number}_"
            f"{self.__class__.__name__.lower()}"
        )

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return device information to link this entity to the SSID device."""
        return resolve_device_info(
            entity_data={"networkId": self._network_id, "number": self._ssid_number},
            config_entry=self._config_entry,
            ssid_data=self._ssid_data_at_init,
        )

    @property
    def icon(self) -> str:
        """Return the icon of the entity."""
        return get_device_type_icon("ssid")

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        if not super().available or not self.coordinator.data:
            return False
        ssid_data = self._get_current_ssid_data()
        return ssid_data is not None and ssid_data.get("enabled", False)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_internal_state()
        self.async_write_ha_state()

    def _update_internal_state(self) -> None:
        """Update the internal state of the switch based on coordinator data."""
        if self.unique_id and self.coordinator.is_pending(self.unique_id):
            return

        current_ssid_data = self._get_current_ssid_data()
        if not current_ssid_data:
            self._attr_is_on = False
            return

        self._attr_is_on = current_ssid_data.get(self._attribute_to_check, False)

    async def _update_ssid_setting(self, value: bool) -> None:
        """Update the specific SSID setting (enabled or visible) via API."""
        if not self._network_id or self._ssid_number is None:
            _LOGGER.error("Cannot update SSID: Missing networkId or SSID number.")
            return

        # Optimistically update the UI
        self._attr_is_on = value
        self.async_write_ha_state()

        payload = {self._attribute_to_check: value}

        self.hass.async_create_task(
            self._meraki_client.wireless.update_network_wireless_ssid(
                network_id=self._network_id,
                number=self._ssid_number,
                **payload,
            )
        )

        if self.unique_id:
            self.coordinator.register_pending_update(self.unique_id)

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        await self._update_ssid_setting(True)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        await self._update_ssid_setting(False)


class MerakiSSIDEnabledSwitch(MerakiSSIDBaseSwitch):
    """Switch to control the enabled/disabled state of a Meraki SSID."""

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        meraki_client: MerakiAPIClient,
        config_entry: ConfigEntry,
        ssid_data: dict[str, Any],
    ) -> None:
        """Initialize the SSID Enabled switch."""
        super().__init__(
            coordinator,
            meraki_client,
            config_entry,
            ssid_data,
            "enabled",
            "enabled",
        )
        self._attr_name = "Enabled Control"

    @property
    def available(self) -> bool:
        """Return True even when disabled so you can toggle it back on."""
        if not self.coordinator.last_update_success or not self.coordinator.data:
            return False
        return self._get_current_ssid_data() is not None


class MerakiSSIDBroadcastSwitch(MerakiSSIDBaseSwitch):
    """Switch to control the broadcast (visible/hidden) state of a Meraki SSID."""

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        meraki_client: MerakiAPIClient,
        config_entry: ConfigEntry,
        ssid_data: dict[str, Any],
    ) -> None:
        """Initialize the SSID Broadcast switch."""
        super().__init__(
            coordinator,
            meraki_client,
            config_entry,
            ssid_data,
            "broadcast",
            "visible",
        )
        self._attr_name = "Broadcast Control"