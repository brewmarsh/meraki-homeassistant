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
<<<<<<< HEAD
        self._dashboard = api_client.dashboard
=======
>>>>>>> d5ccb99 (Merge pull request #604 from brewmarsh/fix/resolve-jq-parse-error-in-deploy-local-workflow-2298884834713058677)

    @handle_meraki_errors
    @async_timed_cache(timeout=3600)
    async def get_organization(self) -> dict[str, Any]:
        """
        Get organization details.

        Returns
        -------
            The organization details.

        """
<<<<<<< HEAD
        org = await self._api_client.run_sync(
            self._dashboard.organizations.getOrganization,
=======
        if self._api_client.dashboard is None:
            return {}
        org = await self._api_client.run_sync(
            self._api_client.dashboard.organizations.getOrganization,
>>>>>>> d5ccb99 (Merge pull request #604 from brewmarsh/fix/resolve-jq-parse-error-in-deploy-local-workflow-2298884834713058677)
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
<<<<<<< HEAD
        networks = await self._api_client.run_sync(
            self._dashboard.organizations.getOrganizationNetworks,
=======
        if self._api_client.dashboard is None:
            return []
        networks = await self._api_client.run_sync(
            self._api_client.dashboard.organizations.getOrganizationNetworks,
>>>>>>> d5ccb99 (Merge pull request #604 from brewmarsh/fix/resolve-jq-parse-error-in-deploy-local-workflow-2298884834713058677)
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
<<<<<<< HEAD
        upgrades = await self._api_client.run_sync(
            self._dashboard.organizations.getOrganizationFirmwareUpgrades,
=======
        if self._api_client.dashboard is None:
            return []
        upgrades = await self._api_client.run_sync(
            self._api_client.dashboard.organizations.getOrganizationFirmwareUpgrades,
>>>>>>> d5ccb99 (Merge pull request #604 from brewmarsh/fix/resolve-jq-parse-error-in-deploy-local-workflow-2298884834713058677)
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
<<<<<<< HEAD
        statuses = await self._api_client.run_sync(
            self._dashboard.organizations.getOrganizationDeviceStatuses,
=======
        if self._api_client.dashboard is None:
            return []
        statuses = await self._api_client.run_sync(
            self._api_client.dashboard.organizations.getOrganizationDeviceStatuses,
>>>>>>> d5ccb99 (Merge pull request #604 from brewmarsh/fix/resolve-jq-parse-error-in-deploy-local-workflow-2298884834713058677)
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
<<<<<<< HEAD
        availabilities = await self._api_client.run_sync(
            self._dashboard.organizations.getOrganizationDevicesAvailabilities,
=======
        if self._api_client.dashboard is None:
            return []
        availabilities = await self._api_client.run_sync(
            self._api_client.dashboard.organizations.getOrganizationDevicesAvailabilities,
>>>>>>> d5ccb99 (Merge pull request #604 from brewmarsh/fix/resolve-jq-parse-error-in-deploy-local-workflow-2298884834713058677)
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
<<<<<<< HEAD
        devices = await self._api_client.run_sync(
            self._dashboard.organizations.getOrganizationDevices,
=======
        if self._api_client.dashboard is None:
            return []
        devices = await self._api_client.run_sync(
            self._api_client.dashboard.organizations.getOrganizationDevices,
>>>>>>> d5ccb99 (Merge pull request #604 from brewmarsh/fix/resolve-jq-parse-error-in-deploy-local-workflow-2298884834713058677)
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
<<<<<<< HEAD
        orgs = await self._api_client.run_sync(
            self._dashboard.organizations.getOrganizations
=======
        if self._api_client.dashboard is None:
            return []
        orgs = await self._api_client.run_sync(
            self._api_client.dashboard.organizations.getOrganizations
>>>>>>> d5ccb99 (Merge pull request #604 from brewmarsh/fix/resolve-jq-parse-error-in-deploy-local-workflow-2298884834713058677)
        )
        validated = validate_response(orgs)
        if not isinstance(validated, list):
            _LOGGER.warning("get_organizations did not return a list.")
            return []
        return validated
