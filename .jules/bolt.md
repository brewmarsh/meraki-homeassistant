## 2024-05-18 - Single-Pass Iteration for Multiple Counts
**Learning:** Performing multiple `sum(1 for ...)` operations on the same list to extract different counts (like "critical" and "warning" alerts) creates a hidden O(k*N) inefficiency.
**Action:** Refactor multiple generator counts into a single `for` loop to perform an O(N) pass, reducing loop overhead and redundant dictionary lookups.
## 2026-08-21 - [O(N) Operations in Entity Properties]
**Learning:** Home Assistant frequently evaluates properties like `native_value` and `extra_state_attributes` on the main event loop (e.g. during state writes or templating evaluation). Putting (N)$ operations (such as list filtering or summation) inside these property getters causes severe performance degradation as the data size grows.
**Action:** Precalculate these values in (1)$ during `__init__` and `_handle_coordinator_update` methods, and store them in attributes like `self._attr_native_value` to ensure property getters return in (1)$ time.
