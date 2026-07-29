## 2024-05-18 - Single-Pass Iteration for Multiple Counts
**Learning:** Performing multiple `sum(1 for ...)` operations on the same list to extract different counts (like "critical" and "warning" alerts) creates a hidden O(k*N) inefficiency.
**Action:** Refactor multiple generator counts into a single `for` loop to perform an O(N) pass, reducing loop overhead and redundant dictionary lookups.
## 2024-05-19 - Home Assistant Sensor Property Optimization
**Learning:** Home Assistant sensor properties like `native_value` and `extra_state_attributes` are accessed frequently. Performing O(N) filtering operations inside these getters can cause performance bottlenecks.
**Action:** Move expensive calculations (like filtering devices or tallying stats) to a `_compute_cache` method triggered once during `_handle_coordinator_update`, and return the O(1) cached values in the property getters.
