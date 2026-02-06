"""Universal Discovery Handler for Meraki devices."""

from __future__ import annotations

import logging
from collections.abc import AsyncIterator
from typing import TYPE_CHECKING, Any

from ...button.reboot import MerakiRebootButton
from ...const_conf import (
    CONF_ENABLE_CAMERA_ENTITIES,
    CONF_ENABLE_DEVICE_SENSORS,
    CONF_ENABLE_DEVICE_STATUS,
    CONF_ENABLE_PORT_SENSORS,
)
from ...core.const import DEFAULT_CAPS, DEVICE_CAPABILITIES
from ...sensor.device.device_status import MerakiDeviceStatusSensor
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
    SwitchPortProvider,
    UplinkPerformanceProvider,
    UplinkProvider,
)
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
        "switch_ports": SwitchPortProvider,
        "poe_usage": MerakiPoeUsageSensor,
        "analytics": CameraAnalyticsProvider,
        "reboot": MerakiRebootButton,
        "status": MerakiDeviceStatusSensor,
        "physical_sensors": PhysicalSensorProvider,
        "camera_stream": CameraStreamProvider,
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
                                "Failed to instantiate entity class %s for "
                                "capability %s: %s",
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
