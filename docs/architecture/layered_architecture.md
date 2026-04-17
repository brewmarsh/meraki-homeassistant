# Layered Architecture and Data Flow

The Meraki HA integration follows a strict layered architecture to ensure scalability and ease of maintenance.

## 1. Architecture Layers

### 1.1. Data Source (Meraki Cloud)

The source of truth. Data is retrieved via the official Meraki Dashboard SDK (v1.x).

### 1.2. Client Layer (`core/api/`)

Stateless wrapper for the Meraki SDK.

- **`MerakiAPIClient`**: Orchestrates all network requests.
- **Throttling**: Implements a global semaphore to ensure we do not exceed organization rate limits.

### 1.3. Strategy Layer (`core/fetch_strategies/`)

The "heavy lifting" layer. Strategies are responsible for:

- Fetching specific slices of data (e.g., `ApplianceUplinkHelper`).
- Normalizing varied API response formats into consistent internal models.
- Merging disparate data (e.g., combining status and performance metrics).

### 1.4. Orchestration Layer (`core/coordinators/`)

- **`MerakiMainCoordinator`**: Manages the integration state.
- **Tiered Polling**: Uses different intervals for "fast" data (Online/Offline) vs "slow" data (Versions/Settings).
- **Update Cycle**: `Coordinator` -> `Strategy` -> `Processor` -> `Registry`.

### 1.5. Platform Layer (`sensor/`, `switch/`, etc.)

Home Assistant specific implementations.

- **Optimistic Entities**: Specialized base classes for entities that modify state.
- **Registration**: Entities are dynamically created by `DiscoveryService` handlers.

## 2. Request Life Cycle

### 2.1. Inbound Update (Webhook)

1. Meraki Cloud sends a POST request to the HA Webhook endpoint.
2. `webhook.py` validates the `sharedSecret`.
3. The specific handler (e.g., `_handle_camera_motion_alert`) parses the payload.
4. The coordinator is notified and immediately updates the relevant device state.

### 2.2. Outbound Command (Service Call)

1. User toggles a switch in the HA UI.
2. `async_turn_on` performs an **Optimistic Update** (UI reflects change instantly).
3. `register_pending_update` starts a cooldown timer.
4. The `MerakiAPIClient` sends the command to Meraki.
5. On failure, the entity reverts state after the cooldown expires.
