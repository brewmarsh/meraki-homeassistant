# Roadmap

This document outlines the technical debt and refactoring goals for the Meraki Home Assistant integration.

## Architectural Standards

To maintain a modular, service-oriented architecture, we will adhere to the following standards. Files that violate these standards are considered "God Classes" and must be refactored.

*   **Size**: Files must not exceed 400 lines of code.
*   **Responsibility**: Classes should handle a single, distinct domain (e.g., API calls, entity creation, or data validation).
*   **Coupling**: Classes should not import more than 3 distinct service modules.

## Refactoring Backlog

| File | Status | God Class Violation(s) | Refactoring Plan |
|---|---|---|---|
| `custom_components/meraki_ha/coordinator.py` | In Progress | Size (439 lines), Responsibility (API data fetching, entity population, state management), Coupling (imports `CameraService`, `DeviceControlService`, `SwitchPortService`) | Split into `helpers.py` (pure logic) and `managers.py` (state tracking) |
| `custom_components/meraki_ha/const.py` | Pending | Responsibility (mixes configuration keys, API constants, platform types, UI labels) | Split into `const_conf.py`, `const_api.py`, etc. |
| `custom_components/meraki_ha/discovery/service.py` | Pending | N/A (previously suspected) | Implement Factory/Handler pattern for entity creation |
| `custom_components/meraki_ha/api.py` | Refactored | N/A (previously suspected) | Split into domain services (e.g., `SwitchService`, `CameraService`, `SensorService`) |

## Future Goals

*   [ ] Refactor MerakiDataUpdateCoordinator
*   [ ] Refactor const.py
*   [ ] Refactor DeviceDiscoveryService
*   [ ] Continue refactoring MerakiAPIClient into domain services
