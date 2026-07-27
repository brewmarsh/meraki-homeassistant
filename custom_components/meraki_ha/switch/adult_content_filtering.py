"""Switch entity for controlling Meraki Adult Content Filtering on an SSID."""

from __future__ import annotations

import logging
from typing import Any

from custom_components.meraki_ha.const.integration import DOMAIN
from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo

from ..coordinators import MerakiSwitchCoordinator
from ..entity import MerakiEntity

_LOGGER = logging.getLogger(__name__)


class MerakiAdultContentFilteringSwitch(MerakiEntity, SwitchEntity):
    """Representation of a Meraki Adult Content Filtering switch."""

    _attr_entity_category = EntityCategory.CONFIG

    def __init__(
        self,
        coordinator: MerakiSwitchCoordinator,
        config_entry: ConfigEntry,
        ssid: dict[str, Any],
    ) -> None:
        """Initialize the Meraki Adult Content Filtering switch."""
        super().__init__(coordinator)
        self._config_entry = config_entry
        self._ssid = ssid
        self._client = coordinator.api

        network = coordinator.get_network(self._network_id)
        network_name = network.name if network else f"Network {self._network_id}"
        self.entity_description = SwitchEntityDescription(
            key="adult_content_filtering",
            name=f"{network_name} SSID {ssid['name']} Adult Content Filtering",
        )

    @property
    def _network_id(self) -> str:
        """Return the network ID."""
        return self._ssid["networkId"]

    @property
    def _ssid_number(self) -> int:
        """Return the SSID number."""
        return self._ssid["number"]

    @property
    def unique_id(self) -> str | None:
        """Return the unique ID."""
        return (
            f"network_{self._network_id}_{self._network_id}_ssid_"
            f"{self._ssid_number}_adult_content_filtering"
        )

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return the device info."""
        return DeviceInfo(
            identifiers={(DOMAIN, f"network_{self._network_id}")},
        )

    @property
    def is_on(self) -> bool:
        """Return true if the switch is on."""
        ssid_data = self.coordinator.get_ssid(
            self._ssid["networkId"], self._ssid["number"]
        )
        if not ssid_data:
            return False
        return ssid_data.get("adultContentFilteringEnabled", False)

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the entity on."""
        await self._async_update_adult_content_filtering(True)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the entity off."""
        await self._async_update_adult_content_filtering(False)

    async def _async_update_adult_content_filtering(self, enabled: bool) -> None:
        """Update the adult content filtering setting."""
        await self._client.wireless.update_network_wireless_ssid(
            network_id=self._ssid["networkId"],
            number=self._ssid["number"],
            adultContentFilteringEnabled=enabled,
        )
        await self.coordinator.async_request_refresh()

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()
