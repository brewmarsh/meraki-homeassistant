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

        # Category mapping cache
        self._category_id_to_name: dict[str, str] = {}
        self._category_name_to_id: dict[str, str] = {}

    async def async_added_to_hass(self) -> None:
        """Fetch category mapping when added to Home Assistant."""
        await super().async_added_to_hass()
        await self._async_fetch_category_mapping()

    async def _async_fetch_category_mapping(self) -> None:
        """Fetch and cache Meraki content filtering categories."""
        try:
            response = await self._meraki_client.appliance.get_network_appliance_content_filtering_categories(
                self._network_id
            )
            categories = response.get("categories", [])
            self._category_id_to_name = {cat["id"]: cat["name"] for cat in categories}
            self._category_name_to_id = {cat["name"]: cat["id"] for cat in categories}
            _LOGGER.debug(
                "Fetched %d content filtering categories for network %s",
                len(categories),
                self._network_id,
            )
        except Exception as e:
            _LOGGER.warning(
                "Failed to fetch content filtering categories for network %s: %s",
                self._network_id,
                e,
            )

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

        raw_categories = ensure_list_of_strings(
            content_filtering.get("blockedUrlCategories", []), key_to_extract="id"
        )

        # Use fetched mapping to resolve IDs to names
        blocked_category_names = set()
        for cat_id in raw_categories:
            if name := self._category_id_to_name.get(cat_id):
                blocked_category_names.add(name)
            elif name := self._category_id_to_name.get(
                f"meraki:contentFiltering/category/{cat_id}"
            ):
                blocked_category_names.add(name)
            else:
                # If name not found, we can't accurately match profiles by name
                _LOGGER.debug(
                    "Category ID %s not found in mapping for network %s",
                    cat_id,
                    self._network_id,
                )

        # Reverse map to find the best matching profile
        for profile, categories in CONTENT_FILTERING_PROFILES.items():
            if set(categories) == blocked_category_names:
                return profile

        # Fallback to "None" if no match
        return None

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        if option not in CONTENT_FILTERING_PROFILES:
            raise ValueError(f"Invalid option: {option}")

        # Ensure we have the latest mapping
        await self._async_fetch_category_mapping()

        desired_names = CONTENT_FILTERING_PROFILES[option]
        api_ids = []
        missing_names = []

        for name in desired_names:
            if cat_id := self._category_name_to_id.get(name):
                api_ids.append(cat_id)
            else:
                missing_names.append(name)

        if missing_names:
            _LOGGER.warning(
                "The following categories were not found on Meraki for network %s: %s",
                self._network_id,
                ", ".join(missing_names),
            )

        try:
            appliance = self._meraki_client.appliance
            await appliance.update_network_appliance_content_filtering(
                network_id=self._network_id,
                blockedUrlCategories=api_ids,
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
