"""SSID switch builder."""

import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from ...coordinator import MerakiDataUpdateCoordinator
from ..meraki_ssid_device_switch import (
    MerakiSSIDBroadcastSwitch,
    MerakiSSIDEnabledSwitch,
)

_LOGGER = logging.getLogger(__name__)


def setup_ssid_switches(
    config_entry: ConfigEntry,
    coordinator: MerakiDataUpdateCoordinator,
    added_entities: set[str],
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up SSID switches."""
    entities = _build_ssid_entities(
        coordinator, coordinator.data, config_entry, added_entities
    )
    if entities:
        async_add_entities(entities)


def _build_ssid_entities(
    coordinator: MerakiDataUpdateCoordinator,
    data: dict[str, Any],
    config_entry: ConfigEntry,
    added_entities: set[str],
) -> list[SwitchEntity]:
    """Build SSID entities."""
    entities: list[SwitchEntity] = []
    ssids = data.get("ssids", [])
    for ssid in ssids:
        entities.extend(
            _build_ssid_pair(coordinator, data, config_entry, ssid, added_entities)
        )
    return entities


def _build_ssid_pair(
    coordinator: MerakiDataUpdateCoordinator,
    data: dict[str, Any],
    config_entry: ConfigEntry,
    ssid: dict[str, Any],
    added_entities: set[str],
) -> list[SwitchEntity]:
    """Build a pair of switches (enabled and broadcast) for an SSID."""
    ssid_number = ssid.get("number")
    if ssid_number is None:
        return []

    entities: list[SwitchEntity] = []
    rf_profile = _get_rf_profile(data, ssid.get("networkId"))

    # Enabled Switch
    unique_id = f"{ssid['networkId']}ssid{ssid_number}_enabled_switch"
    if unique_id not in added_entities:
        entities.append(
            MerakiSSIDEnabledSwitch(
                coordinator,
                coordinator.api,
                config_entry,
                ssid,
                rf_profile,
            )
        )
        added_entities.add(unique_id)

    # Broadcast Switch
    unique_id = f"{ssid['networkId']}ssid{ssid_number}_broadcast_switch"
    if unique_id not in added_entities:
        entities.append(
            MerakiSSIDBroadcastSwitch(
                coordinator,
                coordinator.api,
                config_entry,
                ssid,
                rf_profile,
            )
        )
        added_entities.add(unique_id)
    return entities


def _get_rf_profile(
    data: dict[str, Any],
    network_id: str | None,
) -> dict[str, Any] | None:
    """Find the RF profile for a network."""
    if not network_id or not data.get("rf_profiles"):
        return None
    network_rf_profiles = data["rf_profiles"].get(network_id)
    if network_rf_profiles:
        return next(iter(network_rf_profiles), None)
    return None
