## 2024-05-18 - Single-Pass Iteration for Multiple Counts
**Learning:** Performing multiple `sum(1 for ...)` operations on the same list to extract different counts (like "critical" and "warning" alerts) creates a hidden O(k*N) inefficiency.
**Action:** Refactor multiple generator counts into a single `for` loop to perform an O(N) pass, reducing loop overhead and redundant dictionary lookups.

## 2024-05-18 - Avoid O(N) operations in sensor property getters
**Learning:** Home Assistant sensor properties like `native_value` and `extra_state_attributes` are called frequently on the main event loop. Performing O(N) list comprehensions or sums within these getters creates a hidden performance bottleneck.
**Action:** Refactor sensors to calculate and store values in `_attr_native_value` and `_attr_extra_state_attributes` during `__init__` and `_handle_coordinator_update`, ensuring O(1) property access.
