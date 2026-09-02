## 2024-05-18 - Single-Pass Iteration for Multiple Counts
**Learning:** Performing multiple `sum(1 for ...)` operations on the same list to extract different counts (like "critical" and "warning" alerts) creates a hidden O(k*N) inefficiency.
**Action:** Refactor multiple generator counts into a single `for` loop to perform an O(N) pass, reducing loop overhead and redundant dictionary lookups.
## 2024-05-18 - [Bolt: Pre-compute property getters]
**Learning:** In Home Assistant integrations using `CoordinatorEntity`, evaluating O(N) loops or building lists inside property getters (like `native_value` and `extra_state_attributes`) creates significant overhead, as these properties are evaluated repeatedly by the event loop (not just when data changes).
**Action:** Always shift expensive computations (e.g., iterating through VLAN data lists) into `_handle_coordinator_update()` or a custom `_update_state()` method, cache the results to instance variables, and return the cached values in the property getters.
