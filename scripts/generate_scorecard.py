#!/usr/bin/env python3
"""
Generate Agent Scorecard Report.

This script runs static analysis tools (ruff for complexity, mypy for typing)
and formats the findings into a CRAFT-formatted report suitable for the
process_scorecard.py script.
"""

import json
import os
import subprocess
import sys

TARGET_DIR = "custom_components/meraki_ha/"

def run_command(cmd):
    """Run a shell command and return its stdout."""
    try:
        # mypy returns non-zero exit code on errors, so check=False is important
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        return result.stdout
    except Exception as e:
        print(f"Error running command {' '.join(cmd)}: {e}")
        return ""

def generate_complexity_report():
    """Generate report for high complexity functions using ruff."""
    # ruff check . --select C901 --output-format json
    cmd = [sys.executable, "-m", "ruff", "check", TARGET_DIR, "--select", "C901", "--output-format", "json"]
    output = run_command(cmd)
    if not output:
        return []

    try:
        errors = json.loads(output)
    except json.JSONDecodeError:
        print(f"Failed to decode ruff output: {output}")
        return []

    tasks = []
    for error in errors:
        # Example: {"code": "C901", "filename": "...", "location": ..., "message": "function `foo` is too complex (15)"}
        filename = error.get("filename")
        message = error.get("message")
        code = error.get("code")

        # Make path relative if absolute
        if os.path.isabs(filename):
            filename = os.path.relpath(filename)

        prompt = f"The {message}. Please refactor it to reduce cyclomatic complexity below 10."

        tasks.append({
            "type": "High Cognitive Load",
            "file": filename,
            "rule": code,
            "prompt": prompt
        })
    return tasks

def generate_typing_report():
    """Generate report for typing issues using mypy."""
    # mypy . --output json
    # Note: mypy output format json returns line-delimited JSON objects
    cmd = [sys.executable, "-m", "mypy", TARGET_DIR, "--output", "json"]
    output = run_command(cmd)
    if not output:
        return []

    errors = []
    try:
        for line in output.splitlines():
            if line.strip():
                errors.append(json.loads(line))
    except json.JSONDecodeError:
        print(f"Failed to decode mypy output line: {line}")
        return []

    tasks = []
    files_with_issues = set()

    for error in errors:
        filename = error.get("file")
        severity = error.get("severity")

        # Only report errors, not notes
        if severity != "error":
            continue

        if filename and filename not in files_with_issues:
            # Check if file is inside target dir (mypy might check dependencies or other files)
            if TARGET_DIR not in filename and not filename.startswith(TARGET_DIR):
                continue

            files_with_issues.add(filename)

            # Make path relative if needed
            if os.path.isabs(filename):
                filename = os.path.relpath(filename)

            prompt = f"The file `{filename}` has type errors or missing type hints. Please fix them to improve type safety."

            tasks.append({
                "type": "Low Type Safety",
                "file": filename,
                "rule": "mypy",
                "prompt": prompt
            })
    return tasks

def main():
    tasks = []
    tasks.extend(generate_complexity_report())
    tasks.extend(generate_typing_report())

    print("Agent Prompts for Remediation (CRAFT Format)")
    print("-------------------------------------------")

    for task in tasks:
        print(f"Type: {task['type']}")
        print(f"File: {task['file']}")
        print(f"Rule: {task['rule']}")
        print("Prompt:")
        print(task['prompt'])
        print("") # Empty line after block

if __name__ == "__main__":
    main()
