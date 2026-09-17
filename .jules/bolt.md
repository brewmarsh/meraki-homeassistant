## 2024-05-18 - Single-Pass Iteration for Multiple Counts
**Learning:** Performing multiple `sum(1 for ...)` operations on the same list to extract different counts (like "critical" and "warning" alerts) creates a hidden O(k*N) inefficiency.
**Action:** Refactor multiple generator counts into a single `for` loop to perform an O(N) pass, reducing loop overhead and redundant dictionary lookups.

## 2024-05-18 - Home Assistant Property Getters in Main Event Loop
**Learning:** Property getters like `native_value` and `extra_state_attributes` are evaluated frequently on the main event loop. Performing O(N) operations (e.g., iterating through lists or generating attributes dynamically) inside these getters can cause performance bottlenecks and block the main loop.
**Action:** Move O(N) calculations to update methods (like `_handle_coordinator_update` or a dedicated `_update_state`) which only run when new data arrives. Store the pre-calculated result in `_attr_native_value` and `_attr_extra_state_attributes` for fast O(1) retrieval.
