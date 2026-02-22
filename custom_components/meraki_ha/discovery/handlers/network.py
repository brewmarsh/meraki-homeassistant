"""Discovery handler for Network-level entities."""

from __future__ import annotations

import logging
from collections.abc import AsyncIterator
from typing import TYPE_CHECKING

from ...const_conf import (
    CONF_ENABLE_CLIENT_STATUS_SENSORS,
    CONF_ENABLE_NETWORK_SENSORS,
    CONF_ENABLE_TRAFFIC_SHAPING,
    CONF_ENABLE_VLAN_SENSORS,
    CONF_ENABLE_VPN_MANAGEMENT,
)
from ...sensor.network.network_clients import MerakiNetworkClientsSensor
from ...sensor.network.traffic_shaping import TrafficShapingSensor
from ...switch.content_filtering import MerakiContentFilteringSwitch
from .base import BaseHandler

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.helpers.entity import Entity

    from ....coordinator import (
        MerakiDataUpdateCoordinator,
    )
    from ...services.network_control_service import NetworkControlService


_LOGGER = logging.getLogger(__name__)


class NetworkHandler(BaseHandler):
    """Handler for network-level entities."""

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        config_entry: ConfigEntry,
        network_control_service: NetworkControlService,
    ) -> None:
        """Initialize the NetworkHandler."""
        super().__init__(coordinator, config_entry)
        self._network_control_service = network_control_service


    async def discover_entities(self) -> AsyncIterator[Entity]:
        """Discover network-level entities."""
        from ...meraki_select.meraki_content_filtering import (
            MerakiContentFilteringSelect,
        )
        from ...meraki_select.vpn import MerakiVpnSelect

        # Check if network sensors are enabled
        if not self._config_entry.options.get(CONF_ENABLE_NETWORK_SENSORS, True):
            _LOGGER.debug("Network sensors are disabled.")
            return

        networks = self._coordinator.data.get("networks", [])
        if not networks:
            _LOGGER.debug("No networks found to create network-level entities.")
            return

        for network in networks:
            # Select Entities
            yield MerakiContentFilteringSelect(
                self._coordinator,
                self._coordinator.api,
                self._config_entry,
                network,
            )
            if self._config_entry.options.get(CONF_ENABLE_VPN_MANAGEMENT):
                yield MerakiVpnSelect(
                    self._coordinator,
                    self._coordinator.api,
                    self._config_entry,
                    network,
                )

            # Network Clients Sensor
            yield MerakiNetworkClientsSensor(
                coordinator=self._coordinator,
                config_entry=self._config_entry,
                network_data=network,
                network_control_service=self._network_control_service,
            )

            # Client Status Sensors
            if self._config_entry.options.get(CONF_ENABLE_CLIENT_STATUS_SENSORS, False):
                # RESOLVED: Beta branch logic - import at top of block and use list comprehension
                from ...sensor.client.status import MerakiClientStatusSensor

                clients = self._coordinator.data.get("clients", [])
                
                network_clients = [
                    c for c in clients if c.get("networkId") == network.id
                ]

                if network_clients:
                    for client in network_clients:
                        yield MerakiClientStatusSensor(
                            self._coordinator,
                            client,
                            self._config_entry,
                        )

            # Content Filtering Switch
            if "appliance" in network.product_types:
                try:
                    categories = await self._coordinator.api.appliance.get_network_appliance_content_filtering_categories(  # noqa: E501
                        network.id
                    )
                    for category in categories.get("categories", []):
                        yield MerakiContentFilteringSwitch(
                            self._coordinator,
                            self._config_entry,
                            network,
                            category,
                        )
                except Exception as e:
                    _LOGGER.warning(
                        "Could not get content filtering categories for network %s: %s",
                        network.id,
                        e,
                    )

            # Traffic Shaping Sensor
            if self._config_entry.options.get(CONF_ENABLE_TRAFFIC_SHAPING, False):
                yield TrafficShapingSensor(
                    self._coordinator,
                    self._config_entry,
                    network.id,
                )

            # VLAN Sensors
            if self._config_entry.options.get(CONF_ENABLE_VLAN_SENSORS, True):
                vlans = self._coordinator.data.get("vlans", {}).get(network.id, [])
                if vlans:
                    # Dynamically import VLAN sensors only if enabled
                    from ...sensor.network.vlan import (
                        MerakiVLANStatusSensor,
                    )
                    from ...sensor.network.vlans_list import VlansListSensor

                    yield VlansListSensor(
                        self._coordinator, self._config_entry, network
                    )

                    for vlan in vlans:
                        yield MerakiVLANStatusSensor(
                            self._coordinator,
                            self._config_entry,
                            network.id,
                            vlan,
                        )
                else:
                    _LOGGER.debug("No VLANs found for network %s", network.id)
            else:
                _LOGGER.debug("VLAN sensors are disabled.")