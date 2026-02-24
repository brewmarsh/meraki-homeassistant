"""Data processing logic for the Meraki HA coordinator."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, cast

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import entity_registry as er

from ..const import DOMAIN
from ..const_conf import CONF_IGNORED_NETWORKS, DEFAULT_IGNORED_NETWORKS
from .helpers.device_registry import (
    async_ensure_network_devices_exist,
    async_ensure_ssid_devices_exist,
)
from .models.device import MerakiDevice
from .models.network import MerakiNetwork

if TYPE_CHECKING:
    from homeassistant.helpers.device_registry import DeviceRegistry
    from homeassistant.helpers.entity_registry import EntityRegistry

_LOGGER = logging.getLogger(__name__)


def cleanup_whitespace(data: dict[str, Any]) -> None:
    """Strip whitespace from string values in the data dictionary."""
    if not data:
        return
    for key, value in data.items():
        if isinstance(value, str):
            data[key] = value.strip()


def filter_ignored_networks(data: dict[str, Any], ignored_ids: list[str]) -> None:
    """Filter out networks that the user has chosen to ignore."""
    if ignored_ids and "networks" in data:
        data["networks"] = [
            n
            for n in data["networks"]
            if (n.id if hasattr(n, "id") else n.get("id")) not in ignored_ids
        ]


def update_device_registry_info(hass: HomeAssistant, devices: list[MerakiDevice]) -> None:
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
        if ha_device:
            entities_for_device = er.async_entries_for_device(
                ent_reg,
                ha_device.id,
            )
            if entities_for_device:
                # Prioritize camera entities, then switch, then fallback to first
                primary_entity = entities_for_device[0]
                for entity in entities_for_device:
                    if entity.domain == "camera":
                        primary_entity = entity
                        break
                    if (
                        entity.domain == "switch"
                        and primary_entity.domain != "camera"
                    ):
                        primary_entity = entity
                device.entity_id = primary_entity.entity_id


class MerakiDataProcessor:
    """Class to handle data normalization and processing."""

    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry) -> None:
        """Initialize the data processor."""
        self.hass = hass
        self.config_entry = config_entry

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

        # Normalize devices
        devices_raw = data.get("devices", [])
        devices = [
            MerakiDevice.from_dict(d) if isinstance(d, dict) else d for d in devices_raw
        ]
        devices_by_serial = {d.serial: d for d in devices if d.serial}
        data["devices"] = devices

        # Normalize networks
        networks_raw = data.get("networks", [])
        networks = [
            MerakiNetwork.from_dict(n) if isinstance(n, dict) else n
            for n in networks_raw
        ]
        networks_by_id = {n.id: n for n in networks if n.id}
        data["networks"] = networks

        # Normalize SSIDs
        ssids_by_network_and_number = {
            (cast(str, s.get("networkId")), int(cast(int, s.get("number")))): s
            for s in data.get("ssids", [])
            if s.get("networkId") and s.get("number") is not None
        }

        # Update device registry info (linking entities)
        update_device_registry_info(self.hass, devices)

        # Return lookup tables
        return {
            "devices_by_serial": devices_by_serial,
            "networks_by_id": networks_by_id,
            "ssids_by_network_and_number": ssids_by_network_and_number,
        }
