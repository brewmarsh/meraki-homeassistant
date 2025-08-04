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
        _LOGGER.debug("Getting organization details")
        org = await self._api_client._run_sync(
            self._dashboard.organizations.getOrganization,
            organizationId=self._api_client.organization_id,
        )
        return validate_response(org)

    @handle_meraki_errors
    @async_timed_cache(timeout=3600)
    async def get_organization_networks(self) -> List[Dict[str, Any]]:
        """Get all networks for an organization."""
        _LOGGER.debug("Getting all networks for organization")
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
        _LOGGER.debug("Getting organization firmware upgrades")
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
        _LOGGER.debug("Getting device statuses for organization")
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
    @async_timed_cache()
    async def get_organization_devices(self) -> List[Dict[str, Any]]:
        """Get all devices in the organization."""
        _LOGGER.debug("Getting devices for entire organization")
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
        _LOGGER.debug("Getting all organizations")
        orgs = await self._api_client._run_sync(
            self._dashboard.organizations.getOrganizations
        )
        validated = validate_response(orgs)
        if not isinstance(validated, list):
            _LOGGER.warning("get_organizations did not return a list.")
            return []
        return validated
