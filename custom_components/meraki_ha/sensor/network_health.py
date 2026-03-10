"""Network-level aggregated health sensors for Meraki."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback

from ..coordinators import MerakiMainCoordinator
from ..core.entities.meraki_network_entity import MerakiNetworkEntity
from ..core.models.network import MerakiNetwork

_LOGGER = logging.getLogger(__name__)


class MerakiNetworkHealthSensor(MerakiNetworkEntity, SensorEntity):
    """Sensor to aggregate health of a specific Meraki device family (MX, MS, MR)."""

    def __init__(
        self,
        coordinator: MerakiMainCoordinator,
        config_entry: ConfigEntry,
        network: MerakiNetwork,
        family_prefix: str,
        family_name: str,
    ) -> None:
        """Initialize the aggregated health sensor."""
        super().__init__(coordinator, config_entry, network)
        self._network_id = network.id
        self._family_prefix = family_prefix
        self._family_name = family_name

        self._attr_name = f"{network.name} {family_name} Health"
        self._attr_unique_id = f"{network.id}_{family_prefix.lower()}_health"

        if family_prefix == "MR":
            self._attr_icon = "mdi:wifi"
        elif family_prefix == "MS":
            self._attr_icon = "mdi:lan"
        elif family_prefix == "MX":
            self._attr_icon = "mdi:router-network"
        else:
            self._attr_icon = "mdi:server-network"

        self._family_devices_cache: list[Any] = []
        self._compute_device_cache()

    def _compute_device_cache(self) -> None:
        """Compute the device cache to avoid O(M) scans on every property access."""
        if not self.coordinator.data:
            self._family_devices_cache = []
            return

        data = self.coordinator.data
        devices = []

        if isinstance(data, dict) and "devices_by_serial" in data:
            devices = list(data["devices_by_serial"].values())
        elif isinstance(data, dict) and "devices" in data:
            devices = data["devices"]
        elif isinstance(data, list):
            devices = data

        self._family_devices_cache = [
            d
            for d in devices
            if getattr(d, "network_id", None) == self._network_id
            and (getattr(d, "model", "") or "").startswith(self._family_prefix)
        ]

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._compute_device_cache()
        self.async_write_ha_state()

    @property
    def _family_devices(self) -> list[Any]:
        """Return the cached family devices."""
        return self._family_devices_cache

    @property
    def native_value(self) -> str:
        """Calculate the aggregated state of the device family."""
        devices = self._family_devices
        if not devices:
            return "N/A"

        offline_count = sum(
            1
            for d in devices
            if str(getattr(d, "status", "offline")).lower()
            not in ("online", "alerting", "dormant")
        )

        if offline_count == 0:
            return "Online"
        if offline_count < len(devices):
            return "Degraded"
        return "Offline"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Provide detailed fractional attributes for Lovelace cards."""
        base_attributes = super().extra_state_attributes
        devices = self._family_devices

        offline_devices = [
            getattr(d, "name", getattr(d, "serial", "unknown"))
            for d in devices
            if str(getattr(d, "status", "offline")).lower()
            not in ("online", "alerting", "dormant")
        ]

        base_attributes.update(
            {
                "total_devices": len(devices),
                "online_devices": len(devices) - len(offline_devices),
                "offline_devices": offline_devices,
                "hardware_family": self._family_name,
            }
        )
        return base_attributes

    @property
    def available(self) -> bool:
        """Sensor is available as long as the coordinator has data."""
        return bool(self.coordinator.data)
