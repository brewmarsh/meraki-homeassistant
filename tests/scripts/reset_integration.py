#!/usr/bin/env python3
"""Reset the Meraki HA integration by deleting and re-adding it via REST API.

This script is used in staging to ensure a clean state for smoke testing.
It uses the Home Assistant REST API to delete any existing Meraki entries,
restarts Home Assistant, and then adds a new entry with the correct credentials.
"""

import asyncio
import logging
import os
import sys
from typing import Any

import aiohttp

# Configuration from environment variables
HA_URL = os.getenv("HA_URL", "http://localhost:8123")
HA_TOKEN = os.getenv("HA_TOKEN")
MERAKI_API_KEY = os.getenv("MERAKI_API_KEY")
MERAKI_ORG_ID = os.getenv("MERAKI_ORG_ID")

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


async def dump_error_log(session: aiohttp.ClientSession) -> None:
    """Fetch and print the last few lines of the Home Assistant log."""
    url = f"{HA_URL}/api/error_log"
    try:
        async with session.get(url) as resp:
            if resp.status == 200:
                text = await resp.text()
                logger.error("--- Home Assistant Error Log (Last 20 lines) ---")
                for line in text.splitlines()[-20:]:
                    print(line)
                logger.error("--- End of Log ---")
    except Exception as e:
        logger.error(f"Error fetching error log: {e}")


async def _get_existing_entries(
    session: aiohttp.ClientSession,
) -> list[dict[str, Any]] | None:
    """Fetch all Meraki HA config entries."""
    url = f"{HA_URL}/api/config/config_entries/entry"
    logger.debug(f"GET {url}")

    async with session.get(url) as resp:
        if resp.status != 200:
            logger.error(f"Error fetching entries: {resp.status} - {await resp.text()}")
            return None

        entries = await resp.json()
        return [e for e in entries if e["domain"] == "meraki_ha"]


async def _delete_entries(
    session: aiohttp.ClientSession, entries: list[dict[str, Any]]
) -> bool:
    """Delete the provided config entries."""
    url = f"{HA_URL}/api/config/config_entries/entry"
    for entry in entries:
        entry_id = entry["entry_id"]
        logger.info(f"Removing existing Meraki HA configuration ({entry_id}).")
        async with session.delete(f"{url}/{entry_id}") as del_resp:
            if del_resp.status != 200:
                logger.error(f"Failed to delete entry: {del_resp.status}")
                return False
    return True


async def delete_existing_entries(session: aiohttp.ClientSession) -> bool:
    """Delete any existing Meraki HA config entries."""
    logger.info("Checking for existing Meraki HA entries...")

    meraki_entries = await _get_existing_entries(session)
    if meraki_entries is None:
        return False

    if not meraki_entries:
        logger.info("No existing entries found.")
        return True

    return await _delete_entries(session, meraki_entries)


async def _send_restart_command(session: aiohttp.ClientSession) -> bool:
    """Send the restart command to Home Assistant."""
    restart_url = f"{HA_URL}/api/services/homeassistant/restart"
    logger.info("Restarting Home Assistant...")
    
    try:
        # A timeout ensures we don't hang if the reverse proxy blackholes the connection
        async with session.post(restart_url, timeout=15) as resp:
            # 200 = OK, 502/504 = Server went down before responding (Normal)
            if resp.status in (200, 502, 504):
                logger.warning(f"Restart command sent with status: {resp.status}")
                return True
                
            logger.error(f"Restart command failed: {resp.status}")
            return False
            
    except (aiohttp.ClientError, asyncio.TimeoutError):
        # Connection violently dropping is the ultimate proof it is restarting
        logger.warning("Connection dropped. Restart is in progress.")
        return True


async def _wait_for_restart(session: aiohttp.ClientSession) -> bool:
    """Wait for Home Assistant to become available again."""
    logger.info("Waiting for Home Assistant to restart...")
    # Wait for HA to go down
    await asyncio.sleep(10)

    max_retries = 30
    retry_interval = 10

    for i in range(max_retries):
        try:
            async with session.get(f"{HA_URL}/api/") as resp:
                if resp.status == 200:
                    logger.info("✅ Home Assistant is back online.")
                    # Wait a little longer for components to initialize
                    await asyncio.sleep(15)
                    return True
        except (aiohttp.ClientError, asyncio.TimeoutError):
            pass

        if i % 3 == 0:
            logger.info(f"  Still waiting... ({i*retry_interval}s)")
        await asyncio.sleep(retry_interval)

    logger.error("Timed out waiting for Home Assistant to restart.")
    return False


async def restart_homeassistant(session: aiohttp.ClientSession) -> bool:
    """Restart Home Assistant and wait for it to be ready."""
    if not await _send_restart_command(session):
        return False

    return await _wait_for_restart(session)


async def _check_api_connection(session: aiohttp.ClientSession) -> bool:
    """Check if the Home Assistant REST API is accessible."""
    try:
        async with session.get(f"{HA_URL}/api/") as resp:
            if resp.status == 200:
                data = await resp.json()
                if data.get("message") == "API running.":
                    return True
            logger.error(f"API Check Failed: {resp.status} - {await resp.text()}")
            return False
    except Exception as e:
        logger.error(f"Failed to connect to Home Assistant at {HA_URL}: {e}")
        return False


def _verify_components(components: set[str]) -> bool:
    """Verify required components are loaded."""
    if "config" in components:
        logger.info("✅ 'config' component is LOADED.")
        return True

    logger.error("🚨 'config' component is MISSING! (This is why WebSocket fails)")
    logger.debug(f"Loaded components: {sorted(components)}")
    return False


def _verify_safe_mode(safe_mode: bool) -> bool:
    """Verify safe mode is not enabled."""
    if safe_mode:
        logger.error("🚨 SAFE MODE IS ENABLED! (Commands are disabled)")
        return False

    logger.info("✅ Safe Mode is OFF.")
    return True


async def _check_components_and_safe_mode(
    session: aiohttp.ClientSession,
) -> bool:
    """Check if safe mode is enabled or critical components are missing."""
    url = f"{HA_URL}/api/config"
    try:
        async with session.get(url) as resp:
            if resp.status != 200:
                logger.error(f"Failed to fetch config: {resp.status}")
                return False

            data = await resp.json()

            components_ok = _verify_components(set(data.get("components", [])))
            safe_mode_ok = _verify_safe_mode(data.get("safe_mode", False))

            if not components_ok or not safe_mode_ok:
                await dump_error_log(session)
                return False

            return True
    except Exception as e:
        logger.error(f"Failed to fetch config components: {e}")
        return False


async def _start_config_flow(session: aiohttp.ClientSession) -> dict[str, Any] | None:
    """Initiate the configuration flow for meraki_ha."""
    flow_url = f"{HA_URL}/api/config/config_entries/flow"
    payload = {"handler": "meraki_ha", "show_advanced_options": True}

    logger.info("Initiating config flow for meraki_ha...")
    async with session.post(flow_url, json=payload) as resp:
        if resp.status != 201:
            logger.error(f"Failed to start config flow: {resp.status}")
            logger.debug(await resp.text())
            return None
        return await resp.json()  # type: ignore


def _build_form_payload(step_id: str, current_step: dict[str, Any]) -> dict[str, Any]:
    """Build the payload for submitting a form step."""
    payload: dict[str, Any] = {}
    if step_id == "user":
        payload = {
            "api_key": MERAKI_API_KEY,
            "org_id": MERAKI_ORG_ID,
        }
    else:
        # Generic handler for other steps - just take defaults
        for field in current_step.get("data_schema", []):
            if "default" in field:
                payload[field["name"]] = field["default"]
            else:
                logger.warning(
                    f"Required field '{field['name']}' has no default value."
                )
    return payload


async def _handle_form_step(
    session: aiohttp.ClientSession, current_step: dict[str, Any], flow_id: str
) -> dict[str, Any] | None:
    """Handle a form step in the configuration flow."""
    step_id = current_step.get("step_id")
    logger.info(f"ℹ️ Received form step: {step_id}")

    payload = _build_form_payload(step_id, current_step)

    submit_url = f"{HA_URL}/api/config/config_entries/flow/{flow_id}"
    logger.info(f"POST {submit_url} for step {step_id} with payload: {payload}")
    async with session.post(submit_url, json=payload) as resp:
        if resp.status != 200:
            logger.error(f"Failed to submit step {step_id}: {resp.status}")
            logger.debug(await resp.text())
            return None
        return await resp.json()  # type: ignore


async def _handle_step_abort(current_step: dict[str, Any]) -> bool:
    """Handle an aborted step in the configuration flow."""
    reason = current_step.get("reason")
    if reason == "already_configured":
        logger.info("Integration is already configured.")
        return True
    logger.error(f"Flow aborted: {current_step}")
    return False


async def _handle_step_form(
    session: aiohttp.ClientSession, current_step: dict[str, Any], flow_id: str
) -> dict[str, Any] | None:
    """Handle a form step and return the next step, or None if failed."""
    next_step = await _handle_form_step(session, current_step, flow_id)
    if next_step is None:
        return None
    return next_step


async def _process_single_flow_step(
    session: aiohttp.ClientSession, current_step: dict[str, Any], flow_id: str
) -> tuple[bool, bool, dict[str, Any] | None]:
    """Process a single step and return (is_done, success_status, next_step)."""
    step_type = current_step.get("type")

    if step_type == "create_entry":
        logger.info("SUCCESS: Integration re-added via REST API.")
        return True, True, None
    if step_type == "abort":
        return True, await _handle_step_abort(current_step), None
    if step_type == "form":
        next_step = await _handle_step_form(session, current_step, flow_id)
        if next_step is None:
            return True, False, None
        return False, False, next_step

    logger.error(f"FAILED: Unexpected response type: {step_type}")
    logger.debug(f"Response: {current_step}")
    return True, False, None


async def _process_flow_steps(
    session: aiohttp.ClientSession, initial_step: dict[str, Any], flow_id: str
) -> bool:
    """Process the steps of the configuration flow."""
    current_step = initial_step
    while True:
        is_done, success, next_step = await _process_single_flow_step(
            session, current_step, flow_id
        )
        if is_done:
            return success
        if next_step is not None:
            current_step = next_step


async def add_integration(session: aiohttp.ClientSession) -> bool:
    """Re-add the Meraki integration using the config flow."""
    flow_data = await _start_config_flow(session)
    if not flow_data:
        return False

    flow_id = flow_data.get("flow_id")
    if not flow_id:
        logger.error("No flow_id returned from initial step.")
        return False

    return await _process_flow_steps(session, flow_data, flow_id)


async def main() -> None:
    """Run the reset sequence."""
    if not HA_TOKEN or not MERAKI_API_KEY or not MERAKI_ORG_ID:
        logger.error(
            "Missing environment variables: HA_TOKEN, MERAKI_API_KEY, or MERAKI_ORG_ID"
        )
        sys.exit(1)

    headers = {
        "Authorization": f"Bearer {HA_TOKEN}",
        "Content-Type": "application/json",
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        # Step 1: Verification
        logger.info("--- Step 1: Pre-Reset Verification ---")
        if not await _check_api_connection(session):
            sys.exit(1)

        if not await _check_components_and_safe_mode(session):
            logger.warning("Continuing despite verification warnings...")

        # Step 2: Delete
        logger.info("--- Step 2: Delete Existing Entry ---")
        if not await delete_existing_entries(session):
            logger.error("Failed to delete existing entries.")
            sys.exit(1)

        # Step 3: Restart
        logger.info("--- Step 3: Restart Home Assistant ---")
        if not await restart_homeassistant(session):
            sys.exit(1)

        # Step 4: Add
        logger.info("--- Step 4: Add Integration ---")
        if not await add_integration(session):
            logger.error("Failed to re-add integration.")
            await dump_error_log(session)
            sys.exit(1)

        logger.info("✨ Meraki HA Reset Sequence Complete!")


if __name__ == "__main__":
    asyncio.run(main())
