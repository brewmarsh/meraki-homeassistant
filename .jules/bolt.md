## 2024-05-18 - Single-Pass Iteration for Multiple Counts
**Learning:** Performing multiple `sum(1 for ...)` operations on the same list to extract different counts (like "critical" and "warning" alerts) creates a hidden O(k*N) inefficiency.
**Action:** Refactor multiple generator counts into a single `for` loop to perform an O(N) pass, reducing loop overhead and redundant dictionary lookups.
## 2026-08-10 - [Cache Home Assistant Sensor Properties]
**Learning:** In Home Assistant components, sensor properties like `native_value` or `extra_state_attributes` are evaluated frequently on the main event loop. If these getters contain O(N) operations (e.g., looping through tens of thousands of API records), they can block the main thread and degrade performance significantly.
**Action:** When extracting aggregate metrics from large datasets (e.g., counting clients), perform the O(N) calculation in the `_update_state` or `_handle_coordinator_update` method which only runs when new data arrives. Store the result in standard attributes like `_attr_native_value` to ensure O(1) read operations.
