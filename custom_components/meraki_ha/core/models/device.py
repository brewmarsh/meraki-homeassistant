"""Device models for Meraki API data structures."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .appliance import ApplianceMixin
from .camera import CameraMixin
from .sensor import SensorMixin
from .switch import SwitchMixin
from .wireless import WirelessMixin


@dataclass(kw_only=True)
class MerakiDevice(
    ApplianceMixin,
    CameraMixin,
    SensorMixin,
    SwitchMixin,
    WirelessMixin,
):
    """Dataclass for a Meraki device."""

    serial: str | None = None
    name: str | None = None
    model: str | None = None
    mac: str | None = None
    lan_ip: str | None = None
    wan1_ip: str | None = None
    wan2_ip: str | None = None
    public_ip: str | None = None
    network_id: str | None = None
    uplinks: list[dict[str, Any]] = field(default_factory=list)
    status: str | None = None
    firmware: str | None = None
    product_type: str | None = None
    tags: list[str] = field(default_factory=list)
    address: str | None = None
    notes: str | None = None
    url: str | None = None
    firmware_upgrades: dict[str, Any] | None = None
    management_interface: dict[str, Any] | None = None
    status_messages: list[str] = field(default_factory=list)
    entity_id: str | None = None

    @property
    def is_online(self) -> bool:
        """Return True if the device is online."""
        return self.status == "online"

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        # Base fields
        data: dict[str, Any] = {
            "serial": self.serial,
            "name": self.name,
            "model": self.model,
            "mac": self.mac,
            "lanIp": self.lan_ip,
            "wan1Ip": self.wan1_ip,
            "wan2Ip": self.wan2_ip,
            "publicIp": self.public_ip,
            "networkId": self.network_id,
            "status": self.status,
            "firmware": self.firmware,
            "productType": self.product_type,
            "tags": self.tags,
            "address": self.address,
            "notes": self.notes,
            "url": self.url,
            "firmwareUpgrades": self.firmware_upgrades,
            "managementInterface": self.management_interface,
            "statusMessages": self.status_messages,
            "uplinks": self.uplinks,
            "entity_id": self.entity_id,
        }

        # Mixin fields
        data.update(self.appliance_to_dict())
        data.update(self.camera_to_dict())
        data.update(self.switch_to_dict())
        data.update(self.wireless_to_dict())
        data.update(self.sensor_to_dict())

        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> MerakiDevice:
        """Create a MerakiDevice instance from a dictionary."""
        device_kwargs: dict[str, Any] = {
            "serial": data.get("serial"),
            "name": data.get("name"),
            "model": data.get("model"),
            "mac": data.get("mac"),
            "lan_ip": data.get("lanIp"),
            "wan1_ip": data.get("wan1Ip"),
            "wan2_ip": data.get("wan2Ip"),
            "public_ip": data.get("publicIp"),
            "network_id": data.get("networkId"),
            "status": data.get("status"),
            "firmware": data.get("firmware"),
            "product_type": data.get("productType"),
            "tags": data.get("tags", []),
            "address": data.get("address"),
            "notes": data.get("notes"),
            "url": data.get("url"),
            "firmware_upgrades": data.get("firmwareUpgrades"),
            "management_interface": data.get("managementInterface"),
            "status_messages": data.get("statusMessages", []),
            "uplinks": data.get("uplinks", []),
            "entity_id": data.get("entity_id"),
        }

        # Mixin fields
        device_kwargs.update(ApplianceMixin.appliance_from_dict(data))
        device_kwargs.update(CameraMixin.camera_from_dict(data))
        device_kwargs.update(SwitchMixin.switch_from_dict(data))
        device_kwargs.update(WirelessMixin.wireless_from_dict(data))
        device_kwargs.update(SensorMixin.sensor_from_dict(data))

        return cls(**device_kwargs)
