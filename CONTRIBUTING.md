# Contributing to Meraki Home Assistant

Thank you for your interest in contributing to this integration!

This document provides project-specific rules, architectural patterns, and guidelines that are essential for successful development. **Please read this file _after_ reading the main `AGENTS.md` file** in this repository.

## 1. Core Architectural Principles

These are the most important patterns to understand before writing any code. Failure to follow them will re-introduce known, high-impact bugs.

### Pattern 1: The "Optimistic UI with Cooldown" (for Configuration Entities)

This is the **most critical pattern** in this codebase for all entities that modify configuration (e.g., `switch`, `select`, `text`).

- **Problem:** The Meraki Cloud API has a significant **provisioning delay**. When you send a `PUT` request (e.g., to disable an SSID), the API returns a `200 OK` immediately. However, the change can take several minutes to actually apply. During this time, any `GET` request will return the _old, stale data_.
- **Bug:** This delay causes the Home Assistant UI to "flicker." The user toggles a switch, the UI updates, the integration refreshes, the API returns the _old_ state, and the UI toggle reverts to its original, incorrect position.
- **Solution:** We **must** use an optimistic state with a timed cooldown.

The required logic is as follows:

<<<<<<< HEAD
1. **Optimistic State Update:** The entity's action method (e.g., `async_turn_on`) **must** immediately update its own state and tell Home Assistant to write this state to the UI.

   ```python
   # Example from a switch
   self._attr_is_on = True
   self.async_write_ha_state()
   ```

2. **Fire-and-Forget API Call:** The method should then make the API call to Meraki without waiting for a response to be confirmed by a refresh.

3. **Register a Cooldown:** After making the API call, the entity **must** register a "pending update" with the central `MerakiDataCoordinator`. This acts as a cooldown period (default 150 seconds).

   ```python
   # Example
   self.coordinator.register_pending_update(self.unique_id)
   ```

4. **Ignore Coordinator Updates:** The entity's state update method (`_update_internal_state`) **must** check if it is in a cooldown period before processing new data. If it is, it must `return` and do nothing.

   ```python
   # Example
   def _update_internal_state(self) -> None:
       if self.coordinator.is_pending(self.unique_id):
           return  # Ignore update, optimistic state is in control

       # ... rest of the update logic ...
   ```
=======
1.  **Optimistic State Update:** The entity's action method (e.g., `async_turn_on`) **must** immediately update its own state and tell Home Assistant to write this state to the UI.

    ```python
    # Example from a switch
    self._attr_is_on = True
    self.async_write_ha_state()
    ```

2.  **Fire-and-Forget API Call:** The method should then make the API call to Meraki without waiting for a response to be confirmed by a refresh.

3.  **Register a Cooldown:** After making the API call, the entity **must** register a "pending update" with the central `MerakiDataCoordinator`. This acts as a cooldown period (default 150 seconds).

    ```python
    # Example
    self.coordinator.register_pending_update(self.unique_id)
    ```

4.  **Ignore Coordinator Updates:** The entity's state update method (`_update_internal_state`) **must** check if it is in a cooldown period before processing new data. If it is, it must `return` and do nothing.

    ```python
    # Example
    def _update_internal_state(self) -> None:
        if self.coordinator.is_pending(self.unique_id):
            return  # Ignore update, optimistic state is in control

        # ... rest of the update logic ...
    ```
>>>>>>> 9bc35b7 (Merge pull request #845 from brewmarsh/fix/frontend-build-2299669574949783162)

**Do not attempt to "fix" this by forcing an immediate refresh after an action.** This will not work and will re-introduce the original bug.

### Pattern 2: API Client Conventions (`meraki` Library)

- **Historical Context:** The underlying `meraki` Python library had a breaking change, moving all its methods from `camelCase` (e.g., `getOrganizationNetworks`) to Python's standard `snake_case` (e.g., `get_organization_networks`).
- **Rule:** All calls to the `meraki` library object (e.g., `self._dashboard.*`) **must** use `snake_case` methods.
- **Internal Convention:** To maintain consistency, this project's _own_ client wrapper methods (in `custom_components/meraki_ha/core/api/endpoints/`) also use `snake_case`. Please follow this pattern.

---

## 2. Home Assistant Integration Best Practices

Follow these rules to ensure consistency with Home Assistant's design patterns and this integration's helpers.

- **Device & Entity Helpers:**
  - **Device Info:** **Do not** create `DeviceInfo` objects manually. Always use the `resolve_device_info` helper in `custom_components/meraki_ha/helpers/device_info_helpers.py`.
  - **Device Name:** Use the `format_device_name` utility for the `name` field within `DeviceInfo`.
  - **Entity Name:** Use the `format_entity_name` helper for the entity's own name (`_attr_name`).

- **Handling Disabled Features:**
  - When an API call fails because a feature (like Traffic Analysis or VLANs) is disabled in the Meraki Dashboard, the corresponding entity should not become `unknown`.
  - Instead, its state **must** be set to `Disabled`, and an attribute should be added to explain the reason.

- **Testing New Entities:**
  - A useful pattern for testing new, dynamically created sensors is to call `async_setup_sensors` (or the equivalent setup helper) with mock coordinator data.
  - You can then inspect the list of entities returned by the helper to validate their properties. This is often more effective than testing the sensor class in isolation.

- **Constants:**
  - All constants (domain names, default values, keys) **must** be defined in `custom_components/meraki_ha/const.py`. Do not use magic strings in entity or coordinator code.

- **Configuration Validation:**
  - All configuration data (from `configuration.yaml` or UI config flows) **must** be validated using `voluptuous` schemas.

- **API Documentation:**
  - When working with a Meraki endpoint, double-check your implementation against the [Meraki API documentation](https://developer.cisco.com/meraki/api-v1/).
  - When interacting with Home Assistant, double-check against the [Home Assistant API documentation](https://developers.home-assistant.io/docs/api/rest/).

---

## 3. Working with the Web UI (React)

The self-hosted web interface is a React application located in `custom_components/meraki_ha/web_ui/`.

- **Source vs. Build:**
  - The human-readable source code is in the `src/` directory.
  - The code actually served to the browser is the compiled/optimized output in the `dist/` directory.

- **Agent Build Simulation:**
  - As an agent, you **cannot** run the `npm run build` command.
  - If you make changes to any files in the `src/` directory, you **must** manually update the corresponding file in `dist/` to reflect your changes.
  - The most important file to keep updated for E2E tests is `dist/assets/index.js`. You may need to write a simplified, non-JSX version of the React logic in this file to ensure tests pass.

- **React Standards:**
  - All new components **must** be **Functional Components** using Hooks.
  - Use `const` over `let` where variable reassignment is not needed.
  - All new functions should have `JSDoc`-formatted documentation.

---

## 4. Development & Testing

### Local Setup

This project uses [Poetry](https://python-poetry.org/) for dependency management.

<<<<<<< HEAD
1. Install dependencies:
   ```bash
   poetry install
   ```
2. Activate the virtual environment:
   ```bash
   poetry shell
   ```
=======
1.  Install dependencies:
    ```bash
    poetry install
    ```
2.  Activate the virtual environment:
    ```bash
    poetry shell
    ```
>>>>>>> 9bc35b7 (Merge pull request #845 from brewmarsh/fix/frontend-build-2299669574949783162)

### Running Quality Checks

Before submitting, you **must** run all quality checks. These are also enforced by pre-commit hooks.

<<<<<<< HEAD
1. **Linting & Formatting (Ruff):**

   ```bash
   poetry run ruff check --fix .
   poetry run ruff format .
   ```

2. **Type Checking (mypy):**

   ```bash
   poetry run mypy .
   ```

3. **Security Analysis (bandit):**

   ```bash
   poetry run bandit -r custom_components/meraki_ha/
   ```

4. **Run Tests (pytest):**

   ```bash
   poetry run pytest
   ```

5. **Home Assistant Validation (hassfest):**
   This ensures the integration's manifest and structure are valid.
   ```bash
   poetry run python -m script.hassfest
   ```
=======
1.  **Linting & Formatting (Ruff):**

    ```bash
    poetry run ruff check --fix .
    poetry run ruff format .
    ```

2.  **Type Checking (mypy):**

    ```bash
    poetry run mypy .
    ```

3.  **Security Analysis (bandit):**

    ```bash
    poetry run bandit -r custom_components/meraki_ha/
    ```

4.  **Run Tests (pytest):**

    ```bash
    poetry run pytest
    ```

5.  **Home Assistant Validation (hassfest):**
    This ensures the integration's manifest and structure are valid.
    ```bash
    poetry run python -m script.hassfest
    ```
>>>>>>> 9bc35b7 (Merge pull request #845 from brewmarsh/fix/frontend-build-2299669574949783162)

### Debugging

- Remove all debugging code (e.g., `_LOGGER.debug` statements, `print()` calls) before submitting your change.
- When writing mocks for tests, ensure they are as accurate as possible to the real API responses they are replacing.

---

## 5. Versioning and Releases

This project uses an automated versioning and release process triggered by merging Pull Requests (PRs) into the `main` branch.

- **Automatic Version Increment:** When a PR is merged, the version number in `custom_components/meraki_ha/manifest.json` and `package.json` is automatically incremented.
- **Determining Increment Type:** The type of version increment is determined by the PR title:
- `[major]` in the PR title will trigger a major version update (e.g., `1.2.3` -> `2.0.0`).
- `[minor]` in the PR title will trigger a minor version update (e.g., `1.2.3` -> `1.3.0`).
- `[patch]` in the PR title or if no prefix is found, will trigger a patch version update (e.g., `1.2.3` -> `1.2.4`).
- **Changelog Generation:** A `CHANGELOG.md` file is automatically updated with commit messages from the PR.
- **GitHub Release:** A new GitHub Release is automatically created, tagged with the new version number.

## 6. Dependencies 📦

- `meraki`: The official Meraki SDK for Python, used for all API interactions.
- `aiohttp`: Used by the Meraki SDK for asynchronous HTTP requests.

---

## 7. Pull Request Guidelines

All pull requests should include the following sections.

### Type of Change

- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)

_Remember to include `[major]`, `[minor]`, or `[patch]` in your PR title based on the type of change. Example: `[minor] Add support for new sensor type`_

### Description

A clear and concise description of the change.

### Motivation and Context

- Why is this change required? What problem does it solve?
- If it fixes an open issue, please link to the issue here.

### How Has This Been Tested?

Please describe the tests that you ran to verify your changes. Provide instructions so we can reproduce. Please also list any relevant details for your test configuration.

- [ ] Test A
- [ ] Test B

### Screenshots (if appropriate)

### Types of changes

- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)

### Checklist

- [ ] My code follows the style guidelines of this project
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
- [ ] Any dependent changes have been merged and published in downstream modules
