# custom_components/meraki_ha/switch/meraki_ssid_device_switch.py
"""Switch entities for controlling Meraki SSID devices."""

import logging
from typing import Any, Dict, Optional

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ..const import DOMAIN, DATA_CLIENT
from ..meraki_api import MerakiAPIClient
from ..coordinators.ssid_device_coordinator import SSIDDeviceCoordinator

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Meraki SSID switches from a config entry."""
    ssid_coordinator: SSIDDeviceCoordinator = hass.data[DOMAIN][config_entry.entry_id]["coordinators"]["ssid_devices"]
    meraki_client: MerakiAPIClient = hass.data[DOMAIN][config_entry.entry_id][DATA_CLIENT]

    if not ssid_coordinator.data:
        _LOGGER.warning("SSID Coordinator has no data, skipping switch setup")
        return

    switches_to_add = []
    for ssid_unique_id, ssid_data in ssid_coordinator.data.items():
        switches_to_add.append(MerakiSSIDEnabledSwitch(ssid_coordinator, meraki_client, config_entry, ssid_unique_id, ssid_data))
        switches_to_add.append(MerakiSSIDBroadcastSwitch(ssid_coordinator, meraki_client, config_entry, ssid_unique_id, ssid_data))

    async_add_entities(switches_to_add, update_before_add=True)


class MerakiSSIDBaseSwitch(CoordinatorEntity[SSIDDeviceCoordinator], SwitchEntity):
    """Base class for Meraki SSID Switches."""

    def __init__(
        self,
        coordinator: SSIDDeviceCoordinator,
        meraki_client: MerakiAPIClient,
        config_entry: ConfigEntry,
        ssid_unique_id: str,
        ssid_data: Dict[str, Any],
        switch_type: str, # "enabled" or "broadcast"
        attribute_to_check: str # "enabled" or "visible"
    ) -> None:
        """Initialize the base SSID switch."""
        super().__init__(coordinator)
        self._meraki_client = meraki_client
        self._config_entry = config_entry
        self._ssid_unique_id = ssid_unique_id # This is the HA device unique ID
        self._ssid_data_at_init = ssid_data # Initial data, will update via coordinator

        self._network_id = ssid_data.get("networkId")
        self._ssid_number = ssid_data.get("number")

        self._attr_unique_id = f"{self._ssid_unique_id}_{switch_type}_switch"
        # self._attr_has_entity_name = True # Use if HA should generate name from device + entity key

        # Construct entity name, e.g., "Office SSID Enabled", "Guest SSID Broadcast"
        # The parent device (SSID device) name will be like "Office (SSID)"
        # So entity name becomes: "Office (SSID) Enabled Control"
        base_name = self.coordinator.data.get(self._ssid_unique_id, {}).get("name", f"SSID {self._ssid_number}")
        self._attr_name = f"{base_name} {switch_type.capitalize()} Control"

        self._attribute_to_check = attribute_to_check # 'enabled' or 'visible'
        self._update_internal_state()

    @property
    def device_info(self) -> Dict[str, Any]:
        """Return device information to link this entity to the SSID device."""
        return {
            "identifiers": {(DOMAIN, self._ssid_unique_id)},
        }

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
            self._attr_name = f"{base_name} {self._attribute_to_check.capitalize()} Control"
        else:
            # Data for this SSID not found in coordinator, assume off or unavailable
            self._attr_is_on = False
            _LOGGER.warning(f"Could not find data for SSID {self._ssid_unique_id} in coordinator, switch state set to False")

    async def _update_ssid_setting(self, value: bool) -> None:
        """Update the specific SSID setting (enabled or visible) via API."""
        if not self._network_id or self._ssid_number is None:
            _LOGGER.error(f"Cannot update SSID {self.name}: Missing networkId or SSID number.")
            return

        payload = {self._attribute_to_check: value}
        _LOGGER.debug(f"Updating SSID {self._network_id}/{self._ssid_number}: {payload}")

        try:
            await self._meraki_client.wireless.updateNetworkWirelessSsid(
                networkId=self._network_id,
                number=self._ssid_number,
                **payload
            )
            # After successful update, request coordinator to refresh data
            # This ensures HA state reflects the actual state from Meraki
            await self.coordinator.async_request_refresh()
        except Exception as e:
            _LOGGER.error(f"Failed to update SSID {self.name} ({self._attribute_to_check} to {value}): {e}")
            # Optionally, force a refresh to revert optimistic update if any,
            # or rely on next scheduled update.
            # For now, we let the coordinator handle the refresh.

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
        super().__init__(coordinator, meraki_client, config_entry, ssid_unique_id, ssid_data, "enabled", "enabled")


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
        super().__init__(coordinator, meraki_client, config_entry, ssid_unique_id, ssid_data, "broadcast", "visible")
