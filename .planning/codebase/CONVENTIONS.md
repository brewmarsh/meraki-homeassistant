# Coding Conventions

**Analysis Date:** 2024-05-14

## Naming Patterns

**Files:**

- Python: snake_case (e.g., `config_flow.py`, `ssid_details.py`).
- Frontend: snake_case for logic, but often depends on component name (e.g., `guest_access_card.ts`).
- Tests: prefixed with `test_` (e.g., `test_config_flow.py`).

**Functions:**

- snake_case (e.g., `async_setup_entry`, `_handle_coordinator_update`).
- Internal/private methods prefixed with underscore `_`.

**Variables:**

- snake_case (e.g., `new_ssid_data`, `network_id`).
- Constants: SCREAMING_SNAKE_CASE (e.g., `DOMAIN`, `CONF_API_KEY`).

**Types:**

- Classes: PascalCase (e.g., `MerakiMainCoordinator`, `MerakiSSIDDetailSensor`).
- Type Aliases: Often use standard Python types or defined in `types.py`.

## Code Style

**Formatting:**

- Python: `ruff` (configured in `pyproject.toml`) with a line length of 88.
- Frontend: `prettier` (configured in `.prettierrc`) and `eslint`.

**Linting:**

- Python: `ruff` using rules: `E` (pycodestyle), `W` (pycodestyle warnings), `F` (Pyflakes), `I` (isort), `D` (pydocstyle), `B` (flake8-bugbear), `C4` (flake8-comprehensions), `UP` (pyupgrade).
- Frontend: `eslint` (configured in `frontend/.eslintrc.json`).

## Import Organization

**Order:**

1. Future imports (`from __future__ import annotations`).
2. Standard library imports.
3. Third-party library imports (e.g., `homeassistant.*`, `voluptuous`).
4. Local integration imports (`custom_components.meraki_ha.*`).
5. Relative imports for internal modules (`...coordinators`, `...entity`).

**Path Aliases:**

- Not explicitly detected in Python (uses standard package structure).
- Frontend may use aliases if configured in `tsconfig.json`.

## Error Handling

**Patterns:**

- Custom exceptions defined in `custom_components/meraki_ha/core/errors.py`.
- Try-except blocks for API calls, often re-raising as integration-specific errors.
- Logging errors using `_LOGGER.error()` or `_LOGGER.exception()`.

## Logging

**Framework:** `logging` (standard Python).

**Patterns:**

- Logger defined at module level: `_LOGGER = logging.getLogger(__name__)`.
- Usage of `_LOGGER.debug`, `_LOGGER.info`, `_LOGGER.warning`, `_LOGGER.error`.
- Some specialized logging helpers in `custom_components/meraki_ha/async_logging.py`.

## Comments

**When to Comment:**

- Complexity: Explaining why a specific logic is used, especially for Meraki API quirks.
- Rules: Some files contain explicit "Rule X" comments to document design decisions (e.g., `custom_components/meraki_ha/sensor/network/ssid_details.py`).

**JSDoc/TSDoc:**

- Used in TypeScript files for documenting components and functions.
- Python uses docstrings.

## Function Design

**Size:**

- Generally modular. Large functions are broken down into helpers (e.g., `_extract_ssid_data`).

**Parameters:**

- Type hinted.
- Extensive use of keyword arguments or dictionaries for data passing in Home Assistant contexts.

**Return Values:**

- Explicitly type hinted (e.g., `-> None`, `-> dict[str, Any]`).

## Module Design

**Exports:**

- Explicitly defined in `__init__.py` files or via standard import mechanisms.

**Barrel Files:**

- `__init__.py` used to aggregate exports in directories like `const/`, `core/api/`, etc.

---

_Convention analysis: 2024-05-14_
