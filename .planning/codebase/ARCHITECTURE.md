# Architecture

**Analysis Date:** 2025-05-23

## Pattern Overview

**Overall:** Multi-layered specialized Coordinator-based architecture with Repository and Strategy patterns.

**Key Characteristics:**

- **Tiered Data Fetching:** Separates fast status polling from heavy detail fetching to optimize API usage and responsiveness.
- **Specialized Coordinators:** Uses multiple `DataUpdateCoordinator` instances (Main, Device, Switch, Camera, etc.) sharing a common data pool to manage complex Meraki product hierarchies.
- **Centralized Discovery:** A dedicated `DeviceDiscoveryService` orchestrates entity creation across all platforms based on the unified state from coordinators.

## Layers

**API Layer:**

- Purpose: Low-level communication with Meraki Dashboard API.
- Location: `custom_components/meraki_ha/core/api/` and `custom_components/meraki_ha/api/`
- Contains: HTTP client, protocol definitions, and endpoint-specific command implementations.
- Depends on: `aiohttp`
- Used by: Fetch strategies and repositories.

**Data Modeling Layer:**

- Purpose: Typed representations of Meraki entities.
- Location: `custom_components/meraki_ha/core/models/` and `custom_components/meraki_ha/core/parsers/`
- Contains: Model classes (e.g., `MerakiDevice`, `MerakiNetwork`) and parsers to transform raw API responses.
- Depends on: Standard library and `custom_components/meraki_ha/core/utils/`
- Used by: Coordinators and discovery service.

**Orchestration Layer:**

- Purpose: Coordinating data fetching, processing, and distribution.
- Location: `custom_components/meraki_ha/core/coordinator_helpers/` and `custom_components/meraki_ha/core/fetch_strategies/`
- Contains: `DataFetchManager`, `UpdateProcessor`, and product-specific `FetchStrategy` implementations (Appliance, Wireless, Switch, etc.).
- Depends on: API Layer, Data Modeling Layer.
- Used by: Coordinators.

**Home Assistant Integration Layer:**

- Purpose: Bridging Meraki data to Home Assistant entities and services.
- Location: `custom_components/meraki_ha/coordinators/`, `custom_components/meraki_ha/discovery/`, and `custom_components/meraki_ha/services/`
- Contains: `DataUpdateCoordinator` implementations, `DeviceDiscoveryService`, and custom service managers.
- Depends on: Orchestration Layer, Home Assistant Core.
- Used by: Platform entities (sensor, switch, etc.).

## Data Flow

**Polling Update Flow:**

1. `DataUpdateCoordinator` triggers a refresh (every 30s or as configured).
2. `DataFetchManager` executes `get_device_data` (Fast Poll) or `get_sensor_data` (Slow Poll).
3. `FetchStrategy` instances are invoked for each product type to gather detailed telemetry.
4. `UpdateProcessor` merges new data into the existing state.
5. Coordinators notify listeners (entities).
6. Home Assistant entities update their state and attributes.

**Real-time Update Flow (Webhook):**

1. Meraki Dashboard sends a POST request to the registered Home Assistant webhook URL.
2. `custom_components/meraki_ha/webhook.py` receives and validates the payload.
3. Payload is dispatched to the relevant coordinator or handled directly (e.g., event triggers).
4. Entities or Device Triggers react to the real-time event.

**Service Call Flow:**

1. User/Automation calls a Meraki-specific service (e.g., `meraki_ha.reboot_device`).
2. `ServicesManager` routes the call to the appropriate service class (e.g., `DeviceControlService`).
3. Service class uses a `MerakiRepository` to send the command via the API Layer.

## Key Abstractions

**DataUpdateCoordinator:**

- Purpose: Centralized state management for a specific domain of Meraki data.
- Examples: `custom_components/meraki_ha/coordinators/switch.py`, `custom_components/meraki_ha/coordinators/camera.py`
- Pattern: Home Assistant DataUpdateCoordinator.

**FetchStrategy:**

- Purpose: Encapsulates the logic for fetching and processing data for a specific Meraki product category.
- Examples: `custom_components/meraki_ha/core/fetch_strategies/wireless.py`, `custom_components/meraki_ha/core/fetch_strategies/appliance.py`
- Pattern: Strategy Pattern.

**DiscoveryHandler:**

- Purpose: Maps Meraki models to specific Home Assistant entity platforms and configurations.
- Examples: `custom_components/meraki_ha/discovery/handlers/network.py`, `custom_components/meraki_ha/discovery/handlers/universal.py`
- Pattern: Handler Pattern.

## Entry Points

**Integration Setup:**

- Location: `custom_components/meraki_ha/__init__.py`
- Triggers: Home Assistant integration loading.
- Responsibilities: Initializing API client, coordinators, discovery service, and registering platforms.

**Config Flow:**

- Location: `custom_components/meraki_ha/config_flow.py`
- Triggers: User adding the integration or configuring options.
- Responsibilities: Validating API keys, selecting organizations, and managing options.

**Webhook Receiver:**

- Location: `custom_components/meraki_ha/webhook.py`
- Triggers: Incoming HTTP requests from Meraki.
- Responsibilities: Authentication and dispatching of real-time events.

## Error Handling

**Strategy:** Multi-level error trapping with specialized exception types.

**Patterns:**

- **API Exceptions:** `custom_components/meraki_ha/core/errors.py` defines integration-specific errors like `MerakiApiError`, `MerakiAuthError`.
- **Coordinator Resilience:** `async_gather_with_timeout` and semaphores are used to prevent API overloading and handle intermittent timeouts gracefully.
- **Entity Availability:** Entities track their availability based on the last successful update from their respective coordinator.

## Cross-Cutting Concerns

**Logging:** Uses structured logging with a standard `_LOGGER` instance, with specific log levels for noisy operations (e.g., polling).
**Validation:** Employs Voluptuous schemas in `custom_components/meraki_ha/schemas.py` for config and service input validation.
**Authentication:** Managed via `custom_components/meraki_ha/authentication.py`, supporting both API key validation and webhook secret verification.

---

_Architecture analysis: 2025-05-23_
