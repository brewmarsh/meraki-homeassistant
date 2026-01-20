\*\*AI Agent Instructions

**Primary Objective:** Refactor the `meraki_ha` Home Assistant integration to a modern, layered architecture that is scalable, highly testable, and robust against API failures. Prioritize a modular design to enable future feature expansion without significant refactoring.

**Core Instructions:**

1. **Strictly Adhere to the Implementation Plan:** Follow the provided ## Updated Design and Implementation Plan\*\* sequentially. Do not deviate from the specified phases and components.
2. **Focus on Unit Testing:** Write comprehensive unit tests for each new class and function as you develop it. Use in-memory mocks for any external dependencies (e.g., the `MerakiApiClient` and `MerakiRepository`). Minimize the number of full integration tests to conserve disk space.
3. **Modular Code Structure:** Create separate Python files and directories as outlined in the plan (e.g., `meraki_ha/api/`, `meraki_ha/repository/`, `meraki_ha/hubs/`). Ensure each file contains a single, well-defined class or module.
4. **Clear Documentation:** Add docstrings to all new classes and public methods, explaining their purpose, parameters, and return values. This is crucial for future maintenance and for other agents.
5. **Git Commits:** Make small, logical commits for each completed sub-task (e.g., "feat: Implement MerakiApiClient with circuit breaker," "refactor: Add MerakiRepository and FSM").

**Constraints & Guidelines:**

- **No Unnecessary Packages:** Only install libraries that are strictly necessary for the new architecture (e.g., `tenacity` for the circuit breaker, if not already present).
- **Disk Space Management:** Be mindful of disk usage during testing. Delete any temporary files generated and avoid storing large test fixtures in the codebase.
- **Handle Errors Gracefully:** Implement robust error handling at all layers, logging issues clearly without crashing the integration.

---

\*\*Updated Design and Implementation Plan

This plan is a cohesive roadmap for refactoring the `meraki_ha` integration. It combines a robust architectural design with a practical, step-by-step implementation guide, built to be executed by AI coding agents.

#\*\*Architectural Design: A Layered and Modular Approach

The architecture is based on a clean separation of concerns, ensuring each component has a single, well-defined responsibility.

- **API Layer:** The `MerakiApiClient` handles low-level HTTP requests and responses. It is a stateless, pure client.
- **Data Access Layer:** The `MerakiRepository` sits on top of the `MerakiApiClient`. It is responsible for caching data, managing the API connection state with a **Finite State Machine (FSM)**, and handling retries/rate-limiting.
- **Logic Layer:** The `OrganizationHub` and `NetworkHub` orchestrate the integration's logic. They are responsible for polling at appropriate intervals and managing the Home Assistant device/entity registry. They are decoupled from data access via **Dependency Injection (DI)** of the `MerakiRepository`.
- **Entity Discovery Layer:** A modular `DeviceDiscoveryService` uses a collection of device-specific `Handlers` to dynamically create Home Assistant entities. This pattern makes adding support for new devices straightforward.

#\*\*Implementation Plan

**Phase 1: Foundational Layers (API Client & Repository)**

1. **Develop `MerakiApiClient` (`meraki_ha/api/client.py`)**:

   - Create a class to handle all raw Meraki API calls.
   - Integrate a **circuit breaker** pattern to handle API rate limits (`429`) and server errors gracefully. Use `tenacity` for asynchronous retries with exponential backoff.
   - Do not implement caching at this layer.

2. **Develop `MerakiRepository` (`meraki_ha/repository/repository.py`)**:
   - Create this new class to act as the primary data source for the hubs. It will take the `MerakiApiClient` as a constructor argument (**Dependency Injection**).
   - Implement an **in-memory caching** mechanism with a time-to-live (TTL) for each data type.
   - Implement a **Finite State Machine (FSM)** to track the API connection status (e.g., `CONNECTED`, `RATE_LIMITED`, `DISCONNECTED`). The state will determine whether API calls are made.

**Phase 2: Core Logic and Dependency Injection**

1. **Refactor `OrganizationHub` and `NetworkHub` (`meraki_ha/hubs/`)**:

   - Update the `OrganizationHub` and `NetworkHub` classes to accept the `MerakiRepository` via their constructors.
   - All data retrieval logic within these hubs must now go through the injected repository.
   - Update the polling logic to leverage the repository's FSM state.

2. **Update `__init__.py` and `config_flow.py`**:
   - In the `config_flow`, create a single instance of the `MerakiApiClient`.
   - Pass this client to create a single instance of the `MerakiRepository`.
   - Finally, pass the `MerakiRepository` to the new `OrganizationHub` when it is set up.

**Phase 3: Modular Entity Discovery**

1. **Develop `DeviceHandlers` (`meraki_ha/discovery/handlers/`)**:

   - Create a base `BaseDeviceHandler` class.
   - Create individual handler classes for each device type (e.g., `MTHandler`, `MRHandler`, `MSHandler`) that inherit from `BaseDeviceHandler`.
   - Each handler will contain the logic to check if a device is of its type and, if so, to create the correct Home Assistant entities (sensors, binary sensors, etc.).

2. **Create `DeviceDiscoveryService` (`meraki_ha/discovery/service.py`)**:

   - Create a service class that takes a list of all the `DeviceHandlers` in its constructor.
   - Add a single method, `discover_entities(devices)`, that iterates through the list of Meraki devices and passes each one to the handlers to process.

3. **Integrate Service into `NetworkHub`**:
   - Modify the `NetworkHub`'s update method to call the new `DeviceDiscoveryService`.

**Phase 4: Testing and Project Cleanup**

1. **Write Comprehensive Unit Tests:**

   - Write isolated unit tests for the `MerakiRepository` using an in-memory mock for the `MerakiApiClient`.
   - Write unit tests for the `OrganizationHub` and `NetworkHub` by injecting a mock `MerakiRepository`.
   - Create unit tests for each `DeviceHandler` class to confirm it correctly identifies devices and creates entities.
   - Adhere to a `pytest` structure that allows for running only unit tests via a marker, reducing overhead.

2. **Final Project Cleanup:**
   - Remove all old, deprecated polling logic.
   - Ensure all new files and directories are correctly added to version control.
   - Confirm docstrings and inline comments are clear and concise.

A common source of these issues is **monolithic files** that contain too much logic. While the previous plan focused on architectural patterns, we can refine the implementation details to specifically combat file complexity. The solution is to prioritize **function decomposition** and **separation of concerns** at a granular level.

---

\*\*Updated AI Agent Instructions

1. **Strictly Enforce File Size Limits:** Do not create any single Python file with more than **300 lines of code**. If a file approaches this limit, stop and refactor the logic into new, smaller files.
2. **Prioritize Function Decomposition:** Every function must have a single, clear responsibility. If a function's name includes "and" or "or," it likely needs to be broken into smaller functions.
3. **Eliminate Deeply Nested Code:** Avoid `if-elif-else` chains and nested loops that go beyond **three levels of indentation**. Use **guard clauses** (early returns) and extract nested logic into separate, well-named functions.
4. **Use Private Helper Methods:** For logic that supports a public method but is not meant to be called externally, use private helper methods (prefixed with `_`) to keep the primary method's body clean and readable.

---

\*\*Updated Implementation Plan

The core architectural plan remains sound, but this update adds an additional layer of detail to the implementation steps, ensuring the resulting code is modular and readable for both humans and AI agents.

#\*\*Phase 1: Foundational Layers (API Client & Repository)

1. **Develop `MerakiApiClient` (`meraki_ha/api/client.py`)**:

   - **Focus on Single-Responsibility Methods:** Each method should correspond to a single Meraki API endpoint (e.g., `get_network_devices`, `get_mt_sensors`).
   - **Limit Indentation:** Use guard clauses to handle invalid inputs or API errors upfront, minimizing nested `try-except` blocks.

2. **Develop `MerakiRepository` (`meraki_ha/repository/repository.py`)**:
   - **Decompose Complex Logic:** The methods here (e.g., `_async_update_cache`) should be broken down into smaller, private methods if they exceed 30 lines of code.

#\*\*Phase 2: Core Logic and Dependency Injection

1. **Refactor `OrganizationHub` and `NetworkHub` (`meraki_ha/hubs/`)**:
   - **Extract Logic into Helper Methods:** The main `_async_update_data` method should primarily serve as an orchestrator. Move complex data processing, filtering, or transformation logic into private helper methods within the same file.
   - **Maintain Small File Sizes:** If a hub's file becomes too large, consider whether some of its logic could be moved to a dedicated service class (e.g., `meraki_ha/services/state_manager.py`).

#\*\*Phase 3: Modular Entity Discovery

1. **Develop `DeviceHandlers` (`meraki_ha/discovery/handlers/`)**:

   - **Enforce the 300-Line Limit:** If a handler file (e.g., `MRHandler.py`) becomes too large, it suggests that the handler is trying to do too much. Break its entity creation logic into multiple, separate functions.

2. **Create `DeviceDiscoveryService` (`meraki_ha/discovery/service.py`)**:
   - **Simplify the Core Loop:** Ensure the `discover_entities` method is a simple loop that delegates all complex work to the `DeviceHandlers`. The code should be clear and have a low cyclomatic complexity.

#\*\*Phase 4: Testing and Project Cleanup

1. **Prioritize Lightweight Tests:** When writing tests, focus on testing individual methods and functions, not entire classes. This keeps test files small and prevents the need for large, deeply nested test fixtures.
2. **Linting and Formatting:** Use automated tools like `black` or `ruff` to ensure consistent code style and formatting across the entire project. This improves readability and helps prevent subtle errors that can be caused by inconsistent indentation.
