"""Fetches detailed data for the Meraki coordinator."""

from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING, Any, cast

if TYPE_CHECKING:
    from ...types import MerakiDevice, MerakiNetwork
    from ..api.client import MerakiAPIClient


_LOGGER = logging.getLogger(__name__)


class DetailFetcher:
    """Class to fetch detailed data."""

    def __init__(self, client: MerakiAPIClient) -> None:
        """
        Initialize the detail fetcher.

        Args:
            client: The Meraki API client.
        """
        self._client = client

    def build_detail_tasks(
        self,
        networks: list[MerakiNetwork],
        devices: list[MerakiDevice],
    ) -> dict[str, asyncio.Task[Any]]:
        """
        Build a dictionary of tasks to fetch detailed data.

        Args:
            networks: A list of networks.
            devices: A list of devices.

        Returns
        -------
            A dictionary of tasks.
        """
        detail_tasks: dict[str, asyncio.Task[Any]] = {}
        for network in networks:
            # Type narrowing for network.id
            if not network.id:
                continue
            network_id = cast(str, network.id)
            product_types = network.product_types
            if "wireless" in product_types:
                detail_tasks[f"ssids_{network_id}"] = asyncio.create_task(
                    self._client.run_with_semaphore(
                        self._client.wireless.get_network_ssids(network_id),
                    )
                )
            if "appliance" in product_types:
                if f"traffic_{network_id}" not in self._client._disabled_features:  # type: ignore[attr-defined]
                    detail_tasks[f"traffic_{network_id}"] = asyncio.create_task(
                        self._client.run_with_semaphore(
                            self._client.network.get_network_traffic(
                                network_id, "appliance"
                            ),
                        )
                    )

                if f"vlans_{network_id}" not in self._client._disabled_features:  # type: ignore[attr-defined]
                    detail_tasks[f"vlans_{network_id}"] = asyncio.create_task(
                        self._client.run_with_semaphore(
                            self._client.appliance.get_network_vlans(network_id),
                        )
                    )

                detail_tasks[f"l3_firewall_rules_{network_id}"] = asyncio.create_task(
                    self._client.run_with_semaphore(
                        self._client.appliance.get_l3_firewall_rules(network_id),
                    )
                )
                detail_tasks[f"traffic_shaping_{network_id}"] = asyncio.create_task(
                    self._client.run_with_semaphore(
                        self._client.appliance.get_traffic_shaping(network_id),
                    )
                )
                if self._client._enable_vpn_management:  # type: ignore[attr-defined]
                    detail_tasks[f"vpn_status_{network_id}"] = asyncio.create_task(
                        self._client.run_with_semaphore(
                            self._client.appliance.get_vpn_status(network_id),
                        )
                    )
                detail_tasks[f"appliance_ports_{network_id}"] = asyncio.create_task(
                    self._client.run_with_semaphore(
                        self._client.appliance.get_appliance_ports(network_id),
                    )
                )
                detail_tasks[f"content_filtering_{network_id}"] = asyncio.create_task(
                    self._client.run_with_semaphore(
                        self._client.appliance.get_network_appliance_content_filtering(
                            network_id,
                        ),
                    )
                )
            if "wireless" in product_types:
                detail_tasks[f"rf_profiles_{network_id}"] = asyncio.create_task(
                    self._client.run_with_semaphore(
                        self._client.wireless.get_network_wireless_rf_profiles(
                            network_id
                        ),
                    )
                )
        for device in devices:
            if device.product_type == "camera":
                detail_tasks[f"video_settings_{device.serial}"] = asyncio.create_task(
                    self._client.run_with_semaphore(
                        self._client.camera.get_camera_video_settings(device.serial),
                    )
                )
                detail_tasks[f"sense_settings_{device.serial}"] = asyncio.create_task(
                    self._client.run_with_semaphore(
                        self._client.camera.get_camera_sense_settings(device.serial),
                    )
                )
                detail_tasks[f"camera_analytics_{device.serial}"] = asyncio.create_task(
                    self._client.run_with_semaphore(
                        self._client.camera.get_device_camera_analytics_recent(
                            device.serial,
                        ),
                    )
                )
            elif device.product_type == "switch":
                detail_tasks[f"ports_statuses_{device.serial}"] = asyncio.create_task(
                    self._client.run_with_semaphore(
                        self._client.switch.get_device_switch_ports_statuses(
                            device.serial
                        ),
                    )
                )
            elif device.product_type == "appliance" and device.network_id:
                detail_tasks[f"appliance_settings_{device.serial}"] = (
                    asyncio.create_task(
                        self._client.run_with_semaphore(
                            self._client.appliance.get_network_appliance_settings(
                                device.network_id,
                            ),
                        )
                    )
                )
        return detail_tasks
