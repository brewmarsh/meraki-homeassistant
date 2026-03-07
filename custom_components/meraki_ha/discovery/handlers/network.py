"""Discovery handler for Network-level entities."""

from __future__ import annotations

import asyncio
import logging
from collections.abc import AsyncIterator
from typing import TYPE_CHECKING

from homeassistant.exceptions import HomeAssistantError

from ...core.errors import MerakiHAException, MerakiInformationalError

from ...const_conf import (
    CONF_ENABLE_CLIENT_STATUS_SENSORS,
    CONF_ENABLE_NETWORK_SENSORS,
    CONF_ENABLE_TRAFFIC_SHAPING,
    CONF_ENABLE_VLAN_SENSORS,
    CONF_ENABLE_VPN_MANAGEMENT,
)
from ...sensor.network.network_clients import MerakiNetworkClientsSensor
from ...sensor.network.traffic_shaping import TrafficShapingSensor
from .base import BaseHandler

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.helpers.entity import Entity

    from ...services.network_control_service import NetworkControlService
    from ...types import MerakiNetwork
    from ..coordinators import MerakiSwitchCoordinator


_LOGGER = logging.getLogger(__name__)


class NetworkHandler(BaseHandler):
    """Handler for network-level entities."""

    def __init__(
        self,
        coordinator: MerakiSwitchCoordinator,
        config_entry: ConfigEntry,
        network_control_service: NetworkControlService,
    ) -> None:
        """Initialize the NetworkHandler."""
        super().__init__(coordinator, config_entry)
        self._network_control_service = network_control_service

    def _get_networks(self) -> list[MerakiNetwork]:
        """Get the list of networks if network sensors are enabled."""
        if not self._config_entry.options.get(CONF_ENABLE_NETWORK_SENSORS, True):
            _LOGGER.debug("Network sensors are disabled.")
            return []
        return self._coordinator.data.get("networks", [])

    async def discover_entities(self) -> AsyncIterator[Entity]:
        """Discover network-level entities."""
        networks = self._get_networks()
        if asyncio.iscoroutine(networks):
            networks = await networks

        if not networks:
            _LOGGER.debug("No networks found to create network-level entities.")
            return

        generators = (
            self._discover_select_entities,
            self._discover_network_clients,
            self._discover_client_status_sensors,
            self._discover_traffic_shaping,
            self._discover_vlans,
        )

        for network in networks:
            for generator in generators:
                try:
                    async for entity in generator(network):
                        yield entity
                except MerakiInformationalError as e:
                    _LOGGER.info(
                        "Optional feature '%s' is disabled for network %s: %s",
                        generator.__name__,
                        network.id,
                        e,
                    )
                except (MerakiHAException, HomeAssistantError) as e:
                    _LOGGER.error(
                        "Error in discovery generator '%s' for network %s: %s",
                        generator.__name__,
                        network.id,
                        e,
                    )

    async def _discover_select_entities(
        self, network: MerakiNetwork
    ) -> AsyncIterator[Entity]:
        """Discover select entities (Content Filtering, VPN)."""
        from ...meraki_select.meraki_content_filtering import (
            MerakiContentFilteringSelect,
        )
        from ...meraki_select.vpn import MerakiVpnSelect

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

    async def _discover_network_clients(
        self, network: MerakiNetwork
    ) -> AsyncIterator[Entity]:
        """Discover network clients sensor."""
        yield MerakiNetworkClientsSensor(
            coordinator=self._coordinator,
            config_entry=self._config_entry,
            network_data=network,
            network_control_service=self._network_control_service,
        )

    async def _discover_client_status_sensors(
        self, network: MerakiNetwork
    ) -> AsyncIterator[Entity]:
        """Discover client status sensors."""
        if not self._config_entry.options.get(CONF_ENABLE_CLIENT_STATUS_SENSORS, False):
            return

        from ...sensor.client.status import MerakiClientStatusSensor

        clients = self._coordinator.data.get("clients")
        if not isinstance(clients, list):
            return

        for client in filter(
            lambda c: isinstance(c, dict) and c.get("networkId") == network.id,
            clients,
        ):
            yield MerakiClientStatusSensor(
                self._coordinator,
                client,
                self._config_entry,
            )

    async def _discover_traffic_shaping(
        self, network: MerakiNetwork
    ) -> AsyncIterator[Entity]:
        """Discover traffic shaping sensors."""
        is_enabled = self._config_entry.options.get(CONF_ENABLE_TRAFFIC_SHAPING, False)
        if not is_enabled or network.id is None:
            return

        yield TrafficShapingSensor(
            self._coordinator,
            self._config_entry,
            network.id,
        )

    async def _discover_vlans(self, network: MerakiNetwork) -> AsyncIterator[Entity]:
        """Discover VLAN sensors."""
        if not self._config_entry.options.get(CONF_ENABLE_VLAN_SENSORS, True):
            _LOGGER.debug("VLAN sensors are disabled.")
            return

        if network.id is None:
            return

        vlans_data = self._coordinator.data.get("vlans", {})
        if not isinstance(vlans_data, dict):
            return
        vlans = vlans_data.get(network.id, [])
        if not vlans or not isinstance(vlans, list):
            _LOGGER.debug("No VLANs found for network %s", network.id)
            return

        from ...sensor.network.vlan import MerakiVLANStatusSensor
        from ...sensor.network.vlans_list import VlansListSensor

        yield VlansListSensor(self._coordinator, self._config_entry, network)

        for vlan in vlans:
            if not vlan:
                continue
            yield MerakiVLANStatusSensor(
                self._coordinator,
                self._config_entry,
                network.id,
                vlan,
            )
