#!/usr/bin/env python3
"""
Process agent scorecard report and automate remediation.

This script parses the scorecard output for CRAFT-formatted prompts.
- High Cognitive Load issues: Created as GitHub issues.
- Low Type Safety issues: Exported to typing_tasks.json for automated fixing.
"""

import json
import os
import re
import subprocess


def run_gh(args):
    """Run a GitHub CLI command and return output."""
    cmd = ["gh"] + args
    try:
        # Use shell=False for security
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running {' '.join(cmd)}: {e.stderr}")
        return None
    except FileNotFoundError:
        print("GitHub CLI (gh) not found. Skipping GitHub interaction.")
        return None

def parse_scorecard(filename):
    """
    Parse the scorecard output file for CRAFT prompts.

    The script uses regex to identify blocks starting with 'Type:' and extracts
    File, Rule, and the CRAFT Prompt content.
    """
    if not os.path.exists(filename):
        print(f"Scorecard file {filename} not found.")
        return []

    with open(filename, encoding="utf-8") as f:
        content = f.read()

    # We look for the specific section first if it exists
    section_marker = "Agent Prompts for Remediation (CRAFT Format)"
    if section_marker in content:
        content = content.split(section_marker, 1)[1]

    # Regex to split into task blocks from the scorecard.
    # - Type: Matches either "High Cognitive Load" or "Low Type Safety"
    # - File: Captures the target file path
    # - Rule: (Optional) Captures the specific lint/complexity rule
    # - Prompt: Captures everything after 'Prompt:' until the next 'Type:' or end of file
    # We use re.DOTALL to allow the prompt to span multiple lines.
    pattern = re.compile(
        r"Type:\s*(?P<type>High Cognitive Load|Low Type Safety)\s*\n"
        r"File:\s*(?P<file>[^\n]+)\s*\n"
        r"(?:Rule:\s*(?P<rule>[^\n]+)\s*\n)?"
        r"Prompt:\s*\n(?P<prompt>.*?)(?=\nType:|\Z)",
        re.DOTALL | re.MULTILINE,
    )

    tasks = []
    for match in pattern.finditer(content):
        task_data = match.groupdict()

        # Clean up data
        task_type = task_data["type"].strip()
        file_path = task_data["file"].strip()
        rule = (task_data["rule"] or "N/A").strip()
        prompt = task_data["prompt"].strip()

        # Requirement: Ignore all errors not related to the meraki_ha integration.
        # This ensures we only process files within the specific custom component.
        if "custom_components/meraki_ha/" not in file_path:
            print(f"Skipping task for {file_path} (not in meraki_ha integration)")
            continue

        tasks.append(
            {"type": task_type, "file": file_path, "rule": rule, "prompt": prompt}
        )

    return tasks

def main():
    """Process the scorecard and automate remediation."""
    scorecard_file = "scorecard.txt"
    tasks = parse_scorecard(scorecard_file)

    if not tasks:
        print("No remediation tasks found in scorecard.")
        return

    typing_tasks = []

    for task in tasks:
        if task["type"] == "High Cognitive Load":
            # Title following Home Assistant Sentence Case standards.
            # Only the first word and proper nouns (if any) are capitalized.
            title = f"Refactor: high cognitive load in {task['file']} ({task['rule']})"

            # Check if an issue already exists (searching both open and closed)
            query = f'"{title}" in:title'
            existing = run_gh(
                [
                    "issue",
                    "list",
                    "--search",
                    query,
                    "--json",
                    "number",
                    "--state",
                    "all",
                ]
            )

            if existing and json.loads(existing):
                print(f"Issue already exists for {task['file']}: {title}")
                continue

            # Create the issue with required labels
            print(f"Creating issue for {task['file']}...")
            run_gh(
                [
                    "issue",
                    "create",
                    "--title",
                    title,
                    "--body",
                    task["prompt"],
                    "--label",
                    "tech-debt,ai-ready",
                ]
            )

        elif task["type"] == "Low Type Safety":
            typing_tasks.append(task)

    # Write typing tasks to JSON for the subsequent CI step
    if typing_tasks:
        with open("typing_tasks.json", "w", encoding="utf-8") as f:
            json.dump(typing_tasks, f, indent=2)
        print(f"Saved {len(typing_tasks)} typing tasks to typing_tasks.json")
    else:
        # Clean up old task file if it exists
        if os.path.exists("typing_tasks.json"):
            os.remove("typing_tasks.json")

if __name__ == "__main__":
    main()
