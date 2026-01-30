# AI Agent Instructions

**Primary Objective:** Refactor the `meraki_ha` Home Assistant integration to a modern, layered architecture that is scalable, highly testable, and robust against API failures. Prioritize a modular design to enable future feature expansion without significant refactoring.

**Core Instructions:**

1.  **Strictly Adhere to the Implementation Plan:** Follow the provided ## Updated Design and Implementation Plan sequentially. Do not deviate from the specified phases and components.
2.  **Focus on Unit Testing:** Write comprehensive unit tests for each new class and function as you develop it. Use in-memory mocks for any external dependencies (e.g., the `MerakiApiClient` and `MerakiRepository`). Minimize the number of full integration tests to conserve disk space.
3.  **Modular Code Structure:** Create separate Python files and directories as outlined in the plan (e.g., `meraki_ha/api/`, `meraki_ha/repository/`, `meraki_ha/hubs/`). Ensure each file contains a single, well-defined class or module.
4.  **Clear Documentation:** Add docstrings to all new classes and public methods, explaining their purpose, parameters, and return values. This is crucial for future maintenance and for other agents.
5.  **Git Commits:** Make small, logical commits for each completed sub-task (e.g., "feat: Implement MerakiApiClient with circuit breaker," "refactor: Add MerakiRepository and FSM").

**Constraints & Guidelines:**

- **No Unnecessary Packages:** Only install libraries that are strictly necessary for the new architecture (e.g., `tenacity` for the circuit breaker, if not already present).
- **Disk Space Management:** Be mindful of disk usage during testing. Delete any temporary files generated and avoid storing large test fixtures in the codebase.
- **Handle Errors Gracefully:** Implement robust error handling at all layers, logging issues clearly without crashing the integration.

---

## Updated Design and Implementation Plan

This plan is a cohesive roadmap for refactoring the `meraki_ha` integration. It combines a robust architectural design with a practical, step-by-step implementation guide, built to be executed by AI coding agents.

### Architectural Design: A Layered and Modular Approach

The architecture is based on a clean separation of concerns, ensuring each component has a single, well-defined responsibility.

- **API Layer:** The `MerakiApiClient` handles low-level HTTP requests and responses. It is a stateless, pure client.
- **Data Access Layer:** The `MerakiRepository` sits on top of the `MerakiApiClient`. It is responsible for caching data, managing the API connection state with a **Finite State Machine (FSM)**, and handling retries/rate-limiting.
- **Logic Layer:** The `OrganizationHub` and `NetworkHub` orchestrate the integration's logic. They are responsible for polling at appropriate intervals and managing the Home Assistant device/entity registry. They are decoupled from data access via **Dependency Injection (DI)** of the `MerakiRepository`.
- **Entity Discovery Layer:** A modular `DeviceDiscoveryService` uses a collection of device-specific `Handlers` to dynamically create Home Assistant entities. This pattern makes adding support for new devices straightforward.

## Implementation Plan

### Phase 1: Foundational Layers (API Client & Repository)

1.  **Refactor `OrganizationHub` and `NetworkHub` (`meraki_ha/hubs/`)**:
    - **Extract Logic into Helper Methods:** The main `_async_update_data` method should primarily serve as an orchestrator. Move complex data processing, filtering, or transformation logic into private helper methods within the same file.
    - **Maintain Small File Sizes:** If a hub's file becomes too large, consider whether some of its logic could be moved to a dedicated service class (e.g., `meraki_ha/services/state_manager.py`).

### Phase 3: Modular Entity Discovery

1.  **Develop `DeviceHandlers` (`meraki_ha/discovery/handlers/`)**:
    - **Enforce the 300-Line Limit:** If a handler file (e.g., `MRHandler.py`) becomes too large, it suggests that the handler is trying to do too much. Break its entity creation logic into multiple, separate functions.
2.  **Create `DeviceDiscoveryService` (`meraki_ha/discovery/service.py`)**:
    - **Simplify the Core Loop:** Ensure the `discover_entities` method is a simple loop that delegates all complex work to the `DeviceHandlers`. The code should be clear and have a low cyclomatic complexity.

### Phase 4: Testing and Project Cleanup

1.  **Prioritize Lightweight Tests:** When writing tests, focus on testing individual methods and functions, not entire classes. This keeps test files small and prevents the need for large, deeply nested test fixtures.
2.  **Linting and Formatting:** Use automated tools like `black` or `ruff` to ensure consistent code style and formatting across the entire project. This improves readability and helps prevent subtle errors that can be caused by inconsistent indentation.
