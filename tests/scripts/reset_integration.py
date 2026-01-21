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
    """Delete existing Meraki HA integration entries."""
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
        if resp.status != 200:
            print(f"Restart call failed: {resp.status}")
            return False
    # Wait loop
    print("Waiting for Home Assistant to restart...")
    await asyncio.sleep(15)  # Initial buffer
    for i in range(30):  # Try for 5 minutes (30 * 10s)
        try:
            async with session.get(f"{HA_URL}/api/", timeout=5) as resp:
                if resp.status == 200:
                    print("Home Assistant is online.")
                    return True
        except Exception:
            pass
        await asyncio.sleep(10)
        print(f"Waiting... ({i+1}/30)")
    return False


async def add_integration():
    """Add the Meraki HA integration via WebSocket config flow."""
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
            await ws.send_json(
                {"id": 1, "type": "config_entries/flow/start", "handler": "meraki_ha"}
            )
            resp = await ws.receive_json()
            flow_id = resp["result"]["flow_id"]

            # Step 1: API Key
            print("Sending API Key...")
            await ws.send_json(
                {
                    "id": 2,
                    "type": "config_entries/flow/handle_step",
                    "flow_id": flow_id,
                    "step_id": "user",
                    "user_input": {"api_key": MERAKI_API_KEY},
                }
            )
            resp = await ws.receive_json()

            # Handle optional Step 2 (Org Selection) if it occurs
            if resp["result"].get("step_id") == "pick_organization":
                print("Selecting Organization...")
                await ws.send_json(
                    {
                        "id": 3,
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
