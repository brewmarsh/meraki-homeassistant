"""
Network Handler.

This module defines the NetworkHandler class, which is responsible for
discovering and creating network-level entities.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ...const import CONF_ENABLE_NETWORK_SENSORS, CONF_ENABLE_VLAN_SENSORS
from ...helpers.logging_helper import MerakiLoggers
from ...sensor.network.meraki_network_info import MerakiNetworkInfoSensor
from ...sensor.network.network_clients import MerakiNetworkClientsSensor
from ...sensor.network.network_identity import MerakiNetworkIdentitySensor
from ...switch.content_filtering import MerakiContentFilteringSwitch
from .base import BaseHandler

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.helpers.entity import Entity

    from ...meraki_data_coordinator import MerakiDataCoordinator
    from ...services.camera_service import CameraService
    from ...services.device_control_service import DeviceControlService
    from ...services.network_control_service import NetworkControlService
    from ...types import MerakiDevice


_LOGGER = MerakiLoggers.DISCOVERY


class NetworkHandler(BaseHandler):
    """Handler for network-level entities."""

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        config_entry: ConfigEntry,
        network_control_service: NetworkControlService,
    ) -> None:
        """Initialize the NetworkHandler."""
        super().__init__(coordinator, config_entry)
        self._network_control_service = network_control_service

    @classmethod
    def create(
        cls,
        coordinator: MerakiDataCoordinator,
        device: MerakiDevice | None,
        config_entry: ConfigEntry,
        camera_service: CameraService,
        control_service: DeviceControlService,
        network_control_service: NetworkControlService,
    ) -> NetworkHandler:
        """Create an instance of the handler."""
        return cls(
            coordinator,
            config_entry,
            network_control_service,
        )

    async def discover_entities(self) -> list[Entity]:
        """Discover network-level entities."""
        entities: list[Entity] = []

        # Check if network sensors are enabled
        if not self._config_entry.options.get(CONF_ENABLE_NETWORK_SENSORS, True):
            return entities

        networks = self._coordinator.data.get("networks", [])
        if not networks:
            _LOGGER.debug("No networks found to create network-level entities.")
            return entities

        for network in networks:
            # Network clients sensor
            entities.append(
                MerakiNetworkClientsSensor(
                    coordinator=self._coordinator,
                    config_entry=self._config_entry,
                    network_data=network,
                    network_control_service=self._network_control_service,
                )
            )
            # Network identity sensor
            entities.append(
                MerakiNetworkIdentitySensor(
                    coordinator=self._coordinator,
                    network_data=network,
                    config_entry=self._config_entry,
                )
            )
            # Network info sensor
            entities.append(
                MerakiNetworkInfoSensor(
                    coordinator=self._coordinator,
                    network_data=network,
                    config_entry=self._config_entry,
                )
            )
            if "appliance" in network.get("productTypes", []):
                try:
                    categories = await self._coordinator.api.appliance.get_network_appliance_content_filtering_categories(  # noqa: E501
                        network["id"]
                    )
                    for category in categories.get("categories", []):
                        entities.append(
                            MerakiContentFilteringSwitch(
                                self._coordinator,
                                self._config_entry,
                                network,
                                category,
                            )
                        )
                except Exception as e:
                    _LOGGER.warning(
                        "Could not get content filtering categories for network %s: %s",
                        network["id"],
                        e,
                    )

            # VLAN Sensors
            if self._config_entry.options.get(CONF_ENABLE_VLAN_SENSORS, True):
                vlans = self._coordinator.data.get("vlans", {}).get(network["id"], [])
                if vlans:
                    from ...sensor.network.vlan import (
                        MerakiVLANIDSensor,
                        MerakiVLANIPv4EnabledSensor,
                        MerakiVLANIPv4InterfaceSensor,
                        MerakiVLANIPv4UplinkSensor,
                        MerakiVLANIPv6EnabledSensor,
                        MerakiVLANIPv6InterfaceSensor,
                        MerakiVLANIPv6UplinkSensor,
                    )

                    for vlan in vlans:
                        entities.extend(
                            [
                                MerakiVLANIDSensor(
                                    self._coordinator,
                                    self._config_entry,
                                    network["id"],
                                    vlan,
                                ),
                                MerakiVLANIPv4EnabledSensor(
                                    self._coordinator,
                                    self._config_entry,
                                    network["id"],
                                    vlan,
                                ),
                                MerakiVLANIPv4InterfaceSensor(
                                    self._coordinator,
                                    self._config_entry,
                                    network["id"],
                                    vlan,
                                ),
                                MerakiVLANIPv4UplinkSensor(
                                    self._coordinator,
                                    self._config_entry,
                                    network["id"],
                                    vlan,
                                ),
                                MerakiVLANIPv6EnabledSensor(
                                    self._coordinator,
                                    self._config_entry,
                                    network["id"],
                                    vlan,
                                ),
                                MerakiVLANIPv6InterfaceSensor(
                                    self._coordinator,
                                    self._config_entry,
                                    network["id"],
                                    vlan,
                                ),
                                MerakiVLANIPv6UplinkSensor(
                                    self._coordinator,
                                    self._config_entry,
                                    network["id"],
                                    vlan,
                                ),
                            ]
                        )
                else:
                    _LOGGER.debug("No VLANs found for network %s", network["id"])
            else:
                _LOGGER.debug("VLAN sensors are disabled.")

        _LOGGER.info("Discovered %d network-level entities", len(entities))
        return entities
