"""Update processor for the Meraki HA integration."""

from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING, Any, cast

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.update_coordinator import UpdateFailed

from ...const import DOMAIN
from ...const_conf import CONF_IGNORED_NETWORKS, DEFAULT_IGNORED_NETWORKS
from ..helpers.device_registry import (
    async_ensure_network_devices_exist,
    async_ensure_ssid_devices_exist,
)
from ..managers import PollingManager
from ..models.device import MerakiDevice
from ..models.network import MerakiNetwork
from .config_helper import CoordinatorConfig

if TYPE_CHECKING:
    from homeassistant.helpers.device_registry import DeviceRegistry
    from homeassistant.helpers.entity_registry import EntityRegistry, RegistryEntry

_LOGGER = logging.getLogger(__name__)


def cleanup_whitespace(data: dict[str, Any]) -> None:
    """Strip whitespace from string values in the data dictionary."""
    if not data:
        return
    for key, value in data.items():
        if isinstance(value, str):
            data[key] = value.strip()


def _get_network_id(network: Any) -> str | None:
    """Get the network ID, handling both object and dict forms."""
    if hasattr(network, "id"):
        return str(network.id)
    if isinstance(network, dict):
        return str(network.get("id"))
    return None


def filter_ignored_networks(data: dict[str, Any], ignored_ids: list[str]) -> None:
    """Filter out networks that the user has chosen to ignore."""
    if not ignored_ids or "networks" not in data:
        return
    data["networks"] = [
        n for n in data["networks"] if _get_network_id(n) not in ignored_ids
    ]


def _get_primary_entity_id(entities: list[RegistryEntry]) -> str | None:
    """Determine the primary entity for a device to link."""
    if not entities:
        return None

    primary_entity = entities[0]
    for entity in entities:
        if entity.domain == "camera":
            primary_entity = entity
            break
        if entity.domain == "switch" and primary_entity.domain != "camera":
            primary_entity = entity

    return primary_entity.entity_id


def update_device_registry_info(
    hass: HomeAssistant, devices: list[MerakiDevice]
) -> None:
    """Populate device data with associated Home Assistant entities."""
    if not devices:
        return

    ent_reg: EntityRegistry = er.async_get(hass)
    dev_reg: DeviceRegistry = dr.async_get(hass)

    for device in devices:
        device.status_messages = []
        if not device.serial:
            continue

        ha_device = dev_reg.async_get_device(
            identifiers={(DOMAIN, device.serial)},
        )
        if not ha_device:
            continue

        entities_for_device = er.async_entries_for_device(ent_reg, ha_device.id)
        if entities_for_device:
            device.entity_id = _get_primary_entity_id(entities_for_device)


class UpdateProcessor:
    """Process update data for the coordinator."""

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        polling_manager: PollingManager,
        config: CoordinatorConfig,
    ) -> None:
        """Initialize the update processor."""
        self.hass = hass
        self.config_entry = config_entry
        self.polling_manager = polling_manager
        self.config = config

    async def process_success(
        self,
        data: dict[str, Any],
        current_data: dict[str, Any] | None = None,
    ) -> tuple[
        dict[str, MerakiDevice],
        dict[str, MerakiNetwork],
        dict[tuple[str, int], dict[str, Any]],
        bool,  # interval_changed
    ]:
        """
        Process successful data update.

        This method acts as an orchestrator, delegating specific tasks to
        sub-methods to maintain a low Agent Cognitive Load (ACL).
        """
        # Process the raw data (previously in MerakiDataProcessor)
        processed_data = await self.async_process(data, current_data)

        # Extract results from the processed payload
        devices_by_serial = processed_data["devices_by_serial"]
        networks_by_id = processed_data["networks_by_id"]
        ssids_by_network_and_number = processed_data["ssids_by_network_and_number"]

        return (
            devices_by_serial,
            networks_by_id,
            ssids_by_network_and_number,
            False,  # interval_changed is now handled in _async_update_data
        )

    async def async_process(
        self, data: dict[str, Any], previous_data: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """
        Process raw API data into normalized objects and lookup tables.

        This method orchestrates all data normalization and registry updates.
        """
        # Ensure registry entries exist
        async_ensure_network_devices_exist(
            self.hass, self.config_entry, data.get("networks", [])
        )
        if "ssids" in data:
            async_ensure_ssid_devices_exist(self.hass, self.config_entry, data["ssids"])

        # Apply filters
        ignored_ids = self.config_entry.options.get(
            CONF_IGNORED_NETWORKS,
            DEFAULT_IGNORED_NETWORKS,
        )
        filter_ignored_networks(data, ignored_ids)

        # Cleanup previous data (as per original coordinator logic)
        if previous_data:
            cleanup_whitespace(previous_data)

        # Normalize data and update registry
        devices, devices_by_serial = self._normalize_devices(data)
        _, networks_by_id = self._normalize_networks(data)
        ssids_by_network_and_number = self._normalize_ssids(data)

        update_device_registry_info(self.hass, devices)

        # Return lookup tables
        return {
            "devices_by_serial": devices_by_serial,
            "networks_by_id": networks_by_id,
            "ssids_by_network_and_number": ssids_by_network_and_number,
        }

    def _normalize_devices(
        self, data: dict[str, Any]
    ) -> tuple[list[MerakiDevice], dict[str, MerakiDevice]]:
        """Normalize device data and build lookup table."""
        devices_raw = data.get("devices", [])
        devices = [
            MerakiDevice.from_dict(d) if isinstance(d, dict) else d for d in devices_raw
        ]
        devices_by_serial = {d.serial: d for d in devices if d.serial}
        data["devices"] = devices
        return devices, devices_by_serial

    def _normalize_networks(
        self, data: dict[str, Any]
    ) -> tuple[list[MerakiNetwork], dict[str, MerakiNetwork]]:
        """Normalize network data and build lookup table."""
        networks_raw = data.get("networks", [])
        networks = [
            MerakiNetwork.from_dict(n) if isinstance(n, dict) else n
            for n in networks_raw
        ]
        networks_by_id = {n.id: n for n in networks if n.id}
        data["networks"] = networks
        return networks, networks_by_id

    def _normalize_ssids(
        self, data: dict[str, Any]
    ) -> dict[tuple[str, int], dict[str, Any]]:
        """Normalize SSID data and build lookup table."""
        return {
            (cast(str, s.get("networkId")), int(cast(int, s.get("number")))): s
            for s in data.get("ssids", [])
            if s.get("networkId") and s.get("number") is not None
        }

    def process_failure(
        self, err: Exception, last_successful_data: dict[str, Any]
    ) -> tuple[dict[str, Any], bool]:
        """
        Handle update failure via PollingManager.

        Returns the data to use and whether the interval changed.
        """
        self._log_failure(err)

        if not last_successful_data:
            if isinstance(err, (asyncio.TimeoutError, TimeoutError)):
                raise UpdateFailed("API Timeout") from err
            # If the error is already an UpdateFailed with the right message, re-raise it
            if isinstance(err, UpdateFailed) and "API Timeout" in str(err):
                raise err
            raise UpdateFailed(f"Error communicating with API: {err}") from err

        return last_successful_data, False  # interval_changed is now handled in _async_update_data

    def _handle_interval_recovery(self) -> bool:
        """Handle polling interval recovery logic and return if interval changed."""
        interval_changed = False
        if self.polling_manager.record_success():
            # If True, the interval was reset after recovery
            interval_changed = True
            _LOGGER.info(
                "Meraki API recovered. Resetting update interval to %s",
                self.polling_manager.update_interval,
            )

        _LOGGER.debug(
            "Coordinator update success rate (last 5): %.1f%%",
            self.polling_manager.get_success_rate(),
        )
        return interval_changed

    def _handle_interval_failure(self, err: Exception) -> bool:
        """Record the failure and return if the interval was changed."""
        return self.polling_manager.record_failure(err)

    def _log_failure(self, err: Exception) -> None:
        """Log failure details."""
        _LOGGER.debug(
            "Coordinator update success rate (last 5): %.1f%%",
            self.polling_manager.get_success_rate(),
        )
        _LOGGER.warning(
            "Failed to fetch new data, using stale data. Error: %s",
            err,
        )
