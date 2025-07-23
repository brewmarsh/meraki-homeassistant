from typing import TYPE_CHECKING, List, Dict, Any

if TYPE_CHECKING:
    from .._api_client import MerakiAPIClient


class Organizations:
    """Mock for organizations endpoint."""

    def __init__(self, client: "MerakiAPIClient"):
        self._client = client

    async def getOrganizations(self) -> List[Dict[str, Any]]:
        """Mock for getOrganizations."""
        return await self._client.get_organizations()

    async def getOrganizationNetworks(self, org_id: str) -> List[Dict[str, Any]]:
        """Mock for getOrganizationNetworks."""
        return await self._client.get_organization_networks()

    async def getOrganizationDevicesStatuses(
        self, org_id: str, total_pages: str
    ) -> List[Dict[str, Any]]:
        """Mock for getOrganizationDevicesStatuses."""
        return await self._client.get_organization_devices_statuses()

    async def getOrganizationFirmwareUpgrades(
        self, org_id: str
    ) -> List[Dict[str, Any]]:
        """Mock for getOrganizationFirmwareUpgrades."""
        return await self._client.get_organization_firmware_upgrades()

    async def getOrganization(self, org_id: str) -> Dict[str, Any]:
        """Mock for getOrganization."""
        return await self._client.get_organization(org_id)
