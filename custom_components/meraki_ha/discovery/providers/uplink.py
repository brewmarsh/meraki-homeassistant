"""Provider for appliance uplink entities."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Literal, cast

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

    from ...core.models.device import MerakiDevice
    from ..coordinators import MerakiApplianceCoordinator

_LOGGER = logging.getLogger(__name__)


def _get_uplink_data_by_interface(device: MerakiDevice) -> dict[str, dict[str, Any]]:
    """Extract uplink data indexed by interface."""
    uplink_data_by_interface: dict[str, dict[str, Any]] = {}
    if not device.appliance_uplink_statuses:
        return uplink_data_by_interface
    for uplink in device.appliance_uplink_statuses:
        if interface := uplink.get("interface"):
            uplink_data_by_interface[interface] = uplink
    return uplink_data_by_interface


def _get_entities_for_device(hass: Any, device_serial: str) -> list[er.RegistryEntry]:
    """Helper to get all entities for a device."""
    ent_reg = er.async_get(hass)
    dev_reg = dr.async_get(hass)
    device_entry = dev_reg.async_get_device(identifiers={(DOMAIN, device_serial)})

    if not device_entry:
        return []

    return er.async_entries_for_device(ent_reg, device_entry.id)


def _get_registry_interfaces(
    coordinator: MerakiApplianceCoordinator, device: MerakiDevice
) -> set[str]:
    """Reconcile interfaces from the Entity Registry to prevent orphan sensors."""
    registry_interfaces: set[str] = set()
    hass = coordinator.hass
    if not hass:
        return registry_interfaces

    reg_entities = _get_entities_for_device(hass, device.serial)

    prefix = f"{device.serial}_uplink_"
    for ent in reg_entities:
        if ent.unique_id and ent.unique_id.startswith(prefix):
            interface = ent.unique_id.replace(prefix, "")
            registry_interfaces.add(interface)

    return registry_interfaces


def _create_performance_entities(
    coordinator: MerakiApplianceCoordinator,
    device: MerakiDevice,
    config_entry: ConfigEntry,
    interface: str,
) -> list[Entity]:
    """Create performance entities for a single interface."""
    entities: list[Entity] = []
    perf_metrics = [
        (
            "latency",
            "latency",
            UnitOfTime.MILLISECONDS,
            SensorDeviceClass.DURATION,
            "mdi:timer-outline",
        ),
        ("lossPercent", "packet_loss", PERCENTAGE, None, "mdi:packet-loss"),
        (
            "jitter",
            "jitter",
            UnitOfTime.MILLISECONDS,
            SensorDeviceClass.DURATION,
            "mdi:pulse",
        ),
    ]

    for attr, key_suffix, unit, dev_class, icon in perf_metrics:
        metric_type = cast(Literal["latency", "jitter", "lossPercent"], attr)
        entities.append(
            MerakiUplinkPerformanceSensor(
                coordinator,
                device,
                config_entry,
                interface,
                metric_type,
                SensorEntityDescription(
                    key=f"{interface}_{key_suffix}",
                    name=f"{interface.capitalize()} {key_suffix.replace('_', ' ')}",
                    native_unit_of_measurement=unit,
                    device_class=dev_class,
                    state_class=SensorStateClass.MEASUREMENT,
                    icon=icon,
                ),
            )
        )
    return entities


def _should_skip_entities(config_entry: ConfigEntry, device: MerakiDevice) -> bool:
    """Check if sensor creation should be skipped."""
    if not config_entry.options.get(CONF_ENABLE_PORT_SENSORS, True):
        return True
    return not bool(device.serial)


def _get_uplinks_from_device(device: MerakiDevice) -> list[dict[str, Any]]:
    """Get uplinks from device."""
    if not device.uplinks:
        return []
    return device.uplinks


class UplinkProvider:
    """Provider for appliance uplink entities."""

    @staticmethod
    def get_entities(
        coordinator: MerakiApplianceCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
        **kwargs: Any,
    ) -> list[Entity]:
        """Get entities for appliance uplinks."""
        if _should_skip_entities(config_entry, device):
            return []

        uplink_data_by_interface = _get_uplink_data_by_interface(device)
        registry_interfaces = _get_registry_interfaces(coordinator, device)

        entities: list[Entity] = []
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
        coordinator: MerakiApplianceCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
        **kwargs: Any,
    ) -> list[Entity]:
        """Get entities for uplink performance (Latency, Loss, Jitter)."""
        if _should_skip_entities(config_entry, device):
            return []

        entities: list[Entity] = []

        for uplink in _get_uplinks_from_device(device):
            if interface := uplink.get("interface"):
                entities.extend(
                    _create_performance_entities(
                        coordinator, device, config_entry, interface
                    )
                )

        return entities
