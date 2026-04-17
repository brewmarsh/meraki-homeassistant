# Architecture Overview: Meraki Home Assistant

This document details the high-performance, event-driven architecture of the Meraki HA integration.

## 1. Core Architectural Pillars

- **Unified Polling:** A central `MerakiMainCoordinator` manages all periodic data refreshes, preventing redundant API calls.
- **Modular Fetch Strategies:** Specialized helpers (e.g., `ApplianceUplinkHelper`) handle the complexity of specific API endpoints and data normalization.
- **Optimistic State Management:** Prevents UI "flicker" by maintaining local state during the Meraki cloud provisioning delay (cooldown pattern).
- **Hybrid Real-Time:** Combines resilient polling with Webhook-driven sub-second updates for critical events (MV Motion, Client Presence).

## 2. Component Hierarchy

### 2.1. API Layer (`core/api/`)

- **`MerakiAPIClient`**: Facade for the underlying SDK, managing semaphores and rate limiting.
- **Endpoints**: Specialized handlers for `wireless`, `appliance`, `switch`, and `camera`.

### 2.2. Logic & Data Layer (`core/coordinators/`)

- **`MerakiMainCoordinator`**: The brain of the integration. Orchestrates parallel data fetching via `FetchStrategies`.
- **`DataFetchManager`**: Dynamically adjusts fetch priority and handles tiered polling (e.g., 30s for health, 10m for firmware).

### 2.3. Discovery & Entity Layer (`discovery/`)

- **`DiscoveryService`**: Maps the Meraki cloud hierarchy (Org -> Network -> Device) to Home Assistant devices.
- **Handlers**: Platform-specific logic for instantiating sensors, switches, and device trackers.

## 3. Resilience & Security

- **PII Redaction:** `diagnostics.py` automatically scrubs serials, MACs, and API keys before export.
- **Fail-Safe Errors:** Uses `UpdateFailed` to correctly communicate API outages to the Home Assistant UI, marking entities as "Unavailable".
- **Optimistic Recovery:** If an API command fails, entities automatically revert to the last known-good state after the cooldown period.
