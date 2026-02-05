"""Universal Discovery Handler for Meraki devices."""

from __future__ import annotations

import logging
from collections.abc import AsyncIterator
from typing import TYPE_CHECKING, Any

from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import entity_registry as er

from ...binary_sensor.device.camera_motion import MerakiMotionSensor
from ...binary_sensor.device.meraki_mt_binary_base import MerakiMtBinarySensor
from ...binary_sensor.switch_port import SwitchPortSensor
from ...button.device.camera_snapshot import MerakiSnapshotButton
from ...button.reboot import MerakiRebootButton
from ...camera import MerakiCamera
from ...const import DOMAIN
from ...const_conf import (
    CONF_ENABLE_CAMERA_ENTITIES,
    CONF_ENABLE_DEVICE_SENSORS,
    CONF_ENABLE_DEVICE_STATUS,
    CONF_ENABLE_PORT_SENSORS,
    CONF_RTSP_STREAM_ENABLED,
)
from ...core.const import DEFAULT_CAPS, DEVICE_CAPABILITIES
from ...core.errors import MerakiInformationalError
from ...descriptions import (
    MT_BATTERY_DESCRIPTION,
    MT_BUTTON_DESCRIPTION,
    MT_CO2_DESCRIPTION,
    MT_CURRENT_DESCRIPTION,
    MT_DOOR_DESCRIPTION,
    MT_ENERGY_DESCRIPTION,
    MT_FREQUENCY_DESCRIPTION,
    MT_HUMIDITY_DESCRIPTION,
    MT_NOISE_DESCRIPTION,
    MT_PM25_DESCRIPTION,
    MT_POWER_DESCRIPTION,
    MT_POWER_FACTOR_DESCRIPTION,
    MT_SIGNAL_STRENGTH_DESCRIPTION,
    MT_TEMPERATURE_DESCRIPTION,
    MT_TVOC_DESCRIPTION,
    MT_VOLTAGE_DESCRIPTION,
    MT_WATER_DESCRIPTION,
)
from ...sensor.device.appliance_port import MerakiAppliancePortSensor
from ...sensor.device.appliance_uplink import MerakiApplianceUplinkSensor
from ...sensor.device.camera_analytics import (
    MerakiPersonCountSensor,
    MerakiVehicleCountSensor,
)
from ...sensor.device.device_status import MerakiDeviceStatusSensor
from ...sensor.device.meraki_mt_base import MerakiMtSensor
from ...sensor.device.poe_usage import MerakiPoeUsageSensor
from ...sensor.device.rtsp_url import MerakiRtspUrlSensor
from ...switch.camera_controls import AnalyticsSwitch
from ...switch.mt40_power_outlet import MerakiMt40PowerOutlet
from .base import BaseDeviceHandler

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.helpers.entity import Entity

    from ....coordinator import MerakiDataUpdateCoordinator
    from ....core.models.device import MerakiDevice
    from ....services.camera_service import CameraService
    from ....services.device_control_service import DeviceControlService
    from ....services.network_control_service import NetworkControlService


_LOGGER = logging.getLogger(__name__)


class MerakiTemperatureSensor(MerakiMtSensor):
    """Temperature sensor."""

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator, device, MT_TEMPERATURE_DESCRIPTION)


class MerakiHumiditySensor(MerakiMtSensor):
    """Humidity sensor."""

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator, device, MT_HUMIDITY_DESCRIPTION)


class MerakiBatterySensor(MerakiMtSensor):
    """Battery sensor."""

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator, device, MT_BATTERY_DESCRIPTION)


class MerakiSignalStrengthSensor(MerakiMtSensor):
    """Signal strength sensor."""

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator, device, MT_SIGNAL_STRENGTH_DESCRIPTION)


class MerakiCO2Sensor(MerakiMtSensor):
    """CO2 sensor."""

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator, device, MT_CO2_DESCRIPTION)


class MerakiButtonPressSensor(MerakiMtSensor):
    """Button press sensor."""

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator, device, MT_BUTTON_DESCRIPTION)


class MerakiWaterSensor(MerakiMtBinarySensor):
    """Water leak sensor."""

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator, device, MT_WATER_DESCRIPTION)


class MerakiDoorSensor(MerakiMtBinarySensor):
    """Door sensor."""

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator, device, MT_DOOR_DESCRIPTION)


class MerakiTVOCSensor(MerakiMtSensor):
    """TVOC sensor."""

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator, device, MT_TVOC_DESCRIPTION)


class MerakiPM25Sensor(MerakiMtSensor):
    """PM2.5 sensor."""

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator, device, MT_PM25_DESCRIPTION)


class MerakiNoiseSensor(MerakiMtSensor):
    """Noise sensor."""

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator, device, MT_NOISE_DESCRIPTION)


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
        if not camera_service:
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
        if not camera_service:
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


class UniversalHandler(BaseDeviceHandler):
    """Universal handler for all Meraki devices."""

    # Mapping of capability strings to entity classes or provider classes
    CAP_TO_ENTITY: dict[str, type | Any] = {
        "temperature": MerakiTemperatureSensor,
        "humidity": MerakiHumiditySensor,
        "battery": MerakiBatterySensor,
        "signal_strength": MerakiSignalStrengthSensor,
        "co2": MerakiCO2Sensor,
        "tvoc": MerakiTVOCSensor,
        "pm25": MerakiPM25Sensor,
        "noise": MerakiNoiseSensor,
        "button_press": MerakiButtonPressSensor,
        "water": MerakiWaterSensor,
        "door": MerakiDoorSensor,
        "power_monitor": MT40PowerMonitorProvider,
        "remote_switch": MerakiMt40PowerOutlet,
        "uplinks": UplinkProvider,
        "appliance_ports": AppliancePortProvider,
        "switch_ports": SwitchPortProvider,
        "poe_usage": MerakiPoeUsageSensor,
        "analytics": CameraAnalyticsProvider,
        "reboot": MerakiRebootButton,
        "status": MerakiDeviceStatusSensor,
        "camera_stream": CameraStreamProvider,
    }

    # Mapping of capabilities to their configuration option toggle
    CAP_TO_OPTION: dict[str, str] = {
        "temperature": CONF_ENABLE_DEVICE_SENSORS,
        "humidity": CONF_ENABLE_DEVICE_SENSORS,
        "battery": CONF_ENABLE_DEVICE_SENSORS,
        "signal_strength": CONF_ENABLE_DEVICE_SENSORS,
        "co2": CONF_ENABLE_DEVICE_SENSORS,
        "tvoc": CONF_ENABLE_DEVICE_SENSORS,
        "pm25": CONF_ENABLE_DEVICE_SENSORS,
        "noise": CONF_ENABLE_DEVICE_SENSORS,
        "button_press": CONF_ENABLE_DEVICE_SENSORS,
        "water": CONF_ENABLE_DEVICE_SENSORS,
        "door": CONF_ENABLE_DEVICE_SENSORS,
        "power_monitor": CONF_ENABLE_DEVICE_SENSORS,
        "remote_switch": CONF_ENABLE_DEVICE_SENSORS,
        "poe_usage": CONF_ENABLE_DEVICE_SENSORS,
        "uplinks": CONF_ENABLE_PORT_SENSORS,
        "appliance_ports": CONF_ENABLE_PORT_SENSORS,
        "switch_ports": CONF_ENABLE_PORT_SENSORS,
        "analytics": CONF_ENABLE_CAMERA_ENTITIES,
        "camera_stream": CONF_ENABLE_CAMERA_ENTITIES,
        "status": CONF_ENABLE_DEVICE_STATUS,
    }

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
        camera_service: CameraService,
        control_service: DeviceControlService,
        network_control_service: NetworkControlService,
        capabilities: list[str] | None = None,
    ) -> None:
        """Initialize the UniversalHandler."""
        super().__init__(coordinator, device, config_entry)
        self.capabilities = (
            capabilities
            if capabilities is not None
            else DEVICE_CAPABILITIES.get(device.model, DEFAULT_CAPS)
        )
        self._camera_service = camera_service
        self._control_service = control_service
        self._network_control_service = network_control_service

    async def discover_entities(self) -> AsyncIterator[Entity]:
        """Discover entities based on capabilities."""
        for cap in self.capabilities:
            # Check if this capability is disabled via options
            option_key = self.CAP_TO_OPTION.get(cap)
            if option_key and not self._config_entry.options.get(option_key, True):
                continue

            provider = self.CAP_TO_ENTITY.get(cap)
            if not provider:
                continue

            # Standardized instantiation logic
            try:
                if hasattr(provider, "get_entities"):
                    # Provider class with get_entities (can be sync or async)
                    res = provider.get_entities(
                        self._coordinator,
                        self.device,
                        self._config_entry,
                        camera_service=self._camera_service,
                        control_service=self._control_service,
                        network_control_service=self._network_control_service,
                    )
                    if hasattr(res, "__await__"):
                        for entity in await res:
                            yield entity
                    else:
                        for entity in res:
                            yield entity

                elif provider == MerakiRebootButton:
                    yield provider(
                        self._control_service, self.device, self._config_entry
                    )
                elif provider == MerakiMt40PowerOutlet:
                    yield provider(
                        self._coordinator,
                        self.device,
                        self._config_entry,
                        self._coordinator.api,
                    )
                else:
                    # Attempt instantiation with (coordinator, device, config_entry)
                    # and fallback to (coordinator, device) if needed.
                    try:
                        yield provider(
                            self._coordinator, self.device, self._config_entry
                        )
                    except TypeError:
                        try:
                            yield provider(self._coordinator, self.device)
                        except Exception as e:
                            _LOGGER.error(
                                "Failed to instantiate entity class %s for capability "
                                "%s: %s",
                                provider.__name__,
                                cap,
                                e,
                            )
                            raise

            except Exception as e:
                _LOGGER.error(
                    "Failed to instantiate entity for capability %s on %s: %s",
                    cap,
                    self.device.serial,
                    e,
                )
