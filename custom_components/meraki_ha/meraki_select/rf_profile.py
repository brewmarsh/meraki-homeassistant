"""Select entity for controlling Meraki RF Profiles."""

import logging
from typing import Any

from homeassistant.components.select import SelectEntity, SelectEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ..coordinator import MerakiDataUpdateCoordinator
from ..core.api.client import MerakiAPIClient
from ..helpers.device_info_helpers import resolve_device_info

_LOGGER = logging.getLogger(__name__)


class MerakiRFProfileSelect(CoordinatorEntity, SelectEntity):
    """Representation of a Meraki RF Profile select entity."""

    coordinator: MerakiDataUpdateCoordinator
    entity_category = EntityCategory.CONFIG
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        meraki_client: MerakiAPIClient,
        config_entry: ConfigEntry,
        ssid_data: dict[str, Any],
    ) -> None:
        """Initialize the Meraki RF Profile select entity."""
        super().__init__(coordinator)
        self._meraki_client = meraki_client
        self._config_entry = config_entry
        self._ssid_data = ssid_data
        self._network_id = ssid_data["networkId"]
        self._ssid_number = ssid_data["number"]
        self._ssid_name = (
            f"[SSID {self._ssid_number}] {ssid_data.get('name', '')}".strip()
        )

        self.entity_description = SelectEntityDescription(
            key=f"{self._network_id}ssid{self._ssid_number}_rf_profile",
            name="RF Profile",
            icon="mdi:wifi-cog",
        )

        self._attr_unique_id = f"{self._network_id}ssid{self._ssid_number}_rf_profile"
        self._attr_options = []
        self._update_internal_state()

    # ### Entity Logic

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return device information to link this entity to the SSID 'device'."""
        return resolve_device_info(
            entity_data=self._ssid_data,
            config_entry=self._config_entry,
        )

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return super().available and self.coordinator.data is not None

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_internal_state()
        self.async_write_ha_state()

    def _update_internal_state(self) -> None:
        """Update the internal state of the select entity."""
        # ### Data Mapping
        options = ["None"]
        current_option = "None"

        if self.coordinator.data:
            # Get available RF profiles for this network
            rf_profiles = self.coordinator.data.get("rf_profiles", {}).get(
                self._network_id, []
            )
            profile_map = {
                p["name"]: p["id"] for p in rf_profiles if "name" in p and "id" in p
            }
            options.extend(sorted(profile_map.keys()))

            # Get current RF profile for this SSID
            # We need to find the SSID in the latest coordinator data
            current_ssid = self.coordinator.get_ssid(
                self._network_id, int(self._ssid_number)
            )
            if current_ssid:
                current_profile_id = current_ssid.get("rfProfileId")
                if current_profile_id:
                    # Find name from ID
                    for name, prof_id in profile_map.items():
                        if prof_id == current_profile_id:
                            current_option = name
                            break

        self._attr_current_option = current_option
        self._attr_options = options

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        # ### Data Mapping
        rf_profiles = self.coordinator.data.get("rf_profiles", {}).get(
            self._network_id, []
        )
        profile_id = None
        if option != "None":
            profile_id = next(
                (p["id"] for p in rf_profiles if p.get("name") == option), None
            )

        try:
            # Preparing update call
            update_params = {"rfProfileId": profile_id}
            await self._meraki_client.wireless.update_network_wireless_ssid(
                network_id=self._network_id,
                number=self._ssid_number,
                **update_params,
            )
            self._attr_current_option = option
            self.async_write_ha_state()
            await self.coordinator.async_request_refresh()
        except Exception as e:
            _LOGGER.error(
                "Failed to set RF profile to '%s' for SSID %s on network %s: %s",
                option,
                self._ssid_number,
                self._network_id,
                e,
            )
            raise HomeAssistantError(
                f"Failed to set RF profile to '{option}': {e}"
            ) from e
