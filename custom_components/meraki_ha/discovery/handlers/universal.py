"""Universal Discovery Handler for Meraki devices."""

from __future__ import annotations

import logging
from collections.abc import AsyncIterator
from typing import TYPE_CHECKING, Any

from ...button.device.mt15_refresh_data import MerakiMt15RefreshDataButton
from ...button.reboot import MerakiRebootButton
from custom_components.meraki_ha.const.integration import (
    CONF_ENABLE_CAMERA_ENTITIES,
    CONF_ENABLE_DEVICE_SENSORS,
    CONF_ENABLE_DEVICE_STATUS,
    CONF_ENABLE_PORT_SENSORS
)
from custom_components.meraki_ha.const.integration import DEFAULT_CAPS, DEVICE_CAPABILITIES

from...sensor.device.device_status import MerakiDeviceStatusSensor
from ...sensor.device.poe_usage import MerakiPoeUsageSensor
from ...switch.mt40_power_outlet import MerakiMt40PowerOutlet
from ..entities import (
    MerakiBatterySensor,
    MerakiButtonPressSensor,
    MerakiCO2Sensor,
    MerakiDoorSensor,
    MerakiHumiditySensor,
    MerakiNoiseSensor,
    MerakiPM25Sensor,
    MerakiSignalStrengthSensor,
    MerakiTemperatureSensor,
    MerakiTVOCSensor,
    MerakiWaterSensor,
)
from ..providers import (
    AppliancePortProvider,
    CameraAnalyticsProvider,
    CameraStreamProvider,
    MT40PowerMonitorProvider,
    PhysicalSensorProvider,
    UplinkPerformanceProvider,
    UplinkProvider,
    WirelessRadioProvider,
)
from .base import BaseDeviceHandler

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.helpers.entity import Entity

    from ...coordinators import MerakiDeviceCoordinator, MerakiMainCoordinator
    from ...core.models.device import MerakiDevice
    from ...services.camera_service import CameraService
    from ...services.device_control_service import DeviceControlService
    from ...services.network_control_service import NetworkControlService


_LOGGER = logging.getLogger(__name__)

SPECIAL_HANDLERS: set[type] = {
    MerakiRebootButton,
    MerakiMt15RefreshDataButton,
    MerakiMt40PowerOutlet,
}


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
        "performance": UplinkPerformanceProvider,
        "appliance_ports": AppliancePortProvider,
        "poe_usage": MerakiPoeUsageSensor,
        "camera_analytics": CameraAnalyticsProvider,
        "mt15_refresh": MerakiMt15RefreshDataButton,
        "reboot": MerakiRebootButton,
        "status": MerakiDeviceStatusSensor,
        "physical_sensors": PhysicalSensorProvider,
        "camera_stream": CameraStreamProvider,
        "wireless": WirelessRadioProvider,
    }

    # Mapping of capabilities to their configuration option toggle
    CAP_TO_OPTION: dict[str, str] = {
        "physical_sensors": CONF_ENABLE_DEVICE_SENSORS,
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
        "performance": CONF_ENABLE_PORT_SENSORS,
        "appliance_ports": CONF_ENABLE_PORT_SENSORS,
        "camera_analytics": CONF_ENABLE_CAMERA_ENTITIES,
        "mt15_refresh": CONF_ENABLE_DEVICE_SENSORS,
        "camera_stream": CONF_ENABLE_CAMERA_ENTITIES,
        "status": CONF_ENABLE_DEVICE_STATUS,
        "wireless": CONF_ENABLE_DEVICE_SENSORS,
    }

    def __init__(
        self,
        coordinator: MerakiMainCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
        camera_service: CameraService,
        control_service: DeviceControlService,
        network_control_service: NetworkControlService,
        capabilities: list[str] | None = None,
        status_coordinator: MerakiDeviceCoordinator | None = None,
        sensor_coordinator: MerakiSensorCoordinator | None = None,
    ) -> None:
        """Initialize the UniversalHandler."""
        super().__init__(coordinator, device, config_entry)
        self._status_coordinator = status_coordinator
        self._sensor_coordinator = sensor_coordinator
        self.capabilities = (
            capabilities
            if capabilities is not None
            else DEVICE_CAPABILITIES.get(device.model, DEFAULT_CAPS)[:]
        )

        # Fallback: if model is unknown but product_type indicates wireless, add ssids
        if "ssids" not in self.capabilities:
            if (device.product_type == "wireless") or (
                device.model and device.model.startswith("MR")
            ):
                self.capabilities.append("ssids")
        self._camera_service = camera_service
        self._control_service = control_service
        self._network_control_service = network_control_service

    async def discover_entities(self) -> AsyncIterator[Entity]:
        """Discover entities based on capabilities."""
        for cap in self.capabilities:
            async for entity in self._discover_capability(cap):
                yield entity

    async def _discover_capability(self, cap: str) -> AsyncIterator[Entity]:
        """Discover entities for a specific capability."""
        if not self._is_capability_enabled(cap):
            return

        provider = self.CAP_TO_ENTITY.get(cap)
        if not provider:
            return

        async for entity in self._instantiate_entities(cap, provider):
            yield entity

    def _is_capability_enabled(self, cap: str) -> bool:
        """Check if a capability is enabled in configuration options."""
        option_key = self.CAP_TO_OPTION.get(cap)
        if not option_key:
            return True
        return bool(self._config_entry.options.get(option_key, True))

    async def _instantiate_entities(
        self, cap: str, provider: type | Any
    ) -> AsyncIterator[Entity]:
        """Instantiate entities for a given capability and provider."""
        try:
            if hasattr(provider, "get_entities"):
                async for entity in self._handle_provider_class(provider):
                    yield entity
                return

            yield self._instantiate_single_entity(cap, provider)
        except Exception as e:
            _LOGGER.error(
                "Failed to instantiate entity for capability %s on %s: %s",
                cap,
                self.device.serial,
                e,
            )

    def _instantiate_single_entity(self, cap: str, provider: type) -> Entity:
        """Instantiate a single entity."""
        # Use specialized coordinator if available for MT sensors
        coordinator = self._coordinator
        if self.device.model and self.device.model.startswith("MT"):
            # Ensure we use the specialized sensor coordinator for MT devices if it's not the main one
            if hasattr(self, "_sensor_coordinator") and self._sensor_coordinator:
                coordinator = self._sensor_coordinator

        if cap == "status" and self._status_coordinator:
            return provider(self._status_coordinator, self.device, self._config_entry)
        if provider in SPECIAL_HANDLERS:
            return self._handle_special_entities(provider)
        return self._handle_default_entity(cap, provider, coordinator)

    async def _handle_provider_class(self, provider: Any) -> AsyncIterator[Entity]:
        """Handle provider classes with get_entities method."""
        res = provider.get_entities(
            self._coordinator,
            self.device,
            self._config_entry,
            camera_service=self._camera_service,
            control_service=self._control_service,
            network_control_service=self._network_control_service,
        )
        if hasattr(res, "__await__"):
            entities = await res
        else:
            entities = res

        for entity in entities:
            yield entity

    def _handle_special_entities(self, provider: type) -> Entity:
        """Handle special entities with unique constructor signatures."""
        if provider == MerakiRebootButton:
            return provider(
                self._status_coordinator or self._coordinator,
                self._control_service,
                self.device,
                self._config_entry,
            )

        # MT15 Refresh or MT40 Power Outlet
        return provider(
            self._coordinator,
            self.device,
            self._config_entry,
            self._coordinator.api,
        )

    def _handle_default_entity(
        self, cap: str, provider: type, coordinator: Any = None
    ) -> Entity:
        """Handle standard entity instantiation with fallback."""
        coord = coordinator or self._coordinator
        try:
            return provider(coord, self.device, self._config_entry)
        except TypeError:
            return provider(coord, self.device)
