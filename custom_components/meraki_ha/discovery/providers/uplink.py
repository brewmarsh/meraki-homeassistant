"""Uplink Providers."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import PERCENTAGE, UnitOfTime
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import entity_registry as er

from ...const import DOMAIN
from ...const_conf import CONF_ENABLE_PORT_SENSORS
from ...sensor.device.appliance_uplink import MerakiApplianceUplinkSensor
from ...sensor.uplink_performance import MerakiUplinkPerformanceSensor

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.helpers.entity import Entity

    from ...coordinator import MerakiDataUpdateCoordinator
    from ...core.models.device import MerakiDevice

_LOGGER = logging.getLogger(__name__)


class UplinkProvider:
    """Provider for appliance uplink entities."""

    @staticmethod
    def get_entities(
        coordinator: MerakiDataUpdateCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
        **kwargs: Any,
    ) -> list[Entity]:
        """Get entities."""
        if not config_entry.options.get(CONF_ENABLE_PORT_SENSORS, True):
            return []

        if not device.serial:
            return []

        entities: list[Entity] = []
        uplink_data_by_interface: dict[str, dict[str, Any]] = {}
        if device.appliance_uplink_statuses:
            for uplink in device.appliance_uplink_statuses:
                if interface := uplink.get("interface"):
                    uplink_data_by_interface[interface] = uplink

        # Logic to identify interfaces from registry
        registry_interfaces = set()
        hass = coordinator.hass
        if hass:
            ent_reg = er.async_get(hass)
            dev_reg = dr.async_get(hass)
            device_entry = dev_reg.async_get_device(
                identifiers={(DOMAIN, device.serial)}
            )
            if device_entry:
                reg_entities = er.async_entries_for_device(ent_reg, device_entry.id)
                for ent in reg_entities:
                    if ent.unique_id and ent.unique_id.startswith(
                        f"{device.serial}_uplink_"
                    ):
                        interface = ent.unique_id.replace(
                            f"{device.serial}_uplink_", ""
                        )
                        registry_interfaces.add(interface)

        all_interfaces = set(uplink_data_by_interface.keys()) | registry_interfaces
        for interface in all_interfaces:
            uplink_data = uplink_data_by_interface.get(interface) or {
                "interface": interface
            }
            entities.append(
                MerakiApplianceUplinkSensor(
                    coordinator, device, config_entry, uplink_data
                )
            )
        return entities


class UplinkPerformanceProvider:
    """Provider for appliance uplink performance entities."""

    @staticmethod
    def get_entities(
        coordinator: MerakiDataUpdateCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
        **kwargs: Any,
    ) -> list[Entity]:
        """Get entities."""
        if not config_entry.options.get(CONF_ENABLE_PORT_SENSORS, True):
            return []

        if not device.serial:
            return []

        entities: list[Entity] = []
        # Use uplinks field which contains merged status and performance data
        if not device.uplinks:
            return []

        for uplink in device.uplinks:
            interface = uplink.get("interface")
            if not interface:
                continue

            # Latency Sensor
            entities.append(
                MerakiUplinkPerformanceSensor(
                    coordinator,
                    device,
                    config_entry,
                    interface,
                    "latencyMs",
                    SensorEntityDescription(
                        key=f"{interface}_latency",
                        name=f"{interface.capitalize()} latency",
                        native_unit_of_measurement=UnitOfTime.MILLISECONDS,
                        device_class=SensorDeviceClass.DURATION,
                        state_class=SensorStateClass.MEASUREMENT,
                        icon="mdi:timer-outline",
                    ),
                )
            )

            # Loss Sensor
            entities.append(
                MerakiUplinkPerformanceSensor(
                    coordinator,
                    device,
                    config_entry,
                    interface,
                    "lossPercent",
                    SensorEntityDescription(
                        key=f"{interface}_packet_loss",
                        name=f"{interface.capitalize()} packet loss",
                        native_unit_of_measurement=PERCENTAGE,
                        state_class=SensorStateClass.MEASUREMENT,
                        icon="mdi:packet-loss",
                    ),
                )
            )

            # Jitter Sensor
            entities.append(
                MerakiUplinkPerformanceSensor(
                    coordinator,
                    device,
                    config_entry,
                    interface,
                    "jitter",
                    SensorEntityDescription(
                        key=f"{interface}_jitter",
                        name=f"{interface.capitalize()} jitter",
                        native_unit_of_measurement=UnitOfTime.MILLISECONDS,
                        device_class=SensorDeviceClass.DURATION,
                        state_class=SensorStateClass.MEASUREMENT,
                        icon="mdi:pulse",
                    ),
                )
            )

        return entities
