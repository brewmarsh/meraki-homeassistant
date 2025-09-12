# custom_components/meraki_ha/switch/meraki_ssid_device_switch.py
"""Switch entities for controlling Meraki SSID devices."""

import logging
from typing import Any, Dict, Optional

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.device_registry import DeviceInfo

from ..core.api.client import MerakiAPIClient
from ..core.coordinators.meraki_data_coordinator import MerakiDataCoordinator
from ..core.utils.icon_utils import get_device_type_icon
from homeassistant.helpers.entity import EntityCategory
from ..helpers.device_info_helpers import resolve_device_info

_LOGGER = logging.getLogger(__name__)


class MerakiSSIDBaseSwitch(CoordinatorEntity[MerakiDataCoordinator], SwitchEntity):
    """Base class for Meraki SSID Switches."""

    entity_category = EntityCategory.CONFIG
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        meraki_client: MerakiAPIClient,
        config_entry: ConfigEntry,
        ssid_data: Dict[str, Any],
        switch_type: str,  # "enabled" or "broadcast"
        attribute_to_check: str,  # "enabled" or "visible"
    ) -> None:
        """Initialize the base SSID switch."""
        super().__init__(coordinator)
        self._meraki_client = meraki_client
        self._config_entry = config_entry
        self._ssid_data_at_init = ssid_data  # Store initial SSID data for device info

        self._network_id = ssid_data.get("networkId")
        self._ssid_number = ssid_data.get("number")
        self._attribute_to_check = attribute_to_check

        self._attr_unique_id = (
            f"ssid-{self._network_id}-{self._ssid_number}-{switch_type}-switch"
        )
        self._attr_name = f"{switch_type.capitalize()} Control"

        self._update_internal_state()

    def _get_current_ssid_data(self) -> Optional[Dict[str, Any]]:
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
    def device_info(self) -> DeviceInfo:
        """Return device information to link this entity to the SSID device."""
        return resolve_device_info(
            entity_data={"networkId": self._network_id},
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
        current_ssid_data = self._get_current_ssid_data()
        if current_ssid_data:
            self._attr_is_on = current_ssid_data.get(self._attribute_to_check, False)
        else:
            self._attr_is_on = False

    async def _update_ssid_setting(self, value: bool) -> None:
        """Update the specific SSID setting (enabled or visible) via API."""
        if not self._network_id or self._ssid_number is None:
            _LOGGER.error(
                f"Cannot update SSID {self.name}: Missing networkId or SSID number for API call."
            )
            return

        # The payload for the API call uses the `_attribute_to_check` (e.g., 'enabled' or 'visible')
        # as the key, and the new boolean `value` as its value.
        payload = {self._attribute_to_check: value}

        try:
            # Make the API call to update the specific SSID setting.
            await self._meraki_client.wireless.update_network_wireless_ssid(
                network_id=self._network_id,
                number=self._ssid_number,
                **payload,
            )
            # After a successful API call, request the coordinator to refresh its data.
            # This ensures that Home Assistant's state for this switch (and any related entities)
            # is updated to reflect the actual state confirmed by the Meraki dashboard.
            await self.coordinator.async_request_refresh()
        except Exception as e:
            _LOGGER.error(
                f"Failed to update SSID {self.name} ({self._attribute_to_check} to {value}): {e}"
            )
            raise HomeAssistantError(f"Failed to update SSID {self.name}: {e}") from e
            # If the API call fails, an error is logged. The state in HA might become stale
            # until the next successful coordinator refresh. Consider if immediate refresh
            # or error state handling is needed here.
            # For now, we rely on the coordinator's next scheduled refresh or manual refresh
            # to eventually reflect the true state or clear the error.

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
        coordinator: MerakiDataCoordinator,
        meraki_client: MerakiAPIClient,
        config_entry: ConfigEntry,
        ssid_data: Dict[str, Any],
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


class MerakiSSIDBroadcastSwitch(MerakiSSIDBaseSwitch):
    """Switch to control the broadcast (visible/hidden) state of a Meraki SSID."""

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        meraki_client: MerakiAPIClient,
        config_entry: ConfigEntry,
        ssid_data: Dict[str, Any],
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
