# Requirements Verification (ha-camera-refactor2)

This document verifies the state of the codebase against the requirements for the camera refactoring task.

- **R1: Complete Discovery:**

  - **[VERIFIED]** `MVHandler` discovers and creates the `MerakiCamera` entity.
  - **[VERIFIED]** `MVHandler` correctly passes `config_entry` and `CameraService` to the `MerakiCamera` entity during initialization.

- **R2: RTSP Stream Control:**

  - **[FAIL]** The `MerakiCamera` entity is missing the `turn_on` and `turn_off` methods required for stream control.
  - **[VERIFIED]** The `CameraService` has the necessary `async_set_rtsp_stream_enabled` method to control the stream.

- **R3: Configuration Honored:**

  - **[FAIL]** The `MVHandler` does not currently check the `rtsp_stream_enabled` option at startup to proactively enable the stream.

- **R4: API Robustness:**

  - **[FAIL]** The `core/utils/api_utils.py` module's `validate_response` function raises an exception on empty API responses, causing crashes instead of handling them gracefully. This is the source of the "Empty response from API" error.

- **R5: Informative Feedback:**
  - **[PARTIAL]** The `MerakiCamera` entity has some error handling for streams, but it needs to be improved to be more state-driven and provide clearer feedback through the coordinator. The `camera_repository.py` also needs to be improved to handle non-RTSP URLs.

- **R6: Maintainability & ACL Score:**
  - **[VERIFIED]** `resolve_device_info` in `helpers/device_info_helpers.py` refactored into specialized private helpers (`_resolve_ssid_info`, `_resolve_client_info`, `_resolve_network_info`, `_resolve_physical_device_info`).
  - **[VERIFIED]** ACL score for `resolve_device_info` reduced below 10 by removing nested conditionals and delegating logic.
  - **[VERIFIED]** All helper functions are strictly typed and under 50 lines of code.

- **R7: Visual Card Editors:**
  - **[VERIFIED]** Implementation of visual configuration editors for Meraki custom cards to replace YAML-only editing and improve user experience with native Home Assistant entity pickers. Fixed a bug where entity pickers were not displaying due to incorrect Lit property bindings.

- **R8: Native Loading States:**
  - **[VERIFIED]** Implementation of native loading states in the `meraki-guest-access-card` to provide visual feedback during asynchronous data fetching.

- **R9: Correct Dropdown Selection:**
  - **[VERIFIED]** All `<ha-select>` components must use `<mwc-list-item>` as children with attribute binding (`value="${...}"`) instead of property binding (`.value="${...}"`) to ensure correct event registration and selection in the Home Assistant UI.

- **R10: No Explicit Material Imports:**
  - **[VERIFIED]** Custom Lovelace cards must not explicitly import `@material/*` components (e.g., `mwc-list-item`). Home Assistant registers these components globally, and bundling them causes a `CustomElementRegistry` collision ("mwc-ripple").
  - **[VERIFIED]** Staging workflow (`deploy-staging.yaml`) enhanced to capture rich error details in the `CI_ERROR_DETAILS` environment variable.
  - **[VERIFIED]** Automated GitHub Issues now include these error details in the body and are tagged with the `jules` label to trigger AI-driven triage.

- **R11: Centralized Logging (No File Dependency):**
  - **[VERIFIED]** Reset and staging scripts must not rely on deprecated Home Assistant file-based logging endpoints (e.g., `/api/error_log`). All troubleshooting data must be sourced from GitHub Actions WebSocket captures or CI logs to ensure compatibility with HA 2025.11+.

- **R12: Diagnostic Observability:**
  - **[VERIFIED]** Implementation of diagnostic tracing in critical parsers to ensure visibility into data mapping during the batch distribution phase.
  - **[VERIFIED]** Established O(1) dictionary traversal as the project standard for entity data retrieval from the centralized coordinator.
  - **[VERIFIED]** Persistent diagnostic logging implemented in the `available` property of `MerakiEntity` and overrides (e.g., `MerakiRebootButton`) to provide precise reasons (missing coordinator data, missing device data, offline status, missing capabilities) for entity unavailability.

- **R13: Webhook Lifecycle Management:**
  - **[VERIFIED]** Implementation of idempotent webhook registration to prevent exhausting the Meraki API limit (100 HTTP servers per network).
  - **[VERIFIED]** Automated discovery and deletion of orphaned webhooks matching the Home Assistant name pattern or specific webhook URL.
  - **[VERIFIED]** Proactive self-healing routine for garbage collection of legacy webhooks.
  - **[VERIFIED]** Reuse of existing webhooks when an exact match (name and URL) is found.

- R14: Structured LLM Outputs (BAML):
  - **[VERIFIED]** BAML (BoundaryML) initialized as the project standard for structured LLM interactions.
  - **[VERIFIED]** `baml-py` added to dependencies.
  - **[VERIFIED]** `baml_src` configuration and generation logic established.

- R15: Native Assist Integration:
  - **[IN PROGRESS]** Implementation of a custom Intent Handler to expose BAML-powered Natural Language Intent Routing to Home Assistant's native Assist conversation pipeline.
  - **[IN PROGRESS]** Registration of `MerakiSmartCommand` intent.
  - **[IN PROGRESS]** Mapping of BAML-parsed intents (Reboot, Guest Access, Status) to internal services.

- R16: Frontend Data Integrity:
  - **[IN PROGRESS]** Implementation of defensive attribute access in custom Lovelace cards to prevent UI crashes following the backend 'God Module' refactor.
  - **[IN PROGRESS]** Injection of card-level diagnostic logging (`MERAKI CARD DIAGNOSTIC`) in `render()` methods to facilitate real-time debugging of entity state mapping.

- R17: Native Tap Actions in Vitals Card:
  - **[VERIFIED]** Upgraded `meraki-network-vitals-card` to support native Home Assistant `tap_action` events.
  - **[VERIFIED]** Gateway, Switch, and AP pills now support clickable actions, defaulting to `more-info`.
  - **[VERIFIED]** Added configuration fields to the card editor for managing these tap actions.

- **R18: Schema Consistency:**
  - **[IN PROGRESS]** Implementation of configuration schema consistency to ensure alignment between constants, translation files, and automated testing scripts. This includes migrating legacy keys (e.g., `meraki_api_key`) to standardized keys (e.g., `api_key`).

This verification confirms the need for the planned refactoring steps. The new requirements (R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18) are now considered part of the standard for this integration.
