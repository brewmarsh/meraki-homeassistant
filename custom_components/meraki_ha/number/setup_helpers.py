"""Helper function for setting up all number entities."""

import logging
from typing import List, Set

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import Entity

from ..coordinator import MerakiDataUpdateCoordinator
from .uplink_bandwidth import MerakiUplinkBandwidthNumber
from ..const import CONF_ENABLE_TRAFFIC_SHAPING

_LOGGER = logging.getLogger(__name__)


def _setup_uplink_bandwidth_numbers(
    config_entry: ConfigEntry,
    coordinator: MerakiDataUpdateCoordinator,
    added_entities: Set[str],
) -> List[Entity]:
    """Set up uplink bandwidth numbers."""
    if not config_entry.options.get(CONF_ENABLE_TRAFFIC_SHAPING):
        return []
    entities: List[Entity] = []
    networks = coordinator.data.get("networks", [])
    for network in networks:
        network_id = network.get("id")
        if not network_id:
            continue
        if "appliance" not in network.get("productTypes", []):
            continue

        traffic_shaping = coordinator.data.get("traffic_shaping", {}).get(network_id)
        if not traffic_shaping:
            continue

        limits = traffic_shaping.get("bandwidthLimits", {})
        if not limits:
            continue

        for uplink in limits.keys():
            for direction in ["up", "down"]:
                unique_id = f"uplink_bandwidth_{network_id}_{uplink}_{direction}"
                if unique_id not in added_entities:
                    entities.append(
                        MerakiUplinkBandwidthNumber(
                            coordinator, config_entry, network, uplink, direction
                        )
                    )
                    added_entities.add(unique_id)
    return entities


def async_setup_numbers(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    coordinator: MerakiDataUpdateCoordinator,
) -> List[Entity]:
    """Set up all number entities from the central coordinator."""
    entities: List[Entity] = []
    added_entities: Set[str] = set()

    if not coordinator.data:
        _LOGGER.warning("Coordinator has no data; skipping number setup.")
        return entities

    entities.extend(
        _setup_uplink_bandwidth_numbers(config_entry, coordinator, added_entities)
    )

    return entities
