import asyncio
import os
import sys

import aiohttp

# Configuration
HA_URL = os.getenv("HA_URL")
HA_TOKEN = os.getenv("HA_TOKEN")
MERAKI_API_KEY = os.getenv("MERAKI_API_KEY")
MERAKI_ORG_ID = os.getenv("MERAKI_ORG_ID")
HEADERS = {"Authorization": f"Bearer {HA_TOKEN}", "Content-Type": "application/json"}


async def delete_existing_entries(session):
    """Delete any existing Meraki HA config entries."""
    print("Checking for existing Meraki HA entries...")
    async with session.get(f"{HA_URL}/api/config/config_entries/entry") as resp:
        if resp.status != 200:
            print(f"Error fetching entries: {resp.status}")
            return False
        entries = await resp.json()
        meraki_entries = [e for e in entries if e["domain"] == "meraki_ha"]
        if not meraki_entries:
            print("No existing entries found.")
            return True

        for entry in meraki_entries:
            print(f"Deleting entry {entry['entry_id']}...")
            async with session.delete(
                f"{HA_URL}/api/config/config_entries/entry/{entry['entry_id']}"
            ) as resp:
                if resp.status != 200:
                    print(f"Failed to delete entry: {resp.status}")
                    return False
        return True


async def restart_and_wait(session):
    """Restart Home Assistant and wait for it to come back online."""
    print("Restarting Home Assistant...")
    async with session.post(f"{HA_URL}/api/services/homeassistant/restart") as resp:
        if resp.status == 200:
            print("Success")
        elif resp.status in [502, 504]:
            print("Server disconnected (Restarting)...")
        else:
            print(f"Restart call failed: {resp.status}")
            return False
    # Wait loop
    print("Waiting for Home Assistant to restart...")
    await asyncio.sleep(15)  # Initial buffer
    for i in range(30):  # Try for 5 minutes (30 * 10s)
        try:
            async with session.get(f"{HA_URL}/api/config", timeout=5) as resp:
                if resp.status == 200:
                    resp_json = await resp.json()
                    state = resp_json.get("state")
                    if state == "RUNNING":
                        print("Home Assistant is RUNNING.")
                        return True
                    else:
                        print(f"Home Assistant state: {state}")

        except Exception:
            pass
        await asyncio.sleep(10)
        print(f"Waiting... ({i + 1}/30)")
    return False


async def add_integration():
    """Add the Meraki HA integration via WebSocket."""
    ws_url = HA_URL.replace("http", "ws").replace("https", "wss") + "/api/websocket"
    print(f"Connecting to WebSocket: {ws_url}")
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(ws_url) as ws:
            # Auth
            await ws.receive_json()  # auth_required
            await ws.send_json({"type": "auth", "access_token": HA_TOKEN})
            auth_resp = await ws.receive_json()
            if auth_resp["type"] != "auth_ok":
                print("WebSocket Auth Failed")
                return False

            # Start Flow
            print("Starting Config Flow...")
            flow_id = None
            message_id = 1
            for i in range(10):  # 10 attempts
                await ws.send_json(
                    {
                        "id": message_id,
                        "type": "config_entries/flow/start",
                        "handler": "meraki_ha",
                    }
                )
                resp = await ws.receive_json()
                if resp.get("success"):
                    flow_id = resp["result"]["flow_id"]
                    print("Config flow started successfully.")
                    break
                else:
                    print(f"Attempt {i + 1}/10 failed: {resp}")
                    message_id += 1
                    await asyncio.sleep(5)  # 5-second delay

            if not flow_id:
                print("Failed to start config flow after multiple attempts.")
                return False

            # Step 1: API Key
            print("Sending API Key...")
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

            # Handle optional Step 2 (Org Selection) if it occurs
            if resp.get("success") and (
                resp["result"].get("step_id") == "pick_organization"
            ):
                print("Selecting Organization...")
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

            if resp["success"] and resp["result"]["type"] == "create_entry":
                print("SUCCESS: Integration re-added.")
                return True
            else:
                print(f"FAILED: {resp}")
                return False


async def main():
    """Run the integration reset script."""
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        if not await delete_existing_entries(session):
            sys.exit(1)
        if not await restart_and_wait(session):
            sys.exit(1)
    if not await add_integration():
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
