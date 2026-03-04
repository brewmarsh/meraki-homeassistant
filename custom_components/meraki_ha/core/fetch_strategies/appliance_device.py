"""Helper for fetching and parsing appliance ports and device details."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from meraki.exceptions import APIError

from ...core.models import MerakiAppliancePort

if TYPE_CHECKING:
    from ...core.api.client import MerakiAPIClient
    from ...core.models.device import MerakiDevice

_LOGGER = logging.getLogger(__name__)

_VLAN_WARNING_LOGGED = False


class ApplianceDeviceHelper:
    """Helper class for processing appliance device details."""

    def __init__(self, client: MerakiAPIClient) -> None:
        """Initialize the helper."""
        self.client = client

    async def get_appliance_ports(self, network_id: str) -> list[dict[str, Any]]:
        """Fetch appliance ports with graceful error handling for disabled VLANs."""
        try:
            return await self.client.appliance.get_appliance_ports(network_id)
        except APIError as e:
            if e.status == 400 and "VLANs" in str(e):
                global _VLAN_WARNING_LOGGED
                if not _VLAN_WARNING_LOGGED:
                    _LOGGER.warning(
                        "Port status/control requires VLANs to be "
                        "enabled in Meraki Dashboard."
                    )
                    _VLAN_WARNING_LOGGED = True
                return []
            raise

    def process_appliance_ports(
        self,
        device: MerakiDevice,
        detail_data: dict[str, Any],
        prev_device: MerakiDevice | None,
    ) -> None:
        """Process appliance ports."""
        if ports := detail_data.get(f"appliance_ports_{device.network_id}"):
            if isinstance(ports, list):
                device.appliance_ports = [
                    MerakiAppliancePort.from_dict(p)
                    for p in ports
                    if isinstance(p, dict)
                ]
        elif prev_device and hasattr(prev_device, "appliance_ports"):
            device.appliance_ports = prev_device.appliance_ports

    def process_dynamic_dns(
        self,
        device: MerakiDevice,
        detail_data: dict[str, Any],
        prev_device: MerakiDevice | None,
    ) -> None:
        """Process dynamic DNS settings."""
        if settings := detail_data.get(f"appliance_settings_{device.serial}"):
            # Defensive check: Ensure settings is a dict before calling .get()
            if isinstance(settings, dict) and isinstance(
                settings.get("dynamicDns"), dict
            ):
                device.dynamic_dns = settings["dynamicDns"]
        elif prev_device and hasattr(prev_device, "dynamic_dns"):
            device.dynamic_dns = prev_device.dynamic_dns

    def process_management_interface(
        self,
        device: MerakiDevice,
        detail_data: dict[str, Any],
        prev_device: MerakiDevice | None,
    ) -> None:
        """Process management interface settings."""
        interface_key = f"management_interface_{device.serial}"
        if management_interface := detail_data.get(interface_key):
            if isinstance(management_interface, dict):
                device.management_interface = management_interface
        elif prev_device and hasattr(prev_device, "management_interface"):
            device.management_interface = prev_device.management_interface
