## 2024-05-18 - Single-Pass Iteration for Multiple Counts
**Learning:** Performing multiple `sum(1 for ...)` operations on the same list to extract different counts (like "critical" and "warning" alerts) creates a hidden O(k*N) inefficiency.
**Action:** Refactor multiple generator counts into a single `for` loop to perform an O(N) pass, reducing loop overhead and redundant dictionary lookups.

## 2026-08-27 - Property Getter Optimization
**Learning:** Home Assistant's property getters like `native_value` and `extra_state_attributes` are evaluated frequently on the main event loop. Performing O(N) operations inside these properties degrades system performance.
**Action:** Move O(N) calculations (such as summing over ports or filtering lists) into `_update_state` or `_handle_coordinator_update` which run only when data changes. Store results in `_attr_native_value` or `_attr_extra_state_attributes` for O(1) retrieval.
