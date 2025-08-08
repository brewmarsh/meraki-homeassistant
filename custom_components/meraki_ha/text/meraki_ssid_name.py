"""Text entity for controlling Meraki SSID Name."""

import logging
from typing import Any, Dict, Optional

from homeassistant.components.text import TextEntity, TextMode
from homeassistant.config_entries import (
    ConfigEntry,
)  # Required for type hinting in __init__
from homeassistant.components.text import TextEntityDescription
from homeassistant.exceptions import HomeAssistantError
from homeassistant.core import callback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.device_registry import DeviceInfo


from ..const import DOMAIN
from ..core.api.client import MerakiAPIClient
from ..core.coordinators.meraki_data_coordinator import MerakiDataCoordinator
from homeassistant.helpers.entity import EntityCategory
from ..core.utils.naming_utils import format_device_name

_LOGGER = logging.getLogger(__name__)


class MerakiSSIDNameText(CoordinatorEntity[MerakiDataCoordinator], TextEntity):
    """Representation of a Meraki SSID Name text entity."""

    _attr_mode = TextMode.TEXT  # Or TextMode.PASSWORD if it were a password
    entity_category = EntityCategory.CONFIG
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        meraki_client: MerakiAPIClient,
        config_entry: ConfigEntry,  # Added to match switch entities
        ssid_unique_id: str,  # unique_id for the HA "device" representing the SSID
        ssid_data: Dict[str, Any],
    ) -> None:
        """Initialize the Meraki SSID Name text entity."""
        super().__init__(coordinator)
        self._meraki_client = meraki_client
        self._config_entry = config_entry  # Store config_entry
        self._ssid_unique_id = ssid_unique_id  # This is the HA device identifier
        self._ssid_data = ssid_data

        # These are crucial for API calls to update the SSID name
        self._network_id: Optional[str] = ssid_data.get("networkId")
        self._ssid_number: Optional[Any] = ssid_data.get(
            "number"
        )  # Can be int or str depending on source

        # EntityDescription can be used for name, icon etc.
        self.entity_description = TextEntityDescription(
            key=f"{self._ssid_unique_id}_ssid_name",
            name="SSID Name",
            icon="mdi:form-textbox",
            native_min=1,
            native_max=32,
        )

        self._attr_unique_id = f"{self._ssid_unique_id}_name_text"

        # Set initial state
        self._update_internal_state()

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information to link this entity to the SSID device."""
        device_name = format_device_name(self._ssid_data, self._config_entry.options)
        return DeviceInfo(
            identifiers={(DOMAIN, self._ssid_unique_id)},
            name=device_name,
            model="SSID",
            manufacturer="Meraki",
            via_device=(DOMAIN, self._network_id),
        )

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        if not super().available or not self.coordinator.data:
            return False
        ssid_data = self._get_current_ssid_data()
        return ssid_data is not None and ssid_data.get("enabled", False)

    def _get_current_ssid_data(self) -> Optional[Dict[str, Any]]:
        """Retrieve the latest data for this sensor's device from the coordinator."""
        if not self.coordinator.data or "ssids" not in self.coordinator.data:
            return None
        for ssid in self.coordinator.data["ssids"]:
            if ssid.get("networkId") == self._network_id and str(
                ssid.get("number")
            ) == str(self._ssid_number):
                return ssid
        return None

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_internal_state()
        self.async_write_ha_state()

    def _update_internal_state(self) -> None:
        """Update the internal state of the text entity based on coordinator data."""
        current_ssid_data = self._get_current_ssid_data()
        if current_ssid_data:
            self._attr_native_value = current_ssid_data.get("name")
        else:
            self._attr_native_value = None

    async def async_set_value(self, value: str) -> None:
        """Change the SSID name."""
        if self._network_id is None or self._ssid_number is None:
            _LOGGER.error(
                "Cannot update SSID name for %s: Missing networkId or SSID number.",
                self.entity_id or self._attr_unique_id,
            )
            return

        try:
            await self._meraki_client.update_network_wireless_ssid(
                network_id=self._network_id,
                number=str(self._ssid_number),
                name=value,
            )
            # Update the local state immediately for better UX
            self._attr_native_value = value
            self.async_write_ha_state()
            # Request a refresh from the coordinator to confirm the change
            await self.coordinator.async_request_refresh()
        except Exception as e:
            _LOGGER.error(
                "Failed to set SSID name for network %s, SSID %s to '%s': %s",
                self._network_id,
                self._ssid_number,
                value,
                e,
            )
            raise HomeAssistantError(
                f"Failed to set SSID name to '{value}': {e}"
            ) from e
            # Optionally, force a refresh to revert optimistic update if API call failed
            # await self.coordinator.async_request_refresh()

    # @property
    # def native_min_length(self) -> int:
    #   """Return the minimum number of characters."""
    #   return 1

    # @property
    # def native_max_length(self) -> int:
    #   """Return the maximum number of characters."""
    #   return 32
