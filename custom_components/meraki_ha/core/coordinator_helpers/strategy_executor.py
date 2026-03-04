"""Strategy Executor for Meraki data fetching."""

from __future__ import annotations

from typing import Any

from ..models.device import MerakiDevice
from ..models.network import MerakiNetwork


def collect_network_tasks(
    data: dict[str, Any], tasks: dict[str, Any], strategies: dict[str, Any]
) -> None:
    """Collect network-level strategy tasks."""
    network_strategy_map = {
        "appliance": lambda nid, pts, tks: strategies["appliance"].build_network_tasks(
            nid, tks
        ),
        "wireless": lambda nid, pts, tks: strategies["wireless"].build_network_tasks(
            nid, pts, tks
        ),
    }

    for network in data.get("networks", []):
        if not isinstance(network, MerakiNetwork) or not network.id:
            continue

        network_id = str(network.id)
        product_types = network.product_types or []

        for ptype, build_func in network_strategy_map.items():
            if ptype in product_types:
                build_func(network_id, product_types, tasks)


def collect_device_tasks(
    data: dict[str, Any],
    tasks: dict[str, Any],
    strategies: dict[str, Any],
    capability_getter: Any,
) -> None:
    """Collect device-level strategy tasks."""
    for device in data.get("devices", []):
        if not isinstance(device, MerakiDevice) or not device.serial:
            continue

        if not device.product_type:
            continue

        if strategy := strategies.get(device.product_type):
            strategy.build_device_tasks(
                device, tasks, capability_getter(device.model), data
            )


def process_device_strategies(
    data: dict[str, Any],
    previous_devices_map: dict[str, MerakiDevice],
    strategies: dict[str, Any],
) -> None:
    """Process strategy-based updates for individual devices."""
    for device in data.get("devices", []):
        if not isinstance(device, MerakiDevice) or not device.serial:
            continue

        if not device.product_type:
            continue

        if strategy := strategies.get(device.product_type):
            strategy.process_device_details(
                device, data, previous_devices_map.get(device.serial)
            )


def _process_single_network_strategies(
    network: MerakiNetwork,
    data: dict[str, Any],
    current_data: dict[str, Any],
    strategies: dict[str, Any],
) -> None:
    """Process strategy-based updates for a single network."""
    if not isinstance(network, MerakiNetwork) or not network.id:
        return

    network_id = str(network.id)
    product_types = network.product_types or []

    for product_type in product_types:
        if strategy := strategies.get(product_type):
            if hasattr(strategy, "process_network_data"):
                strategy.process_network_data(
                    network_id,
                    data,
                    current_data,
                    data,
                )


def process_network_strategies(
    data: dict[str, Any],
    current_data: dict[str, Any] | None,
    strategies: dict[str, Any],
) -> None:
    """Process strategy-based updates for networks."""
    for network in data.get("networks", []):
        _process_single_network_strategies(
            network, data, current_data or {}, strategies
        )
