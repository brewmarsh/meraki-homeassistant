## 2024-05-18 - Single-Pass Iteration for Multiple Counts
**Learning:** Performing multiple `sum(1 for ...)` operations on the same list to extract different counts (like "critical" and "warning" alerts) creates a hidden O(k*N) inefficiency.
**Action:** Refactor multiple generator counts into a single `for` loop to perform an O(N) pass, reducing loop overhead and redundant dictionary lookups.
## 2025-02-12 - Prevent Home Assistant Event Loop Blocking via O(N) Property Avoidance
**Learning:** Home Assistant core heavily polls sensor properties (`native_value`, `extra_state_attributes`) on the main event loop during rendering and state updates. Performing O(N) calculations (like list filtering or aggregation) inside property getters leads to repeated, blocking computations and degrades system performance.
**Action:** When implementing or refactoring Home Assistant entities, perform complex calculations in `_handle_coordinator_update` or `__init__`, cache the results in standard `_attr_*` variables, and ensure property getters simply return those pre-computed values in O(1) time.
