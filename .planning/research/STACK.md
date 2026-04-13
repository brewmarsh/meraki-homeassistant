# Technology Stack

**Project:** Home Assistant Network Device Hub Integration (Meraki focus)
**Researched:** February 2025

## Recommended Stack

### Core Framework

| Technology          | Version  | Purpose              | Why                                                                                                  |
| ------------------- | -------- | -------------------- | ---------------------------------------------------------------------------------------------------- |
| Home Assistant Core | 2024.10+ | Integration platform | Standard for modern integration features (like `_async_setup` and `CoordinatorEntity` improvements). |
| Python              | 3.12+    | Execution language   | Current HA core requirement.                                                                         |

### Database

| Technology       | Version | Purpose       | Why                                                                                                                   |
| ---------------- | ------- | ------------- | --------------------------------------------------------------------------------------------------------------------- |
| SQLite / MariaDB | N/A     | State history | HA default. Large network integrations generate high event volume; recommendation is MariaDB for high-density setups. |

### Infrastructure

| Technology            | Version | Purpose       | Why                                                                                |
| --------------------- | ------- | ------------- | ---------------------------------------------------------------------------------- |
| Webhooks              | N/A     | Push updates  | Meraki's preferred method for real-time client tracking; reduces polling overhead. |
| DataUpdateCoordinator | Core    | Data fetching | Simplifies polling management and state updates across many entities.              |

### Supporting Libraries

| Library      | Version | Purpose           | When to Use                                              |
| ------------ | ------- | ----------------- | -------------------------------------------------------- |
| `meraki`     | Latest  | SDK               | Official Cisco Meraki Python SDK for API interactions.   |
| `aiohttp`    | Core    | Async HTTP        | For non-blocking API calls; already in HA core.          |
| `voluptuous` | Core    | Schema validation | Standard for HA config flow and options flow validation. |

## Alternatives Considered

| Category     | Recommended             | Alternative           | Why Not                                                                                                                   |
| ------------ | ----------------------- | --------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| Tracking     | Webhooks                | Polling               | Polling 1000+ clients via API will hit rate limits and cause latency.                                                     |
| Coordination | `DataUpdateCoordinator` | Manual `async_update` | `CoordinatorEntity` handles state management and polling interval logic better.                                           |
| Persistence  | `EntityRegistry`        | `RestoreEntity`       | `RestoreEntity` is for state recovery; `EntityRegistry` is for existence. Network devices should be managed via registry. |

## Installation

```bash
# Core requirements (handled by HA)
# Custom dependencies should be in manifest.json
```

## Sources

- [Home Assistant Developer Docs: DataUpdateCoordinator](https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-fetching)
- [Home Assistant Architecture: Entity Lifecycle](https://developers.home-assistant.io/docs/core/entity)
- [Cisco Meraki SDK Documentation](https://developer.cisco.com/meraki/api-v1/python-sdk-overview/)
