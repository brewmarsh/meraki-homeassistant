"""Manager for timed guest access keys."""

from __future__ import annotations

import asyncio
import logging
import secrets
import string
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Any

from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import storage
from homeassistant.util import dt as dt_util

from ..const import DATA_CLIENT, DOMAIN

if TYPE_CHECKING:
    from .api.client import MerakiAPIClient

_LOGGER = logging.getLogger(__name__)

STORAGE_KEY = f"{DOMAIN}.timed_access_keys"
STORAGE_VERSION = 1


@dataclass
class TimedAccessKey:
    """Class to represent a timed access key."""

    identity_psk_id: str
    network_id: str
    ssid_number: str
    name: str
    passphrase: str
    expires_at: str  # ISO formatted string
    config_entry_id: str


class TimedAccessManager:
    """Manager for timed guest access keys."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the manager."""
        self._hass = hass
        self._store = storage.Store(hass, STORAGE_VERSION, STORAGE_KEY)
        self._keys: list[TimedAccessKey] = []
        self._scheduled_removals: dict[str, asyncio.TimerHandle] = {}

    async def async_setup(self) -> None:
        """Set up the manager."""
        await self._load_keys()
        self._schedule_expirations()

    async def _load_keys(self) -> None:
        """Load keys from storage."""
        data = await self._store.async_load()
        if data:
            self._keys = [TimedAccessKey(**key) for key in data]

    @callback
    def _async_save_keys(self) -> None:
        """Save keys to storage."""
        self._hass.async_create_task(
            self._store.async_save([key.__dict__ for key in self._keys])
        )

    def _schedule_expirations(self) -> None:
        """Schedule expiration for all keys."""
        now = dt_util.utcnow()
        for key in self._keys:
            expires_at = dt_util.parse_datetime(key.expires_at)
            if not expires_at:
                continue

            if expires_at <= now:
                # Expired, remove immediately
                self._hass.async_create_task(self._remove_key_task(key))
            else:
                # Schedule removal
                self._schedule_removal(key, expires_at)

    def _schedule_removal(self, key: TimedAccessKey, expires_at: datetime) -> None:
        """Schedule removal of a key."""
        delay = (expires_at - dt_util.utcnow()).total_seconds()

        # Avoid scheduling if already passed or very close
        if delay <= 0:
            self._hass.async_create_task(self._remove_key_task(key))
            return

        self._scheduled_removals[key.identity_psk_id] = self._hass.loop.call_later(
            delay,
            lambda: self._hass.async_create_task(self._remove_key_task(key)),
        )

    async def _remove_key_task(self, key: TimedAccessKey) -> None:
        """Task wrapper to remove a key."""
        await self.delete_key(
            key.identity_psk_id,
            key.network_id,
            key.ssid_number,
            key.config_entry_id,
        )

    async def create_key(
        self,
        config_entry_id: str,
        network_id: str,
        ssid_number: str,
        duration_minutes: int,
        name: str | None = None,
        passphrase: str | None = None,
        group_policy_id: str | None = None,
    ) -> TimedAccessKey:
        """Create a new timed access key."""
        client = self._get_client(config_entry_id)
        if not client:
            raise ValueError("Meraki API client not found for config entry")

        if not name:
            name = f"HA-Guest-{int(dt_util.utcnow().timestamp())}"

        if not passphrase:
            passphrase = self._generate_passphrase()

        # Call API
        try:
            result = await client.wireless.create_identity_psk(
                network_id,
                ssid_number,
                name,
                group_policy_id,
                passphrase,
            )
        except Exception as e:
            _LOGGER.error("Failed to create Identity PSK: %s", e)
            raise

        if not result or "id" not in result:
             raise ValueError("Failed to create Identity PSK, invalid response")

        expires_at = dt_util.utcnow() + timedelta(minutes=duration_minutes)

        key = TimedAccessKey(
            identity_psk_id=result["id"],
            network_id=network_id,
            ssid_number=ssid_number,
            name=name,
            passphrase=passphrase,
            expires_at=expires_at.isoformat(),
            config_entry_id=config_entry_id,
        )

        self._keys.append(key)
        self._async_save_keys()
        self._schedule_removal(key, expires_at)

        return key

    def _generate_passphrase(self, length: int = 8) -> str:
        """Generate a secure passphrase."""
        alphabet = string.ascii_letters + string.digits
        return "".join(secrets.choice(alphabet) for _ in range(length))

    def _get_client(self, config_entry_id: str) -> MerakiAPIClient | None:
        """Get the Meraki API client."""
        # This assumes the client is stored in hass.data
        if DOMAIN not in self._hass.data:
            return None
        if config_entry_id not in self._hass.data[DOMAIN]:
            return None
        return self._hass.data[DOMAIN][config_entry_id][DATA_CLIENT]

    async def delete_key(
        self,
        identity_psk_id: str,
        network_id: str | None = None,
        ssid_number: str | None = None,
        config_entry_id: str | None = None
    ) -> None:
        """Delete a timed access key."""
        # Find key in memory
        key_to_remove = None
        for key in self._keys:
            if key.identity_psk_id == identity_psk_id:
                key_to_remove = key
                break

        if not key_to_remove:
            _LOGGER.warning("Attempted to delete unknown key %s", identity_psk_id)
            return

        # Cancel timer
        if identity_psk_id in self._scheduled_removals:
            self._scheduled_removals[identity_psk_id].cancel()
            del self._scheduled_removals[identity_psk_id]

        # Call API
        config_entry_id = config_entry_id or key_to_remove.config_entry_id
        client = self._get_client(config_entry_id)
        if client:
            try:
                await client.wireless.delete_identity_psk(
                    key_to_remove.network_id,
                    key_to_remove.ssid_number,
                    key_to_remove.identity_psk_id,
                )
            except Exception as e:
                _LOGGER.error("Failed to delete Identity PSK from Meraki: %s", e)
        else:
            _LOGGER.warning(
                "Meraki Client not available to delete PSK %s", identity_psk_id
            )

        # Remove from list and save
        self._keys.remove(key_to_remove)
        self._async_save_keys()

    def get_keys(self, network_id: str | None = None) -> list[dict[str, Any]]:
        """Get all keys, optionally filtered by network."""
        if network_id:
            return [k.__dict__ for k in self._keys if k.network_id == network_id]
        return [k.__dict__ for k in self._keys]
