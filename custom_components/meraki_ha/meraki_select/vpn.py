"""Select entity for controlling Meraki Site-to-Site VPN."""

import logging

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
from ..types import MerakiNetwork, MerakiVpn

_LOGGER = logging.getLogger(__name__)


class MerakiVpnSelect(CoordinatorEntity, SelectEntity):
    """Representation of a Meraki VPN select entity."""

    entity_category = EntityCategory.CONFIG
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        meraki_client: MerakiAPIClient,
        config_entry: ConfigEntry,
        network_data: MerakiNetwork,
    ) -> None:
        """Initialize the Meraki VPN select entity."""
        super().__init__(coordinator)
        self._meraki_client = meraki_client
        self._config_entry = config_entry
        self._network_data = network_data
        self._network_id = network_data.id

        self.entity_description = SelectEntityDescription(
            key=f"vpn_status_{self._network_id}",
            name="VPN Mode",
            icon="mdi:vpn",
        )

        self._attr_unique_id = f"meraki-network-{self._network_id}-vpn"
        self._update_internal_state()

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return device information to link this entity to the network device."""
        return resolve_device_info(
            entity_data=self._network_data,
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
        if self.coordinator.data and self.coordinator.data.get("vpn_status"):
            vpn_status = self.coordinator.data["vpn_status"].get(self._network_id)
            if vpn_status and isinstance(vpn_status, MerakiVpn):
                self._attr_current_option = vpn_status.mode
                self._attr_options = ["none", "spoke", "hub"]
        else:
            self._attr_current_option = None
            self._attr_options = []

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        try:
            await self._meraki_client.appliance.update_vpn_status(
                network_id=self._network_id,
                mode=option,
            )
            self._attr_current_option = option
            self.async_write_ha_state()
            await self.coordinator.async_request_refresh()
        except Exception as e:
            _LOGGER.error(
                "Failed to set VPN mode to '%s' for network %s: %s",
                option,
                self._network_id,
                e,
            )
            raise HomeAssistantError(
                f"Failed to set VPN mode to '{option}': {e}"
            ) from e
