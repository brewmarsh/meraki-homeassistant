# Contributing to Meraki Home Assistant

Thank you for contributing! To maintain high code quality and stability, please adhere to these guidelines.

## 1. Development Workflow

This project uses **[uv](https://github.com/astral-sh/uv)** for environment management.

1.  **Sync Environment:** `uv sync`
2.  **Create Branch:** Use `feat/`, `fix/`, or `chore/` prefixes.
3.  **Run Quality Gate:**
    ```bash
    uv run ruff check --fix .
    uv run ruff format .
    uv run mypy .
    uv run pytest
    ```

## 2. Core Architectural Patterns

### 2.1. Optimistic UI with Cooldown

**Problem:** Meraki API provisioning delays cause UI "flicker" (reverting to old state before cloud syncs).
**Solution:**

- Update `self._attr_is_on` immediately in `async_turn_on`.
- Call `self.coordinator.register_pending_update(self.unique_id)`.
- In `_update_internal_state`, check `if self.coordinator.is_pending(self.unique_id): return`.

### 2.2. API Client Conventions

- Use `snake_case` for all calls to the underlying `meraki` SDK.
- Ensure all I/O is awaited; never use `time.sleep()`.

### 2.3. Native Platform Helpers

- **Device Info:** Use `resolve_device_info` from `helpers/device_info_helpers.py`.
- **Constants:** Define all keys in `const.py`; no magic strings.
- **Error Handling:** Use `UpdateFailed` in coordinators for terminal API errors to show "Unavailable" in the UI.

## 3. Pull Request Standards

PR titles determine the version bump:

- `[major]` for breaking changes.
- `[minor]` for new features.
- `[patch]` for bug fixes.

**Checklist:**

- [ ] Type hints included for all new code (>90% coverage required).
- [ ] No nesting depth > 2.
- [ ] Function length < 50 lines.
- [ ] `uv run pytest` passes.

## 4. Agent Readiness (ACL)

To support AI-assisted development, we enforce an **Agent Cognitive Load (ACL)** score of **<= 10**.

- **Modularity:** Extract complex logic into private helpers.
- **Small Files:** Keep files under 300 lines where possible.
- **Explicit Types:** Use Python 3.10+ type union syntax (`str | None`).
