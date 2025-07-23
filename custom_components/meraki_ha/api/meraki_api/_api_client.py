"""
Meraki API Client.

This module provides a client for the Meraki API.
"""

import logging
from typing import Any, List, Dict, Optional

from meraki.aio import AsyncDashboardAPI
from meraki.exceptions import APIError as MerakiSDKAPIError

from .api_endpoints import (
    Organizations,
    Networks,
    Devices,
    Wireless,
    Camera,
)

_LOGGER = logging.getLogger(__name__)


class MerakiAPIClient:
    """A client for the Meraki API."""

    def __init__(
        self,
        api_key: str,
        org_id: str,
    ) -> None:
        """Initialize the Meraki API client."""
        self.api_key: str = api_key
        self.org_id: str = org_id
        self._api: Optional[AsyncDashboardAPI] = None

    @property
    def api(self) -> AsyncDashboardAPI:
        """Return the API object."""
        if self._api is None:
            raise MerakiApiError("API not initialized")
        return self._api

    async def __aenter__(self) -> "MerakiAPIClient":
        """Enter the async context manager."""
        await self.initialize()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit the async context manager."""
        await self.close()

    async def initialize(self) -> None:
        """Initialize the API client."""
        if self._api is None:
            self._api = AsyncDashboardAPI(
                api_key=self.api_key,
                base_url="https://api.meraki.com/api/v1",
                log_file_prefix=None,
            )

    async def close(self) -> None:
        """Close the API client session."""
        if self._api:
            await self._api.close()
            self._api = None

    @property
    def organizations(self) -> "Organizations":
        """Return the organizations API endpoint."""
        return self.api.organizations

    @property
    def networks(self) -> "Networks":
        """Return the networks API endpoint."""
        return self.api.networks

    @property
    def devices(self) -> "Devices":
        """Return the devices API endpoint."""
        return self.api.devices

    @property
    def wireless(self) -> "Wireless":
        """Return the wireless API endpoint."""
        return self.api.wireless

    @property
    def camera(self) -> "Camera":
        """Return the camera API endpoint."""
        return self.api.camera

    async def get_organizations(self) -> List[Dict[str, Any]]:
        """Get all organizations."""
        try:
            return await self.api.organizations.getOrganizations()
        except MerakiSDKAPIError as e:
            raise MerakiApiError(f"Error getting organizations: {e}") from e

    async def get_organization_networks(self) -> List[Dict[str, Any]]:
        """Get all networks for the organization."""
        try:
            return await self.api.organizations.getOrganizationNetworks(self.org_id)
        except MerakiSDKAPIError as e:
            raise MerakiApiError(f"Error getting organization networks: {e}") from e

    async def get_network_devices(self, network_id: str) -> List[Dict[str, Any]]:
        """Get all devices for a network."""
        try:
            return await self.api.networks.getNetworkDevices(networkId=network_id)
        except MerakiSDKAPIError as e:
            raise MerakiApiError(f"Error getting network devices: {e}") from e

    async def get_device_clients(self, serial: str) -> List[Dict[str, Any]]:
        """Get all clients for a device."""
        try:
            return await self.api.devices.getDeviceClients(serial=serial)
        except MerakiSDKAPIError as e:
            raise MerakiApiError(f"Error getting device clients: {e}") from e

    async def get_network_wireless_ssids(
        self, network_id: str
    ) -> List[Dict[str, Any]]:
        """Get all wireless SSIDs for a network."""
        try:
            return await self.api.wireless.getNetworkWirelessSsids(networkId=network_id)
        except MerakiSDKAPIError as e:
            raise MerakiApiError(
                f"Error getting network wireless SSIDs: {e}"
            ) from e

    async def get_device_camera_video_settings(self, serial: str) -> Dict[str, Any]:
        """Get camera video settings for a device."""
        try:
            return await self.api.camera.getDeviceCameraVideoSettings(serial=serial)
        except MerakiSDKAPIError as e:
            raise MerakiApiError(
                f"Error getting device camera video settings: {e}"
            ) from e

    async def update_device_camera_video_settings(
        self, serial: str, **kwargs
    ) -> Dict[str, Any]:
        """Update camera video settings for a device."""
        try:
            return await self.api.camera.updateDeviceCameraVideoSettings(
                serial=serial, **kwargs
            )
        except MerakiSDKAPIError as e:
            raise MerakiApiError(
                f"Error updating device camera video settings: {e}"
            ) from e

    async def get_organization_devices_statuses(self) -> List[Dict[str, Any]]:
        """Get all device statuses for the organization."""
        try:
            return await self.api.organizations.getOrganizationDevicesStatuses(
                self.org_id, total_pages="all"
            )
        except MerakiSDKAPIError as e:
            raise MerakiApiError(
                f"Error getting organization device statuses: {e}"
            ) from e

    async def get_organization_firmware_upgrades(self) -> List[Dict[str, Any]]:
        """Get all firmware upgrades for the organization."""
        try:
            return await self.api.organizations.getOrganizationFirmwareUpgrades(
                self.org_id
            )
        except MerakiSDKAPIError as e:
            raise MerakiApiError(
                f"Error getting organization firmware upgrades: {e}"
            ) from e

    async def get_network_clients(self, network_id: str) -> List[Dict[str, Any]]:
        """Get all clients for a network."""
        try:
            return await self.api.networks.getNetworkClients(
                networkId=network_id, timespan=3600
            )
        except MerakiSDKAPIError as e:
            raise MerakiApiError(f"Error getting network clients: {e}") from e

    async def provision_network_clients(
        self,
        network_id: str,
        clients: List[Dict[str, Any]],
        policies_by_mac: Dict[str, Any],
        group_policy_id: str,
    ) -> Dict[str, Any]:
        """Provision clients for a network."""
        try:
            return await self.api.networks.provisionNetworkClients(
                networkId=network_id,
                clients=clients,
                policiesByMac=policies_by_mac,
                groupPolicyId=group_policy_id,
            )
        except MerakiSDKAPIError as e:
            raise MerakiApiError(f"Error provisioning network clients: {e}") from e

    def __getattr__(self, name: str) -> Any:
        """Delegate attribute access to the API object."""
        return getattr(self.api, name)


class MerakiApiError(Exception):
    """Custom exception for Meraki API errors."""
