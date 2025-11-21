# Agent File Cleanup & Guidelines

## Purpose

This document explains where coding agents and automated tools should place temporary or diagnostic files, and the required cleanup steps to keep the repository tidy.

## Guidelines for Agents

- Do not leave temporary or diagnostic files in the repository root.
- If an agent needs to emit logs or error dumps, create them under `archive/agent-artifacts/` or under a uniquely named subdirectory inside `tmp/` and add a short README explaining why the artifact exists.
- Prefer returning results via the agent's communication channel (e.g., the chat session), not by writing files into the repository.
- If you create files, include a single-line header in the file with: agent name, date, and a short reason (e.g., `# agent: copilot | 2025-11-20 | lint-debug-output`).

## Recommended Artifact Directory Structure

- `archive/agent-artifacts/` — place long-term artifacts here when manual review is needed.
- `tmp/agent-<run-id>/` — use for short-lived outputs; these directories may be removed automatically by CI.

## Automated Cleanup Rules

- CI and pre-commit hooks should reject commits that add files matching these patterns in the repo root: `git-error-*`, `git-output-*`, `*~`, `*.tmp`, `message_to_user.txt`.
- If an agent writes to the repo, it should also create a cleanup script `tmp/agent-<run-id>/CLEANUP.md` explaining what to remove and how.

## Checklist for Humans Reviewing a PR from an Agent

1. Scan the PR for new top-level files not relevant to the feature (e.g., `message_to_user.txt`, `git-error-*.txt`).
2. If the file is needed for debugging, move it to `archive/agent-artifacts/` and add an entry to `archive/agent-artifacts/README.md` explaining the reason.
3. If the file contains nothing useful, delete it and request the agent team to re-run and publish outputs to the chat instead.

## Example: Common Items to Look For

- `message_to_user.txt` — ephemeral message leftovers; move to archive or delete.
- `git-error-*.txt` — test or git hook dumps; archive for triage, then delete.
- `Screenshot *.png` — only keep these if they are intentionally part of the feature or documentation.

## How to Move Artifacts (safe approach)

1. Create `archive/agent-artifacts/` and add `README.md` describing contents.
2. Move files into that directory instead of deleting them right away.
3. Keep artifacts for a short window (e.g., 30 days), then remove after confirmation.

## Contact

If you're unsure whether a file should be removed, mention `@maintainers` in the PR description or open an issue for discussion.
