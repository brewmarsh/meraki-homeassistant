"""Discovery providers for Meraki devices."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import PERCENTAGE, EntityCategory, UnitOfTime
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import entity_registry as er

from ..binary_sensor.device.appliance_port import AppliancePortBinarySensor
from ..binary_sensor.device.camera_motion import MerakiMotionSensor
from ..binary_sensor.device.switch_port import SwitchPortSensor
from ..button.device.camera_snapshot import MerakiSnapshotButton
from ..button.device.poe_cycle import MerakiPoECycleButton
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
from ..sensor.device.network_settings import (
    MerakiDeviceDNSSensor,
    MerakiDeviceGatewaySensor,
    MerakiDeviceIPSensor,
)
from ..sensor.device.rtsp_url import MerakiRtspUrlSensor
from ..sensor.device.switch_poe import MerakiSwitchPoESensor
from ..sensor.device.switch_port import (
    MerakiSwitchPortEnergySensor,
    MerakiSwitchPortPowerSensor,
    MerakiSwitchPortSensor,
)
from ..sensor.device.wireless_radio import MerakiWirelessRadioSensor
from ..sensor.uplink_performance import MerakiUplinkPerformanceSensor
from ..switch.camera_controls import AnalyticsSwitch
from ..switch.switch_port import MerakiAppliancePortSwitch, MerakiSwitchPortToggle

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
                entities.append(AppliancePortBinarySensor(coordinator, device, port))
                entities.append(
                    MerakiAppliancePortSwitch(coordinator, device, port, config_entry)
                )
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
                entities.append(
                    MerakiSwitchPortSensor(coordinator, device, port, config_entry)
                )
                entities.append(
                    MerakiSwitchPortPowerSensor(coordinator, device, port, config_entry)
                )
                entities.append(
                    MerakiSwitchPortEnergySensor(
                        coordinator, device, port, config_entry
                    )
                )
                if (
                    port.get("powerUsageInWh") is not None
                    or port.get("powerUsage") is not None
                ):
                    entities.append(
                        MerakiSwitchPoESensor(coordinator, device, port, config_entry)
                    )
                # RESOLVED: Updated constructor to include config_entry per beta branch
                entities.append(
                    MerakiSwitchPortToggle(coordinator, device, port, config_entry)
                )
                entities.append(
                    MerakiPoECycleButton(coordinator, device, port, config_entry)
                )
        return entities


class WirelessRadioProvider:
    """Provider for wireless radio entities."""

    @staticmethod
    def get_entities(
        coordinator: MerakiDataUpdateCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
        **kwargs: Any,
    ) -> list[Entity]:
        """Get entities."""
        if not device.serial or not device.wireless_radio_settings:
            return []

        entities: list[Entity] = []
        settings = device.wireless_radio_settings

        # 2.4GHz Channel
        if "twoFourGhzSettings" in settings:
            entities.append(
                MerakiWirelessRadioSensor(
                    coordinator,
                    device,
                    config_entry,
                    SensorEntityDescription(
                        key="2.4ghz_channel",
                        name="2.4GHz channel",
                        icon="mdi:wifi",
                        entity_category=EntityCategory.DIAGNOSTIC,
                    ),
                    "twoFourGhzSettings",
                    "channel",
                )
            )

        # 5GHz Channel
        if "fiveGhzSettings" in settings:
            entities.append(
                MerakiWirelessRadioSensor(
                    coordinator,
                    device,
                    config_entry,
                    SensorEntityDescription(
                        key="5ghz_channel",
                        name="5GHz channel",
                        icon="mdi:wifi",
                        entity_category=EntityCategory.DIAGNOSTIC,
                    ),
                    "fiveGhzSettings",
                    "channel",
                )
            )

        # 2.4GHz Target Power
        if "twoFourGhzSettings" in settings:
            entities.append(
                MerakiWirelessRadioSensor(
                    coordinator,
                    device,
                    config_entry,
                    SensorEntityDescription(
                        key="2.4ghz_target_power",
                        name="2.4GHz target power",
                        native_unit_of_measurement="dBm",
                        icon="mdi:transmission-tower",
                        entity_category=EntityCategory.DIAGNOSTIC,
                    ),
                    "twoFourGhzSettings",
                    "targetPower",
                )
            )

        # 5GHz Target Power (Generic "Target power" sensor for backward
        # compatibility/requested name)
        if "fiveGhzSettings" in settings:
            entities.append(
                MerakiWirelessRadioSensor(
                    coordinator,
                    device,
                    config_entry,
                    SensorEntityDescription(
                        key="target_power",
                        name="Target power",
                        native_unit_of_measurement="dBm",
                        icon="mdi:transmission-tower",
                        entity_category=EntityCategory.DIAGNOSTIC,
                    ),
                    "fiveGhzSettings",
                    "targetPower",
                )
            )

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


class PhysicalSensorProvider:
    """Provider for physical device sensors (IP, Status, Diagnostics)."""

    @staticmethod
    def get_entities(
        coordinator: MerakiDataUpdateCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
        **kwargs: Any,
    ) -> list[Entity]:
        """Get entities."""
        entities: list[Entity] = []

        # Standard IPs
        entities.append(
            MerakiDeviceIPSensor(coordinator, device, config_entry, "lanIp", "LAN IP")
        )
        entities.append(
            MerakiDeviceIPSensor(
                coordinator, device, config_entry, "publicIp", "Public IP"
            )
        )

        # Diagnostics (IP/Gateway/DNS) from uplinks
        if device.uplinks:
            for uplink in device.uplinks:
                interface = uplink.get("interface")
                if interface:
                    entities.append(
                        MerakiDeviceIPSensor(
                            coordinator, device, config_entry, interface
                        )
                    )
                    entities.append(
                        MerakiDeviceGatewaySensor(
                            coordinator, device, config_entry, interface
                        )
                    )
                    entities.append(
                        MerakiDeviceDNSSensor(
                            coordinator, device, config_entry, interface
                        )
                    )

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
