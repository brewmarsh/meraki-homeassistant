"""Device models for Meraki API data structures."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class MerakiAppliancePort:
    """Represents a Meraki Appliance Port."""

    number: int | None = None
    enabled: bool = False
    type: str | None = None
    drop_untagged_traffic: bool = False
    vlan: int | None = None
    access_policy: str | None = None
    allowed_vlans: str | None = None
    status: str | None = None
    speed: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "number": self.number,
            "enabled": self.enabled,
            "type": self.type,
            "dropUntaggedTraffic": self.drop_untagged_traffic,
            "vlan": self.vlan,
            "accessPolicy": self.access_policy,
            "allowedVlans": self.allowed_vlans,
            "status": self.status,
            "speed": self.speed,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> MerakiAppliancePort:
        """Create a MerakiAppliancePort instance from a dictionary."""
        return cls(
            number=data.get("number"),
            enabled=data.get("enabled", False),
            type=data.get("type"),
            drop_untagged_traffic=data.get("dropUntaggedTraffic", False),
            vlan=data.get("vlan"),
            access_policy=data.get("accessPolicy"),
            allowed_vlans=data.get("allowedVlans"),
            status=data.get("status"),
            speed=data.get("speed"),
        )


@dataclass
class MerakiDevice:
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
    appliance_uplink_statuses: list[dict[str, Any]] = field(default_factory=list)
    status: str | None = None
    firmware: str | None = None
    product_type: str | None = None
    tags: list[str] = field(default_factory=list)
    address: str | None = None
    notes: str | None = None
    url: str | None = None
    firmware_upgrades: dict[str, Any] | None = None
    readings: list[dict[str, Any]] = field(default_factory=list)
    video_settings: dict[str, Any] | None = None
    rtsp_url: str | None = None
    sense_settings: dict[str, Any] | None = None
    analytics: list[dict[str, Any]] = field(default_factory=list)
    ports_statuses: list[dict[str, Any]] = field(default_factory=list)
    appliance_ports: list[MerakiAppliancePort] = field(default_factory=list)
    sensor_relationships: list[dict[str, Any]] = field(default_factory=list)
    dynamic_dns: dict[str, Any] | None = None
    status_messages: list[str] = field(default_factory=list)
    entity_id: str | None = None
    ambient_noise: float | None = None
    pm25: float | None = None
    real_power: float | None = None
    power_factor: float | None = None
    current: float | None = None
    voltage: float | None = None
    door_open: bool | None = None
    water_present: bool | None = None
    button_press: dict[str, Any] | None = None
    frequency: float | None = None
    energy: float | None = None
    outlet_status: bool | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
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
            "readings": self.readings,
            "videoSettings": self.video_settings,
            "rtspUrl": self.rtsp_url,
            "senseSettings": self.sense_settings,
            "analytics": self.analytics,
            "portsStatuses": self.ports_statuses,
            "appliancePorts": [p.to_dict() for p in self.appliance_ports],
            "sensorRelationships": self.sensor_relationships,
            "dynamicDns": self.dynamic_dns,
            "statusMessages": self.status_messages,
            "applianceUplinkStatuses": self.appliance_uplink_statuses,
            "entity_id": self.entity_id,
            "outletStatus": self.outlet_status,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> MerakiDevice:
        """Create a MerakiDevice instance from a dictionary."""
        return cls(
            serial=data.get("serial"),
            name=data.get("name"),
            model=data.get("model"),
            mac=data.get("mac"),
            lan_ip=data.get("lanIp"),
            wan1_ip=data.get("wan1Ip"),
            wan2_ip=data.get("wan2Ip"),
            public_ip=data.get("publicIp"),
            network_id=data.get("networkId"),
            status=data.get("status"),
            firmware=data.get("firmware"),
            product_type=data.get("productType"),
            tags=data.get("tags", []),
            address=data.get("address"),
            notes=data.get("notes"),
            url=data.get("url"),
            firmware_upgrades=data.get("firmwareUpgrades"),
            readings=data.get("readings", []),
            video_settings=data.get("videoSettings"),
            rtsp_url=data.get("rtspUrl"),
            sense_settings=data.get("senseSettings"),
            analytics=data.get("analytics", []),
            ports_statuses=data.get("portsStatuses", []),
            appliance_ports=[
                MerakiAppliancePort.from_dict(p) for p in data.get("appliancePorts", [])
            ],
            sensor_relationships=data.get("sensorRelationships", []),
            dynamic_dns=data.get("dynamicDns"),
            status_messages=data.get("statusMessages", []),
            appliance_uplink_statuses=data.get("applianceUplinkStatuses", []),
            entity_id=data.get("entity_id"),
            outlet_status=data.get("outletStatus"),
        )
