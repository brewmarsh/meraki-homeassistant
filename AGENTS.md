# 🤖 AGENTS.md: AI Agent Guidelines

**This document is for AI agents (Jules, Claude Code, Cursor) working on the Meraki HA codebase.** ## 1. Core Mission & Project Context
Your goal is to assist in modernizing the Meraki Home Assistant integration for the **2026.1 Infrastructure Update**.
- **Domain:** Home Assistant Integration (`meraki_ha`).
- **Language:** Python 3.13+ using `homeassistant.core`.
- **Target:** High-scale Cisco Meraki environments.

## 2. 2026.1 Mandatory Conventions
You must strictly adhere to these architectural rules:
1. **Naming:** Always use `has_entity_name = True`. Do not prefix entity names with the device name.
2. **Case:** All UI strings must use **Sentence case** (e.g., "Client count", not "Client Count").
3. **Categorization:** Technical metadata (Serial numbers, IPs, Firmware) MUST be set to `EntityCategory.DIAGNOSTIC`.
4. **Translations:** `strings.json` is the source of truth. Ensure any new entity keys are added there first.

## 3. Tool Usage & Reliability
- **Verification:** Always use `read_file` to get exact content before attempting a `replace` or `write`.
- **Context:** Use the `replace` tool with sufficient surrounding context to avoid accidental duplicate edits.
- **Diagnostics:** If you use `run_shell_command`, only log or act upon errors within the `meraki_ha` namespace. Ignore unrelated system or HACS errors.

## 4. Onboarding & References
Before starting any task, you **must** review:
- **`ROADMAP.md`**: For the specific phase requirements.
- **`jules.yaml`**: For current branch and milestone logic.
- **`manifest.json`**: To verify versioning and requirements.

## 5. Code Contributions
- **Style:** Follow PEP8 and Home Assistant `async/await` patterns.
- **Commits:** Use **Conventional Commits** (e.g., `feat:`, `fix:`, `refactor:`).
- **PRs:** Use the provided PR template and fill out the checklist completely.

---
*Self-Correction: If a task conflicts with Home Assistant Core design guidelines, prioritize the Core guidelines and inform the human developer.*
