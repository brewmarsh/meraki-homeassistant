"""Device models for Meraki API data structures."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .appliance import MerakiApplianceMixin, MerakiAppliancePort
from .camera import MerakiCameraMixin
from .sensor import MerakiSensorMixin
from .switch import MerakiSwitchMixin
from .wireless import MerakiWirelessMixin


@dataclass(kw_only=True)
class MerakiDevice(
    MerakiApplianceMixin,
    MerakiCameraMixin,
    MerakiSensorMixin,
    MerakiSwitchMixin,
    MerakiWirelessMixin,
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

        # Appliance fields
        data.update(
            {
                "applianceUplinkStatuses": self.appliance_uplink_statuses,
                "appliancePorts": [p.to_dict() for p in self.appliance_ports],
                "dynamicDns": self.dynamic_dns,
            }
        )

        # Camera fields
        data.update(
            {
                "videoSettings": self.video_settings,
                "rtspUrl": self.rtsp_url,
                "senseSettings": self.sense_settings,
                "analytics": self.analytics,
            }
        )

        # Switch fields
        data.update({"portsStatuses": self.ports_statuses})

        # Wireless fields
        data.update({"wirelessRadioSettings": self.wireless_radio_settings})

        # Sensor fields
        data.update(
            {
                "sensorRelationships": self.sensor_relationships,
                "readings": self.readings,
                "outletStatus": self.outlet_status,
                "ambientNoise": self.ambient_noise,
                "pm25": self.pm25,
                "realPower": self.real_power,
                "powerFactor": self.power_factor,
                "current": self.current,
                "voltage": self.voltage,
                "doorOpen": self.door_open,
                "waterPresent": self.water_present,
                "buttonPress": self.button_press,
                "frequency": self.frequency,
                "energy": self.energy,
            }
        )

        return data

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
            management_interface=data.get("managementInterface"),
            status_messages=data.get("statusMessages", []),
            uplinks=data.get("uplinks", []),
            entity_id=data.get("entity_id"),
            # Appliance fields
            appliance_uplink_statuses=data.get("applianceUplinkStatuses", []),
            appliance_ports=[
                MerakiAppliancePort.from_dict(p) for p in data.get("appliancePorts", [])
            ],
            dynamic_dns=data.get("dynamicDns"),
            # Camera fields
            video_settings=data.get("videoSettings"),
            rtsp_url=data.get("rtspUrl"),
            sense_settings=data.get("senseSettings"),
            analytics=data.get("analytics", []),
            # Switch fields
            ports_statuses=data.get("portsStatuses", []),
            # Wireless fields
            wireless_radio_settings=data.get("wirelessRadioSettings"),
            # Sensor fields
            sensor_relationships=data.get("sensorRelationships", []),
            readings=data.get("readings", []),
            outlet_status=data.get("outletStatus"),
            ambient_noise=data.get("ambientNoise"),
            pm25=data.get("pm25"),
            real_power=data.get("realPower"),
            power_factor=data.get("powerFactor"),
            current=data.get("current"),
            voltage=data.get("voltage"),
            door_open=data.get("doorOpen"),
            water_present=data.get("waterPresent"),
            button_press=data.get("buttonPress"),
            frequency=data.get("frequency"),
            energy=data.get("energy"),
        )
