"""Meraki API endpoints for organizations."""

import logging
from typing import Any, Dict, List

from ...utils.api_utils import handle_meraki_errors, validate_response
from ..cache import async_timed_cache

_LOGGER = logging.getLogger(__name__)


class OrganizationEndpoints:
    """Organization-related endpoints."""

    def __init__(self, api_client):
        """Initialize the endpoint."""
        self._api_client = api_client
        self._dashboard = api_client._dashboard

    @handle_meraki_errors
    @async_timed_cache(timeout=3600)
    async def get_organization(self) -> Dict[str, Any]:
        """Get organization details."""
        org = await self._api_client._run_sync(
            self._dashboard.organizations.getOrganization,
            organizationId=self._api_client.organization_id,
        )
        validated = validate_response(org)
        if not isinstance(validated, dict):
            _LOGGER.warning("get_organization did not return a dict.")
            return {}
        return validated

    @handle_meraki_errors
    @async_timed_cache(timeout=3600)
    async def get_organization_networks(self) -> List[Dict[str, Any]]:
        """Get all networks for an organization."""
        networks = await self._api_client._run_sync(
            self._dashboard.organizations.getOrganizationNetworks,
            organizationId=self._api_client.organization_id,
        )
        validated = validate_response(networks)
        if not isinstance(validated, list):
            _LOGGER.warning("get_organization_networks did not return a list.")
            return []
        return validated

    @handle_meraki_errors
    @async_timed_cache()
    async def get_organization_firmware_upgrades(self) -> List[Dict[str, Any]]:
        """Get firmware upgrade status for the organization."""
        upgrades = await self._api_client._run_sync(
            self._dashboard.organizations.getOrganizationFirmwareUpgrades,
            organizationId=self._api_client.organization_id,
        )
        validated = validate_response(upgrades)
        if not isinstance(validated, list):
            _LOGGER.warning("get_organization_firmware_upgrades did not return a list.")
            return []
        return validated

    @handle_meraki_errors
    @async_timed_cache(timeout=60)
    async def get_organization_device_statuses(self) -> List[Dict[str, Any]]:
        """Get status information for all devices in the organization."""
        statuses = await self._api_client._run_sync(
            self._dashboard.organizations.getOrganizationDeviceStatuses,
            organizationId=self._api_client.organization_id,
        )
        validated = validate_response(statuses)
        if not isinstance(validated, list):
            _LOGGER.warning("get_organization_device_statuses did not return a list.")
            return []
        return validated

    @handle_meraki_errors
    @async_timed_cache(timeout=60)
    async def get_organization_devices_availabilities(self) -> List[Dict[str, Any]]:
        """Get availability information for all devices in the organization."""
        availabilities = await self._api_client._run_sync(
            self._dashboard.organizations.getOrganizationDevicesAvailabilities,
            organizationId=self._api_client.organization_id,
            total_pages="all",
        )
        validated = validate_response(availabilities)
        if not isinstance(validated, list):
            _LOGGER.warning(
                "get_organization_devices_availabilities did not return a list."
            )
            return []
        return validated

    @handle_meraki_errors
    async def create_organization_webhook(
        self, name: str, url: str, secret: str
    ) -> Dict[str, Any]:
        """Create a webhook for the organization."""
        webhook = await self._api_client._run_sync(
            self._dashboard.organizations.createOrganizationWebhooksHttpServer,
            organizationId=self._api_client.organization_id,
            name=name,
            url=url,
            sharedSecret=secret,
        )
        validated = validate_response(webhook)
        if not isinstance(validated, dict):
            _LOGGER.warning("create_organization_webhook did not return a dict.")
            return {}
        return validated

    @handle_meraki_errors
    async def delete_organization_webhook(self, webhook_id: str) -> None:
        """Delete a webhook for the organization."""
        await self._api_client._run_sync(
            self._dashboard.organizations.deleteOrganizationWebhooksHttpServer,
            organizationId=self._api_client.organization_id,
            httpServerId=webhook_id,
        )

    @handle_meraki_errors
    @async_timed_cache()
    async def get_organization_devices(self) -> List[Dict[str, Any]]:
        """Get all devices in the organization."""
        devices = await self._api_client._run_sync(
            self._dashboard.organizations.getOrganizationDevices,
            organizationId=self._api_client.organization_id,
        )
        validated = validate_response(devices)
        if not isinstance(validated, list):
            _LOGGER.warning("get_devices did not return a list, returning empty list.")
            return []
        return validated

    @handle_meraki_errors
    @async_timed_cache(timeout=3600)
    async def get_organizations(self) -> List[Dict[str, Any]]:
        """Get all organizations accessible by the API key."""
        orgs = await self._api_client._run_sync(
            self._dashboard.organizations.getOrganizations
        )
        validated = validate_response(orgs)
        if not isinstance(validated, list):
            _LOGGER.warning("get_organizations did not return a list.")
            return []
        return validated

    @handle_meraki_errors
    @async_timed_cache(timeout=60)
    async def get_organization_appliance_uplink_statuses(self) -> List[Dict[str, Any]]:
        """Get uplink status for all appliances in the organization."""
        statuses = await self._api_client._run_sync(
            self._dashboard.appliance.getOrganizationApplianceUplinkStatuses,
            organizationId=self._api_client.organization_id,
            total_pages="all",
        )
        validated = validate_response(statuses)
        if not isinstance(validated, list):
            _LOGGER.warning(
                "get_organization_appliance_uplink_statuses did not return a list."
            )
            return []
        return validated
