# Testing Patterns

**Analysis Date:** 2024-05-14

## Test Framework

**Runner:**

- `pytest` (configured in `pytest.ini` and `pyproject.toml`).
- `pytest-asyncio` for async test support.

**Assertion Library:**

- `pytest` (standard `assert` statements).

**Run Commands:**

```bash
pytest                  # Run all Python tests
pytest tests/sensor     # Run specific test directory
npx playwright test     # Run UI tests
```

## Test File Organization

**Location:**

- Mirrored to source: `tests/` directory follows `custom_components/meraki_ha/` structure (e.g., `tests/sensor/network/test_ssid_details.py`).
- UI Tests: `tests/ui/` (using Playwright).

**Naming:**

- Files: `test_*.py` for Python, `*.spec.ts` for Playwright.
- Functions: `test_*` for Python.

**Structure:**

```
tests/
├── conftest.py             # Global fixtures
├── const.py                # Mock data constants
├── fixtures/               # Test data files
├── core/                   # Core logic tests
├── sensor/                 # Sensor platform tests
├── ui/                     # UI/E2E tests (Playwright)
└── ...                     # Other platform/module tests
```

## Test Structure

**Suite Organization:**

```python
async def test_sensor_name() -> None:
    """Test description."""
    # 1. Setup (mocks, data)
    coordinator = MagicMock()

    # 2. Initialization
    sensor = MerakiSensor(coordinator, ...)

    # 3. Assertions
    assert sensor.state == "expected"

    # 4. Trigger Action (e.g., update)
    sensor._handle_coordinator_update()

    # 5. Final Assertions
    assert sensor.state == "new_expected"
```

**Patterns:**

- Extensive use of `async def` for tests.
- High reliance on mocking for external dependencies (`MagicMock`, `AsyncMock`).

## Mocking

**Framework:** `unittest.mock` (standard Python).

**Patterns:**

```python
# Mocks the Meraki API client globally via fixture in conftest.py
@pytest.fixture
def mock_meraki_client():
    with patch("custom_components.meraki_ha.core.api.client.meraki.DashboardAPI") as mock_api:
        # Mock specific endpoints...
        yield mock_api
```

**What to Mock:**

- API Clients (`meraki.DashboardAPI`).
- Home Assistant core components (`hass.http`, `hass.data`).
- Network-bound operations (webhooks, etc.).

**What NOT to Mock:**

- Pure logic (helpers, calculation methods) where possible.
- Small data models or constants.

## Fixtures and Factories

**Test Data:**

```python
# Defined in tests/const.py
MOCK_ALL_DATA = {
    "networks": [...],
    "devices": [...],
    "wireless_settings": {...},
}
```

**Location:**

- `tests/const.py` for shared mock data.
- `tests/fixtures/` for potentially larger data blobs (e.g., JSON response snapshots).

## Coverage

**Requirements:** No strict minimum percentage enforced in `pyproject.toml`, but files like `coverage_report.txt` suggest active monitoring.

**View Coverage:**

```bash
pytest --cov=custom_components/meraki_ha tests/
```

## Test Types

**Unit Tests:**

- Test individual entity classes, parsers, and helpers (e.g., `tests/sensor/network/test_ssid_details.py`).

**Integration Tests:**

- Testing interaction between coordinators and discovery (e.g., `tests/discovery/test_service.py`).
- Testing `config_flow` and `reauth_flow`.

**E2E Tests:**

- UI tests using Playwright (`tests/ui/guest_access_card.spec.ts`).
- Some "E2E" labeled backend tests like `tests/test_e2e_ipsk.py`.

## Common Patterns

**Async Testing:**

- `pytest-asyncio` with `asyncio_mode = "auto"`.
- Use `await` for calls that return awaitables.

**Error Testing:**

- Use `pytest.raises(ExceptionClass)` to verify error conditions.

---

_Testing analysis: 2024-05-14_
