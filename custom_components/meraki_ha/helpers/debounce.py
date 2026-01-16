# custom_components/meraki_ha/helpers/debounce.py
"""Debounce helper for Meraki Home Assistant integration."""

import asyncio
from collections.abc import Awaitable, Callable
from typing import Any, TypeVar

from homeassistant.core import HomeAssistant

T = TypeVar("T")


class Debounce:
    """Class to handle debouncing of calls."""

    def __init__(self, hass: HomeAssistant, cooldown: float) -> None:
        """Initialize the debouncer."""
        self.hass = hass
        self.cooldown = cooldown
        self._task: asyncio.TimerHandle | None = None
        self._target: Callable[..., Awaitable[T]] | None = None
        self._args: tuple[Any, ...] | None = None
        self._kwargs: dict[str, Any] | None = None

    async def async_call(
        self,
        target: Callable[..., Awaitable[T]],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Call the debounced function."""
        if self._task:
            self._task.cancel()

        self._target = target
        self._args = args
        self._kwargs = kwargs

        self._task = self.hass.loop.call_later(self.cooldown, self._execute)

    def _execute(self) -> None:
        """Execute the debounced function."""
        if self._target and self._args is not None and self._kwargs is not None:
            self.hass.create_task(self._target(*self._args, **self._kwargs))
        self._task = None
        self._target = None
        self._args = None
        self._kwargs = None

    def async_cancel(self) -> None:
        """Cancel any pending debounced call."""
        if self._task:
            self._task.cancel()
            self._task = None
            self._target = None
            self._args = None
            self._kwargs = None
