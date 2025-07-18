# custom_components/meraki_ha/switch/meraki_ssid_device_switch.py
"""Switch entities for controlling Meraki SSID devices."""

import logging
from typing import Any, Dict # Optional removed

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, DATA_CLIENT
from ..api.meraki_api import MerakiAPIClient
from .coordinators.ssid_device_coordinator import SSIDDeviceCoordinator

_LOGGER = logging.getLogger(__name__)


from homeassistant.helpers.entity import EntityCategory


class MerakiSSIDBaseSwitch(CoordinatorEntity[SSIDDeviceCoordinator], SwitchEntity):
    """Base class for Meraki SSID Switches."""

    entity_category = EntityCategory.CONFIG

    def __init__(
        self,
        coordinator: SSIDDeviceCoordinator,
        meraki_client: MerakiAPIClient,
        config_entry: ConfigEntry,
        ssid_unique_id: str,
        ssid_data: Dict[str, Any],
        switch_type: str,  # "enabled" or "broadcast"
        attribute_to_check: str,  # "enabled" or "visible"
    ) -> None:
        """Initialize the base SSID switch."""
        super().__init__(coordinator)
        self._meraki_client = meraki_client
        self._config_entry = config_entry
        self._ssid_unique_id = (
            ssid_unique_id  # This is the HA device unique ID for the SSID "device".
        )
        self._ssid_data_at_init = ssid_data  # Store initial SSID data, though state is derived from coordinator.

        # Network ID and SSID number are crucial for API calls to update the SSID.
        self._network_id = ssid_data.get("networkId")
        self._ssid_number = ssid_data.get("number")

        # Unique ID for this specific switch entity (e.g., "networkId_ssidNum_enabled_switch").
        self._attr_unique_id = f"{self._ssid_unique_id}_{switch_type}_switch"
        # self._attr_has_entity_name = True # Set to True if you want HA to prepend the device name automatically.
        # If False (or not set), self._attr_name is used as is.

        # Construct a descriptive entity name, e.g., "Guest WiFi Enabled Control".
        # It uses the SSID name from the coordinator (or a fallback) and the type of switch.
        base_name = self.coordinator.data.get(self._ssid_unique_id, {}).get(
            "name", f"SSID {self._ssid_number}"
        )
        self._attr_name = f"{base_name} {switch_type.capitalize()} Control"

        # This attribute determines which key in the SSID data dict corresponds to this switch's state.
        # For MerakiSSIDEnabledSwitch, it's "enabled". For MerakiSSIDBroadcastSwitch, it's "visible".
        self._attribute_to_check = attribute_to_check
        self._update_internal_state()

    @property
    def device_info(self) -> Dict[str, Any]:
        """Return device information to link this entity to the SSID device."""
        return {
            "identifiers": {(DOMAIN, self._ssid_unique_id)},
        }

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        # First, check coordinator readiness (includes self.coordinator.data is not None)
        if not super().available:
            return False
        # Then, check if this specific SSID's data key exists in the coordinator's data
        # self.coordinator.data is Dict[unique_ssid_id, ssid_data_dict]
        return self._ssid_unique_id in self.coordinator.data

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_internal_state()
        self.async_write_ha_state()

    def _update_internal_state(self) -> None:
        """Update the internal state of the switch based on coordinator data."""
        current_ssid_data = self.coordinator.data.get(self._ssid_unique_id)
        if current_ssid_data:
            self._attr_is_on = current_ssid_data.get(self._attribute_to_check, False)
            # Update name if SSID name changed
            base_name = current_ssid_data.get("name", f"SSID {self._ssid_number}")
            self._attr_name = (
                f"{base_name} {self._attribute_to_check.capitalize()} Control"
            )
        else:
            # Data for this SSID not found in coordinator, assume off or unavailable
            self._attr_is_on = False
            _LOGGER.warning(
                f"Could not find data for SSID {self._ssid_unique_id} in coordinator, switch state set to False"
            )

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
        # _LOGGER.debug(
        #     f"Updating SSID {self._network_id}/{self._ssid_number}: {payload}"
        # ) # Removed

        try:
            # Make the API call to update the specific SSID setting.
            await self._meraki_client.wireless.updateNetworkWirelessSsid(
                networkId=self._network_id,
                number=self._ssid_number,  # Meraki API expects SSID number as string or int depending on SDK version/method.
                # The SDK handles type consistency here.
                **payload,  # Pass the specific setting to update (e.g., enabled=True).
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
        coordinator: SSIDDeviceCoordinator,
        meraki_client: MerakiAPIClient,
        config_entry: ConfigEntry,
        ssid_unique_id: str,
        ssid_data: Dict[str, Any],
    ) -> None:
        """Initialize the SSID Enabled switch."""
        super().__init__(
            coordinator,
            meraki_client,
            config_entry,
            ssid_unique_id,
            ssid_data,
            "enabled",
            "enabled",
        )


class MerakiSSIDBroadcastSwitch(MerakiSSIDBaseSwitch):
    """Switch to control the broadcast (visible/hidden) state of a Meraki SSID."""

    def __init__(
        self,
        coordinator: SSIDDeviceCoordinator,
        meraki_client: MerakiAPIClient,
        config_entry: ConfigEntry,
        ssid_unique_id: str,
        ssid_data: Dict[str, Any],
    ) -> None:
        """Initialize the SSID Broadcast switch."""
        super().__init__(
            coordinator,
            meraki_client,
            config_entry,
            ssid_unique_id,
            ssid_data,
            "broadcast",
            "visible",
        )
