"""Meraki API Client for the Meraki Home Assistant integration.

This module provides the `MerakiAPIClient` class, which is a wrapper around
the Meraki SDK to provide a simplified interface for making API calls.
"""

import asyncio
import logging
from typing import Any, Awaitable, Optional

from meraki.exceptions import APIError as MerakiSDKAPIError

_LOGGER = logging.getLogger(__name__)


class MerakiAPIClientWrapper:
    """A wrapper for the Meraki SDK client to handle API calls and errors."""

    def __init__(self, meraki_client: Any, semaphore_value: int = 5) -> None:
        """Initialize the Meraki API client wrapper.

        Args:
            meraki_client: An instance of the Meraki SDK client.
            semaphore_value: The maximum number of concurrent API calls.
        """
        self.meraki_client = meraki_client
        self._api_call_semaphore = asyncio.Semaphore(semaphore_value)

    async def call(
        self,
        api_coro: Awaitable[Any],
        call_description: str,
        return_empty_list_on_404: bool = False,
    ) -> Optional[Any]:
        """Make a Meraki API call with error handling.

        Args:
            api_coro: The Meraki SDK coroutine to await.
            call_description: A description of the API call for logging.
            return_empty_list_on_404: Whether to return an empty list on a 404 error.

        Returns:
            The result of the API call, or None if an error occurred.
        """
        try:
            async with self._api_call_semaphore:
                return await api_coro
        except MerakiSDKAPIError as e:
            if e.status == 404 and return_empty_list_on_404:
                _LOGGER.debug(
                    "Handled 404 for '%s' by returning an empty list.",
                    call_description,
                )
                return []
            _LOGGER.error(
                "Meraki API error during '%s': %s",
                call_description,
                e,
            )
            return None
        except Exception as e:
            _LOGGER.exception(
                "Unexpected error during '%s': %s",
                call_description,
                e,
            )
            return None
