"""Meraki API endpoints for organizations."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from custom_components.meraki_ha.core.utils.api_utils import (
    handle_meraki_errors,
    validate_response,
)

from ..cache import async_timed_cache

if TYPE_CHECKING:
    from ..client import MerakiAPIClient


_LOGGER = logging.getLogger(__name__)


class OrganizationEndpoints:

    """Organization-related endpoints."""

    def __init__(self, api_client: MerakiAPIClient) -> None:
        """
        Initialize the endpoint.

        Args:
        ----
            api_client: The Meraki API client.

        """
        self._api_client = api_client
        self._dashboard = api_client.dashboard

    @handle_meraki_errors
    @async_timed_cache(timeout=3600)
    async def get_organization(self) -> dict[str, Any]:
        """
        Get organization details.

        Returns
        -------
            The organization details.

        """
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
    async def get_organization_networks(self) -> list[dict[str, Any]]:
        """
        Get all networks for an organization.

        Returns
        -------
            A list of networks.

        """
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
    async def get_organization_firmware_upgrades(self) -> list[dict[str, Any]]:
        """
        Get firmware upgrade status for the organization.

        Returns
        -------
            A list of firmware upgrades.

        """
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
    async def get_organization_device_statuses(self) -> list[dict[str, Any]]:
        """
        Get status information for all devices in the organization.

        Returns
        -------
            A list of device statuses.

        """
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
    async def get_organization_devices_availabilities(self) -> list[dict[str, Any]]:
        """
        Get availability information for all devices in the organization.

        Returns
        -------
            A list of device availabilities.

        """
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
    @async_timed_cache()
    async def get_organization_devices(self) -> list[dict[str, Any]]:
        """
        Get all devices in the organization.

        Returns
        -------
            A list of devices.

        """
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
    async def get_organizations(self) -> list[dict[str, Any]]:
        """
        Get all organizations accessible by the API key.

        Returns
        -------
            A list of organizations.

        """
        orgs = await self._api_client._run_sync(
            self._dashboard.organizations.getOrganizations
        )
        validated = validate_response(orgs)
        if not isinstance(validated, list):
            _LOGGER.warning("get_organizations did not return a list.")
            return []
        return validated
