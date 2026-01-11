# `AGENTS.md`: AI Agent Guidelines

**This document is for AI agents working on this codebase.** Human developers should refer to `DEVELOPMENT.md` for setup and contribution guidelines.

---

## Quick Reference

| What                    | Where                                                    |
| ----------------------- | -------------------------------------------------------- |
| Integration entry point | `custom_components/meraki_ha/__init__.py`                |
| API client              | `custom_components/meraki_ha/core/meraki_api_client.py`  |
| Data coordinator        | `custom_components/meraki_ha/meraki_data_coordinator.py` |
| Constants               | `custom_components/meraki_ha/const.py`                   |
| Config flow             | `custom_components/meraki_ha/config_flow.py`             |
| Options flow            | `custom_components/meraki_ha/options_flow.py`            |
| Logging helper          | `custom_components/meraki_ha/helpers/logging_helper.py`  |
| Frontend source         | `custom_components/meraki_ha/www/src/`                   |
| Frontend build output   | `custom_components/meraki_ha/www/meraki-panel.js`        |
| Tests                   | `tests/` (mirrors source structure)                      |
| Tool configurations     | `pyproject.toml` (ruff, mypy, pytest, bandit)            |

---

## 1. Project Overview

This is a **Cisco Meraki integration for Home Assistant**. It monitors and manages Meraki network infrastructure (access points, switches, cameras, security appliances, environmental sensors) directly from Home Assistant.

### Key Technologies

| Layer       | Technologies                                                      |
| ----------- | ----------------------------------------------------------------- |
| Backend     | Python 3.13.2, Home Assistant Core, `meraki` SDK, `aiohttp`       |
| Frontend    | React, TypeScript, Vite, Home Assistant custom panel architecture |
| Testing     | pytest, pytest-asyncio, pytest-homeassistant-custom-component     |
| Linting     | Ruff, mypy, bandit, pylint                                        |
| CI/CD       | GitHub Actions, semantic-release, HACS                            |
| **Package** | **`uv` with `pyproject.toml`** (NOT pip/requirements.txt)         |

### Repository Structure

```
meraki-homeassistant/
├── custom_components/meraki_ha/     # Main integration code
│   ├── __init__.py                  # Integration entry point
│   ├── api/                         # WebSocket handlers
│   ├── binary_sensor/               # Binary sensor platform
│   ├── button/                      # Button platform
│   ├── camera.py                    # Camera platform
│   ├── coordinators/                # Data update coordinators
│   ├── core/                        # Core business logic & API client
│   │   ├── api/endpoints/           # Meraki API endpoint wrappers
│   │   └── utils/                   # API utilities
│   ├── discovery/                   # Device discovery handlers
│   ├── helpers/                     # Utility functions
│   ├── hubs/                        # Hub/bridge implementations
│   ├── number/                      # Number platform
│   ├── select/                      # Select platform
│   ├── sensor/                      # Sensor platform (largest)
│   ├── services/                    # HA service implementations
│   ├── switch/                      # Switch platform
│   ├── text/                        # Text input platform
│   └── www/                         # React frontend (Vite project)
├── tests/                           # Test suite (mirrors source structure)
├── docs/                            # Architecture & design documentation
├── pyproject.toml                   # Python dependencies & tool config
├── uv.lock                          # Lock file for reproducible builds
└── run_checks.sh                    # Quality check script
```

---

## 2. Critical Rules (Read First)

### 2.1. Package Management: uv Only

This project uses **`uv`** as the Python package manager. **Never use `requirements.txt` files.**

```bash
# Install all dev dependencies
uv sync --all-extras

# Add a new dependency
uv add <package-name>

# Or edit pyproject.toml directly, then:
uv sync --all-extras
```

### 2.2. Tool Configuration: pyproject.toml Only

**All tool configurations are centralized in `pyproject.toml`**. Never create separate config files:

- ❌ `.bandit.yaml`
- ❌ `.ruff.toml`
- ❌ `mypy.ini`
- ❌ `pytest.ini`
- ❌ `requirements.txt`

### 2.3. Git Branching: Always from Beta

**Always create new branches FROM the `beta` branch, never from `main`.**

```bash
git checkout beta
git pull origin beta
git checkout -b feat/my-new-feature

# When complete, merge back into beta
git checkout beta
git merge feat/my-new-feature
git push origin beta
```

The `main` branch is for **production releases only**.

### 2.4. Never Break Tests

**Always run the full test suite before completing work.**

```bash
uv run pytest
```

If any previously passing test fails after your changes, fix it before marking the task complete.

---

## 3. Core Architectural Patterns

### 3.1. The "Optimistic UI with Cooldown" Pattern ⚠️ CRITICAL

This is the **most important pattern** for entities that modify configuration (`switch`, `select`, `text`, `number`).

**Problem:** The Meraki Cloud API has a significant provisioning delay (up to 2-3 minutes).

**Solution:** Optimistic state with a timed cooldown:

1. Immediately update the entity's state and write to UI
2. Make a "fire-and-forget" API call to Meraki
3. Register a "pending update" with the coordinator (default 150 seconds)
4. Ignore coordinator updates while in the cooldown period

**Correct Implementation:**

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

**Anti-Pattern (WRONG):**

```python
async def async_turn_on(self, **kwargs: Any) -> None:
    """DON'T DO THIS - waits for API before updating UI."""
    await self.coordinator.client.update_ssid(...)  # User sees stale state
    await self.coordinator.async_refresh()  # Still stale - API hasn't propagated
    self._attr_is_on = True  # Too late - poor UX
    self.async_write_ha_state()
```

### 3.2. Centralized Logging ⚠️ REQUIRED

**Never use `logging.getLogger(__name__)`**. Always use `MerakiLoggers`:

```python
from custom_components.meraki_ha.helpers.logging_helper import MerakiLoggers

# Choose the appropriate logger for your module:
_LOGGER = MerakiLoggers.SENSOR     # For sensor entities
_LOGGER = MerakiLoggers.SWITCH     # For switch/select/number/text entities
_LOGGER = MerakiLoggers.API        # For API client code
_LOGGER = MerakiLoggers.CAMERA     # For camera operations
_LOGGER = MerakiLoggers.COORDINATOR  # For coordinators
_LOGGER = MerakiLoggers.DISCOVERY  # For discovery handlers
_LOGGER = MerakiLoggers.MQTT       # For MQTT services
_LOGGER = MerakiLoggers.FRONTEND   # For frontend/web UI
_LOGGER = MerakiLoggers.DEVICE_TRACKER  # For client tracking
_LOGGER = MerakiLoggers.MAIN       # For core integration code
_LOGGER = MerakiLoggers.ALERTS     # For webhook alerts
_LOGGER = MerakiLoggers.SCANNING_API   # For Scanning API/CMX
```

**Logger Selection Guide:**

| Module Type                           | Logger to Use                  |
| ------------------------------------- | ------------------------------ |
| `__init__.py`, config flows, helpers  | `MerakiLoggers.MAIN`           |
| `core/api/endpoints/`, API utils      | `MerakiLoggers.API`            |
| Coordinators, repositories            | `MerakiLoggers.COORDINATOR`    |
| `services/mqtt_*.py`                  | `MerakiLoggers.MQTT`           |
| Webhook handlers                      | `MerakiLoggers.ALERTS`         |
| `discovery/` handlers                 | `MerakiLoggers.DISCOVERY`      |
| Camera platform                       | `MerakiLoggers.CAMERA`         |
| Sensor entities                       | `MerakiLoggers.SENSOR`         |
| Switch, select, number, text entities | `MerakiLoggers.SWITCH`         |
| Frontend, web server                  | `MerakiLoggers.FRONTEND`       |
| Device tracker                        | `MerakiLoggers.DEVICE_TRACKER` |

### 3.3. API Client Conventions

- All calls to the `meraki` library object **must** use `snake_case` methods
- The project's client wrapper (`MerakiAPIClient`) also uses `snake_case`
- Always use the client from the coordinator: `self.coordinator.client`

### 3.4. Performance Timing Decorator

For async operations that may be slow, use the `async_log_time` decorator:

```python
from custom_components.meraki_ha.async_logging import async_log_time
from custom_components.meraki_ha.helpers.logging_helper import MerakiLoggers

@async_log_time(MerakiLoggers.API, slow_threshold=3.0)
async def get_organization_devices(self) -> list[dict]:
    """Fetch all devices - logs timing, warns if > 3 seconds."""
    ...
```

---

## 4. Home Assistant Integration Patterns

### 4.1. Required Patterns

| Pattern            | Implementation                                                        |
| ------------------ | --------------------------------------------------------------------- |
| Entity unique IDs  | All entities must have unique, stable IDs                             |
| Entity naming      | Use `_attr_has_entity_name = True`                                    |
| Device info        | Use `resolve_device_info()` and `format_device_name()` helpers        |
| Entity names       | Use `format_entity_name()` helper                                     |
| Unavailable states | Mark entities unavailable when device/service is offline, don't throw |
| CoordinatorEntity  | Use for data updates - centralized polling with automatic refresh     |
| Config entries     | Use config entries (not YAML configuration)                           |
| Async code         | Use async/await throughout for I/O-bound operations                   |

### 4.2. Entity Categories

Assign appropriate entity categories:

```python
from homeassistant.helpers.entity import EntityCategory

# For configuration entities
_attr_entity_category = EntityCategory.CONFIG

# For diagnostic entities
_attr_entity_category = EntityCategory.DIAGNOSTIC
```

### 4.3. Handling Disabled Features

When a feature is disabled in the Meraki Dashboard, set the entity to `Disabled`, not `unknown`:

```python
# Correct
self._attr_available = False

# Wrong - don't use unknown for disabled features
self._attr_native_value = None  # This shows as "unknown"
```

### 4.4. Constants

All constants must be defined in `custom_components/meraki_ha/const.py`.

### 4.5. Configuration Validation

All configuration data must be validated using `voluptuous` schemas in `schemas.py`.

---

## 5. MQTT Real-Time Sensor Updates

The integration supports **real-time MQTT updates** for Meraki MT environmental sensors.

**How it works:**

1. Meraki MT sensors publish to MQTT: `meraki/v1/mt/{network_id}/ble/{sensor_mac}/{metric}`
2. `MerakiMqttService` subscribes via HA's MQTT integration
3. Messages map sensor MAC to device serial and update the coordinator
4. MT sensor entities receive immediate updates (bypass polling delay)

**Key Components:**

| Component                | Location                       | Purpose                           |
| ------------------------ | ------------------------------ | --------------------------------- |
| `MerakiMqttService`      | `services/mqtt_service.py`     | Subscribe and parse MQTT messages |
| `MqttRelayManager`       | `services/mqtt_relay.py`       | Forward to external MQTT brokers  |
| `MerakiMqttStatusSensor` | `binary_sensor/mqtt_status.py` | Show MQTT connection status       |

**Configuration Options:**

- `enable_mqtt`: Enable/disable MQTT (default: `False`)
- `mqtt_relay_destinations`: List of external MQTT brokers to forward to

---

## 6. Development Workflow

### 6.1. Running Quality Checks

Before submitting changes, run all quality checks:

```bash
# All-in-one (recommended)
./run_checks.sh

# Or individually:
uv run ruff check --fix .
uv run ruff format .
uv run mypy custom_components/meraki_ha/ tests/
uv run bandit -c pyproject.toml -r custom_components/meraki_ha/
uv run pytest

# Home Assistant validation
docker run --rm -v "$(pwd)":/github/workspace ghcr.io/home-assistant/hassfest
```

### 6.2. Frontend Development

The Meraki side panel is a React application in `custom_components/meraki_ha/www/`.

```bash
cd custom_components/meraki_ha/www/
npm install
npm run build    # Required before committing
npm run dev      # Development server with hot-reload
```

**Important:** After any frontend changes, run `npm run build` and commit the built assets (`meraki-panel.js`, `style.css`).

### 6.3. Docker Test Environment

```bash
docker compose up
# Access at http://localhost:8123
```

---

## 7. Testing Requirements

### 7.1. Test Coverage

- **Unit tests are mandatory** for new features and bug fixes
- New features need tests proving they work
- Bug fixes need tests proving the bug is fixed
- Tests should be placed in `tests/`, mirroring the source structure
- Mock external API calls; never make real Meraki API calls in tests

### 7.2. Test File Naming

```
tests/
├── sensor/
│   └── test_temperature_sensor.py
├── switch/
│   └── test_ssid_switch.py
└── test_config_flow.py
```

### 7.3. Example Test Structure

```python
"""Tests for the SSID switch platform."""

import pytest
from unittest.mock import AsyncMock, patch

from custom_components.meraki_ha.switch.ssid_switch import MerakiSSIDSwitch


@pytest.fixture
def mock_coordinator():
    """Create a mock coordinator."""
    coordinator = AsyncMock()
    coordinator.client = AsyncMock()
    return coordinator


async def test_ssid_switch_turn_on(mock_coordinator):
    """Test turning on an SSID switch."""
    switch = MerakiSSIDSwitch(coordinator=mock_coordinator, ...)
    await switch.async_turn_on()

    assert switch.is_on is True
    mock_coordinator.client.update_ssid.assert_called_once()
```

---

## 8. Code Style

### 8.1. Python Code Style

- Follow **PEP 8** and Ruff rules
- Use **NumPy-style docstrings** (configured in `pyproject.toml`)
- Use **type hints** for all function signatures
- Prefer **async/await** for I/O-bound operations
- Use **early returns** for error conditions; place happy path last

### 8.2. Entity Naming Conventions

```python
# Device name format
f"{network_name} {device_name}"

# Entity name format
f"{device_name} {sensor_type}"

# Entity ID format (auto-generated)
# sensor.{network}_{device}_{type}
```

### 8.3. Commit Messages

Use **Conventional Commits** format:

```
type(scope): description

feat(camera): add configurable snapshot refresh interval
fix(api): filter networks before making API calls
docs(readme): update installation instructions
refactor(sensor): consolidate MT sensor base class
test(switch): add SSID toggle tests
build(deps): update homeassistant to 2025.11
ci(workflow): add beta branch workflow
```

**Types:** `feat`, `fix`, `docs`, `refactor`, `test`, `build`, `ci`, `style`, `perf`, `chore`

---

## 9. Common Tasks

### 9.1. Adding a New Sensor

1. Create the sensor class in `custom_components/meraki_ha/sensor/`
2. **Use the correct logger:** `_LOGGER = MerakiLoggers.SENSOR`
3. Register it in the sensor platform's `async_setup_entry()`
4. Add constants to `const.py`
5. Write unit tests in `tests/sensor/`
6. Run all quality checks

### 9.2. Adding a New Device Type Handler

1. Create a handler in `custom_components/meraki_ha/discovery/handlers/`
2. **Use the correct logger:** `_LOGGER = MerakiLoggers.DISCOVERY`
3. Register the handler in the discovery service
4. Ensure proper `DeviceInfo` is returned
5. Write unit tests

### 9.3. Adding a New Logger

If adding a completely new feature area:

1. Add to `MerakiLoggers` class in `helpers/logging_helper.py`:
   ```python
   MY_FEATURE: logging.Logger = logging.getLogger(f"{DOMAIN}.my_feature")
   ```
2. Add config constant in `const.py`:
   ```python
   CONF_LOG_LEVEL_MY_FEATURE: Final = "log_level_my_feature"
   ```
3. Add schema entry in `schemas.py` under `SCHEMA_LOGGING`
4. Add mapping in `logging_helper.py` → `_CONFIG_TO_LOGGER_MAP`
5. Add translations in `strings.json` and `translations/en.json`
6. Run `tests/helpers/test_logging_helper.py` to verify

### 9.4. Modifying the Frontend

1. Make changes in `custom_components/meraki_ha/www/src/`
2. Test with `npm run dev`
3. Build with `npm run build`
4. Commit both source and built files

---

## 10. Troubleshooting

### 10.1. Common Issues

| Issue                      | Solution                                                       |
| -------------------------- | -------------------------------------------------------------- |
| `ha-blocking-import` error | Defer imports using `async_get_loaded_integrations()`          |
| Circular import            | Use deferred imports or restructure modules                    |
| Entity shows "unavailable" | Check coordinator data population and entity `_attr_available` |
| Frontend not loading       | Rebuild with `npm run build`, clear browser cache              |
| API rate limiting          | Increase scan interval in integration options                  |
| Test failures              | Check if mocks are set up correctly for async operations       |

### 10.2. Debug Logging

Add to `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.meraki_ha: debug
    # Or target specific features:
    custom_components.meraki_ha.api: debug
    custom_components.meraki_ha.mqtt: warning # Silence noisy MQTT
```

---

## 11. Security Guidelines

### 11.1. Credentials

- **NEVER** hardcode API keys, tokens, or credentials in source code
- Use environment variables or Home Assistant's `config_entry` for secrets
- The Meraki API key is stored in `entry.data[CONF_API_KEY]`

### 11.2. Cryptography

- Use only modern, secure algorithms (SHA-256+, AES-GCM, ECDHE)
- Never use MD5, SHA-1, DES, 3DES, or RC4

---

## 12. Quality Scale Compliance

This integration targets **🥇 Gold tier** on the [HA Integration Quality Scale](https://developers.home-assistant.io/docs/core/integration-quality-scale/).

### Key Rules to Maintain

| Rule                | Requirement                                   |
| ------------------- | --------------------------------------------- |
| entity-unique-id    | All entities must have unique IDs             |
| has-entity-name     | Use `_attr_has_entity_name = True`            |
| entity-unavailable  | Mark entities unavailable when offline        |
| entity-device-class | Use appropriate device classes                |
| entity-category     | Assign CONFIG or DIAGNOSTIC where appropriate |
| test-coverage       | Maintain 95%+ test coverage                   |
| strict-typing       | All code must be fully typed                  |
| async-dependency    | Use async patterns throughout                 |

---

## 13. CI/CD Workflows

The project uses GitHub Actions for CI/CD:

| Workflow                         | Trigger         | Purpose                         |
| -------------------------------- | --------------- | ------------------------------- |
| `beta-ci.yaml`                   | Push to beta    | Run all quality checks          |
| `main-ci.yaml`                   | Push to main    | Production release checks       |
| `beta-version-update.yaml`       | Merge to beta   | Bump beta version               |
| `production-version-update.yaml` | Merge to main   | Bump production version         |
| `hassfest.yaml`                  | PR              | Validate manifest and structure |
| `deploy-local.yml`               | Manual/workflow | Deploy to local HA instance     |

---

## 14. Self-Correction

- If you make a mistake, acknowledge it and correct it
- If you discover a better technique, incorporate it
- Always verify changes pass all quality checks before completing a task
- If tests fail, investigate and fix—don't skip or disable tests

---

_This document was last updated for version 3.1.0._
