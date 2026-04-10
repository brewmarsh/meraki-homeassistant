"""Automated Health Auditor for Meraki Integration."""

import asyncio
import json
import os
import re
import subprocess  # nosec
from typing import Any

import aiohttp

# Constants
DOMAIN = "meraki_ha"
HA_URL = os.getenv("HA_URL", "http://localhost:8123")
HA_TOKEN = os.getenv("HA_TOKEN", "")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY", "")
ISSUE_LABEL = "jules"
VERSION_FILE = "custom_components/meraki_ha/manifest.json"


async def get_version() -> str:
    """Get the integration version from the manifest file."""
    with open(VERSION_FILE) as f:
        manifest = json.load(f)
    return manifest["version"]


async def fetch_ha_states(session: aiohttp.ClientSession) -> list[dict[str, Any]]:
    """Fetch all state entities from Home Assistant."""
    headers = {
        "Authorization": f"Bearer {HA_TOKEN}",
        "Content-Type": "application/json",
    }
    url = f"{HA_URL}/api/states"

    try:
        async with session.get(
            url, headers=headers, timeout=aiohttp.ClientTimeout(total=30)
        ) as response:
            if response.status == 200:
                return await response.json()
            print(f"Error fetching entities: {response.status}")
    except (aiohttp.ClientConnectorError, asyncio.TimeoutError) as e:
        print(f"Home Assistant API request failed: {e}")
    return []


def is_unhealthy_meraki_entity(entity: dict[str, Any]) -> bool:
    """Check if an entity belongs to Meraki and is unhealthy."""
    is_meraki = entity.get("entity_id", "").startswith(f"{DOMAIN}.")
    is_unhealthy = entity.get("state") in ["unavailable", "unknown"]
    return is_meraki and is_unhealthy


async def get_unhealthy_entities(
    session: aiohttp.ClientSession,
) -> list[dict[str, Any]]:
    """Fetch all entities from Home Assistant and filter for unhealthy ones."""
    entities = await fetch_ha_states(session)
    return [entity for entity in entities if is_unhealthy_meraki_entity(entity)]


def run_gh_command(command: list[str]) -> str:
    """Run a gh command and return the output."""
    if GITHUB_TOKEN is None:
        print("GITHUB_TOKEN is not set")
        return ""

    try:
        result = subprocess.run(  # nosec
            ["gh"] + command,
            capture_output=True,
            text=True,
            check=True,
            env={**os.environ, "GITHUB_TOKEN": GITHUB_TOKEN},
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"GitHub CLI command failed: {e}")
        raise


def find_existing_issue(version: str) -> int | None:
    """Check if a release audit issue already exists on GitHub."""
    if GITHUB_REPOSITORY is None:
        print("GITHUB_REPOSITORY is not set")
        return None

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


def create_github_issue(version: str, unhealthy_entities: list[dict[str, Any]]) -> None:
    """Create a new GitHub issue with the audit results."""
    if GITHUB_REPOSITORY is None:
        print("GITHUB_REPOSITORY is not set")
        return

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


def get_existing_issue_body(issue_number: int) -> str | None:
    """Retrieve the body of an existing GitHub issue."""
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
        return None
    return json.loads(existing_issue_body)["body"]


def get_existing_entities(body: str) -> set[str]:
    """Extract existing entities from the issue body."""
    return set(re.findall(r"- \[[ x]\] `(.*?)`", body))


def mark_resolved_entities(
    body: str, existing_entities: set[str], new_entities: set[str]
) -> str:
    """Mark resolved entities as complete in the issue body."""
    resolved_entities = existing_entities - new_entities
    for entity_id in resolved_entities:
        body = re.sub(
            f"(- \\[ \\] `{entity_id}`)",
            f"- [x] `{entity_id}`",
            body,
        )
    return body


def append_new_entities(
    body: str, unhealthy_entities: list[dict[str, Any]], existing_entities: set[str]
) -> str:
    """Append newly unhealthy entities to the issue body."""
    for entity in unhealthy_entities:
        if entity["entity_id"] not in existing_entities:
            body += f"\n- [ ] `{entity['entity_id']}` (State: {entity['state']})"
    return body


def update_github_issue(
    issue_number: int, unhealthy_entities: list[dict[str, Any]]
) -> None:
    """Update an existing GitHub issue with the latest audit results."""
    if GITHUB_REPOSITORY is None:
        print("GITHUB_REPOSITORY is not set")
        return

    existing_body = get_existing_issue_body(issue_number)
    if not existing_body:
        return

    existing_entities = get_existing_entities(existing_body)
    new_entities = {entity["entity_id"] for entity in unhealthy_entities}

    updated_body = mark_resolved_entities(
        existing_body, existing_entities, new_entities
    )
    updated_body = append_new_entities(
        updated_body, unhealthy_entities, existing_entities
    )

    run_gh_command(
        [
            "issue",
            "edit",
            str(issue_number),
            "--repo",
            GITHUB_REPOSITORY,
            "--body",
            updated_body,
        ]
    )
    print(f"Updated GitHub issue #{issue_number}")


async def main() -> None:
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

    try:
        if existing_issue:
            update_github_issue(existing_issue, unhealthy_entities)
        else:
            create_github_issue(version, unhealthy_entities)
    except Exception as e:
        print(f"An error occurred: {e}")
        # Exit with a non-zero status code to indicate failure
        exit(1)


if __name__ == "__main__":
    asyncio.run(main())
