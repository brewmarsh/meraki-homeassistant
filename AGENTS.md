# Agent Instructions and Project Standards (v2.6.0)

## 1. Project Overview

A high-performance Meraki Home Assistant integration utilizing a centralized coordinator and specialized fetch strategies.

## 2. Core Architecture

- **Coordinator:** `MerakiMainCoordinator` (central state management).
- **Fetch Logic:** Modular `FetchStrategies` (e.g., `ApplianceUplinkHelper`) for parallel, throttled API requests.
- **Discovery:** `DiscoveryService` with platform-specific handlers.

## 3. Mandatory Development Pattern (Optimistic UI)

To prevent "toggle flicker" caused by Meraki API latency, all interactive entities MUST:

1. Update `self._attr_is_on` / `self._attr_native_value` immediately.
2. Call `self.async_write_ha_state()`.
3. Invoke the API call.
4. Register a pending update: `self.coordinator.register_pending_update(self.unique_id)`.
5. Check `if self.coordinator.is_pending(self.unique_id): return` in the update handler.

## 4. Quality & "Agent Readiness" Standards

- **ACL (Agent Cognitive Load):** Max **10** per function.
- **Function Length:** Max **50** lines.
- **Nesting:** Max depth of **2**.
- **Type Safety:** All new code MUST have 100% type hint coverage.
- **File Length:** Keep files under **300** lines.

## 5. Tooling & Git

- **Env:** Always use `uv` for dependency management.
- **Target:** Branch from `beta`. Linear history only (use rebase).
- **Versioning:** Automated via PR title labels (`[major]`, `[minor]`, `[patch]`).

## 6. PR Requirements

Every PR MUST include:

1. **Technical Plan:** List of files and justification.
2. **Type:** (Bugfix/Feature/Chore).
3. **Verification:** Evidence of `uv run pytest` passing.
