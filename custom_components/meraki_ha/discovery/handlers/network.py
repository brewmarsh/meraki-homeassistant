"""
Network Handler.

This module defines the NetworkHandler class, which is responsible for
discovering and creating network-level entities.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from ...sensor.network.network_clients import MerakiNetworkClientsSensor
from ...switch.content_filtering import MerakiContentFilteringSwitch
from .base import BaseHandler

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.helpers.entity import Entity

<<<<<<< HEAD
    from ....core.coordinators.switch_port_status_coordinator import (
        SwitchPortStatusCoordinator,
    )
    from ....services.camera_service import CameraService
    from ....services.device_control_service import DeviceControlService
    from ....types import MerakiDevice
    from ...coordinator import MerakiDataUpdateCoordinator
=======
<<<<<<< HEAD
    from ....core.coordinators.switch_port_status_coordinator import (
        SwitchPortStatusCoordinator,
    )
    from ....services.camera_service import CameraService
    from ....services.device_control_service import DeviceControlService
    from ....types import MerakiDevice
    from ...coordinator import MerakiDataUpdateCoordinator
=======
    from ....services.camera_service import CameraService
    from ....services.device_control_service import DeviceControlService
    from ....types import MerakiDevice
    from ...meraki_data_coordinator import MerakiDataCoordinator
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
    from ...services.network_control_service import NetworkControlService


_LOGGER = logging.getLogger(__name__)


class NetworkHandler(BaseHandler):
    """Handler for network-level entities."""

    def __init__(
        self,
<<<<<<< HEAD
        coordinator: MerakiDataUpdateCoordinator,
=======
<<<<<<< HEAD
        coordinator: MerakiDataUpdateCoordinator,
=======
        coordinator: MerakiDataCoordinator,
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
        config_entry: ConfigEntry,
        network_control_service: NetworkControlService,
    ) -> None:
        """Initialize the NetworkHandler."""
        super().__init__(coordinator, config_entry)
        self._network_control_service = network_control_service

    @classmethod
    def create(
        cls,
<<<<<<< HEAD
        coordinator: MerakiDataUpdateCoordinator,
=======
<<<<<<< HEAD
        coordinator: MerakiDataUpdateCoordinator,
=======
        coordinator: MerakiDataCoordinator,
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
        device: MerakiDevice,
        config_entry: ConfigEntry,
        camera_service: CameraService,
        control_service: DeviceControlService,
        network_control_service: NetworkControlService,
<<<<<<< HEAD
        switch_port_coordinator: SwitchPortStatusCoordinator,
=======
<<<<<<< HEAD
        switch_port_coordinator: SwitchPortStatusCoordinator,
=======
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
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
        networks = self._coordinator.data.get("networks", [])
        if not networks:
            _LOGGER.debug("No networks found to create network-level entities.")
            return entities

        for network in networks:
            entities.append(
                MerakiNetworkClientsSensor(
                    coordinator=self._coordinator,
                    config_entry=self._config_entry,
                    network_data=network,
                    network_control_service=self._network_control_service,
                )
            )
            if "appliance" in network.get("productTypes", []):
                try:
<<<<<<< HEAD
                    categories = await self._coordinator.meraki_client.appliance.get_network_appliance_content_filtering_categories(  # noqa: E501
=======
<<<<<<< HEAD
                    categories = await self._coordinator.meraki_client.appliance.get_network_appliance_content_filtering_categories(  # noqa: E501
=======
                    categories = await self._coordinator.api.appliance.get_network_appliance_content_filtering_categories(  # noqa: E501
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
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

        _LOGGER.info("Discovered %d network-level entities", len(entities))
        return entities
