"""Select entity for controlling Meraki Content Filtering."""

import logging

from homeassistant.components.select import SelectEntity, SelectEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.device_registry import DeviceInfo

from ..coordinators import MerakiMainCoordinator
from ..core.api import MerakiApiClientProtocol
from ..core.models.network import MerakiNetwork
from ..core.utils.data import ensure_list_of_strings
from ..entity import MerakiEntity
from ..helpers.device_info_helpers import resolve_device_info

_LOGGER = logging.getLogger(__name__)

# Profiles mapped to generic, lowercase category names.
# We will dynamically resolve these to actual API IDs at runtime.
CONTENT_FILTERING_PROFILE_TARGETS: dict[str, list[str]] = {
    "None": [],
    "Security": [
        "malware sites",
        "phishing and other frauds",
        "bot nets",
        "botnets",
    ],
    "Family": [
        "adult and pornography",
        "gambling",
        "nudity",
        "malware sites",
        "phishing and other frauds",
        "bot nets",
        "botnets",
    ],
    "Strict": [
        "adult and pornography",
        "illegal",
        "gambling",
        "hate and racism",
        "weapons",
        "violence",
        "keyloggers and monitoring",
        "spam urls",
        "malware sites",
        "phishing and other frauds",
        "bot nets",
        "botnets",
    ],
}


class MerakiContentFilteringSelect(MerakiEntity[MerakiMainCoordinator], SelectEntity):
    """Representation of a Meraki Content Filtering select entity."""

    _attr_has_entity_name = False

    def __init__(
        self,
        coordinator: MerakiMainCoordinator,
        meraki_client: MerakiApiClientProtocol,
        config_entry: ConfigEntry,
        network_data: MerakiNetwork,
    ) -> None:
        """Initialize the Meraki Content Filtering select entity."""
        super().__init__(coordinator)
        self._meraki_client = meraki_client
        self._config_entry = config_entry
        self._network_data = network_data
        self._network_id = network_data.id

        self.entity_description = SelectEntityDescription(
            key=f"content_filtering_{self._network_id}",
            name=f"{network_data.name} Content Filter",
            icon="mdi:web-filter",
        )

        self._attr_unique_id = (
            f"meraki-network-{self._network_id}-content-filtering-profile"
        )
        self._attr_options = list(CONTENT_FILTERING_PROFILE_TARGETS.keys())

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return device information to link this entity to the network device."""
        return resolve_device_info(
            entity_data=self._network_data,
            config_entry=self._config_entry,
        )

    @property
    def current_option(self) -> str | None:
        """Return the current selected option based on blocked categories."""
        if not self.coordinator.data or not self.coordinator.data.get(
            "content_filtering"
        ):
            return None

        content_filtering = self.coordinator.data["content_filtering"].get(
            self._network_id
        )
        if not content_filtering or not isinstance(content_filtering, dict):
            return None

        blocked_categories = ensure_list_of_strings(
            content_filtering.get("blockedUrlCategories", []), key_to_extract="id"
        )

        # Use a robust heuristic to map current state without synchronous API calls
        count = len(blocked_categories)
        if count == 0:
            return "None"
        elif count <= 4:
            return "Security"
        elif count <= 8:
            return "Family"
        else:
            return "Strict"

    async def async_select_option(self, option: str) -> None:
        """Change the selected option by dynamically resolving valid category IDs."""
        if option not in CONTENT_FILTERING_PROFILE_TARGETS:
            raise ValueError(f"Invalid option: {option}")

        target_names = CONTENT_FILTERING_PROFILE_TARGETS[option]
        resolved_ids = set()

        try:
            appliance = self._meraki_client.appliance

            # If not 'None', fetch master list of valid categories for MX
            if target_names:
                resp = (
                    await appliance.get_network_appliance_content_filtering_categories(
                        network_id=self._network_id
                    )
                )

                # Handle both list and dict response formats from the Meraki library
                valid_categories = (
                    resp if isinstance(resp, list) else resp.get("categories", [])
                )
                name_to_id = {
                    cat["name"].lower(): cat["id"] for cat in valid_categories
                }

                # Match target names against valid API names (fuzzy matching for spaces)
                for target in target_names:
                    for valid_name, valid_id in name_to_id.items():
                        if target == valid_name or target.replace(
                            " ", ""
                        ) == valid_name.replace(" ", ""):
                            resolved_ids.add(valid_id)

            final_blocked_ids = list(resolved_ids)

            # Send the validated payload
            await appliance.update_network_appliance_content_filtering(
                network_id=self._network_id,
                blockedUrlCategories=final_blocked_ids,
            )
            await self.coordinator.async_request_refresh()

        except Exception as e:
            _LOGGER.error(
                "Failed to set content filtering profile to '%s' for network %s: %s",
                option,
                self._network_id,
                e,
            )
            raise HomeAssistantError(
                f"Failed to set content filtering profile to '{option}': {e}"
            ) from e

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()
