"""Batch execution utilities with smart error handling."""

from __future__ import annotations

import asyncio
import logging
from typing import Any

from ...core.errors import (
    MerakiTrafficAnalysisError,
    MerakiVlansDisabledError,
)

_LOGGER = logging.getLogger(__name__)

BATCH_SIZE = 5

SILENT_ERRORS = [
    "Traffic Analysis with Hostname Visibility must be enabled",
    "VLANs are not enabled for this network",
]


async def execute_batches(
    tasks: dict[str, Any],
    label: str,
    batch_size: int = BATCH_SIZE,
    cooldown: float = 1.0,
) -> list[Any]:
    """Execute tasks in batches with cooldown."""
    task_items = list(tasks.items())
    all_results = []
    for i in range(0, len(task_items), batch_size):
        if i > 0 and cooldown > 0:
            _LOGGER.debug("Cooling down for %.2fs between %s batches...", cooldown, label)
            await asyncio.sleep(cooldown)

        chunk = dict(task_items[i : i + batch_size])
        _LOGGER.debug(
            "Executing %s batch: items %d to %d",
            label,
            i + 1,
            min(i + batch_size, len(task_items)),
        )
        chunk_results = await asyncio.gather(*chunk.values(), return_exceptions=True)
        all_results.extend(chunk_results)
    return all_results


def handle_fetch_exception(
    exception: Exception, key: str, label: str
) -> Exception | None:
    """Handle and transform fetch exceptions for smart updates."""
    if isinstance(exception, (MerakiTrafficAnalysisError, MerakiVlansDisabledError)):
        _LOGGER.debug("Feature disabled for %s during %s: %s", key, label, exception)
        return exception

    _LOGGER.error("Error fetching %s during %s: %s", key, label, exception)
    return None


def process_single_result(key: str, result: Any, label: str) -> Any:
    """Process a single task result with smart error handling."""
    if isinstance(result, Exception):
        error_msg = str(result)
        is_silent = False
        for silent_msg in SILENT_ERRORS:
            if silent_msg in error_msg:
                _LOGGER.debug(
                    "Skipping %s: Configuration requirement not met in Meraki Dashboard.",
                    key,
                )
                is_silent = True
                break

        if is_silent:
            if "Traffic Analysis" in error_msg:
                return MerakiTrafficAnalysisError(error_msg)
            if "VLANs" in error_msg:
                return MerakiVlansDisabledError(error_msg)
            return []

        return handle_fetch_exception(result, key, label)

    if isinstance(result, (dict, list)) or result is None:
        return result

    _LOGGER.debug(
        "Filtering out unexpected type %s for %s during %s",
        type(result),
        key,
        label,
    )
    return None


def process_batch_results(
    tasks: dict[str, Any], results: list[Any], label: str
) -> dict[str, Any]:
    """Process raw batch results into sanitized dictionary."""
    sanitized_results: dict[str, Any] = {}
    for key, result in zip(tasks.keys(), results, strict=True):
        sanitized_results[key] = process_single_result(key, result, label)
    return sanitized_results


def handle_batch_exceptions(tasks: dict[str, Any], label: str) -> None:
    """Handle timeout exceptions during batch gathering."""
    _LOGGER.error("Timeout during %s. Potential semaphore deadlock.", label)
    _LOGGER.debug("Pending keys for %s: %s", label, list(tasks.keys()))
    for task in tasks.values():
        if asyncio.iscoroutine(task):
            task.close()


async def async_gather_with_timeout(
    tasks: dict[str, Any],
    timeout: int = 25,
    label: str = "Tasks",
    batch_size: int = BATCH_SIZE,
    cooldown: float = 1.0,
) -> dict[str, Any]:
    """Gather tasks with timeout, batching, and smart error transformation."""
    if not tasks:
        return {}

    _LOGGER.debug(
        "Starting %s: %s items in batches of %s", label, len(tasks), batch_size
    )

    try:
        results = await asyncio.wait_for(
            execute_batches(tasks, label, batch_size=batch_size, cooldown=cooldown),
            timeout=timeout,
        )
        return process_batch_results(tasks, results, label)

    except asyncio.TimeoutError:
        handle_batch_exceptions(tasks, label)
        raise
