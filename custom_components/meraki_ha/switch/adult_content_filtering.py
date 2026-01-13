"""Switch entity for controlling Meraki Adult Content Filtering on an SSID."""

import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

<<<<<<< HEAD
from ..coordinator import MerakiDataUpdateCoordinator
from ..helpers.device_info_helpers import resolve_device_info
=======
from ..helpers.device_info_helpers import resolve_device_info
from ..meraki_data_coordinator import MerakiDataCoordinator
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)

_LOGGER = logging.getLogger(__name__)


class MerakiAdultContentFilteringSwitch(CoordinatorEntity, SwitchEntity):
    """Representation of a Meraki Adult Content Filtering switch."""

    def __init__(
        self,
<<<<<<< HEAD
        coordinator: MerakiDataUpdateCoordinator,
=======
        coordinator: MerakiDataCoordinator,
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
        config_entry: ConfigEntry,
        ssid: dict[str, Any],
    ) -> None:
        """Initialize the Meraki Adult Content Filtering switch."""
        super().__init__(coordinator)
        self._config_entry = config_entry
        self._ssid = ssid
        self._client = coordinator.api

        self.entity_description = SwitchEntityDescription(
            key=f"adult_content_filtering_{ssid['networkId']}_{ssid['number']}",
            name=f"Adult Content Filtering on {ssid['name']}",
        )

    @property
    def unique_id(self) -> str:
        """Return a unique ID."""
        return (
            f"meraki-adult-content-filtering-{self._ssid['networkId']}-"
            f"{self._ssid['number']}"
        )

    @property
    def device_info(self):
        """Return the device info."""
        return resolve_device_info(self._ssid, self._config_entry)

    @property
    def is_on(self) -> bool:
        """Return true if the switch is on."""
        ssid_data = self.coordinator.get_ssid(
            self._ssid["networkId"], self._ssid["number"]
        )
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
