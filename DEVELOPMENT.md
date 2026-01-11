# Meraki Home Assistant Development Guide

This document provides a comprehensive guide for developers who want to contribute to the Meraki Home Assistant integration.

---

## Table of Contents

1. [Getting Started](#1-getting-started)
2. [Running Quality Checks](#2-running-quality-checks)
3. [Frontend Development](#3-frontend-development)
4. [Docker Test Environment](#4-docker-test-environment)
5. [Core Architectural Principles](#5-core-architectural-principles)
6. [Home Assistant Integration Patterns](#6-home-assistant-integration-patterns)
7. [Git Branching Strategy](#7-git-branching-strategy)
8. [Testing Requirements](#8-testing-requirements)
9. [Versioning and Releases](#9-versioning-and-releases)
10. [Commit Message Format](#10-commit-message-format)
11. [Debugging & Logging](#11-debugging--logging)
12. [Project Structure](#12-project-structure)

---

## 1. Getting Started

### 1.1. Prerequisites

- **Python 3.13.2+** (required)
- **Node.js 18+** (for frontend development)
- **Docker** (optional, for isolated testing)
- **Git** (obviously)

### 1.2. Package Manager: uv

This project uses **`uv`** as the Python package manager and **`pyproject.toml`** for all dependency management. **Never use `requirements.txt` files.**

1. **Install uv** (if not already installed):

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Install dependencies:**

   ```bash
   uv sync --all-extras
   ```

   This reads `pyproject.toml` and installs all dev dependencies from `[project.optional-dependencies].dev`. The `uv.lock` file ensures reproducible builds.

3. **Adding new dependencies:**

   ```bash
   # Add a new package
   uv add <package-name>

   # Or edit pyproject.toml directly under [project.optional-dependencies].dev
   uv sync --all-extras
   ```

### 1.3. Quick Start

    ```bash

# Clone the repository

git clone https://github.com/liptonj/meraki-homeassistant.git
cd meraki-homeassistant

# Switch to beta branch (development happens here)

git checkout beta
git pull origin beta

# Install dependencies

uv sync --all-extras

# Run quality checks to verify setup

./run_checks.sh

````

---

## 2. Running Quality Checks

Before submitting changes, you **must** run all quality checks.

**All tool configurations are centralized in `pyproject.toml`** - never create separate config files (no `.bandit.yaml`, `.ruff.toml`, `mypy.ini`, `pytest.ini`, etc.).

### 2.1. Recommended: Use the Helper Script

The easiest way to run all checks is with the helper script:

```bash
./run_checks.sh
````

This script will:

- Auto-install `uv` if not present
- Sync all dependencies
- Run ruff, bandit, mypy, and pytest

### 2.2. Running Checks Individually

If you need to run checks individually, use `uv run` to ensure tools run in the virtual environment:

1. **Linting & Formatting (Ruff):**

   ```bash
   # Check and auto-fix issues
   uv run ruff check --fix .

   # Format code
   uv run ruff format .
   ```

2. **Type Checking (mypy):**

   ```bash
   uv run mypy custom_components/meraki_ha/ tests/
   ```

3. **Security Analysis (bandit):**

   ```bash
   uv run bandit -c pyproject.toml -r custom_components/meraki_ha/
   ```

4. **Run Tests (pytest):**

   ```bash
   # Run all tests
   uv run pytest

   # Run with coverage report
   uv run pytest --cov=custom_components/meraki_ha --cov-report=term-missing

   # Run specific test file
   uv run pytest tests/sensor/test_temperature_sensor.py -v
   ```

5. **Home Assistant Validation (hassfest):**

   ```bash
   docker run --rm -v "$(pwd)":/github/workspace ghcr.io/home-assistant/hassfest
   ```

### 2.3. Pre-Commit Checklist

Before committing:

- [ ] `uv run ruff check --fix .` passes
- [ ] `uv run ruff format .` shows no changes needed
- [ ] `uv run mypy custom_components/meraki_ha/ tests/` passes
- [ ] `uv run pytest` passes (all tests green)
- [ ] Frontend rebuilt if modified (`npm run build`)

---

## 3. Frontend Development

The Meraki side panel is a modern web application built with React, Vite, and TypeScript.

### 3.1. Frontend Code Location

```
custom_components/meraki_ha/www/
├── src/                    # Source code
│   ├── components/         # React components
│   ├── hooks/              # Custom React hooks
│   ├── types/              # TypeScript type definitions
│   ├── App.tsx             # Main application component
│   └── main.tsx            # Entry point
├── package.json            # Dependencies and scripts
├── vite.config.ts          # Vite configuration
├── meraki-panel.js         # Built output (committed)
└── style.css               # Built CSS (committed)
```

### 3.2. Installing Dependencies

```bash
cd custom_components/meraki_ha/www/
npm install
```

### 3.3. Building the Frontend

After making changes, rebuild the panel:

```bash
npm run build
```

This compiles the application and places `meraki-panel.js` and `style.css` in the `www/` directory.

**Important:** Always commit the built files alongside source changes.

### 3.4. Development Server

For interactive development with hot-reloading:

```bash
npm run dev
```

This starts a local server on port 5173. Note that in this mode, the panel won't have access to the Home Assistant `hass` object and may not function completely.

### 3.5. Frontend Architecture

The panel uses Home Assistant's custom panel architecture:

- **Web Component Wrapper:** Receives `hass` and `panel` props from HA
- **React Application:** Mounted inside the Web Component
- **API Communication:** Uses `hass.callWS()` for authenticated WebSocket calls

```typescript
// Example: Making a WebSocket call
const data = await hass.callWS({
  type: 'meraki_ha/get_data',
  config_entry_id: configEntryId,
});
```

---

## 4. Docker Test Environment

For isolated testing with a real Home Assistant instance:

### 4.1. Starting the Environment

```bash
docker compose up
```

### 4.2. Accessing Home Assistant

- URL: `http://localhost:8123`
- Follow the on-screen prompts to create a user
- Add the Meraki integration via **Settings** > **Devices & Services**

### 4.3. Rebuilding After Changes

```bash
# Stop the container
docker compose down

# Rebuild and start
docker compose up --build
```

---

## 5. Core Architectural Principles

### 5.1. The "Optimistic UI with Cooldown" Pattern

This is the **most critical pattern** for entities that modify configuration (`switch`, `select`, `text`, `number`).

**Problem:** The Meraki Cloud API has a significant provisioning delay (up to 2-3 minutes after an API call before the change is reflected in subsequent API reads).

**Solution:** Optimistic state with a timed cooldown:

1. The entity's action method immediately updates its own state and writes it to the UI
2. It makes a "fire-and-forget" API call to Meraki
3. After the API call, it registers a "pending update" with the `MerakiDataCoordinator` (default 150 seconds)
4. The entity's state update method ignores coordinator updates while in the cooldown period

**Implementation Example:**

```python
async def async_turn_on(self, **kwargs: Any) -> None:
    """Turn the entity on."""
    # 1. Optimistically update state immediately
    self._attr_is_on = True
    self.async_write_ha_state()

    # 2. Fire-and-forget API call
    await self.coordinator.client.update_ssid(
        network_id=self._network_id,
        number=self._ssid_number,
        enabled=True
    )

    # 3. Register pending update to ignore stale coordinator data
    self.coordinator.register_pending_update(
        self.entity_id,
        cooldown_seconds=150
    )
```

### 5.2. API Client Conventions

- All calls to the `meraki` library object **must** use `snake_case` methods
- This project's client wrapper methods also use `snake_case` for consistency
- Always access the client through the coordinator: `self.coordinator.client`

### 5.3. Centralized Logging

This integration uses a centralized logging system. **Never use `logging.getLogger(__name__)`**.

See [Section 11: Debugging & Logging](#11-debugging--logging) for details.

---

## 6. Home Assistant Integration Patterns

### 6.1. Device & Entity Helpers

```python
from custom_components.meraki_ha.helpers.device_helper import (
    resolve_device_info,
    format_device_name,
)
from custom_components.meraki_ha.helpers.entity_helper import format_entity_name

# For DeviceInfo
device_info = resolve_device_info(coordinator, device_data)

# For device names
name = format_device_name(network_name, device_name)

# For entity names
entity_name = format_entity_name(device_name, sensor_type)
```

### 6.2. Handling Disabled Features

When a feature is disabled in the Meraki Dashboard, set the entity to unavailable rather than unknown:

```python
# Correct - marks entity as unavailable
self._attr_available = False

# Wrong - shows "unknown" state which is misleading
self._attr_native_value = None
```

### 6.3. Constants

All constants must be defined in `custom_components/meraki_ha/const.py`:

```python
from custom_components.meraki_ha.const import (
    DOMAIN,
    CONF_API_KEY,
    CONF_SCAN_INTERVAL,
    # ...
)
```

### 6.4. Configuration Validation

All configuration data must be validated using `voluptuous` schemas:

```python
from custom_components.meraki_ha.schemas import SCHEMA_OPTIONS_STEP
```

---

## 7. Git Branching Strategy

### 7.1. Branch Structure

- **`main`:** Production releases only. Protected branch.
- **`beta`:** Active development. All feature branches merge here first.
- **Feature branches:** Created from `beta`, named descriptively.

### 7.2. Creating a Feature Branch

**Always create new branches FROM the `beta` branch, never from `main`.**

```bash
git checkout beta
git pull origin beta
git checkout -b feat/my-new-feature
```

### 7.3. Branch Naming Conventions

| Prefix      | Use Case                |
| ----------- | ----------------------- |
| `feat/`     | New features            |
| `fix/`      | Bug fixes               |
| `bugfix/`   | Bug fixes (alternative) |
| `refactor/` | Code refactoring        |
| `docs/`     | Documentation updates   |
| `test/`     | Test additions/fixes    |

### 7.4. Completing Work

```bash
# Ensure all checks pass
./run_checks.sh

# Merge back into beta
git checkout beta
git merge feat/my-new-feature
git push origin beta
```

---

## 8. Testing Requirements

### 8.1. Critical Rule

**Never break existing functionality.** Always run the full test suite before completing work.

```bash
uv run pytest
```

If any previously passing test fails after your changes, **fix it before marking the task complete**.

### 8.2. Test Coverage Requirements

- All code changes **require corresponding unit tests**
- New features need tests proving they work
- Bug fixes need tests proving the bug is fixed
- Target: 95%+ test coverage

### 8.3. Test Structure

Place tests in `tests/` mirroring the source structure:

```
custom_components/meraki_ha/sensor/temperature.py
→ tests/sensor/test_temperature.py
```

### 8.4. Testing Best Practices

```python
"""Tests for the temperature sensor."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from custom_components.meraki_ha.sensor.temperature import TemperatureSensor


@pytest.fixture
def mock_coordinator():
    """Create a mock coordinator."""
    coordinator = AsyncMock()
    coordinator.client = AsyncMock()
    coordinator.data = {"devices": [...]}
    return coordinator


@pytest.fixture
def mock_hass():
    """Create a mock Home Assistant instance."""
    hass = MagicMock()
    hass.data = {}
    return hass


async def test_temperature_sensor_value(mock_coordinator, mock_hass):
    """Test that temperature sensor returns correct value."""
    sensor = TemperatureSensor(coordinator=mock_coordinator, ...)

    assert sensor.native_value == 72.5
    assert sensor.native_unit_of_measurement == "°F"
```

### 8.5. Mocking External APIs

**Never make real Meraki API calls in tests.** Always mock:

```python
@patch("custom_components.meraki_ha.core.meraki_api_client.MerakiAPIClient")
async def test_api_call(mock_client):
    mock_client.return_value.get_devices = AsyncMock(return_value=[...])
    # Test code here
```

---

## 9. Versioning and Releases

### 9.1. Automated Versioning

This project uses automated versioning based on PR titles:

| PR Title Prefix   | Version Bump         | Example           |
| ----------------- | -------------------- | ----------------- |
| `[major]`         | Major (breaking)     | `1.2.3` → `2.0.0` |
| `[minor]`         | Minor (new features) | `1.2.3` → `1.3.0` |
| `[patch]` or none | Patch (bug fixes)    | `1.2.3` → `1.2.4` |

### 9.2. Release Process

1. Changes merge to `beta` branch
2. CI runs and creates beta releases (e.g., `3.1.0-beta.3`)
3. When ready for production, PR from `beta` to `main`
4. Merge creates a production release (e.g., `3.1.0`)

### 9.3. Version Files

Version is tracked in:

- `custom_components/meraki_ha/manifest.json` (source of truth)
- `CHANGELOG.md` (auto-updated)

---

## 10. Commit Message Format

Use **Conventional Commits** format:

```
type(scope): description

[optional body]

[optional footer]
```

### 10.1. Types

| Type       | Use Case                     |
| ---------- | ---------------------------- |
| `feat`     | New feature                  |
| `fix`      | Bug fix                      |
| `docs`     | Documentation only           |
| `refactor` | Code change (no feature/fix) |
| `test`     | Adding/fixing tests          |
| `build`    | Build system/dependencies    |
| `ci`       | CI configuration             |
| `style`    | Formatting (no logic change) |
| `perf`     | Performance improvement      |
| `chore`    | Maintenance tasks            |

### 10.2. Examples

```bash
feat(camera): add configurable snapshot refresh interval
fix(api): filter networks before making API calls
docs(readme): update installation instructions
refactor(sensor): consolidate MT sensor base class
test(switch): add SSID toggle tests
build(deps): update homeassistant to 2025.11
ci(workflow): add beta branch workflow
```

---

## 11. Debugging & Logging

### 11.1. Centralized Logging System

This integration uses a centralized logging system with feature-specific loggers that can be individually controlled.

**Always use `MerakiLoggers` from `helpers/logging_helper.py`:**

```python
from custom_components.meraki_ha.helpers.logging_helper import MerakiLoggers

_LOGGER = MerakiLoggers.SENSOR  # Choose appropriate logger
```

### 11.2. Available Loggers

| Logger           | Use For                              |
| ---------------- | ------------------------------------ |
| `MAIN`           | Core integration, config flows, hubs |
| `API`            | API client code, endpoints           |
| `COORDINATOR`    | Data coordinators                    |
| `MQTT`           | MQTT service for MT sensors          |
| `ALERTS`         | Webhook alerts                       |
| `SCANNING_API`   | Scanning API (CMX)                   |
| `DISCOVERY`      | Device/entity discovery              |
| `CAMERA`         | Camera operations                    |
| `SENSOR`         | Sensor entities                      |
| `SWITCH`         | Switch/toggle entities               |
| `FRONTEND`       | Frontend panel                       |
| `DEVICE_TRACKER` | Client tracking                      |

### 11.3. Basic Debug Logging

Enable debug logging for the entire integration in `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.meraki_ha: debug
```

### 11.4. Feature-Specific Logging

Control individual features to reduce noise:

```yaml
logger:
  default: info
  logs:
    custom_components.meraki_ha: info
    custom_components.meraki_ha.mqtt: warning # Silence MQTT spam
    custom_components.meraki_ha.api: debug # Debug API calls
    custom_components.meraki_ha.scanning_api: debug # Debug Scanning API
```

### 11.5. Performance Timing Decorator

For async methods that may be slow, use the `async_log_time` decorator:

```python
from custom_components.meraki_ha.async_logging import async_log_time
from custom_components.meraki_ha.helpers.logging_helper import MerakiLoggers

class MyApiClient:
    @async_log_time(MerakiLoggers.API, slow_threshold=2.0)
    async def get_devices(self) -> list[dict]:
        """Fetch devices - logs timing, warns if > 2 seconds."""
        return await self._api.get_devices()
```

---

## 12. Project Structure

### 12.1. Key Directories

| Directory                             | Purpose                     |
| ------------------------------------- | --------------------------- |
| `custom_components/meraki_ha/`        | Main integration code       |
| `custom_components/meraki_ha/core/`   | Business logic & API client |
| `custom_components/meraki_ha/sensor/` | Sensor platform entities    |
| `custom_components/meraki_ha/switch/` | Switch platform entities    |
| `custom_components/meraki_ha/www/`    | React frontend              |
| `tests/`                              | Test suite                  |
| `docs/`                               | Architecture documentation  |

### 12.2. Key Files

| File                         | Purpose                    |
| ---------------------------- | -------------------------- |
| `__init__.py`                | Integration entry point    |
| `config_flow.py`             | Setup wizard               |
| `options_flow.py`            | Options configuration      |
| `const.py`                   | All constants              |
| `schemas.py`                 | Voluptuous schemas         |
| `meraki_data_coordinator.py` | Data update coordinator    |
| `manifest.json`              | Integration metadata       |
| `pyproject.toml`             | Dependencies & tool config |

### 12.3. Platform Modules

Each entity platform follows a consistent structure:

```
sensor/
├── __init__.py              # Platform setup (async_setup_entry)
├── base.py                  # Base class for sensors
├── device_sensors.py        # Device-specific sensors
├── network_sensors.py       # Network-level sensors
└── mt_sensors/              # MT environmental sensors
    ├── temperature.py
    ├── humidity.py
    └── ...
```

---

## Need Help?

- **Issues:** [GitHub Issues](https://github.com/liptonj/meraki-homeassistant/issues)
- **Discussions:** [GitHub Discussions](https://github.com/liptonj/meraki-homeassistant/discussions)
- **Contributing:** See [CONTRIBUTING.md](CONTRIBUTING.md)
- **AI Agents:** See [AGENTS.md](AGENTS.md)

---

_This document was last updated for version 3.1.0._
