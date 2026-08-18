## 2024-05-18 - Single-Pass Iteration for Multiple Counts
**Learning:** Performing multiple `sum(1 for ...)` operations on the same list to extract different counts (like "critical" and "warning" alerts) creates a hidden O(k*N) inefficiency.
**Action:** Refactor multiple generator counts into a single `for` loop to perform an O(N) pass, reducing loop overhead and redundant dictionary lookups.
## 2024-05-19 - [O(1) Property Access in MerakiPoeUsageSensor]
**Learning:** Home Assistant evaluates Sensor property getters (like `native_value` and `extra_state_attributes`) frequently on the main event loop. Performing O(N) operations (e.g. iterating over device ports) in these getters causes significant performance overhead.
**Action:** Always perform O(N) calculations in lifecycle methods that run only when new data arrives (e.g., `_update_state` called from `_handle_coordinator_update`) and store the results in internal `_attr_*` properties for O(1) retrieval.
