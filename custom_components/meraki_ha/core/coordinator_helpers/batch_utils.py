"""Batch execution utilities with smart error handling."""

from __future__ import annotations

import asyncio
import logging
import time
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


async def execute_batches(tasks: dict[str, Any], label: str) -> list[Any]:
    """Execute tasks in batches with dynamic cooldown bypass for cached data."""
    task_items = list(tasks.items())
    all_results = []
    for i in range(0, len(task_items), BATCH_SIZE):
        chunk = dict(task_items[i : i + BATCH_SIZE])
        _LOGGER.debug(
            "Executing %s batch: items %d to %d",
            label,
            i + 1,
            min(i + BATCH_SIZE, len(task_items)),
        )

        # Action 2 & 3: Measure execution time to detect local cache hits
        start_time = time.perf_counter()
        chunk_results = await asyncio.gather(*chunk.values(), return_exceptions=True)
        elapsed = time.perf_counter() - start_time

        all_results.extend(chunk_results)

        # Action 4: If there are more items, determine if we need to sleep
        if i + BATCH_SIZE < len(task_items):
            if elapsed < 0.2:  # 200ms heuristic for local memory cache
                _LOGGER.debug(
                    "%s batch executed in %.3fs (likely cached). Skipping cooldown.",
                    label,
                    elapsed,
                )
            else:
                _LOGGER.debug(
                    "%s batch executed in %.3fs. Cooling down for 1s...",
                    label,
                    elapsed,
                )
                await asyncio.sleep(1)

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
                    "Skipping %s: Configuration requirement not met in Dashboard.",
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
    tasks: dict[str, Any], timeout: int = 25, label: str = "Tasks"
) -> dict[str, Any]:
    """Gather tasks with timeout, batching, and smart error transformation."""
    if not tasks:
        return {}

    _LOGGER.debug(
        "Starting %s: %s items in batches of %s", label, len(tasks), BATCH_SIZE
    )

    try:
        results = await asyncio.wait_for(execute_batches(tasks, label), timeout=timeout)
        return process_batch_results(tasks, results, label)

    except asyncio.TimeoutError:
        handle_batch_exceptions(tasks, label)
        raise
