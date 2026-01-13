"""
Organization Hub.

This module defines the OrganizationHub class, which is responsible for
<<<<<<< HEAD
processing and managing organization-level data from the MerakiDataUpdateCoordinator.
=======
<<<<<<< HEAD
processing and managing organization-level data from the MerakiDataUpdateCoordinator.
=======
processing and managing organization-level data from the MerakiDataCoordinator.
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
<<<<<<< HEAD
    from ..coordinator import MerakiDataUpdateCoordinator
=======
<<<<<<< HEAD
    from ..coordinator import MerakiDataUpdateCoordinator
=======
    from ..meraki_data_coordinator import MerakiDataCoordinator
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)

_LOGGER = logging.getLogger(__name__)


class OrganizationHub:
    """A hub for processing organization-level data."""

<<<<<<< HEAD
    def __init__(self, coordinator: MerakiDataUpdateCoordinator) -> None:
=======
<<<<<<< HEAD
    def __init__(self, coordinator: MerakiDataUpdateCoordinator) -> None:
=======
    def __init__(self, coordinator: MerakiDataCoordinator) -> None:
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
        """Initialize the OrganizationHub."""
        self._coordinator = coordinator
        self.data: dict = {}

    @property
    def organization_id(self) -> str | None:
        """Return the organization ID."""
        if self._coordinator.data and self._coordinator.data.get("networks"):
            # All networks belong to the same org, so we can take the first one
            return self._coordinator.data["networks"][0].get("organizationId")
        return None

    async def async_update_data(self) -> None:
        """Update organization-level data from the coordinator."""
        _LOGGER.debug("Updating organization hub data")
        # In the future, this method will process raw data from the coordinator
        # into a more structured format for the organization.
        # For now, we'll just keep a reference to the raw data.
        self.data = self._coordinator.data
