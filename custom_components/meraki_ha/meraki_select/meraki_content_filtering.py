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

# Profiles mapped to Meraki category IDs from const_data.py
# Updated with 'C' prefixes for Cisco Talos integration (firmware MX17+)
CONTENT_FILTERING_PROFILES: dict[str, list[str]] = {
    "None": [],
    "Security": [
        "meraki:contentFiltering/category/C8",  # Malware sites
        "meraki:contentFiltering/category/C9",  # Phishing and other frauds
        "meraki:contentFiltering/category/C11",  # Botnets
    ],
    "Family": [
        "meraki:contentFiltering/category/C1",  # Adult and Pornography
        "meraki:contentFiltering/category/C3",  # Gambling
        "meraki:contentFiltering/category/C8",  # Malware sites
        "meraki:contentFiltering/category/C9",  # Phishing and other frauds
        "meraki:contentFiltering/category/C11",  # Botnets
        "meraki:contentFiltering/category/C20",  # Nudity
    ],
    "Strict": [
        "meraki:contentFiltering/category/C1",  # Adult and Pornography
        "meraki:contentFiltering/category/C2",  # Illegal
        "meraki:contentFiltering/category/C3",  # Gambling
        "meraki:contentFiltering/category/C4",  # Hate and Racism
        "meraki:contentFiltering/category/C5",  # Weapons
        "meraki:contentFiltering/category/C6",  # Violence
        "meraki:contentFiltering/category/C8",  # Malware sites
        "meraki:contentFiltering/category/C9",  # Phishing and other frauds
        "meraki:contentFiltering/category/C10",  # Key loggers and monitoring
        "meraki:contentFiltering/category/C11",  # Botnets
        "meraki:contentFiltering/category/C12",  # Spam URLs
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

        # Unique ID must include network_id to prevent collision and generic suffixes
        self._attr_unique_id = (
            f"meraki-network-{self._network_id}-content-filtering-profile"
        )
        self._attr_options = list(CONTENT_FILTERING_PROFILES.keys())

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return device information to link this entity to the network device."""
        return resolve_device_info(
            entity_data=self._network_data,
            config_entry=self._config_entry,
        )

    @property
    def current_option(self) -> str | None:
        """Return the current selected option."""
        if not self.coordinator.data or not self.coordinator.data.get(
            "content_filtering"
        ):
            return None

        content_filtering = self.coordinator.data["content_filtering"].get(
            self._network_id
        )
        # Safety check: ensure content_filtering is a dictionary and not None
        if not content_filtering or not isinstance(content_filtering, dict):
            return None

        blocked_categories = set(
            ensure_list_of_strings(
                content_filtering.get("blockedUrlCategories", []), key_to_extract="id"
            )
        )

        # Reverse map to find the best matching profile
        # We look for an exact match first
        for profile, categories in CONTENT_FILTERING_PROFILES.items():
            if set(categories) == blocked_categories:
                return profile

        # Fallback to "None" if no match
        return None

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        if option not in CONTENT_FILTERING_PROFILES:
            raise ValueError(f"Invalid option: {option}")

        categories = CONTENT_FILTERING_PROFILES[option]

        try:
            appliance = self._meraki_client.appliance
            await appliance.update_network_appliance_content_filtering(
                network_id=self._network_id,
                blockedUrlCategories=categories,
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
