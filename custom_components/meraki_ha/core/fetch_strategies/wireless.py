"""Wireless fetch strategy."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ...core.models.network import MerakiNetwork

if TYPE_CHECKING:
    from ...core.models.device import MerakiDevice
from ..parsers.wireless import parse_wireless_data, update_processed_wireless_data
from .base import BaseFetchStrategy


class WirelessFetchStrategy(BaseFetchStrategy):
    """Strategy for fetching wireless data."""

    def build_network_tasks(
        self,
        network_id: str,
        product_types: list[str],
        tasks: dict[str, Any],
    ) -> None:
        """Add wireless specific network tasks."""
        tasks.update(
            self.client.wireless.get_network_detail_tasks(network_id, product_types)
        )

    def build_device_tasks(
        self,
        device: MerakiDevice,
        tasks: dict[str, Any],
        capabilities: list[str],
        detail_data: dict[str, Any] | None = None,
    ) -> None:
        """Add wireless specific device tasks."""
        if "led_control" in capabilities and device.serial:
            tasks[f"management_interface_{device.serial}"] = (
                self.client.run_with_semaphore(
                    self.client.devices.get_device_management_interface(device.serial),
                )
            )
        if "wireless" in capabilities and device.serial:
            tasks[f"wireless_radio_settings_{device.serial}"] = (
                self.client.run_with_semaphore(
                    self.client.wireless.get_wireless_settings(device.serial),
                )
            )

    def process_device_details(
        self,
        device: MerakiDevice,
        detail_data: dict[str, Any],
        prev_device: MerakiDevice | None,
    ) -> None:
        """Process wireless device details."""
        interface_key = f"management_interface_{device.serial}"
        if management_interface := detail_data.get(interface_key):
            if isinstance(management_interface, dict):
                device.management_interface = management_interface
        elif prev_device and hasattr(prev_device, "management_interface"):
            device.management_interface = prev_device.management_interface

        radio_settings_key = f"wireless_radio_settings_{device.serial}"
        if radio_settings := detail_data.get(radio_settings_key):
            if isinstance(radio_settings, dict):
                device.wireless_radio_settings = radio_settings
        elif prev_device and hasattr(prev_device, "wireless_radio_settings"):
            device.wireless_radio_settings = prev_device.wireless_radio_settings

    def process_network_data(
        self,
        network_id: str,
        detail_data: dict[str, Any],
        previous_data: dict[str, Any],
        processed_data: dict[str, Any],
    ) -> None:
        """Process wireless data (SSIDs and RF Profiles) for a network."""
        # Use the common wireless parser. Since this strategy method is called
        # per network, we pass the individual network's data.
        # We create a dummy MerakiNetwork object if we don't have the full list
        # but the parser only really needs the ID from it.
        network = MerakiNetwork(id=network_id, name="", product_types=["wireless"])

        wireless_data = parse_wireless_data(
            detail_data,
            [network],
            previous_data,
            clients=detail_data.get("clients"),
        )

        update_processed_wireless_data(processed_data, wireless_data)
