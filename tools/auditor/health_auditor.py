"""Automated Health Auditor for Meraki Integration."""
import asyncio
import json
import os
import re
import subprocess
from typing import Any, Dict, List, Optional

import aiohttp

# Constants
DOMAIN = "meraki_ha"
HA_URL = os.getenv("HA_URL", "http://localhost:8123")
HA_TOKEN = os.getenv("HA_TOKEN")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY")
ISSUE_LABEL = "jules"
VERSION_FILE = "custom_components/meraki_ha/manifest.json"


async def get_version() -> str:
    """Get the integration version from the manifest file."""
    with open(VERSION_FILE) as f:
        manifest = json.load(f)
    return manifest["version"]


async def get_unhealthy_entities(
    session: aiohttp.ClientSession,
) -> List[Dict[str, Any]]:
    """Fetch all entities from Home Assistant and filter for unhealthy ones."""
    headers = {
        "Authorization": f"Bearer {HA_TOKEN}",
        "Content-Type": "application/json",
    }
    url = f"{HA_URL}/api/states"
    unhealthy_entities = []

    try:
        async with session.get(url, headers=headers, timeout=30) as response:
            if response.status == 200:
                entities = await response.json()
                for entity in entities:
                    if (
                        entity["entity_id"].startswith(f"{DOMAIN}.")
                        and entity["state"] in ["unavailable", "unknown"]
                    ):
                        unhealthy_entities.append(entity)
            else:
                print(f"Error fetching entities: {response.status}")
    except (aiohttp.ClientConnectorError, asyncio.TimeoutError) as e:
        print(f"Home Assistant API request failed: {e}")

    return unhealthy_entities


def run_gh_command(command: List[str]) -> str:
    """Run a gh command and return the output."""
    try:
        result = subprocess.run(
            ["gh"] + command,
            capture_output=True,
            text=True,
            check=True,
            env={**os.environ, "GITHUB_TOKEN": GITHUB_TOKEN},
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"GitHub CLI command failed: {e}")
        return ""


def find_existing_issue(version: str) -> Optional[int]:
    """Check if a release audit issue already exists on GitHub."""
    issue_title = f"[Release Audit] {version}"
    output = run_gh_command(
        [
            "issue",
            "list",
            "--repo",
            GITHUB_REPOSITORY,
            "--search",
            f'"{issue_title}" in:title',
            "--state",
            "open",
            "--json",
            "number",
        ]
    )
    if output:
        issues = json.loads(output)
        if issues:
            return issues[0]["number"]
    return None


def create_github_issue(version: str, unhealthy_entities: List[Dict[str, Any]]):
    """Create a new GitHub issue with the audit results."""
    issue_title = f"[Release Audit] {version}"
    body = "The following entities were found to be in an unhealthy state:\n\n"
    for entity in unhealthy_entities:
        body += f"- [ ] `{entity['entity_id']}` (State: {entity['state']})\n"

    run_gh_command(
        [
            "issue",
            "create",
            "--repo",
            GITHUB_REPOSITORY,
            "--title",
            issue_title,
            "--body",
            body,
            "--label",
            ISSUE_LABEL,
        ]
    )
    print(f"Created new GitHub issue: {issue_title}")


def update_github_issue(issue_number: int, unhealthy_entities: List[Dict[str, Any]]):
    """Update an existing GitHub issue with the latest audit results."""
    existing_issue_body = run_gh_command(
        [
            "issue",
            "view",
            str(issue_number),
            "--repo",
            GITHUB_REPOSITORY,
            "--json",
            "body",
        ]
    )
    if not existing_issue_body:
        return

    existing_body = json.loads(existing_issue_body)["body"]
    existing_entities = set(re.findall(r"- \[[ x]\] `(.*?)`", existing_body))
    new_entities = {entity["entity_id"] for entity in unhealthy_entities}

    # Mark resolved entities as complete
    for entity_id in existing_entities - new_entities:
        existing_body = re.sub(
            f"(- \\[ \\] `{entity_id}`)",
            f"- [x] `{entity_id}`",
            existing_body,
        )

    # Add new unhealthy entities
    for entity in unhealthy_entities:
        if entity["entity_id"] not in existing_entities:
            existing_body += (
                f"\n- [ ] `{entity['entity_id']}` (State: {entity['state']})"
            )

    run_gh_command(
        [
            "issue",
            "edit",
            str(issue_number),
            "--repo",
            GITHUB_REPOSITORY,
            "--body",
            existing_body,
        ]
    )
    print(f"Updated GitHub issue #{issue_number}")


async def main():
    """Run the main execution function."""
    if not all([HA_TOKEN, GITHUB_TOKEN, GITHUB_REPOSITORY]):
        print(
            "Missing required environment variables: "
            "HA_TOKEN, GITHUB_TOKEN, GITHUB_REPOSITORY"
        )
        return

    version = await get_version()

    async with aiohttp.ClientSession() as session:
        unhealthy_entities = await get_unhealthy_entities(session)

    existing_issue = find_existing_issue(version)

    if not unhealthy_entities and not existing_issue:
        print("All entities are healthy. No action needed.")
        return

    if existing_issue:
        update_github_issue(existing_issue, unhealthy_entities)
    else:
        create_github_issue(version, unhealthy_entities)


if __name__ == "__main__":
    asyncio.run(main())
