"""Discovery providers for Meraki devices."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import entity_registry as er

from ..binary_sensor.device.camera_motion import MerakiMotionSensor
from ..binary_sensor.switch_port import SwitchPortSensor
from ..button.device.camera_snapshot import MerakiSnapshotButton
from ..camera import MerakiCamera
from ..const import DOMAIN
from ..const_conf import (
    CONF_ENABLE_CAMERA_ENTITIES,
    CONF_ENABLE_PORT_SENSORS,
    CONF_RTSP_STREAM_ENABLED,
)
from ..core.errors import MerakiInformationalError
from ..descriptions import (
    MT_CURRENT_DESCRIPTION,
    MT_ENERGY_DESCRIPTION,
    MT_FREQUENCY_DESCRIPTION,
    MT_POWER_DESCRIPTION,
    MT_POWER_FACTOR_DESCRIPTION,
    MT_VOLTAGE_DESCRIPTION,
)
from ..sensor.device.appliance_port import MerakiAppliancePortSensor
from ..sensor.device.appliance_uplink import MerakiApplianceUplinkSensor
from ..sensor.device.camera_analytics import (
    MerakiPersonCountSensor,
    MerakiVehicleCountSensor,
)
from ..sensor.device.meraki_mt_base import MerakiMtSensor
from ..sensor.device.rtsp_url import MerakiRtspUrlSensor
from ..switch.camera_controls import AnalyticsSwitch

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.helpers.entity import Entity

    from ..coordinator import MerakiDataUpdateCoordinator
    from ..core.models.device import MerakiDevice
    from ..services.camera_service import CameraService

_LOGGER = logging.getLogger(__name__)


class MT40PowerMonitorProvider:
    """Provider for MT40 power monitoring entities."""

    @staticmethod
    def get_entities(
        coordinator: MerakiDataUpdateCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
        **kwargs: Any,
    ) -> list[Entity]:
        """Get entities."""
        descriptions = [
            MT_POWER_DESCRIPTION,
            MT_VOLTAGE_DESCRIPTION,
            MT_CURRENT_DESCRIPTION,
            MT_POWER_FACTOR_DESCRIPTION,
            MT_FREQUENCY_DESCRIPTION,
            MT_ENERGY_DESCRIPTION,
        ]
        return [MerakiMtSensor(coordinator, device, desc) for desc in descriptions]


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


class AppliancePortProvider:
    """Provider for appliance port entities."""

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
        entities: list[Entity] = []
        if device.appliance_ports:
            for port in device.appliance_ports:
                entities.append(MerakiAppliancePortSensor(coordinator, device, port))
        return entities


class SwitchPortProvider:
    """Provider for switch port entities."""

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
        entities: list[Entity] = []
        if device.ports_statuses:
            for port in device.ports_statuses:
                entities.append(SwitchPortSensor(coordinator, device, port))
        return entities


class CameraAnalyticsProvider:
    """Provider for camera analytics entities."""

    @staticmethod
    async def get_entities(
        coordinator: MerakiDataUpdateCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
        **kwargs: Any,
    ) -> list[Entity]:
        """Get entities."""
        camera_service: CameraService | None = kwargs.get("camera_service")
        if not camera_service or not device.serial:
            return []

        entities: list[Entity] = []
        try:
            features = await camera_service.get_supported_analytics(device.serial)
            if "person_detection" in features:
                entities.append(MerakiPersonCountSensor(coordinator, device))
            if "vehicle_detection" in features:
                entities.append(MerakiVehicleCountSensor(coordinator, device))
        except Exception:
            _LOGGER.debug("Could not fetch analytics features for %s", device.serial)

        return entities


class CameraStreamProvider:
    """Provider for camera stream entities."""

    @staticmethod
    async def get_entities(
        coordinator: MerakiDataUpdateCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
        **kwargs: Any,
    ) -> list[Entity]:
        """Get entities."""
        camera_service: CameraService | None = kwargs.get("camera_service")
        if not camera_service or not device.serial:
            return []

        # If configured, ensure the RTSP stream is enabled by default for cameras
        if config_entry.options.get(CONF_RTSP_STREAM_ENABLED, False):
            try:
                _LOGGER.debug(
                    "RTSP stream is defaulted to on, enabling for camera %s",
                    device.serial,
                )
                await camera_service.async_set_rtsp_stream_enabled(device.serial, True)
            except MerakiInformationalError as e:
                _LOGGER.warning(
                    "Could not enable RTSP stream for %s: %s", device.serial, e
                )
                coordinator.add_status_message(
                    device.serial, f"Could not enable RTSP stream: {e}"
                )

        if not config_entry.options.get(CONF_ENABLE_CAMERA_ENTITIES, True):
            return []

        return [
            MerakiCamera(
                coordinator,
                config_entry,
                device,
                camera_service,
            ),
            MerakiMotionSensor(
                coordinator,
                device,
                camera_service,
                config_entry,
            ),
            MerakiSnapshotButton(
                coordinator,
                device,
                camera_service,
                config_entry,
            ),
            MerakiRtspUrlSensor(
                coordinator,
                device,
                config_entry,
            ),
            AnalyticsSwitch(coordinator, coordinator.api, device),
        ]
