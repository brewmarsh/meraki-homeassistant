"""Base class for Meraki SSID sensors."""

from typing import Any, Dict, Optional
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.sensor import SensorEntity
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from ...const import DOMAIN
from ...core.coordinators.meraki_data_coordinator import MerakiDataCoordinator
from ...core.utils.naming_utils import format_device_name


class MerakiSSIDBaseSensor(CoordinatorEntity[MerakiDataCoordinator], SensorEntity):
    """Base class for Meraki SSID sensors."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        config_entry: ConfigEntry,
        ssid_data: Dict[str, Any],
        attribute: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._config_entry = config_entry
        self._ssid_data_at_init = ssid_data
        self._attribute = attribute
        self._network_id = ssid_data.get("networkId")
        self._ssid_number = ssid_data.get("number")
        self._attr_unique_id = f"ssid-{self._network_id}-{self._ssid_number}-{self._attribute}"

    def _get_current_ssid_data(self) -> Optional[Dict[str, Any]]:
        """Retrieve the latest data for this SSID from the coordinator."""
        if not self.coordinator.data or "ssids" not in self.coordinator.data:
            return None
        for ssid in self.coordinator.data["ssids"]:
            if ssid.get("networkId") == self._network_id and str(
                ssid.get("number")
            ) == str(self._ssid_number):
                return ssid
        return None

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information to link this entity to the SSID device."""
        ssid_unique_id = f"ssid-{self._network_id}-{self._ssid_number}"
        device_name = format_device_name(
            self._ssid_data_at_init, self._config_entry.options
        )
        return DeviceInfo(
            identifiers={(DOMAIN, ssid_unique_id)},
            name=device_name,
            model="SSID",
            manufacturer="Cisco Meraki",
            via_device=(DOMAIN, self._network_id),
        )

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        if not super().available or not self.coordinator.data:
            return False
        ssid_data = self._get_current_ssid_data()
        return ssid_data is not None and ssid_data.get("enabled", False)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        ssid_data = self._get_current_ssid_data()
        if ssid_data:
            self._attr_native_value = ssid_data.get(self._attribute)
        self.async_write_ha_state()
