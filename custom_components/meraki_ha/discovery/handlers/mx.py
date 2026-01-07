"""Discovery handler for MX devices."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import entity_registry as er

from ...button.reboot import MerakiRebootButton
from ...const import CONF_ENABLE_DEVICE_STATUS, CONF_ENABLE_PORT_SENSORS, DOMAIN
from ...sensor.device.appliance_port import MerakiAppliancePortSensor
from ...sensor.device.appliance_uplink import MerakiApplianceUplinkSensor
from ...sensor.device.connected_clients import MerakiDeviceConnectedClientsSensor
from ...sensor.device.data_usage import MerakiDataUsageSensor
from ...sensor.device.device_status import MerakiDeviceStatusSensor
from ...sensor.device.meraki_firmware_status import MerakiFirmwareStatusSensor
from ...sensor.device.meraki_wan1_connectivity import MerakiWAN1ConnectivitySensor
from ...sensor.device.meraki_wan2_connectivity import MerakiWAN2ConnectivitySensor
from .base import BaseDeviceHandler

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.helpers.entity import Entity

    from ...meraki_data_coordinator import MerakiDataCoordinator
    from ...services.camera_service import CameraService
    from ...services.device_control_service import DeviceControlService
    from ...services.network_control_service import NetworkControlService
    from ...types import MerakiDevice


_LOGGER = logging.getLogger(__name__)


class MXHandler(BaseDeviceHandler):
    """Handler for MX series security appliances."""

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
        control_service: DeviceControlService,
        network_control_service: NetworkControlService,
    ) -> None:
        """Initialize the MXHandler."""
        super().__init__(coordinator, device, config_entry)
        self._control_service = control_service
        self._network_control_service = network_control_service

    @classmethod
    def create(
        cls,
        coordinator: MerakiDataCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
        camera_service: CameraService,
        control_service: DeviceControlService,
        network_control_service: NetworkControlService,
    ) -> MXHandler:
        """Create an instance of the handler."""
        return cls(
            coordinator,
            device,
            config_entry,
            control_service,
            network_control_service,
        )

    async def discover_entities(self) -> list[Entity]:
        """Discover entities for the device."""
        entities: list[Entity] = []
        entities.append(
            MerakiRebootButton(self._control_service, self.device, self._config_entry)
        )

        # Check if device status sensor is enabled
        if self._config_entry.options.get(CONF_ENABLE_DEVICE_STATUS, True):
            entities.append(
                MerakiDeviceStatusSensor(
                    self._coordinator, self.device, self._config_entry
                )
            )

        # Connected clients sensor
        entities.append(
            MerakiDeviceConnectedClientsSensor(
                self._coordinator, self.device, self._config_entry
            )
        )

        # WAN connectivity sensors
        entities.append(
            MerakiWAN1ConnectivitySensor(
                self._coordinator, self.device, self._config_entry
            )
        )
        entities.append(
            MerakiWAN2ConnectivitySensor(
                self._coordinator, self.device, self._config_entry
            )
        )

        # Firmware status sensor
        entities.append(
            MerakiFirmwareStatusSensor(
                self._coordinator, self.device, self._config_entry
            )
        )

        # Data usage sensor
        entities.append(
            MerakiDataUsageSensor(self._coordinator, self.device, self._config_entry)
        )

        # Check if port/uplink sensors are enabled
        if self._config_entry.options.get(CONF_ENABLE_PORT_SENSORS, True):
            # Collect data from API
            uplink_data_by_interface: dict[str, dict[str, Any]] = {}
            if self._coordinator.data and self._coordinator.data.get(
                "appliance_uplink_statuses"
            ):
                for status in self._coordinator.data["appliance_uplink_statuses"]:
                    if status.get("serial") == self.device["serial"]:
                        for uplink in status.get("uplinks", []):
                            if interface := uplink.get("interface"):
                                uplink_data_by_interface[interface] = uplink

            # Identify interfaces from existing entities in the registry
            # to handle cases where API data is temporarily missing.
            registry_interfaces = set()
            ent_reg = er.async_get(self._coordinator.hass)
            dev_reg = dr.async_get(self._coordinator.hass)

            device_entry = dev_reg.async_get_device(
                identifiers={(DOMAIN, self.device["serial"])}
            )
            if device_entry:
                reg_entities = er.async_entries_for_device(ent_reg, device_entry.id)
                for ent in reg_entities:
                    # Check if it looks like an uplink sensor
                    # Format: {serial}_uplink_{interface}
                    if ent.unique_id and ent.unique_id.startswith(
                        f"{self.device['serial']}_uplink_"
                    ):
                        interface = ent.unique_id.replace(
                            f"{self.device['serial']}_uplink_", ""
                        )
                        registry_interfaces.add(interface)

            # Combine interfaces from API and registry
            all_interfaces = set(uplink_data_by_interface.keys()) | registry_interfaces

            for interface in all_interfaces:
                uplink_data = uplink_data_by_interface.get(interface)
                if not uplink_data:
                    # Construct dummy data if missing from API
                    uplink_data = {"interface": interface}

                entities.append(
                    MerakiApplianceUplinkSensor(
                        coordinator=self._coordinator,
                        device_data=self.device,
                        config_entry=self._config_entry,
                        uplink_data=uplink_data,
                    )
                )

            # Add appliance port sensors (LAN ports)
            ports: list[dict[str, Any]] = self.device.get("ports", [])  # type: ignore[assignment]
            for port in ports:
                entities.append(
                    MerakiAppliancePortSensor(
                        coordinator=self._coordinator,
                        device=self.device,
                        port=port,
                    )
                )
        else:
            _LOGGER.debug(
                "Uplink sensors disabled for device %s", self.device.get("serial")
            )

        return entities
