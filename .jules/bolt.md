## 2024-05-18 - Single-Pass Iteration for Multiple Counts
**Learning:** Performing multiple `sum(1 for ...)` operations on the same list to extract different counts (like "critical" and "warning" alerts) creates a hidden O(k*N) inefficiency.
**Action:** Refactor multiple generator counts into a single `for` loop to perform an O(N) pass, reducing loop overhead and redundant dictionary lookups.

## 2024-05-18 - [Optimize PoE Usage Sensor Properties]
**Learning:** Home Assistant Sensor property getters (like `native_value` and `extra_state_attributes`) are evaluated very frequently on the main event loop. Performing O(N) operations (e.g., looping through device ports) inside these getters can block the event loop and degrade performance.
**Action:** Move O(N) calculations to `_update_state` (called on initialization and via `_handle_coordinator_update`), store results in standard `_attr_native_value` and `_attr_extra_state_attributes` fields, and return those pre-computed values in the property getters for O(1) performance.
