## 2024-05-18 - Single-Pass Iteration for Multiple Counts
**Learning:** Performing multiple `sum(1 for ...)` operations on the same list to extract different counts (like "critical" and "warning" alerts) creates a hidden O(k*N) inefficiency.
**Action:** Refactor multiple generator counts into a single `for` loop to perform an O(N) pass, reducing loop overhead and redundant dictionary lookups.
## 2024-05-18 - Home Assistant Property Access Performance
**Learning:** Home Assistant frequently accesses entity properties like `native_value` and `extra_state_attributes` to determine state changes. Performing O(N) operations, such as filtering lists or processing strings, inside these property getters causes unnecessary, repeated computations on the main loop.
**Action:** Pre-calculate and cache complex values or filtered lists during the data update phase (e.g. within the `_handle_coordinator_update` or a custom computation method like `_compute_device_cache`) so that property getters only return pre-computed O(1) state.
