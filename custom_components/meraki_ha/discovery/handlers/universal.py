"""Universal Discovery Handler for Meraki devices."""

from __future__ import annotations

import logging
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
)
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
                        interface = ent.unique_id.replace(f"{device.serial}_uplink_", "")
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


class UniversalHandler(BaseDeviceHandler):
    """Universal handler for all Meraki devices."""

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
        capabilities: list[str],
        camera_service: CameraService,
        control_service: DeviceControlService,
        network_control_service: NetworkControlService,
    ) -> None:
        """Initialize the UniversalHandler."""
        super().__init__(coordinator, device, config_entry)
        self.capabilities = capabilities
        self._camera_service = camera_service
        self._control_service = control_service
        self._network_control_service = network_control_service

    @classmethod
    def create(
        cls,
        coordinator: MerakiDataUpdateCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
        camera_service: CameraService,
        control_service: DeviceControlService,
        network_control_service: NetworkControlService,
    ) -> UniversalHandler:
        """Create an instance of the handler."""
        from ...const import DEFAULT_CAPS, DEVICE_CAPABILITIES

        capabilities = DEVICE_CAPABILITIES.get(device.model, DEFAULT_CAPS)
        return cls(
            coordinator,
            device,
            config_entry,
            capabilities,
            camera_service,
            control_service,
            network_control_service,
        )

    async def discover_entities(self) -> list[Entity]:
        """Discover entities based on capabilities."""
        # If configured, ensure the RTSP stream is enabled by default for cameras
        if "camera_stream" in self.capabilities:
            if self._config_entry.options.get("rtsp_stream_enabled", False):
                try:
                    _LOGGER.debug(
                        "RTSP stream is defaulted to on, enabling for camera %s",
                        self.device.serial,
                    )
                    await self._camera_service.async_set_rtsp_stream_enabled(
                        self.device.serial, True
                    )
                except MerakiInformationalError as e:
                    _LOGGER.warning(
                        "Could not enable RTSP stream for %s: %s", self.device.serial, e
                    )
                    self._coordinator.add_status_message(
                        self.device.serial, f"Could not enable RTSP stream: {e}"
                    )

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
            "camera_stream": MerakiCamera,
            "analytics": CameraAnalyticsProvider,
            "reboot": MerakiRebootButton,
            "status": MerakiDeviceStatusSensor,
        }

        entities: list[Entity] = []

        # Special logic for MV camera stream/base entities
        if "camera_stream" in self.capabilities:
            if self._config_entry.options.get(CONF_ENABLE_CAMERA_ENTITIES, True):
                # Always create the base camera entity
                entities.append(
                    MerakiCamera(
                        self._coordinator,
                        self._config_entry,
                        self.device,
                        self._camera_service,
                    )
                )
                # Add extra camera entities
                entities.extend(
                    [
                        MerakiMotionSensor(
                            self._coordinator,
                            self.device,
                            self._camera_service,
                            self._config_entry,
                        ),
                        MerakiSnapshotButton(
                            self._coordinator,
                            self.device,
                            self._camera_service,
                            self._config_entry,
                        ),
                        MerakiRtspUrlSensor(
                            self._coordinator,
                            self.device,
                            self._config_entry,
                        ),
                        AnalyticsSwitch(
                            self._coordinator, self._coordinator.api, self.device
                        ),
                    ]
                )

        for cap in self.capabilities:
            if cap == "camera_stream":
                continue  # Handled above

            # Check for device sensors toggle (MT)
            if cap in (
                "temperature",
                "humidity",
                "battery",
                "signal_strength",
                "co2",
                "tvoc",
                "pm25",
                "noise",
                "button_press",
                "water",
                "door",
                "power_monitor",
                "remote_switch",
            ):
                if not self._config_entry.options.get(CONF_ENABLE_DEVICE_SENSORS, True):
                    continue

            provider = CAP_TO_ENTITY.get(cap)
            if not provider:
                continue

            # Check if it's a provider with get_entities
            if hasattr(provider, "get_entities"):
                res = provider.get_entities(
                    self._coordinator,
                    self.device,
                    self._config_entry,
                    camera_service=self._camera_service,
                    control_service=self._control_service,
                    network_control_service=self._network_control_service,
                )
                if hasattr(res, "__await__"):
                    entities.extend(await res)
                else:
                    entities.extend(res)
            # Check if it's RebootButton which takes specific args
            elif provider == MerakiRebootButton:
                entities.append(
                    provider(self._control_service, self.device, self._config_entry)
                )
            # Check if it's StatusSensor which takes specific args
            elif provider == MerakiDeviceStatusSensor:
                if self._config_entry.options.get(CONF_ENABLE_DEVICE_STATUS, True):
                    entities.append(
                        provider(self._coordinator, self.device, self._config_entry)
                    )
            # Check if it's MT40 remote switch
            elif provider == MerakiMt40PowerOutlet:
                entities.append(
                    provider(
                        self._coordinator,
                        self.device,
                        self._config_entry,
                        self._coordinator.api,
                    )
                )
            # Standard entity instantiation
            else:
                try:
                    # Some take config_entry, some don't. Try with 3 first.
                    entities.append(
                        provider(self._coordinator, self.device, self._config_entry)
                    )
                except TypeError:
                    # Fallback for entities that take only 2
                    try:
                        entities.append(provider(self._coordinator, self.device))
                    except Exception as e:
                        _LOGGER.error(
                            "Failed to instantiate entity for capability %s: %s", cap, e
                        )

        return entities
