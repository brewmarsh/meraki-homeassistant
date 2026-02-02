import asyncio
import logging
import os
import sys

import aiohttp

# --- Setup Logging ---
logging.basicConfig(
    level=logging.DEBUG,  # Set to DEBUG to see detailed flow
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

# --- Configuration ---
HA_URL = os.getenv("HA_URL")
HA_TOKEN = os.getenv("HA_TOKEN")
MERAKI_API_KEY = os.getenv("MERAKI_API_KEY")
MERAKI_ORG_ID = os.getenv("MERAKI_ORG_ID")

# IMPROVED Sanity Check
required_vars = {
    "HA_URL": HA_URL,
    "HA_TOKEN": HA_TOKEN,
    "MERAKI_API_KEY": MERAKI_API_KEY,
    "MERAKI_ORG_ID": MERAKI_ORG_ID,
}
missing = [key for key, val in required_vars.items() if not val]

if missing:
    logger.critical(
        "❌ CRITICAL: The following environment variables are MISSING or EMPTY: %s",
        ", ".join(missing),
    )
    logger.critical(
        "Please check your GitHub Repository Secrets and "
        ".github/workflows/test.yml mappings."
    )
    sys.exit(1)

HEADERS = {
    "Authorization": f"Bearer {HA_TOKEN}",
    "Content-Type": "application/json",
}


async def dump_error_log(session):
    """Fetch and log the last 20 lines of the Home Assistant error log."""
    logger.info("Fetching error log to diagnose failure...")
    try:
        async with session.get(f"{HA_URL}/api/error/log") as log_resp:
            if log_resp.status == 200:
                log_text = await log_resp.text()
                logger.error("--- SYSTEM LOG (Last 20 lines) ---")
                lines = log_text.splitlines()
                for line in lines[-20:]:
                    logger.error(line)
                logger.error("----------------------------------")
            else:
                logger.error(f"Failed to fetch error log: {log_resp.status}")
    except Exception as e:
        logger.error(f"Error fetching error log: {e}")


async def delete_existing_entries(session):
    """Delete any existing Meraki HA config entries."""
    logger.info("Checking for existing Meraki HA entries...")
    url = f"{HA_URL}/api/config/config_entries/entry"
    logger.debug(f"GET {url}")

    async with session.get(url) as resp:
        if resp.status != 200:
            logger.error(f"Error fetching entries: {resp.status} - {await resp.text()}")
            return False

        entries = await resp.json()
        meraki_entries = [e for e in entries if e["domain"] == "meraki_ha"]

        if not meraki_entries:
            logger.info("No existing entries found.")
            return True

        for entry in meraki_entries:
            entry_id = entry["entry_id"]
            logger.info(f"Deleting entry {entry_id}...")
            async with session.delete(f"{url}/{entry_id}") as del_resp:
                if del_resp.status != 200:
                    logger.error(f"Failed to delete entry: {del_resp.status}")
                    return False
        return True


async def restart_and_wait(session):
    """Restart Home Assistant and wait for it to come back online."""
    logger.info("Restarting Home Assistant...")
    try:
        async with session.post(f"{HA_URL}/api/services/homeassistant/restart") as resp:
            if resp.status == 200:
                logger.debug("Restart command sent successfully.")
            else:
                logger.warning(f"Restart command sent with status: {resp.status}")
    except (
        aiohttp.ServerDisconnectedError,
        aiohttp.ClientConnectionError,
        aiohttp.ClientOSError,
    ):
        logger.info("Server disconnected immediately (Restart successful).")
    except Exception as e:
        logger.error(f"Unexpected error during restart: {e}")
        return False

    logger.info("Waiting for Home Assistant to restart...")
    await asyncio.sleep(15)  # Initial buffer

    # Poll for status
    for i in range(30):
        try:
            async with session.get(f"{HA_URL}/api/config", timeout=5) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    state = data.get("state")
                    if state == "RUNNING":
                        logger.info("Home Assistant is RUNNING.")
                        return True
                    else:
                        logger.debug(f"Home Assistant state: {state}")
                else:
                    logger.debug(f"API Ping failed: {resp.status}")
        except Exception as e:
            logger.debug(f"Connection failed: {e}")

        await asyncio.sleep(10)
        logger.info(f"Waiting... ({i + 1}/30)")

    logger.error("Timed out waiting for Home Assistant to restart.")
    return False


async def diagnose_server_state(session):
    """Diagnose server state.

    Perform deep diagnostics to check permissions, components, and safe mode.
    Replaces the simple 'check_loaded_components'.
    """
    logger.info("--- DIAGNOSTIC CHECK ---")

    # 1. Check User Permissions (Authentication Check)
    async with session.get(f"{HA_URL}/api/") as resp:
        if resp.status == 200:
            msg = await resp.json()
            logger.info(f"✅ API Connection OK. Message: {msg.get('message')}")
        else:
            logger.error(
                f"❌ API Connection Failed: {resp.status} "
                "(Check HA_STAGING_TOKEN permissions)"
            )
            return False

    # 2. Check Loaded Components & Safe Mode
    async with session.get(f"{HA_URL}/api/config") as resp:
        if resp.status != 200:
            logger.error(f"❌ Failed to fetch config: {resp.status}")
            return False

        data = await resp.json()
        components = set(data.get("components", []))

        # A. Check for 'config' integration
        if "config" in components:
            logger.info("✅ 'config' component is LOADED.")
        else:
            logger.error(
                "🚨 'config' component is MISSING! (This is why WebSocket fails)"
            )
            logger.debug(f"Loaded components: {sorted(components)}")

        # B. Check for Safe Mode
        if data.get("safe_mode", False):
            logger.error("🚨 SAFE MODE IS ENABLED! (Commands are disabled)")
        else:
            logger.info("✅ Safe Mode is OFF.")

        # C. Dump Error Log if things look bad
        if "config" not in components or data.get("safe_mode", False):
            await dump_error_log(session)
            return False

    logger.info("------------------------")
    return True


async def add_integration(session):
    """Add the Meraki HA integration via HTTP REST API."""
    logger.info("--- Starting REST API Config Flow ---")

    # 1. Start Config Flow
    start_url = f"{HA_URL}/api/config/config_entries/flow"
    start_payload = {"handler": "meraki_ha"}
    logger.info(f"POST {start_url} with payload: {start_payload}")

    async with session.post(start_url, json=start_payload) as resp:
        if resp.status != 200:
            logger.error(f"Failed to start config flow: {resp.status}")
            logger.error(await resp.text())
            return False

        start_data = await resp.json()
        flow_id = start_data.get("flow_id")
        if not flow_id:
            logger.error(f"Could not find flow_id in response: {start_data}")
            return False
        logger.info(f"Config flow started. flow_id: {flow_id}")

    # 2. Submit Credentials
    submit_url = f"{HA_URL}/api/config/config_entries/flow/{flow_id}"
    submit_payload = {
        "meraki_api_key": MERAKI_API_KEY,
        "meraki_org_id": MERAKI_ORG_ID,
    }
    logger.info(f"POST {submit_url}")

    async with session.post(submit_url, json=submit_payload) as resp:
        if resp.status != 200:
            logger.error(f"Failed to submit credentials: {resp.status}")
            logger.error(await resp.text())
            return False

        submit_data = await resp.json()

    # 3. Final Verification
    if submit_data.get("type") == "create_entry":
        logger.info("SUCCESS: Integration re-added via REST API.")
        return True
    else:
        logger.error(f"FAILED: Unexpected final response: {submit_data}")
        return False


async def main():
    """
    Remove existing Meraki entries, restart Home Assistant,
    verify server state, and re-add integration.
    """  # noqa: D205
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        # --- Stop Delete Existing Entries ---
        #        if not await delete_existing_entries(session):
        #            sys.exit(1)
        if not await restart_and_wait(session):
            sys.exit(1)
        # Added Diagnostic Step:
        if not await diagnose_server_state(session):
            sys.exit(1)

        if not await add_integration(session):
            sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
