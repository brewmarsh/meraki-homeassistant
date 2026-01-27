"""Fetches device data for the Meraki coordinator."""
from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING, Any, cast

from ...core.parsers.devices import parse_device_data
from ...types import MerakiDevice

if TYPE_CHECKING:
    from ..api.client import MerakiAPIClient


_LOGGER = logging.getLogger(__name__)


class DeviceFetcher:
    """Class to fetch device data."""

    def __init__(self, client: MerakiAPIClient) -> None:
        """
        Initialize the device fetcher.

        Args:
            client: The Meraki API client.
        """
        self._client = client

    async def async_fetch_devices(self) -> dict[str, Any]:
        """
        Fetch device data from the Meraki API.

        Returns
        -------
            A dictionary containing the list of Meraki devices and battery readings.
        """
        tasks = {
            "devices": self._client._run_with_semaphore(
                self._client.organization.get_organization_devices(),
            ),
            "device_statuses": self._client._run_with_semaphore(
                self._client.organization.get_organization_devices_statuses(),
            ),
            "devices_availabilities": self._client._run_with_semaphore(
                self._client.organization.get_organization_devices_availabilities(),
            ),
        }
        results = await asyncio.gather(*tasks.values(), return_exceptions=True)
        data = dict(zip(tasks.keys(), results, strict=True))

        devices_res = data.get("devices", [])
        if isinstance(devices_res, Exception):
            _LOGGER.warning(
                "Could not fetch devices, device data will be unavailable: %s",
                devices_res,
            )
            devices_list = []
            devices_raw: list[dict[str, Any]] = []
        else:
            devices_res = cast(list[dict[str, Any]], devices_res)
            devices_list = [MerakiDevice.from_dict(d) for d in devices_res]
            devices_raw = devices_res

        device_statuses = data.get("device_statuses", [])
        if isinstance(device_statuses, Exception):
            _LOGGER.warning(
                "Could not fetch device statuses, "
                "device status data will be unavailable: %s",
                device_statuses,
            )
            device_statuses = []
        else:
            device_statuses = cast(list[dict[str, Any]], device_statuses)

        parse_device_data(devices_list, device_statuses)

        # Fetch battery data separately
        battery_data_res = None
        mt_serials = [
            device["serial"]
            for device in devices_raw
            if device.get("model", "").startswith("MT")
        ]
        if mt_serials:
            battery_data_res = await self._client._run_with_semaphore(
                self._client.sensor.get_organization_sensor_readings_latest_for_serials(
                    serials=mt_serials,
                    metrics=["battery"],
                ),
            )

        return {"devices": devices_list, "battery_readings": battery_data_res}
