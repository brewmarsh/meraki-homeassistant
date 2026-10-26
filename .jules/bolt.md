## 2024-05-18 - Single-Pass Iteration for Multiple Counts
**Learning:** Performing multiple `sum(1 for ...)` operations on the same list to extract different counts (like "critical" and "warning" alerts) creates a hidden O(k*N) inefficiency.
**Action:** Refactor multiple generator counts into a single `for` loop to perform an O(N) pass, reducing loop overhead and redundant dictionary lookups.

## 2024-10-26 - O(N) operations inside property getters
**Learning:** Computing heavy operations like `sum()` and comprehensions inside property getters like `native_value` or `extra_state_attributes` for Home Assistant sensors causes O(N) execution every time HA reads the state (which happens frequently).
**Action:** Move heavy calculations to `_handle_coordinator_update` (or `_update_state`) and store the results in `_attr_native_value` and `_attr_extra_state_attributes`. These only run when data changes, turning O(N) properties into O(1).
