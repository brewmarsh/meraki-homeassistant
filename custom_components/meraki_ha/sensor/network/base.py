"""Base class for Meraki SSID sensors."""

import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback

from ..coordinators import MerakiSwitchCoordinator
from ...entity import MerakiEntity
from ...helpers.device_info_helpers import resolve_device_info

_LOGGER = logging.getLogger(__name__)


class MerakiSSIDBaseSensor(MerakiEntity, SensorEntity):
    """Base class for Meraki SSID sensors."""

    _attr_name: str | None = None

    def __init__(
        self,
        coordinator: MerakiSwitchCoordinator,
        config_entry: ConfigEntry,
        ssid_data: dict[str, Any],
        attribute: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._config_entry = config_entry
        self._ssid_data_at_init = ssid_data
        self._attribute = attribute
        self._network_id = ssid_data.get("networkId")
        self._ssid_number = ssid_data.get("number")

        # Unique ID is now handled by the dynamic @property method below
        self._attr_has_entity_name = True
        ssid_name = ssid_data.get("name", f"SSID {self._ssid_number}")
        if (
            hasattr(self, "entity_description")
            and self.entity_description
            and self.entity_description.name
        ):
            self._attr_name = f"{ssid_name} {self.entity_description.name}"

        # SSID entities are logical children of the "Virtual SSID Device"
        self._attr_device_info = resolve_device_info(
            entity_data=self._ssid_data_at_init,
            config_entry=self._config_entry,
        )

    def _get_current_ssid_data(self) -> dict[str, Any] | None:
        """Retrieve the latest data for this SSID from the coordinator."""
        if not self.coordinator.data:
            return None

        # Look in wireless_settings (preferred) or flat ssids list
        if "wireless_settings" in self.coordinator.data:
            network_ssids = self.coordinator.data["wireless_settings"].get(
                self._network_id
            )
            if network_ssids:
                for ssid in network_ssids:
                    if str(ssid.get("number")) == str(self._ssid_number):
                        return ssid
            return None

        if "ssids" in self.coordinator.data:
            for ssid in self.coordinator.data["ssids"]:
                if ssid.get("networkId") == self._network_id and str(
                    ssid.get("number")
                ) == str(self._ssid_number):
                    return ssid
        return None

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        if not super().available or not self.coordinator.data:
            return False
        ssid_data = self._get_current_ssid_data()
        return ssid_data is not None and ssid_data.get("enabled", False)

    @property
    def unique_id(self) -> str | None:
        """Return a unique ID that prevents platform collisions.

        For SSID-based entities, we combine the network ID, SSID number, and
        the lowercased class name. This allows multiple entities (Switch, Sensor, Text)
        to exist for the same SSID without ID conflicts.
        """
        if (
            hasattr(self, "entity_description")
            and self.entity_description
            and self.entity_description.key
        ):
            return (
                f"{self._network_id}ssid{self._ssid_number}_"
                f"{self.entity_description.key}"
            )

        return (
            f"{self._network_id}ssid{self._ssid_number}"
            f"{self.__class__.__name__.lower()}"
        )

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        ssid_data = self._get_current_ssid_data()
        if ssid_data:
            self._attr_native_value = ssid_data.get(self._attribute)
        self.async_write_ha_state()
