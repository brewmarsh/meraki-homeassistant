"""Switch entity for controlling Meraki Content Filtering categories."""

import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

<<<<<<< HEAD
from ..coordinator import MerakiDataUpdateCoordinator
from ..helpers.device_info_helpers import resolve_device_info
=======
from ..helpers.device_info_helpers import resolve_device_info
from ..meraki_data_coordinator import MerakiDataCoordinator
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)

_LOGGER = logging.getLogger(__name__)


class MerakiContentFilteringSwitch(
    CoordinatorEntity,
    SwitchEntity,
):
    """Representation of a Meraki Content Filtering category switch."""

    def __init__(
        self,
<<<<<<< HEAD
        coordinator: MerakiDataUpdateCoordinator,
=======
        coordinator: MerakiDataCoordinator,
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
        config_entry: ConfigEntry,
        network: dict[str, Any],
        category: dict[str, Any],
    ) -> None:
        """
        Initialize the Meraki Content Filtering switch.

        Args:
        ----
            coordinator: The data update coordinator.
            config_entry: The config entry.
            network: The network data.
            category: The content filtering category.

        """
        super().__init__(coordinator)
        self._config_entry = config_entry
        self._network = network
        self._category = category
        self._client = coordinator.api

        self.entity_description = SwitchEntityDescription(
            key=f"content_filtering_{network['id']}_{category['id']}",
            name=f"Block {category['name']}",
        )

    @property
    def unique_id(self) -> str:
        """Return a unique ID."""
        return f"meraki-content-filtering-{self._network['id']}-{self._category['id']}"

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return the device info."""
        return resolve_device_info(self._network, self._config_entry)

    @property
    def is_on(self) -> bool:
        """Return true if the switch is on."""
        content_filtering = self.coordinator.data.get("content_filtering", {}).get(
            self._network["id"],
            {},
        )
        return self._category["id"] in content_filtering.get("blockedUrlCategories", [])

    async def async_turn_on(self, **kwargs: Any) -> None:
        """
        Turn the entity on.

        Args:
        ----
            **kwargs: Additional arguments.

        """
        await self._async_update_content_filtering(add=True)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """
        Turn the entity off.

        Args:
        ----
            **kwargs: Additional arguments.

        """
        await self._async_update_content_filtering(add=False)

    async def _async_update_content_filtering(self, add: bool) -> None:
        """
        Update the content filtering settings.

        Args:
        ----
            add: Whether to add or remove the category.

        """
        current_settings = (
            await self._client.appliance.get_network_appliance_content_filtering(
                self._network["id"],
            )
        )
        blocked_categories = current_settings.get("blockedUrlCategories", [])

        if add:
            if self._category["id"] not in blocked_categories:
                blocked_categories.append(self._category["id"])
        elif self._category["id"] in blocked_categories:
            blocked_categories.remove(self._category["id"])

        await self._client.appliance.update_network_appliance_content_filtering(
            self._network["id"],
            blockedUrlCategories=blocked_categories,
        )
        await self.coordinator.async_request_refresh()

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()
