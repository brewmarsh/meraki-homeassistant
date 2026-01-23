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

# Sanity Check
if not all([HA_URL, HA_TOKEN, MERAKI_API_KEY, MERAKI_ORG_ID]):
    logger.error("Missing required environment variables.")
    sys.exit(1)

HEADERS = {
    "Authorization": f"Bearer {HA_TOKEN}",
    "Content-Type": "application/json",
}


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


async def add_integration():
    """Add the Meraki HA integration via WebSocket."""
    ws_url = HA_URL.replace("http", "ws").replace("https", "wss") + "/api/websocket"
    logger.info(f"Connecting to WebSocket: {ws_url}")

    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(ws_url) as ws:
            # 1. Authenticate
            logger.debug("Waiting for auth_required...")
            await ws.receive_json()  # Consume 'auth_required'

            logger.debug("Sending auth token...")
            await ws.send_json({"type": "auth", "access_token": HA_TOKEN})

            auth_resp = await ws.receive_json()
            if auth_resp["type"] != "auth_ok":
                logger.error(f"WebSocket Auth Failed: {auth_resp}")
                return False
            logger.info("WebSocket Authentication Successful.")

            # 2. Start Config Flow
            logger.info("Starting Config Flow...")
            flow_id = None
            message_id = 1

            for i in range(10):
                msg = {
                    "id": message_id,
                    "type": "config_entries/flow/start",
                    "handler": "meraki_ha",
                }
                logger.debug(f"Sending: {msg}")
                await ws.send_json(msg)

                resp = await ws.receive_json()
                logger.debug(f"Received: {resp}")

                if resp.get("success"):
                    flow_id = resp["result"]["flow_id"]
                    logger.info(f"Config flow started successfully. ID: {flow_id}")
                    break

                error_code = resp.get("error", {}).get("code")
                error_msg = resp.get("error", {}).get("message")

                if error_code == "unknown_command":
                    logger.warning(
                        "Attempt %s: 'unknown_command'. The 'config' integration "
                        "is not loaded yet.",
                        i + 1,
                    )
                elif error_msg == "Invalid handler specified":
                    logger.critical(
                        "❌ Critical Error: Config Flow Handler mismatch. "
                        "Is 'meraki_ha' installed?"
                    )
                    sys.exit(1)
                else:
                    logger.error(f"Attempt {i+1} failed with error: {error_msg}")

                message_id += 1
                await asyncio.sleep(5)

            if not flow_id:
                logger.error("Failed to start config flow after multiple attempts.")
                return False

            # 3. Submit API Key
            logger.info("Sending API Key...")
            message_id += 1
            await ws.send_json(
                {
                    "id": message_id,
                    "type": "config_entries/flow/handle_step",
                    "flow_id": flow_id,
                    "step_id": "user",
                    "user_input": {"api_key": MERAKI_API_KEY},
                }
            )
            resp = await ws.receive_json()
            logger.debug(f"API Key Response: {resp}")

            # 4. Handle Optional Organization Step
            if (
                resp.get("success")
                and resp["result"].get("step_id") == "pick_organization"
            ):
                logger.info("Selecting Organization...")
                message_id += 1
                await ws.send_json(
                    {
                        "id": message_id,
                        "type": "config_entries/flow/handle_step",
                        "flow_id": flow_id,
                        "step_id": "pick_organization",
                        "user_input": {"organization_id": MERAKI_ORG_ID},
                    }
                )
                resp = await ws.receive_json()
                logger.debug(f"Org Selection Response: {resp}")

            # 5. Final Verification
            if resp.get("success") and resp["result"].get("type") == "create_entry":
                logger.info("SUCCESS: Integration re-added.")
                return True
            else:
                logger.error(f"FAILED: {resp}")
                return False


async def main():
    """
    Remove existing Meraki entries, restart Home Assistant,
    and re-add integration.
    """  # noqa: D205
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        if not await delete_existing_entries(session):
            sys.exit(1)
        if not await restart_and_wait(session):
            sys.exit(1)
    if not await add_integration():
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
