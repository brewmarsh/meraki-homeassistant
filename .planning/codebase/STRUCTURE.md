# Codebase Structure

**Analysis Date:** 2025-05-23

## Directory Layout

```
meraki-homeassistant/
├── custom_components/meraki_ha/     # Core integration code
│   ├── api/                        # Higher-level API commands and websocket
│   ├── binary_sensor/              # Binary sensor entity implementations
│   ├── blueprints/                 # Automation blueprints for Meraki
│   ├── button/                     # Button entity implementations
│   ├── const/                      # Shared constants
│   ├── coordinators/               # Home Assistant DataUpdateCoordinators
│   ├── core/                       # Underlying business logic and models
│   ├── discovery/                  # Entity discovery logic and handlers
│   ├── event/                      # Event entity implementations (webhook events)
│   ├── helpers/                    # Utility functions and migrations
│   ├── hubs/                       # High-level representations of Orgs and Networks
│   ├── media/                      # Static icons and logos
│   ├── meraki_select/              # Custom select entities (profiles, VPN, etc.)
│   ├── number/                     # Number entity implementations (bandwidth, etc.)
│   ├── sensor/                     # Sensor entity implementations
│   ├── services/                   # Custom service implementations
│   ├── switch/                     # Switch entity implementations
│   ├── text/                       # Text entity implementations (SSID naming)
│   ├── translations/               # Localization (en, es, fr)
│   └── www/                        # Frontend assets for custom cards
├── frontend/                       # Source code for the Meraki dashboard card
├── tests/                          # Automated test suite (pytest)
├── docs/                           # Documentation and architecture diagrams
├── scripts/                        # Maintenance and development scripts
├── tools/                          # Internal developer tools
└── .planning/                      # Project planning and codebase analysis
```

## Directory Purposes

**custom_components/meraki_ha/core/:**

- Purpose: The engine of the integration, containing all logic independent of the HA entity lifecycle.
- Contains: Models, parsers, fetch strategies, and the low-level API client.
- Key files: `core/coordinator_helpers/data_fetcher.py`, `core/api/client.py`

**custom_components/meraki_ha/coordinators/:**

- Purpose: Specialized data managers that sync Meraki data with Home Assistant.
- Contains: Subclasses of `DataUpdateCoordinator` for different product categories.
- Key files: `coordinators/main.py`, `coordinators/switch.py`, `coordinators/camera.py`

**custom_components/meraki_ha/discovery/:**

- Purpose: Logic to dynamically discover and register entities based on fetched data.
- Contains: `DeviceDiscoveryService` and domain-specific handlers.
- Key files: `discovery/service.py`, `discovery/handlers/universal.py`

**custom_components/meraki_ha/platforms (sensor, switch, etc.):**

- Purpose: Implementation of standard Home Assistant entity platforms.
- Contains: Entity classes that provide state and attributes.
- Key files: `sensor/device/device_status.py`, `switch/switch_port.py`

## Key File Locations

**Entry Points:**

- `custom_components/meraki_ha/__init__.py`: Main integration setup and entry point.
- `custom_components/meraki_ha/config_flow.py`: User configuration interface.
- `custom_components/meraki_ha/webhook.py`: Real-time data processing from Meraki.

**Configuration:**

- `custom_components/meraki_ha/manifest.json`: Integration metadata and dependencies.
- `custom_components/meraki_ha/schemas.py`: Validation schemas for configuration and services.
- `custom_components/meraki_ha/const/`: Centralized constant definitions.

**Core Logic:**

- `custom_components/meraki_ha/core/coordinator_helpers/data_fetcher.py`: Orchestrates multi-tiered data fetching.
- `custom_components/meraki_ha/core/api/protocol.py`: Defines the low-level communication protocol.

**Testing:**

- `tests/conftest.py`: Shared test fixtures and mocks.
- `tests/test_config_flow.py`: Tests for the configuration UI.
- `tests/test_coordinator.py`: Core logic tests for data synchronization.

## Naming Conventions

**Files:**

- Snake case: `device_status.py`, `config_flow.py`
- Suffix for entities: Often mirrors their purpose, e.g., `_sensor.py`, `_switch.py`.

**Directories:**

- Snake case: `binary_sensor`, `fetch_strategies`.

## Where to Add New Code

**New Feature (e.g., adding a new Meraki product type):**

- Primary logic: `custom_components/meraki_ha/core/fetch_strategies/`
- Data model: `custom_components/meraki_ha/core/models/`
- Coordinator: `custom_components/meraki_ha/coordinators/` (if it warrants a new one)
- Discovery: `custom_components/meraki_ha/discovery/handlers/`
- Entities: `custom_components/meraki_ha/sensor/` (or relevant platform)
- Tests: `tests/` (corresponding to the product type)

**New Component/Module:**

- Implementation: Create a sub-directory in `custom_components/meraki_ha/` or within `core/` if it's internal logic.

**Utilities:**

- Shared helpers: `custom_components/meraki_ha/core/utils/` or `custom_components/meraki_ha/helpers/`

## Special Directories

**custom_components/meraki_ha/www/:**

- Purpose: Contains static JavaScript assets for the Home Assistant frontend.
- Generated: Yes (built from `frontend/` source).
- Committed: Yes.

**custom_components/meraki_ha/**pycache**/:**

- Purpose: Python bytecode cache.
- Generated: Yes.
- Committed: No.

---

_Structure analysis: 2025-05-23_
