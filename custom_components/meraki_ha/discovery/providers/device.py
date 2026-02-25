"""Provider for physical device sensors (IP, Status, Diagnostics)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ...sensor.device.network_settings import (
    MerakiDeviceDNSSensor,
    MerakiDeviceGatewaySensor,
    MerakiDeviceIPSensor,
)

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.helpers.entity import Entity

    from ...coordinator import MerakiDataUpdateCoordinator
    from ...core.models.device import MerakiDevice


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
